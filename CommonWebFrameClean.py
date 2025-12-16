import pandas as pd
import re
from typing import Dict

INPUT_FILE = "WebFrameWantToValues Only.csv"
OUTPUT_FILE = "WebFrameWantValuesClean.csv"

# Normalize common web frameworks / libraries
NORMALIZATION_MAP: Dict[str, str] = {
    # React ecosystem
    "react": "React",
    "reactjs": "React",
    "react.js": "React",
    # Angular
    "angular": "Angular",
    "angularjs": "AngularJS",
    "angular.js": "AngularJS",
    # Vue
    "vue": "Vue.js",
    "vuejs": "Vue.js",
    "vue.js": "Vue.js",
    # Svelte
    "svelte": "Svelte",
    # Next.js / Nuxt.js
    "next": "Next.js",
    "nextjs": "Next.js",
    "next.js": "Next.js",
    "nuxt": "Nuxt.js",
    "nuxtjs": "Nuxt.js",
    "nuxt.js": "Nuxt.js",
    # Remix
    "remix": "Remix",
    # Astro
    "astro": "Astro",
    # Solid
    "solid": "SolidJS",
    "solidjs": "SolidJS",
    # jQuery
    "jquery": "jQuery",
    # Backend web frameworks
    "django": "Django",
    "flask": "Flask",
    "fastapi": "FastAPI",
    "express": "Express",
    "expressjs": "Express",
    "express.js": "Express",
    "spring": "Spring",
    "spring boot": "Spring Boot",
    "rails": "Ruby on Rails",
    "ruby on rails": "Ruby on Rails",
    "laravel": "Laravel",
    "symfony": "Symfony",
    "phoenix": "Phoenix",
    "nest": "NestJS",
    "nestjs": "NestJS",
    "gin": "Gin (Go)",
    "asp.net": "ASP.NET",
    "aspnet": "ASP.NET",
    "asp .net": "ASP.NET",
    "play": "Play Framework",
    # Others
    "backbone": "Backbone.js",
    "ember": "Ember.js",
    "emberjs": "Ember.js",
    "ember.js": "Ember.js",
    "bootstrap": "Bootstrap",
    "tailwind": "Tailwind CSS",
    "tailwindcss": "Tailwind CSS",
}


def _norm_token(s: str) -> str:
    s = str(s).strip().lower()
    s = s.replace("_", " ")
    s = s.replace("-", " ")
    s = s.replace(".", " ")
    s = re.sub(r"\s+", " ", s)
    return s


def normalize_webframe(name: str) -> str:
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
    if "WebFrame" not in df.columns:
        raise KeyError("Expected a 'WebFrame' column in the input file")

    series = df["WebFrame"].dropna().astype(str).str.strip()
    series = series[series != ""]

    normalized = series.apply(normalize_webframe)

    out_df = pd.DataFrame({"WebFrame": normalized})
    out_df.to_csv(OUTPUT_FILE, index=False)

    counts = out_df["WebFrame"].value_counts().head(20)
    print(f"Wrote {OUTPUT_FILE} with {len(out_df)} rows.")
    print("Top 20 web frameworks after normalization:\n", counts.to_string())


if __name__ == "__main__":
    main()
