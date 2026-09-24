# Nautilus Trader Data Catalog Verification Test
import os
import pandas as pd
from nautilus_trader.model.data import BarType
from nautilus_trader.model.identifiers import InstrumentId, Symbol, Venue
from nautilus_trader.model.instruments import CurrencyPair
from nautilus_trader.model.currencies import BTC, USD
from nautilus_trader.model.objects import Price, Quantity
from nautilus_trader.persistence.wranglers import BarDataWrangler
from nautilus_trader.persistence.catalog.parquet import ParquetDataCatalog

def test_load_sample():
    sample_file = os.path.join(os.path.dirname(__file__), "sample_nautilus_bars.parquet")
    df = pd.read_parquet(sample_file)
    print(f"Loaded sample dataframe with {len(df)} rows.")

    instrument = CurrencyPair(
        instrument_id=InstrumentId(Symbol("BTCUSD"), Venue("CRYPTO")),
        raw_symbol=Symbol("BTCUSD"),
        base_currency=BTC,
        quote_currency=USD,
        price_precision=2,
        size_precision=6,
        price_increment=Price.from_str("0.01"),
        size_increment=Quantity.from_str("0.000001"),
        ts_event=0,
        ts_init=0,
    )

    bar_type = BarType.from_str("BTCUSD.CRYPTO-1-MINUTE-LAST-EXTERNAL")
    wrangler = BarDataWrangler(bar_type=bar_type, instrument=instrument)
    bars = wrangler.process(df.set_index("timestamp")[["open", "high", "low", "close", "volume"]])

    print(f"Wrangler generated {len(bars)} Nautilus Bar objects.")
    print("Bar 0:", bars[0])
    print("Bar -1:", bars[-1])
    assert len(bars) == len(df), "Bar count mismatch"
    print("Test passed successfully!")

if __name__ == "__main__":
    test_load_sample()
