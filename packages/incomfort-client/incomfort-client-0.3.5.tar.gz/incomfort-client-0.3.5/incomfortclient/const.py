# key label: displ_code
DISPLAY_CODES = {
    0: "opentherm",
    15: "boiler ext.",
    24: "frost",
    37: "central heating rf",
    51: "tapwater int.",
    85: "sensortest",
    102: "central heating",
    126: "standby",
    153: "postrun boiler",
    170: "service",
    204: "tapwater",
    231: "postrun ch",
    240: "boiler int.",
    255: "buffer",
}

FAULT_CODES = {
    0: "Sensor fault after self check",
    1: "Temperature too high",
    2: "S1 and S2 interchanged",
    4: "No flame signal",
    5: "Poor flame signal",
    6: "Flame detection fault",
    8: "Incorrect fan speed",

    10: "Sensor fault S1",
    11: "Sensor fault S1",
    12: "Sensor fault S1",
    13: "Sensor fault S1",
    14: "Sensor fault S1",

    20: "Sensor fault S2",
    21: "Sensor fault S2",
    22: "Sensor fault S2",
    23: "Sensor fault S2",
    24: "Sensor fault S2",

    27: "Shortcut outside sensor temperature",

    29: "Gas valve relay faulty",
    30: "Gas valve relay faulty",
}  # "0.0": "Low system pressure"