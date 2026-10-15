# iotconfig/settings.py
WIDTH = 960
HEIGHT = 660

# Industrial SOC Interface Color Schemes (Hex Codes)
COLOR_BG_DARK = "#090c15"       # Deep slate plant floor background
COLOR_PANEL_BG = "#121824"      # Factory equipment telemetry panel container
COLOR_TEXT_WHITE = "#ffffff"    # Main sensor numbers white readout labels
COLOR_TEXT_MUTED = "#7d8fa9"    # Grey-blue secondary channel names

# Industrial Alert Identifiers
COLOR_STABLE = "#00e676"       # Neon green tag for stable operational parameters
COLOR_BREAKDOWN = "#ff1744"    # Warning red tag for predicted machine breakdowns

CRITICAL_TEMP_CELSIUS = 92.5   # Safety limit boundary for machinery overheating
