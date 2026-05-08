from src.ingest import save_to_db
from src.indicators import compute_indicators
from src.backtest import run_backtest

ticker = "RELIANCE.NS"

save_to_db(ticker)
compute_indicators(ticker)
run_backtest(ticker)




