import random
import time
from textual.app import App, ComposeResult
from textual.containers import Horizontal, Vertical
from textual.widgets import Header, Footer, Static, DataTable

# --- STREAM DATA ENGINE WITH DYNAMIC TIME-BASED SEEDING ---
def get_live_ticker_data(ticker: str):
    ticker = ticker.upper().strip()
    
    # Establish realistic baseline anchor prices per company
    base_prices = {"AAPL": 240.50, "TSLA": 312.45, "NVDA": 135.80, "MSFT": 422.10}
    base_price = base_prices.get(ticker, 150.00)
    
    # FIX: Seed with the unique ticker ID AND the shifting epoch millisecond timestamp!
    current_time_ms = int(time.time() * 1000)
    seed = sum(ord(c) for c in ticker) + current_time_ms
    random.seed(seed)
    
    # Calculate constantly moving market data ticks
    change = random.uniform(-4.5, 4.5)
    current_price = base_price + change
    pct_change = (change / base_price) * 100
    
    names = {
        "AAPL": "APPLE INC.", "TSLA": "TESLA, INC.", "NVDA": "NVIDIA CORP.", "MSFT": "MICROSOFT CORP."
    }
    name = names.get(ticker, f"{ticker} GLOBAL HOLDINGS CORP.")
    trend_arrow = "▲" if change >= 0 else "▼"
    
    return {
        "name": name,
        "price": f"${current_price:.2f}",
        "change": f"{trend_arrow} {change:+.2f}",
        "pct": f"{pct_change:+.2f}%",
        "high": f"${base_price + 5.25:.2f}",
        "low": f"${base_price - 5.25:.2f}",
        "volume": f"{random.randint(1500000, 75000000):,}",
        "pe": f"{random.uniform(18.5, 34.2):.2f}"
    }

# --- THE REAL-TIME BLOOMBERG CONSOLE ---
class LiveBloomberg(App):
    CSS = """
    Screen { background: #010101; }
    #header_bar { color: #FFA500; text-align: center; background: #111111; padding: 1; text-style: bold; border-bottom: tall #FFA500; }
    #left_panel { width: 40%; border-right: solid #333333; padding: 1; }
    #right_panel { width: 60%; }
    #main_display { height: 55%; border-bottom: solid #333333; padding: 1; color: #00FF00; }
    #news_feed { height: 45%; padding: 1; color: #00FFFF; }
    """
    
    BINDINGS = [("q", "quit", "Exit Terminal")]
    ticker_universe = ["AAPL", "TSLA", "NVDA", "MSFT"]
    current_index = 0

    def compose(self) -> ComposeResult:
        yield Header(show_clock=True)
        yield Static("📟 LIVE BLOOMBERG TERMINAL v9.0 - REALTIME DESK STREAM", id="header_bar")
        
        with Horizontal():
            with Vertical(id="left_panel"):
                yield Static("📊 CORE WATCHLIST INDEX [Cycling Desks Every 5s]\n")
                yield DataTable(id="watchlist_table")
                
            with Vertical(id="right_panel"):
                yield Static("", id="main_display")
                yield Static("📰 BLOOMBERG REAL-TIME NEWS WIRE\n\n"
                             "• [SYSTEM] CORE TIMESTEP RANDOMIZER CHANNELS SYNCHRONIZED\n"
                             "• [MARKETS] VOLUME BREAKS AFTERHOURS VOLATILITY RECORD\n"
                             "• [MACRO] TECH SECTOR INDEX LEADS MOMENTUM SHIFT", id="news_feed")
        yield Footer()

    def on_mount(self) -> None:
        table = self.query_one("#watchlist_table", DataTable)
        
        table.add_column("TICKER", key="col_ticker")
        table.add_column("LAST PRICE", key="col_price")
        table.add_column("LIVE MOVE", key="col_move")
        
        table.add_row("AAPL", "$0.00", "0.00%", key="row_aapl")
        table.add_row("TSLA", "$0.00", "0.00%", key="row_tsla")
        table.add_row("NVDA", "$0.00", "0.00%", key="row_nvda")
        table.add_row("MSFT", "$0.00", "0.00%", key="row_msft")
        
        self.set_interval(1.0, self.refresh_terminal_ticks)
        self.set_interval(5.0, self.cycle_active_desk)

    def cycle_active_desk(self) -> None:
        self.current_index = (self.current_index + 1) % len(self.ticker_universe)

    def refresh_terminal_ticks(self) -> None:
        table = self.query_one("#watchlist_table", DataTable)
        display = self.query_one("#main_display", Static)
        
        aapl = get_live_ticker_data("AAPL")
        tsla = get_live_ticker_data("TSLA")
        nvda = get_live_ticker_data("NVDA")
        msft = get_live_ticker_data("MSFT")
        
        table.update_cell("row_aapl", "col_price", aapl["price"])
        table.update_cell("row_aapl", "col_move", aapl["pct"])
        
        table.update_cell("row_tsla", "col_price", tsla["price"])
        table.update_cell("row_tsla", "col_move", tsla["pct"])
        
        table.update_cell("row_nvda", "col_price", nvda["price"])
        table.update_cell("row_nvda", "col_move", nvda["pct"])
        
        table.update_cell("row_msft", "col_price", msft["price"])
        table.update_cell("row_msft", "col_move", msft["pct"])
        
        active_ticker = self.ticker_universe[self.current_index]
        active_data = get_live_ticker_data(active_ticker)
        
        extended_text = (
            f"🏢 CURRENT CONSOLE VIEW: {active_ticker} : {active_data['name']}\n"
            f"─────────────────────────────────────────────────────────────\n"
            f"LAST PRICE:  {active_data['price']}   CHANGE: {active_data['change']} ({active_data['pct']})\n"
            f"⚡ HIGH PRICE: {active_data['high']}    ⚡ LOW PRICE:  {active_data['low']}\n"
            f"📊 STREAM VOL: {active_data['volume']}   📦 P/E RATIO:  {active_data['pe']}\n\n"
            f"[📡] Time-seeded stream online. Numbers shifting actively."
        )
        display.update(extended_text)

if __name__ == "__main__":
    app = LiveBloomberg()
    app.run()
