import pandas as pd

# Pull current NFL player statistics
url = "https://github.com/nflverse/nflverse-data/releases/download/player_stats/player_stats.csv"

df = pd.read_csv(url)

# Keep recent seasons
df = df[df["season"] >= 2024]

df.to_csv("nfl_data.csv", index=False)

print(f"Updated {len(df)} records.")
