import pandas as pd

# ── 1. Paths ───────────────────────────────────────────────────────
DATA_DIR = "Datasets"      # where your raw CSVs live
OUT_DIR  = "clean_data"          # where you want to save merged_singapore.csv

# ── 2. Load raw tables ────────────────────────────────────────────
races        = pd.read_csv(f"{DATA_DIR}/races.csv")
results      = pd.read_csv(f"{DATA_DIR}/results.csv")
drivers      = pd.read_csv(f"{DATA_DIR}/drivers.csv")
constructors = pd.read_csv(f"{DATA_DIR}/constructors.csv")
circuits     = pd.read_csv(f"{DATA_DIR}/circuits.csv")

print("Races columns:", races.columns.tolist())
print("Constructors columns:", constructors.columns.tolist())

# ── 3. Prepare constructors ───────────────────────────────────────
#    Rename 'name' → 'team_name' so we don’t collide with races.name
constructors = constructors.rename(columns={'name': 'team_name'})

# ── 4. Merge results + races ──────────────────────────────────────
df = results.merge(
    races[['raceId', 'year', 'name', 'circuitId']],
    on='raceId',
    how='left'
)

# ── 5. Merge in drivers ────────────────────────────────────────────
df = df.merge(
    drivers[['driverId', 'forename', 'surname']],
    on='driverId',
    how='left'
)
df['driver_name'] = df['forename'] + ' ' + df['surname']

# ── 6. Merge in constructors (team names) ─────────────────────────
df = df.merge(
    constructors[['constructorId', 'team_name']],
    on='constructorId',
    how='left'
)

# ── 7. Merge in circuits ──────────────────────────────────────────
df = df.merge(
    circuits[['circuitId', 'circuitRef', 'country']],
    on='circuitId',
    how='left'
)

# ── 8. Filter for Singapore GP ────────────────────────────────────
#    Use the race 'name' column, not team_name
singapore_df = df[df['name'].str.contains("Singapore", case=False, na=False)]

# ── 9. Drop columns you won’t need ────────────────────────────────
cols_to_drop = [
    'number', 'positionText', 'url',
    'forename', 'surname', 'circuitRef'
]
singapore_df = singapore_df.drop(columns=cols_to_drop, errors='ignore')

# ── 10. Save the merged dataset ───────────────────────────────────
singapore_df.to_csv(f"{OUT_DIR}/merged_singapore.csv", index=False)
print("✅ Merged Singapore dataset saved to", f"{OUT_DIR}/merged_singapore.csv")
print("Shape:", singapore_df.shape)
