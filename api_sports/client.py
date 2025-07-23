import http.client
import json
import pandas as pd

API_SPORTS_KEY = "5938d62283047e543aecb2673adcf425"
API_SPORTS_FQDN = "v3.football.api-sports.io"
API_SPORTS_HEADERS = {
    'x-rapidapi-host': API_SPORTS_FQDN,
    'x-rapidapi-key': API_SPORTS_KEY
}

def get_leagues():
    """Get all leagues from the API"""
    conn = http.client.HTTPSConnection(API_SPORTS_FQDN)
    conn.request("GET", "/leagues", headers=API_SPORTS_HEADERS)
    res = conn.getresponse()
    data = res.read()
    leagues_data = json.loads(data.decode("utf-8"))
    
    if leagues_data['results'] == 0:
        return None
    
    return leagues_data['response']

def get_standings(league_id, season=2023):
    """Get standings for a specific league and season"""
    conn = http.client.HTTPSConnection(API_SPORTS_FQDN)
    conn.request("GET", f"/standings?league={league_id}&season={season}", headers=API_SPORTS_HEADERS)
    res = conn.getresponse()
    data = res.read()
    standings_data = json.loads(data.decode("utf-8"))
    
    if standings_data['results'] == 0:
        return None
    
    return standings_data['response']

def get_league_fixtures(league_id, season=2023, last=10):
    """Get recent fixtures for a league"""
    conn = http.client.HTTPSConnection(API_SPORTS_FQDN)
    conn.request("GET", f"/fixtures?league={league_id}&season={season}&last={last}", headers=API_SPORTS_HEADERS)
    res = conn.getresponse()
    data = res.read()
    fixtures_data = json.loads(data.decode("utf-8"))
    
    if fixtures_data['results'] == 0:
        return None
    
    return fixtures_data['response']

def get_team_statistics(league_id, team_id, season=2023):
    """Get statistics for a specific team in a league"""
    conn = http.client.HTTPSConnection(API_SPORTS_FQDN)
    conn.request("GET", f"/teams/statistics?league={league_id}&team={team_id}&season={season}", headers=API_SPORTS_HEADERS)
    res = conn.getresponse()
    data = res.read()
    stats_data = json.loads(data.decode("utf-8"))
    
    if stats_data['results'] == 0:
        return None
    
    return stats_data['response']