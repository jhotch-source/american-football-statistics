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

print("Creating smaller team analytics file...")

pbp_filtered = pbp_df[
    (pbp_df["season_type"] == "REG") &
    (pbp_df["posteam"].notna())
].copy()

# Some nflverse versions do not have a direct turnover column,
# so we create one from interceptions and lost fumbles.
for col in ["interception", "fumble_lost", "touchdown", "success", "epa", "yards_gained"]:
    if col not in pbp_filtered.columns:
        pbp_filtered[col] = 0

pbp_filtered["turnovers"] = (
    pbp_filtered["interception"].fillna(0) +
    pbp_filtered["fumble_lost"].fillna(0)
)

team_analytics = (
    pbp_filtered.groupby("posteam", as_index=False)
    .agg(
        plays=("play_id", "count"),
        avg_epa=("epa", "mean"),
        success_rate=("success", "mean"),
        avg_yards_gained=("yards_gained", "mean"),
        total_touchdowns=("touchdown", "sum"),
        turnovers=("turnovers", "sum")
    )
)

team_analytics["success_rate"] = team_analytics["success_rate"] * 100

team_analytics.to_csv("team_analytics.csv", index=False)

print(f"Saved {len(team_analytics)} team analytics records.")
