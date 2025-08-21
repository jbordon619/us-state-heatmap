import pandas as pd

# Mapping from full name to abbreviation
US_STATE_ABBR = {
    "Alabama": "AL", "Alaska": "AK", "Arizona": "AZ", "Arkansas": "AR",
    "California": "CA", "Colorado": "CO", "Connecticut": "CT", "Delaware": "DE",
    "Florida": "FL", "Georgia": "GA", "Hawaii": "HI", "Idaho": "ID",
    "Illinois": "IL", "Indiana": "IN", "Iowa": "IA", "Kansas": "KS",
    "Kentucky": "KY", "Louisiana": "LA", "Maine": "ME", "Maryland": "MD",
    "Massachusetts": "MA", "Michigan": "MI", "Minnesota": "MN", "Mississippi": "MS",
    "Missouri": "MO", "Montana": "MT", "Nebraska": "NE", "Nevada": "NV",
    "New Hampshire": "NH", "New Jersey": "NJ", "New Mexico": "NM", "New York": "NY",
    "North Carolina": "NC", "North Dakota": "ND", "Ohio": "OH", "Oklahoma": "OK",
    "Oregon": "OR", "Pennsylvania": "PA", "Rhode Island": "RI", "South Carolina": "SC",
    "South Dakota": "SD", "Tennessee": "TN", "Texas": "TX", "Utah": "UT",
    "Vermont": "VT", "Virginia": "VA", "Washington": "WA", "West Virginia": "WV",
    "Wisconsin": "WI", "Wyoming": "WY", "District Of Columbia": "DC"
}

# Build reverse mapping: abbreviation → full name
US_STATE_ABBR_REV = {abbr: name for name, abbr in US_STATE_ABBR.items()}

# Build a lookup dict for both full names and abbreviations (all normalized to uppercase)
US_STATE_LOOKUP = {k.upper(): v for k, v in US_STATE_ABBR.items()}
US_STATE_LOOKUP.update({k.upper(): k.upper() for k in US_STATE_ABBR.values()})  # Add abbrev-to-abbrev

def load_and_validate(csv_file):
    df = pd.read_csv(csv_file)

    # Heuristic: first string column = state, first numeric column = value
    str_cols = df.select_dtypes(include="object").columns
    num_cols = df.select_dtypes("number").columns

    if not (str_cols.size and num_cols.size):
        raise ValueError("Need at least one text and one numeric column.")

    df = df[[str_cols[0], num_cols[0]]].copy()
    df.columns = ["state_raw", "value"]

    # Normalize input states
    df["state_clean"] = df["state_raw"].str.strip().str.upper()
    df["state"] = df["state_clean"].map(US_STATE_LOOKUP)

    # Identify any unrecognized values
    bad = df[df["state"].isna()]["state_raw"].unique()
    if bad.size:
        raise ValueError(f"Unknown state(s): {', '.join(bad)}")

    return df[["state_raw", "state", "value"]]
