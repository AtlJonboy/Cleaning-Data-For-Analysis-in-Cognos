import pandas as pd

# Load the source CSV
SOURCE_PATH = "survey_data_updated 5.csv"
df = pd.read_csv(SOURCE_PATH)
print(f"Loaded rows: {len(df)}; columns: {list(df.columns)[:5]} ...")

# Extract just the WebFrameHaveWorkedWith values into a single column CSV
WF_COL = "WebframeHaveWorkedWith"
OUTPUT_VALUES_ONLY = "webframes_values_only.csv"

if WF_COL not in df.columns:
	raise KeyError(f"Column '{WF_COL}' not found in the source file")

# Split the semicolon-delimited entries, trim whitespace, and drop empties
wf_series = (
	df[WF_COL]
	.dropna()
	.astype(str)
	.str.split(';')
	.explode()
	.str.strip()
)
wf_series = wf_series[wf_series != ""]

# Write to a new CSV with a single column named 'WebFrames'
wf_df = pd.DataFrame({"WebFrames": wf_series})
wf_df.to_csv(OUTPUT_VALUES_ONLY, index=False)
print(f"Wrote {OUTPUT_VALUES_ONLY} with {len(wf_df)} rows and column 'WebFrames'.")

