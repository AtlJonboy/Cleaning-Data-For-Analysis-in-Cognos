import pandas as pd
import re
from typing import Dict

INPUT_FILE = "DatabaseWantToValues Only.csv"
OUTPUT_FILE = "DatabaseWantValuesClean.csv"

# Map common nicknames, misspellings, and variants to canonical database names
NORMALIZATION_MAP: Dict[str, str] = {
    # PostgreSQL
    "postgres": "PostgreSQL",
    "postgresql": "PostgreSQL",
    "postgre": "PostgreSQL",
    "postgress": "PostgreSQL",
    "psql": "PostgreSQL",
    # MySQL / MariaDB
    "mysql": "MySQL",
    "maria": "MariaDB",
    "mariadb": "MariaDB",
    # SQLite
    "sqlite": "SQLite",
    "sqlite3": "SQLite",
    # SQL Server
    "sql server": "SQL Server",
    "mssql": "SQL Server",
    "ms sql": "SQL Server",
    "azure sql": "SQL Server",
    # Oracle
    "oracle": "Oracle",
    "oracle db": "Oracle",
    # Redis
    "redis": "Redis",
    # MongoDB
    "mongodb": "MongoDB",
    "mongo": "MongoDB",
    # Cassandra
    "cassandra": "Cassandra",
    # Elastic
    "elasticsearch": "Elasticsearch",
    "elastic": "Elasticsearch",
    "es": "Elasticsearch",
    # DynamoDB
    "dynamodb": "DynamoDB",
    # BigQuery
    "bigquery": "BigQuery",
    # Snowflake
    "snowflake": "Snowflake",
    # Firebase
    "firebase": "Firebase Realtime Database",
    "firebase realtime database": "Firebase Realtime Database",
    "firestore": "Cloud Firestore",
    # Neo4j
    "neo4j": "Neo4j",
    # CockroachDB
    "cockroach": "CockroachDB",
    "cockroachdb": "CockroachDB",
    # DuckDB
    "duckdb": "DuckDB",
    # Supabase (Postgres-based, but keep distinct label unless desired merge)
    "supabase": "Supabase",
    # TimescaleDB (Postgres extension)
    "timescaledb": "TimescaleDB",
    # InfluxDB
    "influx": "InfluxDB",
    "influxdb": "InfluxDB",
    # MariaDB already above
    # Teradata
    "teradata": "Teradata",
    # IBM Db2
    "db2": "IBM Db2",
    "ibm db2": "IBM Db2",
    # SAP HANA
    "hana": "SAP HANA",
    "sap hana": "SAP HANA",
}

MERGE_SQL_VARIANTS = True  # Optionally merge generic "sql" to common engines (kept as generic label)
GENERIC_SQL_LABEL = "SQL (Generic)"


def _norm_token(s: str) -> str:
    s = str(s).strip().lower()
    s = s.replace("_", " ")
    s = s.replace("-", " ")
    s = s.replace(".", " ")
    s = re.sub(r"\s+", " ", s)
    return s


def normalize_db(name: str) -> str:
    t = _norm_token(name)
    if t in NORMALIZATION_MAP:
        return NORMALIZATION_MAP[t]
    # try removing spaces
    t_ns = t.replace(" ", "")
    if t_ns in NORMALIZATION_MAP:
        return NORMALIZATION_MAP[t_ns]
    # optional generic SQL bucket
    if MERGE_SQL_VARIANTS and (t == "sql" or t.startswith("sql ") or t.endswith(" sql")):
        return GENERIC_SQL_LABEL
    # title-case fallback
    return str(name).strip().title()


def main() -> None:
    df = pd.read_csv(INPUT_FILE)
    if "Database" not in df.columns:
        raise KeyError("Expected a 'Database' column in the input file")

    series = df["Database"].dropna().astype(str).str.strip()
    series = series[series != ""]

    normalized = series.apply(normalize_db)

    out_df = pd.DataFrame({"Database": normalized})
    out_df.to_csv(OUTPUT_FILE, index=False)

    counts = out_df["Database"].value_counts().head(20)
    print(f"Wrote {OUTPUT_FILE} with {len(out_df)} rows.")
    print("Top 20 databases after normalization:\n", counts.to_string())


if __name__ == "__main__":
    main()
