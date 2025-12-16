import pandas as pd
import re
from typing import Dict

# Configuration
INPUT_FILE = "LanguageWantValuesOnly.csv"
OUTPUT_FILE = "LanguageWantValuesClean.csv"
# If True, conflates 'java' and 'javascript' (and 'js') to the same label
MERGE_JAVA_AND_JAVASCRIPT = True
JAVA_JS_CANONICAL = "JavaScript"  # Used when MERGE_JAVA_AND_JAVASCRIPT is True

# Build normalization map: keys are normalized tokens (lowercase, stripped)
# Values are canonical labels to emit
BASE_NORMALIZATION_MAP: Dict[str, str] = {
    # JavaScript and variants
    "javascript": "JavaScript",
    "javasript": "JavaScript",
    "javacript": "JavaScript",
    "javscript": "JavaScript",
    "js": "JavaScript",
    "node": "JavaScript",
    "nodejs": "JavaScript",
    "node.js": "JavaScript",
    "typescript": "TypeScript",
    "ts": "TypeScript",
    # Python and variants
    "python": "Python",
    "py": "Python",
    "python3": "Python",
    "python 3": "Python",
    "python2": "Python",
    "python 2": "Python",
    "pyhton": "Python",
    "pyrthon": "Python",
    "phyton": "Python",
    # Java and variants
    "java": "Java",
    # C family
    "c#": "C#",
    "c-sharp": "C#",
    "c sharp": "C#",
    "cs": "C#",
    "c++": "C++",
    "cpp": "C++",
    "c plus plus": "C++",
    "c": "C",
    # Go
    "go": "Go",
    "golang": "Go",
    # Web basics
    "html": "HTML",
    "css": "CSS",
    # Other common languages
    "php": "PHP",
    "ruby": "Ruby",
    "rb": "Ruby",
    "rust": "Rust",
    "kotlin": "Kotlin",
    "swift": "Swift",
    "scala": "Scala",
    "r": "R",
    "matlab": "MATLAB",
    "octave": "Octave",
    "perl": "Perl",
    "dart": "Dart",
    "lua": "Lua",
    "haskell": "Haskell",
    "elixir": "Elixir",
    "clojure": "Clojure",
    "powershell": "PowerShell",
    "bash": "Bash/Shell",
    "sh": "Bash/Shell",
    "zsh": "Bash/Shell",
    "shell": "Bash/Shell",
    # SQL and related terms (keep specific engines distinct)
    "sql": "SQL",
    "postgres": "PostgreSQL",
    "postgresql": "PostgreSQL",
    "mysql": "MySQL",
    "sqlite": "SQLite",
}

# If requested, force Java and JavaScript (and JS) into one bucket
if MERGE_JAVA_AND_JAVASCRIPT:
    for k in ("java", "javascript", "js"):
        BASE_NORMALIZATION_MAP[k] = JAVA_JS_CANONICAL
    # Also map node to the canonical if chosen as JavaScript
    BASE_NORMALIZATION_MAP["node"] = JAVA_JS_CANONICAL
    BASE_NORMALIZATION_MAP["nodejs"] = JAVA_JS_CANONICAL
    BASE_NORMALIZATION_MAP["node.js"] = JAVA_JS_CANONICAL


def _basic_tokenize(s: str) -> str:
    """Lowercase, trim, and collapse punctuation/spaces for matching."""
    if s is None:
        return ""
    s = str(s).strip().lower()
    # normalize common punctuation and multiple spaces
    s = s.replace("_", " ")
    s = s.replace("-", " ")
    s = s.replace(".", " ")
    s = re.sub(r"\s+", " ", s)
    return s


def normalize_language(label: str) -> str:
    token = _basic_tokenize(label)
    if token in BASE_NORMALIZATION_MAP:
        return BASE_NORMALIZATION_MAP[token]
    # Try lightweight fixes for near-misses (drop spaces)
    token_nospace = token.replace(" ", "")
    if token_nospace in BASE_NORMALIZATION_MAP:
        return BASE_NORMALIZATION_MAP[token_nospace]
    # Fallback: Title-case the original stripped string
    return str(label).strip().title()


def main() -> None:
    df = pd.read_csv(INPUT_FILE)
    if "Language" not in df.columns:
        raise KeyError("Expected a 'Language' column in the input file")

    # Drop missing/blank
    series = df["Language"].dropna().astype(str).str.strip()
    series = series[series != ""]

    # Normalize
    normalized = series.apply(normalize_language)

    # Output single-column CSV with canonical names
    out_df = pd.DataFrame({"Language": normalized})
    out_df.to_csv(OUTPUT_FILE, index=False)

    # Basic summary to console
    counts = out_df["Language"].value_counts().head(20)
    print(f"Wrote {OUTPUT_FILE} with {len(out_df)} rows.")
    print("Top 20 languages after normalization:\n", counts.to_string())


if __name__ == "__main__":
    main()
