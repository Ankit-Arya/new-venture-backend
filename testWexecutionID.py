# ----------------------FORMATTING TC
import re
import pandas as pd
# ================= CONFIG =================

INPUT_FILE = "temp_files/trip_chart_15f93bd7-dce5-4d15-875f-62193dfd61fb.xlsx"
OUTPUT_FILE = "temp_files/final_trip_chart_15f93bd7-dce5-4d15-875f-62193dfd61fb.csv"

DATETIME_COLS = [
    "Sign_On",
    "Sign_Off",
    "Trip_Start",
    "Trip_End"
]

DURATION_COLS = [
    "ACTUAL_DUTYHOURS",
    "Trip_Duration",
    "breaks",
    "Single_Run",
    "Total_Run"
]

# ================= HELPERS =================

def format_datetime_to_hhmm(val):
    """Convert datetime to HH:MM"""
    if pd.isna(val):
        return ""
    try:
        return pd.to_datetime(val).strftime("%H:%M")
    except Exception:
        return ""

def format_duration_to_hhmm(val):
    """
    Handles:
    - Excel time fractions (0.325694444)
    - HH:MM strings
    - H:M strings
    """
    if pd.isna(val):
        return ""

    val_str = str(val).strip()

    if val_str == "":
        return ""

    # Case 1: Excel duration as float (fraction of day)
    try:
        f = float(val_str)
        if 0 <= f < 1:
            total_minutes = round(f * 24 * 60)
            h = total_minutes // 60
            m = total_minutes % 60
            return f"{h:02d}:{m:02d}"
    except ValueError:
        pass

    # Case 2: HH:MM or H:M string
    match = re.fullmatch(r"(\d{1,2}):(\d{1,2})", val_str)
    if match:
        h, m = match.groups()
        return f"{int(h):02d}:{int(m):02d}"

    return ""

# ================= READ =================

# Read Excel WITHOUT forcing dtype
df = pd.read_excel(INPUT_FILE)

# Drop accidental index column
df = df.loc[:, ~df.columns.str.contains("^Unnamed")]

# ================= TRANSFORM =================

# Datetime columns
for col in DATETIME_COLS:
    if col in df.columns:
        df[col] = df[col].apply(format_datetime_to_hhmm)

# Duration columns
for col in DURATION_COLS:
    if col in df.columns:
        df[col] = df[col].apply(format_duration_to_hhmm)

# ================= SAVE =================

df.to_csv(OUTPUT_FILE, index=False)
print("✅ Saved correctly formatted file:", OUTPUT_FILE)