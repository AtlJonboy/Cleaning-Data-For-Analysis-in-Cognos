import pandas as pd

# Step 1: Load the source CSV
SOURCE_PATH = "survey_data_updated 5.csv"
df = pd.read_csv(SOURCE_PATH)
print(f"Loaded rows: {len(df)}; columns: {list(df.columns)[:5]} ...")

# Step 2: Extract just the DatabaseHaveWorkedWith values into a single column CSV
DB_COL = "DatabaseHaveWorkedWith"
OUTPUT_VALUES_ONLY = "database_values_only.csv"

if DB_COL not in df.columns:
	raise KeyError(f"Column '{DB_COL}' not found in the source file")

# Split the semicolon-delimited entries, trim whitespace, and drop empties
db_series = (
	df[DB_COL]
	.dropna()
	.astype(str)
	.str.split(';')
	.explode()
	.str.strip()
)
db_series = db_series[db_series != ""]

# Write to a new CSV with a single column named 'databases'
db_df = pd.DataFrame({"Databases": db_series})
db_df.to_csv(OUTPUT_VALUES_ONLY, index=False)
print(f"Wrote {OUTPUT_VALUES_ONLY} with {len(db_df)} rows and column 'Databases'.")

