import json
from ui import dot, esc

# (color, mode, light label, meaning, severity ok|wait|fix, what to do)
ATT_BGW = [
 ("white", "", "Service: solid white", "Gateway is online.", "ok", "Nothing to do. Connect your devices."),
 ("white", "slow", "Service: blinking white (slow)", "Gateway is powering up.", "wait", "Wait a few minutes."),
 ("white", "blink", "Service: blinking white (fast)", "Gateway is starting up.", "wait", "Wait for it to finish."),
 ("green", "blink", "Service: blinking green (fast)", "Connected to the network and ready for activation. Seen during first-time setup.", "wait", "Finish activation in the AT&T app or site."),
 ("red", "", "Service: solid red, WPS light off", "Gateway is overheating.", "fix", "Move it to a flat, carpet-free surface with open space around, above and under it."),
 ("red", "", "Service: solid red, WPS light solid red", "Hardware issue.", "fix", "Reboot it. If red stays, it needs replacing, so contact AT&T."),
 ("red", "blink", "Service: blinking red (fast)", "Network service issue that may need AT&T to step in. Can be momentary.", "fix", "Check for an outage in myAT&T or Smart Home Manager, then reboot the gateway."),
 ("red", "slow", "Service: blinking red (slow)", "No broadband connection.", "fix", "Check for a loose, disconnected or damaged cable, then press and hold the red reset button for 10 seconds."),
 ("amber", "", "Service: solid amber", "Gateway is powered on.", "wait", "Wait until it turns solid white."),
 ("amber", "slow", "Service: blinking amber (slow)", "Gateway is installing an update.", "wait", "Wait until it turns solid white."),
 ("blue", "blink", "Service: blinking blue (fast)", "Your internet is part of a network outage and the gateway is switching to internet backup mode.", "wait", "Wait. Service should come back on its own."),
 ("blue", "", "Service: solid blue", "Gateway is in internet backup mode.", "wait", "It returns to fiber internet when the outage ends."),
 ("yellow", "blink", "Service: blinking yellow (fast)", "Phone registration failed; one of your VoIP lines has a problem.", "fix", "Reboot the gateway; contact AT&T if it continues."),
 ("yellow", "", "Service: solid yellow", "A phone (VoIP) line is registered. Also shown during a call.", "ok", "Nothing to do."),
]
ATT_OTHER = [
 ("red", "", "Power: solid red", "Gateway or power supply may be malfunctioning.", "fix", "Try another outlet, then contact AT&T."),
 ("green", "", "Broadband: solid green", "Connected to the AT&T network.", "ok", "Nothing to do."),
 ("green", "blink", "Broadband: flashing green", "Trying to connect to the network.", "wait", "Wait a few minutes."),
 ("red", "blink", "Broadband: flashing red", "Cannot connect to the network.", "fix", "Check the line or cable, restart, then contact AT&T."),
 ("green", "", "Service: solid green", "Gateway has an IP address and the connection is active.", "ok", "Nothing to do."),
 ("red", "", "Service: solid red", "Internet service authentication failed.", "fix", "Restart; if it stays red, contact AT&T."),
]
XFI = [
 ("off", "", "No light", "Device is off.", "fix", "Check power cable and outlet."),
 ("white", "", "White (steady, or with a purple tint)", "On and working.", "ok", "Nothing to do."),
 ("white", "blink", "White steady or blinking during activation", "Limited operation while the device is being set up.", "wait", "Follow the Getting Started guide if you have not activated it yet."),
 ("red", "", "Red (steady)", "No internet connection.", "fix", "Xfinity says it is having trouble connecting to your device. Contact Xfinity."),
 ("blue", "blink", "Blue (blinking)", "WPS mode: the gateway is pairing with another wireless device.", "wait", "Finish pairing on the other device."),
 ("amber", "blink", "Any other color combination", "Connecting to Xfinity systems.", "wait", "Wait about 15 minutes for the cycle to finish; contact Xfinity if it does not."),
]
VZ = [
 ("white", "", "White (solid)", "Normal operation, connected and working.", "ok", "Nothing to do."),
 ("white", "blink", "White (fast blink)", "Router is booting.", "wait", "Wait a couple of minutes."),
 ("blue", "slow", "Blue (slow blink)", "Pairing mode is active.", "wait", "Finish pairing on your device."),
 ("blue", "", "Blue (solid)", "Pairing succeeded.", "ok", "Nothing to do."),
 ("green", "", "Green (solid)", "Wi-Fi has been turned off.", "wait", "Turn Wi-Fi back on in the My Fios app or router settings."),
 ("yellow", "", "Yellow (solid)", "No internet connection.", "fix", "Restart the router, check the Ethernet cable to the ONT, then contact Verizon."),
 ("red", "", "Red (solid)", "Hardware or system failure.", "fix", "Contact Verizon; the router may need replacing."),
 ("red", "blink", "Red (fast blink)", "Overheating.", "fix", "Give it airflow and move it away from heat."),
 ("red", "slow", "Red (slow blink)", "WPS pairing failed.", "wait", "Wait for it to clear and try pairing again."),
 ("off", "", "Off", "Power is off.", "fix", "Check the power adapter and outlet."),
]
CL_RING = [
 ("blue", "blink", "Blue (blinking or solid)", "Booting up and syncing with the network.", "wait", "Wait up to 5 minutes. If it keeps blinking blue, check the DSL cord at the modem and wall jack."),
 ("green", "", "Green (solid)", "Connected.", "ok", "Nothing to do."),
 ("green", "blink", "Green (flickering)", "Sending or receiving data.", "ok", "Normal."),
 ("red", "", "Red (solid)", "Network failure.", "fix", "Call or chat with CenturyLink."),
]
CL_TOWER = [
 ("off", "", "Power light off", "The modem is not plugged in or has no power.", "fix", "Check the power cord and outlet."),
 ("red", "", "Power light red", "The modem is testing its hardware at startup.", "wait", "If still red after a few minutes, restart it; a failed test means hardware or software failure."),
 ("amber", "", "Power light orange or blinking green/orange", "The modem is testing its software.", "wait", "Wait; restart if it never settles."),
 ("green", "slow", "DSL light blinking green slowly", "The modem is searching for the CenturyLink network.", "wait", "If it blinks for more than 5 minutes, reboot the modem and check the DSL cord."),
 ("red", "", "DSL light red", "Not connecting to the network: service not activated, or a faulty jack.", "fix", "Try another jack, then contact CenturyLink."),
]
COX_ARRIS = [
 ("off", "", "Power: off", "No power.", "fix", "Check all cable connections and try resetting the modem."),
 ("green", "", "Power: solid", "Powered on.", "ok", "Nothing to do."),
 ("green", "blink", "US/DS: flashing", "Not connected to the internet.", "fix", "Check cable connections and reset the modem."),
 ("green", "", "US/DS: solid", "Connected to the internet.", "ok", "Nothing to do."),
 ("off", "", "Online: off", "Internet is not available.", "fix", "Verify cable connections and reset the modem."),
 ("white", "", "Panoramic Wifi gateways: one solid white light", "Gateway is registered and online.", "ok", "Any other pattern means it is not fully online; see Cox's page for your model."),
]
SPECTRUM_LEDS = [
 ("white", "", "Solid steady light", "Everything is connected and working.", "ok", "Nothing to do."),
 ("blue", "blink", "Blue/green flashing (Spectrum WiFi 6 router)", "The router is booting up.", "wait", "Wait a few minutes."),
 ("blue", "slow", "Blue/green pulsing", "Connecting to the internet.", "wait", "Wait for it to go solid."),
 ("green", "", "Blue/green solid", "Connected to the internet.", "ok", "Nothing to do."),
 ("red", "blink", "Off, or an unusual color or pattern lasting 10 to 15 minutes after a full power cycle", "Usually a cable, power or signal problem rather than a bad modem.", "fix", "Check cables, then contact Spectrum; they can run a remote test and send a replacement."),
]
SPECTRUM_INV = [
 ("off", "", "Off", "Device is off.", "fix", "Check power."),
 ("blue", "blink", "Blue flashing", "Booting up.", "wait", "Wait."),
 ("blue", "slow", "Blue easing", "Connecting to the internet.", "wait", "Wait."),
 ("blue", "", "Blue solid", "Connected to the internet.", "ok", "Nothing to do."),
 ("white", "", "White solid", "Backup mode is active.", "wait", "Returns to your normal connection when power and service are restored."),
 ("white", "blink", "White flashing", "Poor cellular reception.", "fix", "Move the router closer to a window."),
]
OPT_LIGHTS = [
 ("green", "", "Modem: four solid lights", "The modem is online.", "ok", "Plug the router in after the modem shows four solid lights."),
 ("green", "", "Arris TM802/TM822: four green lights and a flashing amber fifth", "Modem is ready during setup.", "wait", "This can take a few minutes."),
 ("blue", "", "Arris TM1602: three solid blue lights and a flashing green WAN port light", "Modem is ready during setup.", "wait", "Continue setup."),
 ("green", "blink", "Smart Router: two front lights flash green together", "The router has finished updating and is ready.", "ok", "Nothing to do."),
 ("white", "", "Altice One standby light: white", "The box is on and ready.", "ok", "Nothing to do."),
 ("red", "", "Altice One standby light: red", "The box is off.", "fix", "Press the power button on the box."),
 ("white", "", "Extender 6/6e Wi-Fi light: solid white", "Good signal.", "ok", "Nothing to do."),
 ("red", "", "Extender 6/6e: solid red or flashing white", "Not enough signal.", "fix", "Move the extender closer to the gateway."),
 ("red", "blink", "Extender 6/6e: flashing red", "The extender needs to be reconnected.", "fix", "Re-pair it to the gateway."),
]
TMO = [
 ("green", "", "Gateway screen: 1 to 5 bars", "Strength of the cellular connection.", "ok", "More bars is better. Move the gateway near a window for a stronger signal."),
 ("red", "", "Gateway screen: X", "The gateway is not connected to the cellular network.", "fix", "Restart the gateway and move it; contact T-Mobile if X stays."),
 ("red", "", "Mesh extender: solid red", "No network signal.", "fix", "Move the extender closer to the gateway."),
 ("white", "", "Mesh extender: solid white at power-up", "Booting; not ready to pair.", "wait", "Wait a few minutes."),
]

PROV = {
 "att": dict(name="AT&T", tag="Fiber, DSL and fixed wireless gateways", equip="AT&T Wi-Fi Gateway (BGW320, BGW210 and others)",
   tables=[("AT&T BGW320 Wi-Fi Gateway: Service light", ATT_BGW), ("Other AT&T gateways (DSL and fixed wireless): Power, Broadband and Service lights", ATT_OTHER)],
   src=[("AT&T: BGW320 getting to know your equipment", "https://www.att.com/device-support/article/134376/at&t/bgw320/"), ("AT&T: gateway status lights", "https://www.att.com/support/article/internet/KM1172762/")],
   noint=["Look at the <b>Service</b> light on the front of the gateway and match it to the table above.",
          "<b>Blinking red slowly</b> means no broadband connection. Check the cables, then press and hold the red <b>reset button for 10 seconds</b>.",
          "<b>Blinking red fast</b> means a network issue that may need AT&T. Check for an outage in the myAT&T app or Smart Home Manager, then reboot.",
          "<b>Solid red</b> with the WPS light off means overheating; with the WPS light red it means a hardware issue. Move it or reboot it as shown above.",
          "Still red? Contact AT&T and ask them to test the line and consider replacing the gateway."],
   restart=["Unplug the gateway power cord, wait 30 seconds and plug it back in.", "Wait until the Service light turns solid white. Amber and blinking white are normal at startup.",
            "Only use the red reset button when the Service light is blinking red slowly, and hold it for 10 seconds. Resets can erase custom Wi-Fi settings, so note your Wi-Fi name and password first."],
   extra=("Fiber ONT lights", "AT&T's indoor ONT guide says a red Power light means a problem with the ONT, and a solid red Alarm light means the ONT isn't working as expected: make sure the fiber cable is in the PON port. If the Data light is off, check both ends of the red ONT cable, which should plug into the ONT's Ethernet port. Contact AT&T if lights stay red.")),
 "xfinity": dict(name="Xfinity", tag="Xfinity Gateway (modem + Wi-Fi router)", equip="Xfinity Gateway",
   tables=[("Xfinity Gateway light guide", XFI)], src=[("Xfinity: what the lights on your gateway mean", "https://www.xfinity.com/support/articles/xfi-gateway-led-lights")],
   noint=["Check the light on your gateway against the table above. A <b>steady red light</b> means no internet connection.",
          "Check for an outage in the Xfinity app or at xfinity.com/status before you do anything else.",
          "Make sure the coax cable is tight at the wall and at the gateway, and remove any splitter to test the cable directly from the wall.",
          "Restart the gateway: unplug it for 30 seconds and plug it back in. If it shows other color combinations, wait about 15 minutes for the cycle to complete.",
          "If red or blinking continues, contact Xfinity. They can check the signal to your home and send a technician."],
   restart=["Unplug the gateway power cord and wait 30 seconds, then plug it back in.", "Allow up to 15 minutes for it to reconnect. Several color combinations are normal while it connects.",
            "You can also restart from the Xfinity app (Overview, then your gateway) if you can still reach it."], extra=None),
 "spectrum": dict(name="Spectrum", tag="Spectrum modem, WiFi 6 router and Invincible WiFi", equip="Spectrum modem and router",
   tables=[("Spectrum modem and WiFi 6 router lights", SPECTRUM_LEDS), ("Spectrum Invincible WiFi router lights", SPECTRUM_INV)],
   src=[("Spectrum: router and modem troubleshooting", "https://www.spectrum.com/resources/internet-wifi/modem-troubleshooting-slow-dropped-connections"), ("Spectrum: Invincible WiFi troubleshooting", "https://www.spectrum.net/support/internet/invincible-wifi-troubleshooting")],
   noint=["Spectrum says light patterns vary by model. Check the label on your equipment or the My Spectrum app for your model.",
          "A <b>solid, steady light</b> is good. <b>Blinking at startup</b> is normal and should settle in a few minutes.",
          "If a light is <b>off or an unusual color</b> for more than 10 to 15 minutes after a full power cycle, it usually points to a cable, power or signal problem, not the modem itself.",
          "Check the coax and power cables, look for visible damage, and check for an outage in the My Spectrum app.",
          "Test with a computer plugged straight into the modem to rule out your router (see the bypass steps in Spectrum's help center).",
          "Contact Spectrum if problems persist, lights never stabilize, a cable looks damaged or equipment is hot. They can run a remote test and ship a new modem or router."],
   restart=["Unplug the modem and router (or the combined unit).", "Wait at least 30 seconds.", "Plug the modem in first and give it 2 to 5 minutes for the lights to settle.", "Plug the router in and wait 1 to 2 minutes.", "Test on the device that had trouble."], extra=None),
 "verizon": dict(name="Verizon", tag="Fios Router (G3100 and similar)", equip="Fios Router",
   tables=[("Fios Router (G3100) front status light", VZ)], src=[("Verizon: Fios Router G3100 user guide", "https://www.verizon.com/content/dam/verizon/support/consumer/documents/internet/fios-router-user-guide.pdf")],
   noint=["Check the front light on the Fios Router. <b>Solid yellow</b> means no internet connection. <b>Solid red</b> means a hardware or system failure.",
          "Check the Ethernet cable between the ONT (fiber box) and the router is firmly plugged in at both ends.",
          "Look at the ONT's lights. If the ONT shows a fault, a router restart will not fix it and a Verizon technician is needed.",
          "Restart the router (see below). Check for an outage in the My Fios app.",
          "If it stays yellow or red, contact Verizon."],
   restart=["<b>Soft reboot:</b> press and hold the rear Reset button for at least 3 seconds.", "<b>Factory reset:</b> press and hold the Reset button for at least 10 seconds. This erases your settings, so note your Wi-Fi name and password first.",
            "You can also reboot from the router's web page (Advanced, Utilities, Reboot Router). Verizon's guide suggests doing that when Verizon support tells you to."], extra=None),
 "frontier": dict(name="Frontier", tag="Frontier fiber ONT and router", equip="Frontier router and ONT",
   tables=[], src=[("Frontier: how to troubleshoot your ONT", "https://frontier.com/helpcenter/internet/troubleshooting/how-to-troubleshoot-your-ont"), ("Frontier: restart router and set-top box", "https://frontier.com/helpcenter/categories/troubleshooting/how-to-instructions/restart-router-set-top-box")],
   noint=["Check for an outage in your area and restart your router first.",
          "Make sure the router is plugged <b>directly into a wall outlet</b> (not a power strip) and the power light is green. Check the router's Internet light: if it is off, red or amber, you have a connection problem.",
          "Find your <b>ONT</b>, the box where fiber enters your home, usually in a garage, basement or outside near the power box. Confirm its lights are on and it has power.",
          "If the house has power but the ONT does not, check whether it is on a <b>GFCI outlet</b>. Unplug the ONT, test the outlet with a lamp, and if it is dead press the outlet's reset button.",
          "Restart the ONT by unplugging it for at least 5 minutes (see below), then wait at least 5 minutes for service to return.",
          "If it still fails, contact Frontier through chat or its help center."],
   restart=["<b>Router:</b> press the power button or unplug the cord, wait 30 seconds, then turn it back on. The globe/internet light glowing means the reset has finished.", "<b>Factory reset:</b> press and hold the router's Reset button for 10 seconds with a pen or paper clip. This erases settings.",
            "<b>ONT:</b> unplug it, wait at least 5 minutes, plug it back in. If it has a battery backup, disconnect one battery lead first and reconnect it 30 seconds after plugging the ONT back in.", "Keep the router on at all times if you have Frontier Fiber TV; the TV needs it."],
   extra=("Frontier TV remote and set-top box", "Frontier says to keep your router plugged in and on at all times, even if you are not using the internet, because Fiber TV needs it. To fix a remote button that does not work, hold OK and Live TV (or OK and star) together until the red light blinks twice and stays on, then follow the on-screen steps. Check the ONT or splitter connections if you think a connection is loose, and make sure your TV is on the right input.")),
 "cox": dict(name="Cox", tag="Cox Panoramic Wifi gateways and cable modems", equip="Cox Panoramic Wifi gateway",
   tables=[("Cox modem and gateway lights", COX_ARRIS)], src=[("Cox: Arris TG2472 troubleshooting", "https://www.cox.com/residential/support/arris-tg2472.html"), ("Cox: Panoramic Wifi router", "https://www.cox.com/residential/support/panoramic-wifi-router.html"), ("Cox: Technicolor CGM4141", "https://www.cox.com/residential/support/technicolor-cgm4141.html")],
   noint=["Check your gateway lights against the table. On Panoramic Wifi gateways, <b>one solid white light</b> means online. Anything else means it is not fully online.",
          "On older modems, flashing <b>US/DS</b> lights mean it is not connected to the internet, and an <b>Online</b> light that is off means no internet.",
          "Check that every cable is tight, and try a different coax wall outlet; unused outlets are common.",
          "Do not plug the gateway into an outlet on a dimmer, and keep it at least 3 feet off the floor in open space.",
          "Reset it: unplug the power cord, wait about 10 seconds, plug it back in and allow a few minutes.",
          "If it still will not come online, contact Cox through its support page and ask for a trouble ticket."],
   restart=["Unplug the gateway power cord from the wall.", "Wait about 10 seconds.", "Plug it back in and allow several minutes for it to fully restart.", "Make sure all connections are tight afterwards."], extra=None),
 "optimum": dict(name="Optimum", tag="Optimum modem, Smart Router and Altice One", equip="Optimum modem and router",
   tables=[("Optimum modem, router, Altice One and extender lights", OPT_LIGHTS)], src=[("Optimum: Smart Router troubleshooting", "https://faq.optimum.net/node/7343"), ("Optimum: Altice One guide", "https://www.optimum.net/cdn/static.tvlistings.optimum.net/ool/static/prod/documents/user-guides/Altice_One_Guide.pdf")],
   noint=["If a computer plugged directly into the router cannot get online, reset the modem first.",
          "Unplug the modem's power (and its battery backup, if you have one) and unplug the router. Shut your computer down. After one minute, plug the modem in and reconnect the battery.",
          "Wait for the modem to show <b>four solid lights</b>, then plug the router in and let it boot.",
          "If the internet works on the wired computer but not on Wi-Fi, check wireless broadcasting is enabled in the router settings.",
          "On Altice One, if you have no picture, check the TV and box are on and connected. To restart TV, hold the button on the box for 10 seconds. <b>Do not unplug the power cord</b> or all services restart.",
          "Still down? Contact Optimum."],
   restart=["Unplug the modem power cord and its battery backup, and unplug the router.", "Wait one minute.", "Plug in the modem and reconnect the battery backup. Wait for four solid lights.", "Plug the router in and wait for it to boot.",
            "<b>Altice One:</b> to restart internet and phone, press and hold the button on the front panel for 10 seconds. Do not unplug the power cord, which restarts all services."], extra=None),
 "centurylink": dict(name="CenturyLink", tag="CenturyLink C4000 and tower modems (DSL and fiber)", equip="CenturyLink modem",
   tables=[("CenturyLink C4000 light ring", CL_RING), ("CenturyLink tower modem: Power and DSL lights", CL_TOWER)], src=[("CenturyLink: C4000 modem light guide", "https://www.centurylink.com/home/help/internet/modems-and-routers/greenwave-c4000/led-display-guide.html"), ("CenturyLink: tower modem lights guide", "https://www.centurylink.com/home/help/internet/modems-and-routers/tower-modem-lights-guide.html")],
   noint=["Check the modem lights against the tables above. On a C4000 the single ring should be <b>solid green</b>. <b>Solid red</b> means a network failure.",
          "On a tower modem, a <b>DSL light that is red</b> means it is not connecting: service may not be activated, or the wall jack may be faulty. Try another jack.",
          "Check the green DSL cord is firmly plugged into the modem and the wall jack, and that a DSL filter is on any phone connected to that line.",
          "Restart the modem. If the DSL light blinks green slowly for more than 5 minutes, reboot it again.",
          "To find out whether the problem is inside or outside your home, CenturyLink suggests testing at the network interface (NID, the phone box): if the DSL light is green there, the problem is most likely in CenturyLink's outside lines and you should submit a repair request; if it is red or off, the problem is inside your wiring.",
          "Contact CenturyLink for a repair request if needed."],
   restart=["Unplug the modem's power cord.", "Wait about 30 seconds and plug it back in.", "Wait for the power light to turn solid green, then check the DSL and Internet lights.", "If you hold the reset button, a long press (about 10 seconds) resets the modem to defaults, so only do that when told to."], extra=None),
 "t-mobile": dict(name="T-Mobile", tag="T-Mobile 5G Home Internet gateway", equip="T-Mobile 5G gateway",
   tables=[("T-Mobile 5G gateway and mesh extender", TMO)], src=[("T-Mobile: Home Internet troubleshooting", "https://www.t-mobile.com/support/home-internet/customer-support"), ("T-Mobile: 5G Gateway Gen5", "https://www.t-mobile.com/support/home-internet/5g-gateway-g5")],
   noint=["Look at the signal bars on the gateway screen. An <b>X</b> means it is not connected to the cellular network.",
          "Move the gateway near a window or to a higher spot, away from large metal objects and appliances. Signal weakens with each wall.",
          "Restart: unplug the gateway, wait 30 seconds, plug it back in, and allow 2 minutes before testing.",
          "Turn off any VPN or firewall, and restart connected devices.",
          "Keep the gateway away from microwaves, baby monitors, Bluetooth devices and fluorescent lights, which can interfere with Wi-Fi.",
          "Contact T-Mobile Home Internet support if X or low bars continue."],
   restart=["Unplug the gateway from power.", "Wait 30 seconds.", "Plug it back in and wait 2 minutes for it to reconnect.", "Restart devices connected to it."], extra=None),
}

def build(P, page, save):
    cards_all = []
    for k, d in PROV.items():
        n = d["name"]; has_lights = bool(d["tables"])
        sup = P.get({"t-mobile": "t-mobile"}.get(k, k), {})
        nums = sup.get("support", [])
        # ---------- lights page ----------
        if has_lights:
            body = (f'<p>Use this guide to read the status lights on your {esc(d["equip"])}. Find the light you see in the first column. Colors are shown as dots (blinking dots flash). '
                    'Exact lights differ by model, so check the label on your equipment too.</p>')
            for title, rows in d["tables"]:
                body += f"<h2>{esc(title)}</h2><table><tr><th>Light</th><th>What it means</th><th>What to do</th></tr>"
                for c, m, lab, mean, sev, act in rows:
                    tag = {"ok": "ok", "wait": "wait", "fix": "fix"}[sev]; lbl = {"ok": "OK", "wait": "WAIT", "fix": "ACTION"}[sev]
                    body += f'<tr><td>{dot(c, m)}<b>{esc(lab)}</b></td><td>{esc(mean)}<br><span class="sev {tag}">{lbl}</span></td><td>{esc(act)}</td></tr>'
                body += "</table>"
            if d["extra"]:
                body += f"<h2>{esc(d['extra'][0])}</h2><p>{esc(d['extra'][1])}</p>"
            body += '<div class="call tip"><b>Quick rule</b>Solid and steady is usually good. Blinking at startup is normal. A red or off light that lasts more than 10 to 15 minutes after a restart usually means a cable, power, signal or equipment problem.</div>'
            body += f'<p>Step-by-step fixes: <a href="/help/{k}">{esc(n)} troubleshooting guide</a>. Official source: ' + " · ".join(f'<a href="{esc(u)}" rel="nofollow noopener">{esc(t)}</a>' for t, u in d["src"]) + ".</p>"
            faq = [(f"What does a red light on my {n} equipment mean?", f"It usually means a problem with the connection or hardware. See the table above for your exact pattern, then restart the equipment. If it stays red, contact {n}."),
                   (f"What does a blinking light mean on {n}?", f"Blinking is normal for a few minutes at startup or while updating. If it keeps blinking for 10 to 15 minutes after a restart, check cables and contact {n}."),
                   (f"How do I restart my {n} {d['equip'].split(' (')[0]}?", f"Unplug the power cord, wait 30 seconds and plug it back in. See our {n} troubleshooting guide for model-specific reset steps.")]
            save(f"/help/{k}/lights", page(f"/help/{k}/lights", f"{n} Router and Modem Lights: What Each Color Means", f"What the lights on your {n} {d['equip'].split(' (')[0]} mean: red, blinking, white, blue, amber and off, with what to do for each.",
                 f"{n} Router Lights: What Each Light Means", f"Red light? Blinking? Here is what each {n} status light means and exactly what to do about it, from {n}'s own support documents.",
                 body, faq, [("Home", "https://yourbillcheck.com/"), ("Troubleshoot", "https://yourbillcheck.com/help"), (n, f"https://yourbillcheck.com/help/{k}"), ("Lights", f"https://yourbillcheck.com/help/{k}/lights")], chips=[n, "Official sources"]))
        # ---------- provider hub page ----------
        body = '<div class="grid">'
        jump = [("🚦", "What do my lights mean?", f"/help/{k}/lights" if has_lights else "#no-internet"), ("🌐", "No internet", "#no-internet"), ("🔄", "Restart it", "#restart"), ("📶", "Wi-Fi problems", "/help/wifi-keeps-disconnecting"), ("🔌", "Connect a LAN cable", "/help/connect-ethernet-lan"), ("📺", "TV not working", "/help/tv-not-working")]
        for ic, t, u in jump:
            body += f'<a class="card" href="{u}"><span class="ic">{ic}</span><b>{esc(t)}</b></a>'
        body += "</div>"
        if has_lights:
            rows = d["tables"][0][1]
            body += f'<h2>{esc(n)} lights at a glance</h2><table><tr><th>Light</th><th>Meaning</th></tr>'
            for c, m, lab, mean, sev, act in [r for r in rows if r[4] != "ok"][:5]:
                body += f'<tr><td>{dot(c, m)}<b>{esc(lab)}</b></td><td>{esc(mean)}</td></tr>'
            body += f'</table><p><a href="/help/{k}/lights">See every {esc(n)} light and what to do →</a></p>'
        mg = [(s_, sh) for kk, lst in MODELS.items() if kk == k for s_, sh, *_ in lst]
        if mg:
            body += f'<h2>{esc(n)} model guides</h2><div class="grid">' + "".join(f'<a class="card" href="/help/{k}/{s_}"><b>{esc(sh)}</b><span>Lights, reset and fixes</span></a>' for s_, sh in mg) + "</div>"
        body += f'<h2 id="no-internet">{esc(n)}: no internet or a red light</h2><ol class="steps">' + "".join(f"<li>{s}</li>" for s in d["noint"]) + "</ol>"
        body += f'<h2 id="restart">How to restart your {esc(n)} equipment</h2><ol class="steps">' + "".join(f"<li>{s}</li>" for s in d["restart"]) + "</ol>"
        body += '<div class="call warn"><b>Before you factory reset</b>A factory reset erases your Wi-Fi name, password and custom settings. Write them down first, and only reset when your provider or its guide tells you to.</div>'
        if d["extra"]:
            body += f"<h2>{esc(d['extra'][0])}</h2><p>{esc(d['extra'][1])}</p>"
        body += f'<h2>Still not working? Contact {esc(n)}</h2>'
        if nums:
            body += "<table><tr><th>For</th><th>Number</th></tr>" + "".join(f"<tr><td>{esc(a)}</td><td><b>{esc(b)}</b></td></tr>" for a, b, c in nums if c) + "</table>"
        body += f'<p>See all <a href="/providers/{k}">{esc(n)} support numbers, plans and coverage</a>. Official sources for this guide: ' + " · ".join(f'<a href="{esc(u)}" rel="nofollow noopener">{esc(t)}</a>' for t, u in d["src"]) + ".</p>"
        body += f'<div class="call tip"><b>Thinking of switching?</b>If {esc(n)} keeps failing, check who else serves your address: <a href="/">enter your ZIP code</a> or see <a href="/compare">provider comparisons</a>.</div>'
        faq = [(f"Why is my {n} internet not working?", f"The most common causes are an outage, a loose cable, or equipment that needs a restart. Check the lights on your {d['equip'].split(' (')[0]}, check for an outage in the {n} app, and restart the equipment."),
               (f"How do I reset my {n} {d['equip'].split(' (')[0]}?", d["restart"][0].replace("<b>", "").replace("</b>", "")),
               (f"How long should I wait after restarting {n} equipment?", "Allow a few minutes. Some equipment needs up to 15 minutes to reconnect and finish updates.")]
        save(f"/help/{k}", page(f"/help/{k}", f"{n} Internet Not Working? Lights, Restart and Fixes", f"{n} troubleshooting: what your router lights mean, how to restart, and what to do when the internet is down or the light is red.",
             f"{n} Troubleshooting: Lights, Restart and Fixes", f"{esc(d['tag'])}. Fix a red light, no internet or a dropped connection step by step, using {esc(n)}'s own support guidance.",
             body, faq, [("Home", "https://yourbillcheck.com/"), ("Troubleshoot", "https://yourbillcheck.com/help"), (n, f"https://yourbillcheck.com/help/{k}")], chips=[n, "Step by step"]))
        cards_all.append((k, n))

    # ---------- universal pages ----------
    lan = ('<p>A wired (LAN) connection is often faster and more reliable than Wi-Fi. Here is how to connect a computer, TV, game console or second router with an Ethernet cable.</p>'
           '<h2>Connect a device to your router</h2><ol class="steps"><li>Plug one end of an Ethernet cable into a <b>LAN</b> port on your router or gateway (usually numbered or yellow, not the port labeled WAN or Internet).</li>'
           '<li>Plug the other end into the Ethernet port on your computer, TV or console.</li><li>Wait 30 seconds. The port light should come on or blink. Your device should show it is connected by cable.</li>'
           '<li>If it says no internet, restart the router and try another LAN port and another cable.</li><li>Run our <a href="/speed-test">speed test</a> on the wired device to confirm your plan speed.</li></ol>'
           '<h2>Connect your modem or ONT to your own router</h2><ol class="steps"><li>Plug the Ethernet cable from the modem or fiber box (ONT) into the router\'s <b>WAN</b> or <b>Internet</b> port. This port is often a different color.</li>'
           '<li>Power the modem on first, wait until its lights settle, then power the router.</li><li>Connect your devices to the router\'s LAN ports or Wi-Fi.</li><li>If you use your own router with fiber, make sure it supports an Ethernet WAN connection.</li></ol>'
           '<div class="call tip"><b>Which port?</b>Plugging a device into the WAN port or plugging the modem into a LAN port is the most common reason a wired setup does not work.</div>'
           '<h2>Troubleshooting a wired connection</h2><ul><li>Try a different cable. Damaged cables are common.</li><li>Try a different LAN port.</li><li>Restart the router and the device.</li><li>Check the port light: no light usually means no link.</li><li>Some providers need the router to be the one connected to the modem. See your provider\'s guide below.</li></ul>'
           '<h2>Provider guides</h2><div class="grid">' + "".join(f'<a class="card" href="/help/{k}"><b>{esc(n)}</b><span>Lights, restart and fixes</span></a>' for k, n in cards_all) + "</div>")
    faq = [("Which port do I plug the Ethernet cable into?", "Use a LAN port to connect a device to your router. Use the WAN or Internet port only to connect the router to a modem or fiber box."),
           ("Why does my wired connection say no internet?", "Restart the router, try another cable and LAN port, and check that the router itself has an internet connection."),
           ("Is Ethernet faster than Wi-Fi?", "Usually it is more stable and often faster, especially for gaming, video calls and large downloads.")]
    save("/help/connect-ethernet-lan", page("/help/connect-ethernet-lan", "How to Connect an Ethernet (LAN) Cable to Your Router or Modem", "Connect devices to your router with an Ethernet cable, connect a modem or ONT to your own router, and fix a wired connection that says no internet.",
         "How to Connect a LAN (Ethernet) Cable", "Which port goes where, how to wire a modem to a router, and how to fix a wired connection.", lan, faq,
         [("Home", "https://yourbillcheck.com/"), ("Troubleshoot", "https://yourbillcheck.com/help"), ("LAN cable", "https://yourbillcheck.com/help/connect-ethernet-lan")], chips=["Any provider"]))

    red = ('<p>A red light almost always means the equipment cannot get online, is overheating or has a fault. The exact meaning depends on your provider. Pick yours:</p><div class="grid">'
           + "".join(f'<a class="card" href="/help/{k}/lights"><b>{esc(n)}</b><span>{esc(PROV[k]["tag"])}</span></a>' for k, n in cards_all if PROV[k]["tables"]) + "</div>"
           '<h2>What red usually means</h2><table><tr><th>Provider</th><th>Red light pattern</th><th>Meaning</th></tr>'
           '<tr><td>AT&T</td><td>Blinking red (slow)</td><td>No broadband connection. Check cables, then hold the red reset button for 10 seconds.</td></tr>'
           '<tr><td>AT&T</td><td>Solid red</td><td>Overheating (WPS light off) or a hardware issue (WPS light red).</td></tr>'
           '<tr><td>Xfinity</td><td>Steady red</td><td>No internet connection. Contact Xfinity.</td></tr>'
           '<tr><td>Verizon Fios</td><td>Solid red / fast blink</td><td>Hardware or system failure / overheating.</td></tr>'
           '<tr><td>CenturyLink C4000</td><td>Solid red ring</td><td>Network failure; call or chat.</td></tr>'
           '<tr><td>Cox</td><td>Online light off</td><td>Internet is not available. Check cables and reset.</td></tr></table>'
           '<h2>What to do first (any provider)</h2><ol class="steps"><li>Check for an outage in your provider\'s app.</li><li>Check that every cable is tight and undamaged, and the power cord is in a working outlet.</li><li>Make sure the equipment is not covered or in a hot, closed space.</li><li>Unplug it for 30 seconds and plug it back in. Wait up to 15 minutes.</li><li>If it stays red, contact your provider and tell them the exact light pattern.</li></ol>')
    faq = [("Is a red light on my router always bad?", "A red light usually means a problem, but some are brief during startup. If it stays red 10 to 15 minutes after a restart, treat it as a problem."), ("Can I fix a red router light myself?", "Often. Check cables, power and airflow and restart the equipment first. If it stays red, your provider needs to test the line or replace the unit."), ("Why is my router red but I still have internet?", "Some red lights point to a secondary issue, like phone registration or overheating. Check your provider's light table.")]
    save("/help/router-red-light", page("/help/router-red-light", "Router Red Light: What It Means and How to Fix It", "Router or modem showing a red light? What red means for AT&T, Xfinity, Verizon, CenturyLink and Cox, and how to fix it step by step.",
         "Router Red Light: What It Means", "Pick your provider to see exactly what your red or blinking light means, then follow the fix.", red, faq,
         [("Home", "https://yourbillcheck.com/"), ("Troubleshoot", "https://yourbillcheck.com/help"), ("Red light", "https://yourbillcheck.com/help/router-red-light")], chips=["All providers"]))

    # ---------- troubleshooter hub ----------
    provs = [(k, n) for k, n in cards_all]
    probs = [("🚦", "Lights: red, blinking or off", "lights"), ("🌐", "No internet / internet down", "no"), ("🐌", "Slow internet", "/help/slow-internet"), ("📶", "Wi-Fi keeps dropping", "/help/wifi-keeps-disconnecting"),
             ("🔌", "Connect a LAN / network cable", "/help/connect-ethernet-lan"), ("🔄", "Restart my router or modem", "restart"), ("📺", "TV not working", "/help/tv-not-working"), ("🎬", "Channels missing (ESPN, Showtime, Starz)", "/help/tv-channels-missing"), ("📱", "Lost or stolen SIM", "/help/lost-or-stolen-sim")]
    js = ("<script>(function(){var P=" + json.dumps({k: {"n": n, "l": bool(PROV[k]["tables"])} for k, n in provs}) + ",sel=null;var pr=document.getElementById('pp'),pb=document.getElementById('pb');"
          "var items=" + json.dumps([[a, b, c] for a, b, c in probs]) + ";"
          "Object.keys(P).forEach(function(k){var b=document.createElement('button');b.textContent=P[k].n;b.onclick=function(){sel=k;[].forEach.call(pr.children,function(x){x.className=''});b.className='on';render();document.getElementById('pb').scrollIntoView({behavior:'smooth',block:'start'})};pr.appendChild(b)});"
          "function render(){pb.innerHTML='';items.forEach(function(it){var u=it[2];if(u==='lights')u=P[sel].l?'/help/'+sel+'/lights':'/help/'+sel+'#no-internet';else if(u==='no')u='/help/'+sel+'#no-internet';else if(u==='restart')u='/help/'+sel+'#restart';"
          "var a=document.createElement('a');a.className='card';a.href=u;a.innerHTML='<span class=\"ic\">'+it[0]+'</span><b>'+it[1]+'</b><span>'+P[sel].n+'</span>';pb.appendChild(a)})}})();</script>")
    body = ('<h2>1. Who is your provider?</h2><div class="pick" id="pp"></div>'
            '<h2 id="problem">2. What is going wrong?</h2><div class="grid" id="pb"><p class="note">Pick your provider above to see fixes for your equipment.</p></div>'
            '<noscript><h2>Pick your provider</h2><ul>' + "".join(f'<li><a href="/help/{k}">{esc(n)}</a></li>' for k, n in provs) + '</ul></noscript>'
            '<h2>Fix by problem (any provider)</h2><div class="grid">' + "".join(f'<a class="card" href="{u}"><span class="ic">{ic}</span><b>{esc(t)}</b></a>' for ic, t, u in
              [("🔴", "Router red light", "/help/router-red-light"), ("🌐", "Internet not working", "/help/internet-not-working"), ("🐌", "Slow internet", "/help/slow-internet"), ("📶", "Wi-Fi keeps disconnecting", "/help/wifi-keeps-disconnecting"),
               ("🔌", "Connect a LAN cable", "/help/connect-ethernet-lan"), ("🛠️", "Modem and router setup", "/help/modem-router-setup"), ("📺", "TV not working", "/help/tv-not-working"), ("🎬", "Channels missing", "/help/tv-channels-missing"),
               ("📱", "Lost or stolen SIM", "/help/lost-or-stolen-sim"), ("✂️", "Cancel internet service", "/help/cancel-internet-service"), ("📦", "Moving your internet", "/help/move-internet-service"), ("🧰", "Self vs pro install", "/help/self-install-vs-professional-install")]) + "</div>"
            '<h2>Not sure what your lights mean?</h2><p>Every provider uses different colors. Our provider guides decode them using each provider\'s own support documents:</p><div class="grid">'
            + "".join(f'<a class="card" href="/help/{k}"><b>{esc(n)}</b><span>{esc(PROV[k]["tag"])}</span></a>' for k, n in provs) + "</div>")
    save("/help", page("/help", "Internet, TV and Router Troubleshooter: Fix It by Provider | YourBillCheck", "Pick your provider and problem: router red light, no internet, blinking lights, restart, Wi-Fi, LAN cable, TV and SIM fixes for AT&T, Xfinity, Spectrum, Verizon, Frontier, Cox and more.",
         "Fix It: Internet, TV and Router Troubleshooter", "Pick your provider, then your problem. Get exact steps for your equipment: what the lights mean, how to restart, and when to call.", body, None,
         [("Home", "https://yourbillcheck.com/"), ("Troubleshoot", "https://yourbillcheck.com/help")], chips=["9 providers", "Official sources"], script=js))
    return cards_all

C4000_RING = [
 ("blue", "blink", "Blinking or solid blue", "Booting up and syncing with the network.", "wait", "Wait up to 5 minutes; if it keeps blinking, check the DSL cord at the modem and wall jack."),
 ("green", "", "Solid green", "Online and connected.", "ok", "Nothing to do."),
 ("green", "blink", "Fast-flickering green", "Sending or receiving data.", "ok", "Normal."),
 ("green", "blink", "Blinking green", "WPS is searching for a device to connect.", "wait", "Select your network on the device."),
 ("red", "blink", "Blinking red", "WPS connection failed.", "wait", "Wait 2 minutes, check you chose the right network name (on the modem sticker), and retry."),
 ("red", "", "Solid red", "Network failure.", "fix", "Reboot the modem first, then call or chat with CenturyLink."),
 ("amber", "blink", "Blinking amber-green or amber-white", "Firmware update in progress.", "wait", "Do not unplug it."),
 ("red", "blink", "Blinking green-red", "Network issue.", "fix", "Call or chat with CenturyLink."),
 ("off", "", "Off", "Not connected to the network.", "fix", "Check power and the line, then reboot."),
]
C4000_DSL = [
 ("green", "", "DSL light solid green", "Connected with an active line (DSL models only).", "ok", "Nothing to do."),
 ("red", "", "DSL light solid red", "Connection error.", "fix", "Call or chat with CenturyLink."),
 ("off", "", "DSL light off", "Nothing connected to the DSL port.", "fix", "Plug the DSL cord into the modem and wall jack."),
]
TMO_G5_SCREENS = [
 ("Connection", "Up to five bars show cellular signal strength. An X means the gateway is not connected to the cellular network."),
 ("Devices", "How many wired and wireless devices are connected. Use the T-Life app to manage each device."),
 ("Internet Line Number", "Shows your internet number when a SIM card is installed."),
 ("Messages", "Lets you read messages from T-Mobile."),
 ("Language", "English and Español."),
]
MODELS = {
 "att": [("bgw320", "AT&T BGW320 Gateway", "AT&T BGW320 Wi-Fi Gateway: Lights, Reset and Fixes", ATT_BGW, None,
   "The BGW320 is the fiber Wi-Fi Gateway AT&T installs with many Fiber plans. A single Service light on the front tells you most of what you need to know, and a WPS light shows Wi-Fi pairing status.",
   ["Look at the front <b>Service</b> light and match it to the table.", "If it is <b>blinking red slowly</b>, check the cable, then press and hold the red <b>reset button for 10 seconds</b>.", "If it is <b>blinking red fast</b>, check myAT&T or Smart Home Manager for an outage and reboot.",
    "If it is <b>solid red</b>, check the WPS light: off means overheating (move it to a flat, carpet-free spot with airflow); red means a hardware issue (reboot, then contact AT&T for a replacement).", "<b>Solid blue</b> means internet backup mode during an outage; it returns to fiber when the outage ends.",
    "If the WPS light blinks green fast, the gateway is doing a factory reset: wait for it to restart."],
   "https://www.att.com/device-support/article/134376/at&t/bgw320/", "AT&T: BGW320 getting to know your equipment"),],
 "verizon": [("fios-router-g3100", "Verizon Fios Router G3100", "Verizon Fios Router G3100: Lights, Reset and Fixes", VZ, None,
   "The Fios Router G3100 has one front status light. Its color and blink pattern tell you whether it is working, booting, pairing or in trouble.",
   ["Read the front light: <b>white solid</b> is normal, <b>yellow solid</b> is no internet, <b>red solid</b> is a hardware or system failure.", "For a <b>soft reboot</b>, press and hold the rear Reset button for at least 3 seconds.",
    "For a <b>factory reset</b>, hold the Reset button at least 10 seconds. This erases settings, so note your Wi-Fi name and password first.", "You can also reboot from the router's web page: Advanced, Utilities, Reboot Router. Verizon's guide suggests doing this when Verizon support tells you to.",
    "<b>Red fast blink</b> means overheating; give it airflow. <b>Green solid</b> means Wi-Fi is turned off.", "If yellow or red persists, contact Verizon."],
   "https://www.verizon.com/content/dam/verizon/support/consumer/documents/internet/fios-router-user-guide.pdf", "Verizon: Fios Router G3100 user guide"),],
 "centurylink": [("c4000", "CenturyLink C4000 Modem", "CenturyLink C4000 Modem: Light Ring, Reset and Fixes", C4000_RING, C4000_DSL,
   "The C4000 has one light ring on the front, and DSL models add a DSL light on the back. The ring works the same on every C4000 model (DSL C4000BG, BZ, LG, LZ and fiber C4000XG).",
   ["Check the front ring color against the table. <b>Solid green</b> means online.", "<b>Solid red</b> means a network failure. Reboot the modem first; CenturyLink calls rebooting the first step for a red ring.",
    "On DSL models, check the rear DSL light: <b>red</b> is a connection error, <b>off</b> means nothing is plugged into the DSL port.", "If the ring keeps blinking blue for more than 5 minutes, check that the green DSL cord is firmly in the modem and the wall jack; if it repeats, service may not be active on that jack, so try another jack.",
    "After a failed WPS pairing, wait 2 minutes for the ring to return to solid green, confirm the network name on the modem sticker, and retry.", "For severe errors, CenturyLink says a reset and repeat setup may be needed, ideally with a support agent."],
   "https://www.centurylink.com/home/help/internet/modems-and-routers/greenwave-c4000/led-display-guide.html", "CenturyLink: C4000 modem light guide"),],
 "t-mobile": [("5g-gateway", "T-Mobile 5G Gateway Gen5", "T-Mobile 5G Gateway (Gen5): Screen, Signal Bars and Fixes", None, None,
   "The T-Mobile 5G Gateway Gen5 has an LCD screen instead of colored lights. You use the arrow buttons to move through screens that show signal, connected devices and messages.",
   ["On the <b>Connection</b> screen, count the bars. <b>An X</b> means the gateway is not connected to the cellular network.", "Move the gateway to a spot with stronger signal (near a window, higher up, away from large metal objects). T-Mobile notes the gateway operates between 32°F and 104°F.",
    "Restart it: unplug the gateway for 30 seconds, plug it back in, and wait 2 minutes before testing.", "T-Mobile installs firmware updates automatically between 1 and 3 a.m. Pacific, so leave the gateway powered on then and do not restart it during an update.",
    "Use the Devices screen or the T-Life app to see how many devices are connected.", "Turn off any VPN or firewall and restart connected devices. If the X stays, contact T-Mobile Home Internet support."],
   "https://www.t-mobile.com/support/home-internet/5g-gateway-g5", "T-Mobile: 5G Gateway Gen5"),],
}

def build_models(P, page, save):
    done = []
    for k, lst in MODELS.items():
        d = PROV[k]; n = d["name"]
        for slug, short, title, rows, rows2, lead, steps, src, srct in lst:
            body = f"<p>{esc(lead)}</p>"
            if rows:
                body += "<h2>What the lights mean</h2><table><tr><th>Light</th><th>What it means</th><th>What to do</th></tr>"
                for c, m, lab, mean, sev, act in rows:
                    lbl = {"ok": "OK", "wait": "WAIT", "fix": "ACTION"}[sev]
                    body += f'<tr><td>{dot(c, m)}<b>{esc(lab)}</b></td><td>{esc(mean)}<br><span class="sev {sev}">{lbl}</span></td><td>{esc(act)}</td></tr>'
                body += "</table>"
            if rows2:
                body += "<h2>Rear DSL light</h2><table><tr><th>Light</th><th>What it means</th><th>What to do</th></tr>" + "".join(
                    f'<tr><td>{dot(c, m)}<b>{esc(lab)}</b></td><td>{esc(mean)}<br><span class="sev {sev}">{ {"ok":"OK","wait":"WAIT","fix":"ACTION"}[sev] }</span></td><td>{esc(act)}</td></tr>' for c, m, lab, mean, sev, act in rows2) + "</table>"
            if not rows:
                body += "<h2>What the screen shows</h2><table><tr><th>Screen</th><th>What it shows</th></tr>" + "".join(f"<tr><td><b>{esc(a)}</b></td><td>{esc(b)}</td></tr>" for a, b in TMO_G5_SCREENS) + "</table>"
            body += f"<h2>Fix it step by step</h2><ol class=\"steps\">" + "".join(f"<li>{s}</li>" for s in steps) + "</ol>"
            body += '<div class="call warn"><b>Before any factory reset</b>It erases your Wi-Fi name, password and custom settings. Note them first, and reset only when the provider guide says to.</div>'
            body += f'<p>More: <a href="/help/{k}">{esc(n)} troubleshooting</a>' + (f' · <a href="/help/{k}/lights">all {esc(n)} lights</a>' if d["tables"] else "") + f' · <a href="/providers/{k}">support numbers</a>. Official source: <a href="{esc(src)}" rel="nofollow noopener">{esc(srct)}</a>.</p>'
            faq = [(f"How do I reset the {short}?", steps[1].replace("<b>", "").replace("</b>", "") if len(steps) > 1 else "See the steps above."),
                   (f"What does a red light mean on the {short}?" if rows else f"What does an X mean on the {short}?", "A red light means a problem such as no connection, overheating or hardware failure; see the table for your exact pattern." if rows else "An X means the gateway is not connected to the cellular network. Move it for a stronger signal and restart it."),
                   (f"Who do I contact if the {short} still fails?", f"Contact {n} support. See our {n} page for official numbers and links.")]
            save(f"/help/{k}/{slug}", page(f"/help/{k}/{slug}", title, f"{short}: what the lights or screen mean, how to reset it and how to fix common problems, from {n}'s own support guidance.",
                 f"{short}: Lights, Reset and Fixes", lead, body, faq,
                 [("Home", "https://yourbillcheck.com/"), ("Troubleshoot", "https://yourbillcheck.com/help"), (n, f"https://yourbillcheck.com/help/{k}"), (short, f"https://yourbillcheck.com/help/{k}/{slug}")], chips=[n, "Model guide"]))
            done.append((k, slug, short))
    return done
