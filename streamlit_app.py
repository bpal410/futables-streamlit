import streamlit as st
import pandas as pd
import http.client
import json
import time

# Set page config
st.set_page_config(
    page_title="FuTables - Football League Tables",
    page_icon="⚽",
    layout="wide"
)

# API configuration
API_SPORTS_KEY = "5938d62283047e543aecb2673adcf425"
API_SPORTS_FQDN = "v3.football.api-sports.io"
API_SPORTS_HEADERS = {
    'x-rapidapi-host': API_SPORTS_FQDN,
    'x-rapidapi-key': API_SPORTS_KEY
}

# Load leagues data
@st.cache_data(ttl=3600)
def load_leagues():
    try:
        df = pd.read_csv('leagues.csv')
        # Convert string representation of dict to actual dict
        df['league'] = df['league'].apply(eval)
        return df
    except Exception as e:
        st.error(f"Error loading leagues: {e}")
        return pd.DataFrame()

# Get standings for a specific league
@st.cache_data(ttl=600)
def get_standings(league_id, season=2023):
    conn = http.client.HTTPSConnection(API_SPORTS_FQDN)
    conn.request("GET", f"/standings?league={league_id}&season={season}", headers=API_SPORTS_HEADERS)
    res = conn.getresponse()
    data = res.read()
    standings_data = json.loads(data.decode("utf-8"))
    
    if standings_data['results'] == 0:
        return None
    
    return standings_data['response']

# Get recent fixtures for a league
@st.cache_data(ttl=600)
def get_league_fixtures(league_id, season=2023, last=10):
    conn = http.client.HTTPSConnection(API_SPORTS_FQDN)
    conn.request("GET", f"/fixtures?league={league_id}&season={season}&last={last}", headers=API_SPORTS_HEADERS)
    res = conn.getresponse()
    data = res.read()
    fixtures_data = json.loads(data.decode("utf-8"))
    
    if fixtures_data['results'] == 0:
        return None
    
    return fixtures_data['response']

# Main app
def main():
    # Custom CSS
    st.markdown("""
    <style>
    .main {
        background-color: #f0f2f6;
    }
    .standings-table {
        font-family: 'Arial', sans-serif;
    }
    .title {
        color: #1e3a8a;
        text-align: center;
    }
    .team-logo {
        vertical-align: middle;
        margin-right: 10px;
    }
    .fixture-card {
        background-color: #ffffff;
        border-radius: 5px;
        padding: 10px;
        margin-bottom: 10px;
        box-shadow: 0 1px 3px rgba(0,0,0,0.1);
    }
    .fixture-result {
        font-weight: bold;
        font-size: 1.2em;
    }
    </style>
    """, unsafe_allow_html=True)
    
    # App title
    st.markdown("<h1 class='title'>⚽ FuTables - Football League Tables</h1>", unsafe_allow_html=True)
    
    # Load leagues
    leagues_df = load_leagues()
    
    if leagues_df.empty:
        st.error("Failed to load leagues data.")
        return
    
    # Filter for only League type (not Cup)
    league_type_leagues = leagues_df[leagues_df['league'].apply(lambda x: x['type'] == 'League')]
    
    # Create a list of leagues for the dropdown
    league_options = []
    for _, row in league_type_leagues.iterrows():
        league_data = row['league']
        league_options.append({
            'id': league_data['id'],
            'name': f"{league_data['name']} ({league_data['id']})",
            'logo': league_data['logo']
        })
    
    # Sort leagues by name
    league_options.sort(key=lambda x: x['name'])
    
    # Create columns for layout
    col1, col2 = st.columns([1, 3])
    
    with col1:
        # League selection
        selected_league = st.selectbox(
            "Select a League",
            options=[league['id'] for league in league_options],
            format_func=lambda x: next((league['name'] for league in league_options if league['id'] == x), x),
            index=league_options.index(next(filter(lambda x: x['id'] == 39, league_options), league_options[0]))  # Default to Premier League
        )
        
        # Season selection (could be expanded with more seasons)
        season = st.selectbox("Select Season", [2023, 2022, 2021, 2020])
        
        # Show league logo
        selected_league_info = next((league for league in league_options if league['id'] == selected_league), None)
        if selected_league_info:
            st.image(selected_league_info['logo'], width=100)
        
        # Add a refresh button
        if st.button("Refresh Data"):
            st.cache_data.clear()
            st.experimental_rerun()
    
    # Create tabs for different views
    tab1, tab2 = st.tabs(["League Table", "Recent Fixtures"])
    
    with tab1:
        # Get standings data
        with st.spinner("Loading standings..."):
            standings_data = get_standings(selected_league, season)
        
        if not standings_data:
            st.error(f"No standings data available for this league (ID: {selected_league}) and season ({season}).")
            return
        
        # Process standings data
        league_info = standings_data[0]['league']
        standings = league_info['standings']
        
        # Display league name and season
        st.subheader(f"{league_info['name']} - {season}/{season+1}")
        
        # Handle multiple groups/standings if they exist
        if isinstance(standings, list) and isinstance(standings[0], list):
            # Multiple groups
            for group_idx, group in enumerate(standings):
                st.subheader(f"Group {group_idx + 1}")
                display_standings_table(group)
        else:
            # Single group
            display_standings_table(standings)
    
    with tab2:
        # Get recent fixtures
        with st.spinner("Loading recent fixtures..."):
            fixtures_data = get_league_fixtures(selected_league, season, last=15)
        
        if not fixtures_data:
            st.error(f"No recent fixtures available for this league (ID: {selected_league}) and season ({season}).")
            return
        
        st.subheader("Recent Matches")
        
        # Display fixtures in a nice format
        for fixture in fixtures_data:
            fixture_info = fixture['fixture']
            teams = fixture['teams']
            goals = fixture['goals']
            
            # Create a card-like display for each fixture
            col1, col2, col3 = st.columns([2, 1, 2])
            
            with col1:
                st.markdown(f"""
                <div style="display: flex; align-items: center; justify-content: flex-end;">
                    <span style="font-weight: bold; margin-right: 10px;">{teams['home']['name']}</span>
                    <img src="{teams['home']['logo']}" width="30">
                </div>
                """, unsafe_allow_html=True)
            
            with col2:
                status = fixture_info['status']['short']
                if status == "FT":  # Full Time
                    st.markdown(f"""
                    <div style="text-align: center; font-weight: bold; font-size: 1.2em;">
                        {goals['home']} - {goals['away']}
                    </div>
                    """, unsafe_allow_html=True)
                else:
                    st.markdown(f"""
                    <div style="text-align: center; color: #888;">
                        {fixture_info['status']['long']}
                    </div>
                    """, unsafe_allow_html=True)
            
            with col3:
                st.markdown(f"""
                <div style="display: flex; align-items: center;">
                    <img src="{teams['away']['logo']}" width="30">
                    <span style="font-weight: bold; margin-left: 10px;">{teams['away']['name']}</span>
                </div>
                """, unsafe_allow_html=True)
            
            # Display match date
            match_date = pd.to_datetime(fixture_info['date']).strftime("%d %b %Y, %H:%M")
            st.caption(f"Date: {match_date}")
            
            st.markdown("---")

def display_standings_table(standings):
    # Create a DataFrame for the standings
    table_data = []
    for team in standings:
        table_data.append({
            'Rank': team['rank'],
            'Team': team['team']['name'],
            'Logo': team['team']['logo'],
            'Points': team['points'],
            'Played': team['all']['played'],
            'Won': team['all']['win'],
            'Draw': team['all']['draw'],
            'Lost': team['all']['lose'],
            'GF': team['all']['goals']['for'],
            'GA': team['all']['goals']['against'],
            'GD': team['goalsDiff'],
            'Form': team.get('form', '')
        })
    
    df = pd.DataFrame(table_data)
    
    # Create a clean table display
    st.markdown("""
    <style>
    .dataframe {
        width: 100%;
        text-align: center;
    }
    th {
        background-color: #1e3a8a;
        color: white;
        text-align: center !important;
    }
    </style>
    """, unsafe_allow_html=True)
    
    # Format the team column to include logo
    def format_team(row):
        return f"<img src='{row['Logo']}' width='20' style='vertical-align: middle; margin-right: 5px;'> {row['Team']}"
    
    df['Team Display'] = df.apply(format_team, axis=1)
    
    # Select columns to display
    display_df = df[['Rank', 'Team Display', 'Points', 'Played', 'Won', 'Draw', 'Lost', 'GF', 'GA', 'GD', 'Form']]
    display_df.columns = ['#', 'Team', 'PTS', 'P', 'W', 'D', 'L', 'GF', 'GA', 'GD', 'Form']
    
    # Display the table
    st.markdown(display_df.to_html(escape=False, index=False), unsafe_allow_html=True)

if __name__ == "__main__":
    main()