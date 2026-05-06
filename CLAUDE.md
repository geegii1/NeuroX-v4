# WizeTrade / NeuroX-v4

## Stack
- dashboard.py — Streamlit UI (mobile-first)
- data/ — JSON state files (latest_signal.json, open_orders.json)
- Alpaca IEX feed for live prices (data API only, no live execution yet)

## UI Rules
- Dark theme: #07091e bg, Plus Jakarta Sans + IBM Plex Mono fonts
- Metric cards: always 2x2 grid, never 4-column
- CSS lives in the st.markdown() block at top of dashboard.py
- Mobile-first: overflow-x hidden, no wide layout

## Do Not Touch
- load_dotenv path (/home/ubuntu/NeuroX/.env)
- Alpaca client init block
- Data loading helper functions

## Deploy
- Push to GitHub, then SSH into Oracle VM and redeploy
