"""Download FCC BDC availability data for one state and build a ZIP-level provider table.

Output format (same as the site's tx-zips.json):
 {"b":[brand names], "z":{zip:{"c":city,"p":[[brandIdx,techCode,maxDown,maxUp,sharePct],...]}}}
Tech codes: 10 DSL, 40 Cable, 50 Fiber, 61 NGSO satellite, 70 Licensed fixed wireless (T-Mobile/Verizon 5G Home),
71 Unlicensed fixed wireless.

Needs env FCC_USERNAME and FCC_TOKEN (free BDC public-data API token, bdc.fcc.gov -> Manage API Access).
Usage: build_zip_table.py <STATE_USPS> <FIPS> <outfile>
"""
import os, sys, io, json, zipfile, glob, requests, duckdb, h3, zipcodes
from collections import defaultdict

state, fips, outfile = sys.argv[1], sys.argv[2], sys.argv[3]
BASE = "https://bdc.fcc.gov/api/public/map"
H = {"username": os.environ["FCC_USERNAME"], "hash_value": os.environ["FCC_TOKEN"]}
WORK = "work"; os.makedirs(WORK, exist_ok=True)
TECH = {"Copper":10, "Cable":40, "FibertothePremises":50, "GSOSatellite":60, "NGSOSatellite":61,
        "LicensedFixedWireless":70, "UnlicensedFixedWireless":71, "LBRFixedWireless":72}

def get(path, **kw):
    r = requests.get(BASE + path, headers=H, timeout=120, **kw); r.raise_for_status(); return r

dates = get("/listAsOfDates").json()["data"]
asof = max(d["as_of_date"] for d in dates if d.get("data_type") == "availability")
files = get(f"/downloads/listAvailabilityData/{asof}", params={"category": "State", "subcategory": "Fixed Broadband"}).json()["data"]
mine = [f for f in files if str(f.get("state_fips")) == fips and f.get("technology_type") != "Mobile Broadband"]
print("as_of", asof, "files", [(f["file_name"]) for f in mine])

con = duckdb.connect(os.path.join(WORK, "s.duckdb"))
con.execute("create or replace table agg(h3 varchar, brand varchar, tech int, down int, up int, locs bigint)")
for f in mine:
    name = f["file_name"]
    tname = next((k for k in TECH if k.lower() in name.lower().replace("_", "")), None)
    if tname is None: print("skip", name); continue
    zpath = os.path.join(WORK, name + ".zip")
    with requests.get(f"{BASE}/downloads/downloadFile/availability/{f['file_id']}/1", headers=H, stream=True, timeout=600) as r:
        r.raise_for_status()
        with open(zpath, "wb") as o:
            for ch in r.iter_content(1 << 22): o.write(ch)
    with zipfile.ZipFile(zpath) as z: z.extractall(WORK)
    os.remove(zpath)
    for csv in glob.glob(os.path.join(WORK, "*.csv")):
        if f["file_name"] not in csv and tname.lower() not in csv.lower(): continue
        con.execute(f"""insert into agg select h3_res8_id, brand_name, technology,
            max(max_advertised_download_speed), max(max_advertised_upload_speed), count(distinct location_id)
            from read_csv('{csv}', header=true, all_varchar=true) where business_residential_code in ('R','X')
            group by 1,2,3""")
        os.remove(csv)
    print("loaded", name)

zs = [z for z in zipcodes.filter_by(state=state) if z["zip_code_type"] == "STANDARD" and z["lat"]]
rows = []
for z in zs:
    c = h3.latlng_to_cell(float(z["lat"]), float(z["long"]), 8)
    for cell in h3.grid_disk(c, 3): rows.append((z["zip_code"], cell))
con.execute("create or replace temp table zc(zip varchar,h3 varchar)")
con.executemany("insert into zc values (?,?)", rows)
res = con.sql("select zip,brand,tech,max(down),max(up),sum(locs) from agg join zc using(h3) group by 1,2,3").fetchall()
by = defaultdict(list)
for r in res: by[r[0]].append(r)
brands, bi, out = [], {}, {}
city = {z["zip_code"]: z["city"] for z in zs}
for zp, rs in by.items():
    ter = [r for r in rs if r[2] not in (60, 61)]
    mx = max([r[5] for r in ter], default=0)
    lst = []
    for _, b, t, d, u, l in rs:
        if t in (60, 61): sh = 100
        else:
            sh = round(100 * l / mx) if mx else 0
            if sh < 3: continue
        if b not in bi: bi[b] = len(brands); brands.append(b)
        lst.append([bi[b], t, int(d), int(u), sh])
    lst.sort(key=lambda x: -x[4])
    out[zp] = {"c": city[zp].title() if city[zp].isupper() else city[zp], "p": lst}
json.dump({"b": brands, "z": out, "asof": asof}, open(outfile, "w"), separators=(",", ":"))
print(state, len(out), "zips", len(brands), "brands")
