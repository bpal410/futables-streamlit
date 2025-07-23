# ⚽ FuTables - Football League Tables

A Streamlit app for tracking football (soccer) league tables from top leagues around the world.

[![Open in Streamlit](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://futables-streamlit.streamlit.app/)

## Features

- View current standings for top football leagues worldwide
- Select different seasons to view historical data
- Clean, responsive interface with team logos and detailed statistics
- Supports leagues with multiple groups/divisions

## Data Source

This app uses the API-Sports Football API to fetch real-time data about football leagues and standings.

## How to run it on your own machine

1. Clone this repository
   ```
   $ git clone https://github.com/yourusername/futables-streamlit.git
   $ cd futables-streamlit
   ```

2. Install the requirements
   ```
   $ pip install -r requirements.txt
   ```

3. Run the app
   ```
   $ streamlit run streamlit_app.py
   ```

4. Open your browser and go to http://localhost:8501

## API Key

The app uses the API-Sports Football API. If you want to use your own API key:
1. Sign up at [API-Sports](https://api-sports.io/)
2. Get your API key
3. Replace the `API_SPORTS_KEY` value in the `streamlit_app.py` file

## License

This project is licensed under the MIT License - see the LICENSE file for details.