data={
    "Network": {
        "Technology": " LTE || HSPA  ||GSM ",
        "2G bands": " 1900 - SIM 1 & SIM 2 || 1800  || 900  ||GSM 850 ",
        "3G bands": " 2100  || 900  ||HSDPA 850 ",
        "4G bands": " 41 - International,  40,  38,  28,  20,  8,  7,  5,  3, 1",
        "\u00a0": " 41 - India,  40,  8,  5,  3, 1",
        "Speed": " LTE ||HSPA 42.2, 5.76 Mbps"
    },
    "Launch": {
        "Announced": " September 06, 2022",
        "Status": " September 09, Available. Released 2022"
    },
    "Body": {
        "Dimensions": "164.9 x 76.8 x 9.1 mm (6.49 x 3.02 x 0.36 in)",
        "Weight": "192 g (6.77 oz)",
        "SIM": " dual stand-by), Dual SIM (Nano-SIM"
    },
    "Display": {
        "Type": " 400 nits (typ), IPS LCD",
        "Size": " 102.6 cm2 (~81.0% screen-to-body ratio), 6.52 inches",
        "Resolution": "9 ratio (~269 ppi density), 720 x 1600 pixels || 20"
    },
    "Platform": {
        "OS": " MIUI 12, Android 12 (Go edition)",
        "Chipset": "Mediatek MT6761 Helio A22 (12 nm)",
        "CPU": "Quad-core 2.0 GHz Cortex-A53",
        "GPU": "PowerVR GE8320"
    },
    "Memory": {
        "Card slot": "microSDXC (dedicated)",
        "Internal": " 32GB 3GB RAM, 32GB 2GB RAM",
        "\u00a0": "eMMC 5.1"
    },
    "Main Camera": {
        "Dual": " f,  (wide)\r0.08 MP (QVGA) ||8 MP, 2.0",
        "Features": " HDR, Dual-LED flash",
        "Video": "1080p@30fps"
    },
    "Selfie camera": {
        "Single": " f, 2.2 ||5 MP",
        "Video": "1080p@30fps"
    },
    "Sound": {
        "Loudspeaker ": "Yes",
        "3.5mm jack ": "Yes"
    },
    "Comms": {
        "WLAN": " hotspot ||g ||b ||Wi-Fi 802.11 a, n",
        "Bluetooth": " LE,  A2DP, 5.0",
        "GPS": " BDS,  GALILEO,  GLONASS,  with A-GPS, Yes",
        "NFC": "No",
        "Radio": "FM radio",
        "USB": "microUSB 2.0"
    },
    "Features": {
        "Sensors": "Accelerometer"
    },
    "Battery": {
        "Type": " non-removable, Li-Po 5000 mAh"
    },
    "Misc": {
        "Colors": " Black,  Light Blue, Light Green",
        "Price": "299 || \u20ac\u2009103.00  ||$\u200999.99 ,  \u20b9\u20096"
    },
    "PRICE": {
        "32GB 2GB RAM": "$\u200999.99"
    }
} 

def jsontotext(data):
    text=""
    for key in data.keys():
        text += "========== "+key+" ==========\n"
        # print("========== "+key+" ==========")
        for ckey in data[key].keys():
            # print("   -> "+ckey+(12-len(ckey))*" "+": "+data[key][ckey])
            text += "   -> "+ckey+(12-len(ckey))*" "+": "+data[key][ckey]+"\n"
        # print("\n")
        text+="\n"
    return text

print(jsontotext(data))