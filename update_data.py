import pandas as pd

print("Downloading player stats...")

player_url = "https://github.com/nflverse/nflverse-data/releases/download/player_stats/player_stats.csv"
player_df = pd.read_csv(player_url)
player_df = player_df[player_df["season"] >= 2024]
player_df.to_csv("nfl_data.csv", index=False)

print(f"Saved {len(player_df)} player stat records.")

print("Downloading play-by-play data...")

pbp_url = "https://github.com/nflverse/nflverse-data/releases/download/pbp/play_by_play_2024.csv"
pbp_df = pd.read_csv(pbp_url, low_memory=False)

pbp_df.to_csv("pbp_data.csv", index=False)

print(f"Saved {len(pbp_df)} play-by-play records.")
