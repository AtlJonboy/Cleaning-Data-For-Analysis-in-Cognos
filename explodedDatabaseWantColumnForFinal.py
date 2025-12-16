import pandas as pd

# Step 1: Load the source CSV
SOURCE_PATH = "survey_data_updated 5.csv"
df = pd.read_csv(SOURCE_PATH)
print(f"Loaded rows: {len(df)}; columns: {list(df.columns)[:5]} ...")

# Step 2: Extract just the DatabaseWantToWorkWith values into a single column CSV
LANG_COL = "DatabaseWantToWorkWith"
OUTPUT_VALUES_ONLY = "DatabaseWantToValues Only.csv"

if LANG_COL not in df.columns:
	raise KeyError(f"Column '{LANG_COL}' not found in the source file")

# Split the semicolon-delimited entries, trim whitespace, and drop empties
langs_series = (
	df[LANG_COL]
	.dropna()
	.astype(str)
	.str.split(';')
	.explode()
	.str.strip()
)
langs_series = langs_series[langs_series != ""]

# Write to a new CSV with a single column named 'Database'
langs_df = pd.DataFrame({"Database": langs_series})
langs_df.to_csv(OUTPUT_VALUES_ONLY, index=False)
print(f"Wrote {OUTPUT_VALUES_ONLY} with {len(langs_df)} rows.")

