import pandas as pd

# ── 1. Load merged Singapore GP data ─────────────────────────────────────────────
df = pd.read_csv("data/merged_singapore.csv")

# ── 2. Coerce 'position' to numeric, drop invalid rows ───────────────────────────
df['position'] = pd.to_numeric(df['position'], errors='coerce')
df = df.dropna(subset=['position'])
df['position'] = df['position'].astype(int)

# ── 3. Create target variable: 1 if the driver won, else 0 ───────────────────────
df['win'] = (df['position'] == 1).astype(int)

# ── 4. Historical performance features ───────────────────────────────────────────
races_count = (
    df.groupby('driver_name')['raceId']
      .count()
      .rename('sg_race_count')
)
wins_count = (
    df.groupby('driver_name')['win']
      .sum()
      .rename('sg_win_count')
)
avg_finish = (
    df.groupby('driver_name')['position']
      .mean()
      .rename('sg_avg_finish')
)

# ── 5. Recent form features (last 3 Singapore races) ─────────────────────────────
recent_stats_list = []
for driver, subdf in df.groupby('driver_name'):
    last3 = subdf.sort_values('year').tail(3)
    recent_stats_list.append({
        'driver_name': driver,
        'sg_last3_avg_finish': last3['position'].mean(),
        'sg_last3_podiums': (last3['position'] <= 3).sum()
    })
recent = pd.DataFrame(recent_stats_list).set_index('driver_name')

# ── 6. Team strength feature: team’s win rate at Singapore ───────────────────────
team_wins = df.groupby('team_name')['win'].sum()
team_races = df.groupby('team_name')['raceId'].count()
team_winrate = (team_wins / team_races).rename('team_sg_winrate')

# ── 7. Combine all features into one DataFrame ──────────────────────────────────
features = pd.DataFrame(df['driver_name'].unique(), columns=['driver_name'])
features = (
    features
    .merge(races_count, on='driver_name', how='left')
    .merge(wins_count, on='driver_name', how='left')
    .merge(avg_finish, on='driver_name', how='left')
    .merge(recent, on='driver_name', how='left')
)

# ── 8. Add each driver’s main team and that team’s win rate ─────────────────────
driver_team = (
    df.groupby('driver_name')['team_name']
      .agg(lambda x: x.value_counts().idxmax())
      .rename('team_name')
)
features = features.merge(driver_team, on='driver_name', how='left')
features = features.merge(team_winrate, on='team_name', how='left')

# ── 9. Handle missing values ───────────────────────────────────────────────────
# Fill any remaining NaNs in numeric columns with the column mean
features.fillna(features.mean(numeric_only=True), inplace=True)

# ── 10. Save the feature dataset ───────────────────────────────────────────────
features.to_csv("data/feature_dataset.csv", index=False)
print("✅ Feature dataset saved to data/feature_dataset.csv")
print("Columns:", list(features.columns))
print("Shape:", features.shape)
