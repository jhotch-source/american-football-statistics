import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(
    page_title="American Football Statistics",
    layout="wide"
)

@st.cache_data
def load_data():
    return pd.read_csv("nfl_data.csv")

df = load_data()

st.title("American Football Statistics Dashboard")

total_players = df["player_display_name"].nunique()
total_teams = df["recent_team"].nunique()
total_seasons = df["season"].nunique()

col1, col2, col3 = st.columns(3)

col1.metric("Players", total_players)
col2.metric("Teams", total_teams)
col3.metric("Seasons", total_seasons)

st.write("NFL player analytics powered by automatically refreshed data.")

tab1, tab2, tab3, tab4 = st.tabs([
    "League Analysis",
    "Team Profiles",
    "Player Comparison",
    "Team Comparison"
])

# --------------------
# League Analysis
# --------------------
with tab1:
    st.header("League Analysis")

    col1, col2 = st.columns(2)

    with col1:
        season = st.selectbox(
            "Season",
            sorted(df["season"].dropna().unique(), reverse=True)
        )

    stat_options = [
        "passing_yards",
        "passing_tds",
        "interceptions",
        "rushing_yards",
        "rushing_tds",
        "receiving_yards",
        "receiving_tds",
        "receptions"
    ]

    available_stats = [s for s in stat_options if s in df.columns]

    with col2:
        stat = st.selectbox("Statistic", available_stats)

    filtered = df[df["season"] == season]

    leaders = (
        filtered.groupby("player_display_name", as_index=False)[stat]
        .sum()
        .sort_values(stat, ascending=False)
        .head(10)
    )

    fig = px.bar(
        leaders,
        x=stat,
        y="player_display_name",
        orientation="h",
        title=f"Top 10 NFL Players by {stat.replace('_', ' ').title()}"
    )

    fig.update_layout(yaxis={"categoryorder": "total ascending"})
    st.plotly_chart(fig, use_container_width=True)

    st.dataframe(leaders, use_container_width=True)

# --------------------
# Team Profiles
# --------------------
with tab2:
    st.header("Team Profiles")

    team = st.selectbox(
        "Choose Team",
        sorted(df["recent_team"].dropna().unique())
    )

    team_df = df[df["recent_team"] == team]

    st.subheader(f"{team} Player Production")

    team_summary = (
        team_df.groupby("player_display_name", as_index=False)[available_stats]
        .sum()
    )

    selected_team_stat = st.selectbox(
        "Team Profile Statistic",
        available_stats,
        key="team_stat"
    )

    top_team_players = (
        team_summary.sort_values(selected_team_stat, ascending=False)
        .head(10)
    )

    fig_team = px.bar(
        top_team_players,
        x=selected_team_stat,
        y="player_display_name",
        orientation="h",
        title=f"{team} Leaders: {selected_team_stat.replace('_', ' ').title()}"
    )

    fig_team.update_layout(yaxis={"categoryorder": "total ascending"})
    st.plotly_chart(fig_team, use_container_width=True)

    st.dataframe(team_summary, use_container_width=True)

# --------------------
# Player Comparison
# --------------------
with tab3:
    st.header("Player Comparison")

    players = sorted(df["player_display_name"].dropna().unique())

    col1, col2 = st.columns(2)

    with col1:
        player1 = st.selectbox("Player 1", players)

    with col2:
        player2 = st.selectbox("Player 2", players, index=1)

    comparison = (
        df[df["player_display_name"].isin([player1, player2])]
        .groupby("player_display_name", as_index=False)[available_stats]
        .sum()
    )

    st.subheader(f"{player1} vs {player2}")

    st.dataframe(comparison, use_container_width=True)

    melted = comparison.melt(
        id_vars="player_display_name",
        value_vars=available_stats,
        var_name="Statistic",
        value_name="Value"
    )

    fig_compare = px.bar(
        melted,
        x="Statistic",
        y="Value",
        color="player_display_name",
        barmode="group",
        title="Player Comparison"
    )

    st.plotly_chart(fig_compare, use_container_width=True)

# --------------------
# Team Comparison
# --------------------
with tab4:
    st.header("Team Comparison")

    teams = sorted(df["recent_team"].dropna().unique())

    col1, col2 = st.columns(2)

    with col1:
        team1 = st.selectbox("Team 1", teams, key="team1")

    with col2:
        team2 = st.selectbox("Team 2", teams, index=1, key="team2")

    team_compare = (
        df[df["recent_team"].isin([team1, team2])]
        .groupby("recent_team", as_index=False)[available_stats]
        .sum()
    )

    st.dataframe(team_compare, use_container_width=True)

    melted_team = team_compare.melt(
        id_vars="recent_team",
        value_vars=available_stats,
        var_name="Statistic",
        value_name="Value"
    )

    fig = px.bar(
        melted_team,
        x="Statistic",
        y="Value",
        color="recent_team",
        barmode="group",
        title=f"{team1} vs {team2}"
    )

    st.plotly_chart(fig, use_container_width=True)
