import pandas as pd
from matplotlib import pyplot as plt


################
# === Paths ===#
################

events_path = "./code/dataset/data_clean/clean_events_data.csv"
matches_path = "./code/dataset/data_clean/clean_matches_data.csv"
teams_path = "./code/dataset/data_clean/clean_teams_data.csv"


####################
# === Functions ===#
####################

def load_all_events():
    """ Loads and returns the football events data """

    data = pd.read_csv(events_path)
    return data

def load_all_matches():
    """ Loads and returns the football matches data """
    
    data = pd.read_csv(matches_path)
    return data

def load_all_teams():
    """ Loads and returns the football matches data """
    
    data = pd.read_csv(teams_path)
    return data


def get_match_events(matchId, all_events_data, teamId):
    """ For a given match ID and all events data, returns the match events data in a pandas dataframe """

    matches_with_matchId = all_events_data[all_events_data["matchId"] == matchId]
    matches_with_matchId_by_teamId = matches_with_matchId[matches_with_matchId["teamId"] ==  teamId]
    return matches_with_matchId_by_teamId


def get_team_side(matchId, teamId, events_data):
    """ For a given match ID, and team ID returns the side on which the team plays on the pitch """
    
    data = pd.read_csv(events_path)
    match = get_match_events(matchId, events_data)
    unique_team_ids = match["teamId"].unique()

    team_right = max(unique_team_ids)
    team_left = min(unique_team_ids)

    if team_right == teamId:
        return "right"
    else:
        return "left"