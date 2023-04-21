import streamlit as st
import pandas as pd
import numpy as np
import json
import utils.event_functions as event
import utils.visual_functions as visual
import utils.helper_functions as helper


###############################
# === Define page objects === #
###############################

# Define football pitch
pitch_width = 100
pitch_height = 60
fig, ax = visual.createPitch(pitch_width, pitch_height, "green")

# Define available colors (available = 1 ; not available = 0)
colors = {
    "Simple pass": "blue",
    "High pass": "red",
}


##########################
# === Render sidebar === #
##########################

# Sidebar title
st.sidebar.title("Match settings")

# Drop-down menu to select the match
all_matches = helper.load_all_matches()
all_match_names = all_matches["match_name"].unique().tolist()
selected_match = st.sidebar.selectbox("Select a match:", all_match_names)

# Drop-down menu to select the team
match_teamsData = json.loads((all_matches.loc[all_matches['match_name'] == selected_match, 
                                        'teamsData'].iloc[0]).replace("'", "\""))
match_teamIds = list(match_teamsData.keys())
all_teams = helper.load_all_teams()
selected_match_team_names = (all_teams.loc[all_teams['wyId'] == int(match_teamIds[0]), 'officialName'].iloc[0],
                        all_teams.loc[all_teams['wyId'] == int(match_teamIds[1]), 'officialName'].iloc[0])
selected_team = st.sidebar.selectbox("Select a team:", selected_match_team_names)
selected_teamId = all_teams.loc[all_teams['officialName'] == selected_team, 'wyId'].iloc[0]


# Filter title
st.sidebar.title(" ")
st.sidebar.title("Filter settings")

# Drop-down menu to select the player
matchId = all_matches.loc[all_matches['match_name'] == selected_match, 'wyId'].iloc[0]
all_players = helper.load_all_players()
all_match_events = helper.get_match_events(matchId=matchId, 
                                       all_events_data=helper.load_all_events(), 
                                       teamId=selected_teamId, 
                                       players="all")
all_match_playerIds = all_match_events["playerId"].unique().tolist()
all_match_player_data = all_players[all_players["wyId"].isin(all_match_playerIds)]
all_match_player_names = all_match_player_data['shortName'].unique().tolist()
filter_by_player = st.sidebar.checkbox("Filter by player")

if filter_by_player:
    selected_players = st.sidebar.multiselect("Select a player:", all_match_player_names)
    ## store player data
    selected_players_dict = {}
    for player_name in selected_players:
        player_data = all_players[all_players['shortName'] == player_name]
        playerId = player_data['wyId'].iloc[0]
        selected_players_dict[playerId] = player_data
    selected_player_Ids = selected_players_dict.keys()
else:
    selected_player_Ids = "all"

# Drop-down menu to select the event type
filtered_match_events = helper.get_match_events(matchId=matchId, 
                                       all_events_data=helper.load_all_events(), 
                                       teamId=selected_teamId, 
                                       players=selected_player_Ids)
event_names = filtered_match_events["subEventName"].unique().tolist()
selected_events = st.sidebar.multiselect("Select an event type:", event_names)


#######################
# === Render page === #
#######################

# Render title
st.title("Football Game Statistics Visualized")

# Render introduction
st.markdown(
    """
    This app allows for the visualization of different actions and events that occurred during the 2018 World Cup matches. \
        The visualizations can be controlled using a time slider.
    """
)

# Render header
st.write("")
st.write("")
st.subheader("Event visualizer")

# Render slider
slider_label = "The visualization below shows the locations of events for a chosen event type, performed during a particular match, chosen team(s). \
    Events can be filtered by team or even by player. The time window (in minutes) can be adjusted in the sidebar. \
        The starting time (in minutes) can be set using the slider below."
game_time = st.slider("Select a time period: ", 0, 120, (0, 5), step=1)


################################
# === Define pitch objects === #
################################

# Define arrows on pitch
if "Simple pass" in selected_events:
    ax = event.simple_pass_render(
        pitch_height=pitch_height,
        pitch_width=pitch_width,
        match=filtered_match_events,
        game_time=game_time,
        color=colors["Simple pass"],
        ax=ax,
    )

if "High pass" in selected_events:
    ax = event.high_pass_render(
        pitch_height=pitch_height,
        pitch_width=pitch_width,
        match=filtered_match_events,
        game_time=game_time,
        color=colors["High pass"],
        ax=ax,
    )


#######################
# === Render pitch === #
#######################

# Render pitch
fig.set_size_inches(15, 10)
st.pyplot(fig)


#######################
# === For testing === #
#######################

# Render raw data
st.write("")
st.write("")
st.subheader("Raw data")
st.write(filtered_match_events)
