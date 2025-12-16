import pandas as pd
import re
from typing import Dict

INPUT_FILE = "PlatformWantToValues Only.csv"
OUTPUT_FILE = "PlatformWantValuesClean.csv"

# Normalize common platform names, ecosystems, and variants
NORMALIZATION_MAP: Dict[str, str] = {
    # Cloud providers
    "aws": "AWS",
    "amazon web services": "AWS",
    "ec2": "AWS",
    "lambda": "AWS",
    "azure": "Azure",
    "microsoft azure": "Azure",
    "gcp": "Google Cloud Platform",
    "google cloud": "Google Cloud Platform",
    "google cloud platform": "Google Cloud Platform",
    # Mobile / OS platforms
    "android": "Android",
    "ios": "iOS",
    "iphone os": "iOS",
    "macos": "macOS",
    "osx": "macOS",
    "windows": "Windows",
    "linux": "Linux",
    # Container / orchestration
    "docker": "Docker",
    "k8s": "Kubernetes",
    "kubernetes": "Kubernetes",
    "openshift": "OpenShift",
    # Runtime/framework ecosystems
    "dotnet": ".NET",
    ".net": ".NET",
    "net": ".NET",
    "node": "Node.js",
    "nodejs": "Node.js",
    "node.js": "Node.js",
    "deno": "Deno",
    # Web stacks / platforms
    "nextjs": "Next.js",
    "nuxt": "Nuxt.js",
    "nuxtjs": "Nuxt.js",
    "wordpress": "WordPress",
    "drupal": "Drupal",
    "shopify": "Shopify",
    "wix": "Wix",
    "vercel": "Vercel",
    "netlify": "Netlify",
    # Data platforms
    "databricks": "Databricks",
    "snowflake": "Snowflake",
    "bigquery": "BigQuery",
    "hadoop": "Hadoop",
    "spark": "Apache Spark",
    # Game engines
    "unity": "Unity",
    "unreal": "Unreal Engine",
    "unreal engine": "Unreal Engine",
}


def _norm_token(s: str) -> str:
    s = str(s).strip().lower()
    s = s.replace("_", " ")
    s = s.replace("-", " ")
    s = s.replace(".", " ")
    s = re.sub(r"\s+", " ", s)
    return s


def normalize_platform(name: str) -> str:
    t = _norm_token(name)
    if t in NORMALIZATION_MAP:
        return NORMALIZATION_MAP[t]
    # try removing spaces
    t_ns = t.replace(" ", "")
    if t_ns in NORMALIZATION_MAP:
        return NORMALIZATION_MAP[t_ns]
    # fallback title-case
    return str(name).strip().title()


def main() -> None:
    df = pd.read_csv(INPUT_FILE)
    if "Platform" not in df.columns:
        raise KeyError("Expected a 'Platform' column in the input file")

    series = df["Platform"].dropna().astype(str).str.strip()
    series = series[series != ""]

    normalized = series.apply(normalize_platform)

    out_df = pd.DataFrame({"Platform": normalized})
    out_df.to_csv(OUTPUT_FILE, index=False)

    counts = out_df["Platform"].value_counts().head(20)
    print(f"Wrote {OUTPUT_FILE} with {len(out_df)} rows.")
    print("Top 20 platforms after normalization:\n", counts.to_string())


if __name__ == "__main__":
    main()
