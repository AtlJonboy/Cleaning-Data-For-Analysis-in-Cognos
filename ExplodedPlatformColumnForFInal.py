import pandas as pd

# Load the source CSV
SOURCE_PATH = "survey_data_updated 5.csv"
df = pd.read_csv(SOURCE_PATH)
print(f"Loaded rows: {len(df)}; columns: {list(df.columns)[:5]} ...")

# Extract just the PlatformHaveWorkedWith values into a single column CSV
PLAT_COL = "PlatformHaveWorkedWith"
OUTPUT_VALUES_ONLY = "platforms_values_only.csv"

if PLAT_COL not in df.columns:
	raise KeyError(f"Column '{PLAT_COL}' not found in the source file")

# Split the semicolon-delimited entries, trim whitespace, and drop empties
plat_series = (
	df[PLAT_COL]
	.dropna()
	.astype(str)
	.str.split(';')
	.explode()
	.str.strip()
)
plat_series = plat_series[plat_series != ""]

# Write to a new CSV with a single column named 'Platforms'
plat_df = pd.DataFrame({"Platforms": plat_series})
plat_df.to_csv(OUTPUT_VALUES_ONLY, index=False)
print(f"Wrote {OUTPUT_VALUES_ONLY} with {len(plat_df)} rows and column 'Platforms'.")

