import pandas as pd

print("Downloading player stats...")

current_year = pd.Timestamp.now().year - 1
player_df = None
player_season_used = None

for y in range(current_year, current_year - 4, -1):
    player_url = (
        f"https://github.com/nflverse/nflverse-data/releases/download/player_stats/"
        f"player_stats_{y}.parquet"
    )

    try:
        print(f"Trying player stats season {y}...")
        player_df = pd.read_parquet(player_url)
        player_season_used = y
        print(f"Loaded player stats for {y}.")
        break
    except Exception:
        print(f"No player stats found for {y}.")

if player_df is None:
    raise Exception("Could not download any recent player stats.")

player_df.to_csv("nfl_data.csv", index=False)

print(f"Saved {len(player_df)} player stat records.")
print(f"Latest player season found: {player_season_used}")

print("Downloading play-by-play data...")

pbp_df = None
pbp_season_used = None

for season in range(int(player_season_used), int(player_season_used) - 4, -1):
    pbp_url = (
        f"https://github.com/nflverse/nflverse-data/releases/download/pbp/"
        f"play_by_play_{season}.csv"
    )

    try:
        print(f"Trying play-by-play season {season}...")
        pbp_df = pd.read_csv(pbp_url, low_memory=False)
        pbp_season_used = season
        print(f"Loaded play-by-play data for {season}.")
        break
    except Exception:
        print(f"No play-by-play data found for {season}.")

if pbp_df is None:
    raise Exception("Could not download any recent play-by-play data.")
print("Creating smaller team analytics file...")

pbp_filtered = pbp_df[
    (pbp_df["season_type"] == "REG") &
    (pbp_df["posteam"].notna())
].copy()

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
team_analytics["season"] = pbp_season_used

team_analytics.to_csv("team_analytics.csv", index=False)

print(f"Saved {len(team_analytics)} team analytics records for {pbp_season_used}.")
