# Global Macro & Multi-Asset Quantitative Databank

**Storage Root**: `/run/user/1000/gvfs/smb-share:server=192.168.1.6,share=iflow/数据库5/nautilus_databank`  
**Native NautilusTrader Catalog**: `/run/user/1000/gvfs/smb-share:server=192.168.1.6,share=iflow/数据库5/nautilus_databank/catalog`  
**Target Resolution**: 1-Minute (`1m`) OHLCV  
**Time Coverage**: 2020-01-01 to Present (2026)  
**Total Validated Bars**: **42,236,012**  
**Total Verified Size**: **1036.32 MB** (1.01 GB)  
**Integrity Standard**: Zero Synthetic Forward-Fill, Monotonic Timestamps, Strict OHLC Geometry Rules ($H \ge \max(O,C), L \le \min(O,C), V \ge 0$)

---

## 1. Asset Universe & Coverage Matrix

| Category | Symbol | Venue | Nautilus BarType | Valid Bars (2020-2026) | Date Range | Duplicates | Invariant Defects | Gaps | Clean Size |
|---|---|---|---|---|---|---|---|---|---|
| **crypto** | `BTCUSD` | `CRYPTO` | `BTCUSD.CRYPTO-1-MINUTE-LAST-EXTERNAL` | 2,887,347 | 2020-01-02 to 2026-02-14 | 0 | 0 | 1,599 | 81.56 MB |
| **crypto** | `ETHUSD` | `CRYPTO` | `ETHUSD.CRYPTO-1-MINUTE-LAST-EXTERNAL` | 2,887,653 | 2020-01-02 to 2026-02-14 | 2 | 0 | 1,335 | 77.87 MB |
| **crypto** | `SOLUSD` | `CRYPTO` | `SOLUSD.CRYPTO-1-MINUTE-LAST-EXTERNAL` | 2,297,722 | 2021-09-18 to 2026-02-14 | 3 | 0 | 7,814 | 52.89 MB |
| **crypto** | `XRPUSD` | `CRYPTO` | `XRPUSD.CRYPTO-1-MINUTE-LAST-EXTERNAL` | 2,873,061 | 2020-01-02 to 2026-02-14 | 2 | 0 | 14,344 | 70.89 MB |
| **crypto** | `BNBUSDT` | `BINANCE` | `BNBUSDT.BINANCE-1-MINUTE-LAST-EXTERNAL` | 2,628,554 | 2020-01-01 to 2024-12-31 | 0 | 0 | 15 | 78.02 MB |
| **crypto** | `DOGEUSD` | `CRYPTO` | `DOGEUSD.CRYPTO-1-MINUTE-LAST-EXTERNAL` | 2,439,592 | 2020-07-10 to 2026-02-14 | 3 | 0 | 17,007 | 57.03 MB |
| **rwa_gold** | `PAXGUSDT` | `BINANCE` | `PAXGUSDT.BINANCE-1-MINUTE-LAST-EXTERNAL` | 2,283,136 | 2020-08-28 to 2024-12-31 | 0 | 0 | 10 | 54.60 MB |
| **metals** | `GOLD` | `METALS` | `GOLD.METALS-1-MINUTE-LAST-EXTERNAL` | 41,210 | 2026-01-05 to 2026-02-13 | 0 | 0 | 29 | 1.10 MB |
| **metals** | `SILVER` | `METALS` | `SILVER.METALS-1-MINUTE-LAST-EXTERNAL` | 2,162,424 | 2020-01-02 to 2026-02-13 | 0 | 0 | 4,868 | 47.06 MB |
| **metals** | `XPTUSD` | `METALS` | `XPTUSD.METALS-1-MINUTE-LAST-EXTERNAL` | 1,799,450 | 2021-01-04 to 2026-02-13 | 0 | 0 | 5,486 | 43.81 MB |
| **metals** | `XPDUSD` | `METALS` | `XPDUSD.METALS-1-MINUTE-LAST-EXTERNAL` | 1,701,154 | 2021-01-04 to 2026-02-13 | 0 | 0 | 73,149 | 40.80 MB |
| **metals** | `GLD` | `US_EQUITY` | `GLD.US_EQUITY-1-MINUTE-LAST-EXTERNAL` | 840,264 | 2020-01-02 to 2026-03-31 | 3 | 0 | 105,248 | 20.07 MB |
| **metals** | `SLV` | `US_EQUITY` | `SLV.US_EQUITY-1-MINUTE-LAST-EXTERNAL` | 877,309 | 2020-01-02 to 2026-03-31 | 1 | 0 | 127,301 | 13.81 MB |
| **fx** | `EURUSD` | `FX` | `EURUSD.FX-1-MINUTE-LAST-EXTERNAL` | 2,276,723 | 2020-01-02 to 2026-02-13 | 0 | 0 | 4,258 | 54.93 MB |
| **fx** | `USDJPY` | `FX` | `USDJPY.FX-1-MINUTE-LAST-EXTERNAL` | 2,276,119 | 2020-01-02 to 2026-02-13 | 0 | 0 | 4,535 | 54.48 MB |
| **fx** | `GBPUSD` | `FX` | `GBPUSD.FX-1-MINUTE-LAST-EXTERNAL` | 2,275,346 | 2020-01-02 to 2026-02-13 | 0 | 0 | 5,019 | 56.29 MB |
| **fx** | `USDCHF` | `FX` | `USDCHF.FX-1-MINUTE-LAST-EXTERNAL` | 2,272,089 | 2020-01-02 to 2026-02-13 | 0 | 0 | 7,298 | 53.46 MB |
| **fx** | `XAUCNH` | `FX` | `XAUCNH.FX-1-MINUTE-LAST-EXTERNAL` | 143,616 | 2025-09-17 to 2026-02-13 | 0 | 0 | 144 | 4.19 MB |
| **equities_indices** | `SPY` | `US_EQUITY` | `SPY.US_EQUITY-1-MINUTE-LAST-EXTERNAL` | 1,281,134 | 2020-01-02 to 2026-03-31 | 34 | 0 | 110,030 | 33.12 MB |
| **equities_indices** | `QQQ` | `US_EQUITY` | `QQQ.US_EQUITY-1-MINUTE-LAST-EXTERNAL` | 1,304,397 | 2020-01-02 to 2026-03-31 | 42 | 0 | 103,429 | 33.67 MB |
| **equities_indices** | `IWM` | `US_EQUITY` | `IWM.US_EQUITY-1-MINUTE-LAST-EXTERNAL` | 1,117,000 | 2020-01-02 to 2026-03-31 | 37 | 0 | 147,444 | 27.63 MB |
| **commodities** | `USO` | `US_EQUITY` | `USO.US_EQUITY-1-MINUTE-LAST-EXTERNAL` | 789,962 | 2020-01-02 to 2026-03-31 | 2 | 0 | 102,087 | 18.14 MB |
| **commodities** | `UNG` | `US_EQUITY` | `UNG.US_EQUITY-1-MINUTE-LAST-EXTERNAL` | 803,647 | 2020-01-02 to 2026-03-31 | 0 | 0 | 135,506 | 17.26 MB |
| **rates_bonds** | `IEF` | `US_EQUITY` | `IEF.US_EQUITY-1-MINUTE-LAST-EXTERNAL` | 612,640 | 2020-01-02 to 2026-03-31 | 0 | 0 | 57,208 | 13.27 MB |
| **rates_bonds** | `SHY` | `US_EQUITY` | `SHY.US_EQUITY-1-MINUTE-LAST-EXTERNAL` | 457,675 | 2020-01-02 to 2026-03-31 | 1 | 0 | 108,857 | 8.99 MB |
| **rates_bonds** | `TLT` | `US_EQUITY` | `TLT.US_EQUITY-1-MINUTE-LAST-EXTERNAL` | 906,788 | 2020-01-02 to 2026-03-31 | 5 | 0 | 106,794 | 21.40 MB |

---

## 2. Canonical Dual-Contract Schema

```text
Field Name     | Data Type               | Role & Description
---------------+-------------------------+---------------------------------------------------
timestamp      | timestamp[us, tz=UTC]   | Universal Quant Research UTC datetime index
symbol         | Utf8                    | Ticker / Instrument Code (e.g. BTCUSD, SPY, EURUSD)
timeframe      | Utf8                    | Interval Resolution (1m)
bar_type       | Utf8                    | Nautilus Trader BarType Identifier
ts_event       | UInt64                  | Nanoseconds UTC epoch timestamp of bar close
ts_init        | UInt64                  | Nanoseconds UTC epoch timestamp of bar receipt
open           | Float64                 | Bar Open Price
high           | Float64                 | Bar High Price
low            | Float64                 | Bar Low Price
close          | Float64                 | Bar Close Price
volume         | Float64                 | Traded Base Volume
```

---

## 3. Nautilus Trader Native Ingestion Example

```python
from nautilus_trader.persistence.catalog.parquet import ParquetDataCatalog

catalog = ParquetDataCatalog("/run/user/1000/gvfs/smb-share:server=192.168.1.6,share=iflow/数据库5/nautilus_databank/catalog")
bars = catalog.bars(bar_types=["BTCUSD.CRYPTO-1-MINUTE-LAST-EXTERNAL"])
print(f"Loaded {len(bars)} bars for event-driven backtest.")
```

---

## 4. Governance & Resilience Notes
- **Resilience**: If any asset encounters upstream vendor issues, the pipeline processes all available assets in parallel without blocking the swarm.
- **Zero Forward-Fill**: Missing minutes during network breaks or off-market hours are logged as gaps, avoiding phantom fills during execution simulations.
