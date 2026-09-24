# Crypto OHLCV Data Cleaning & Integrity Audit Log

## Executive Summary
- **Domain**: Crypto OHLCV (24/7 UTC continuous trading)
- **Target Specification**: Compatible with Nautilus Trader DataCatalog & Quant VectorBT/Polars Research
- **Pipeline Start**: 2026-09-23T18:37:25.477241+00:00
- **Pipeline End**: 2026-09-23T18:37:59.545076+00:00
- **Total Instruments Cleaned**: 7
- **Total Validated Rows**: 20,848,105
- **Total Output Size On Disk**: 509.15 MB (0.50 GB)
- **Audit Tool**: `quantskills/skill-intraday-data-quality-auditor` deterministic methodology

---

## Canonical & Nautilus Trader Target Schema
| Field | Type | Description |
|---|---|---|
| `timestamp` | `timestamp[us, tz=UTC]` | UTC timestamp of the bar (human/research standard) |
| `symbol` | `Utf8` | Base instrument identifier (e.g. `BTCUSD`, `ETHUSD`) |
| `timeframe` | `Utf8` | Bar interval resolution (`1m`) |
| `bar_type` | `Utf8` | Nautilus Trader BarType identifier (`<symbol>.<exchange>-<resolution>-<aggregation>-<price>`) |
| `ts_event` | `UInt64` | Nanoseconds UTC epoch timestamp of bar close (Nautilus Trader native) |
| `ts_init` | `UInt64` | Nanoseconds UTC epoch timestamp of bar capture (Nautilus Trader native) |
| `open` | `Float64` | Bar open price |
| `high` | `Float64` | Bar high price ($H \ge \max(O, C)$) |
| `low` | `Float64` | Bar low price ($L \le \min(O, C)$) |
| `close` | `Float64` | Bar close price |
| `volume` | `Float64` | Base currency traded volume ($V \ge 0$) |

---

## Per-Instrument Cleaning & Integrity Report

| Symbol | BarType | Clean Rows | Date Range | Duplicates Removed | Invalid OHLC | Gaps Detected | Clean Size |
|---|---|---|---|---|---|---|---|
| `BTCUSD` | `BTCUSD.CRYPTO-1-MINUTE-LAST-EXTERNAL` | 3,778,481 | 2013-01-02 to 2026-02-14 | 0 | 0 | 25269 | 107.02 MB |
| `ETHUSD` | `ETHUSD.CRYPTO-1-MINUTE-LAST-EXTERNAL` | 3,850,009 | 2016-11-08 to 2026-02-14 | 3 | 0 | 13121 | 101.01 MB |
| `SOLUSD` | `SOLUSD.CRYPTO-1-MINUTE-LAST-EXTERNAL` | 2,297,722 | 2021-09-18 to 2026-02-14 | 3 | 0 | 7814 | 52.89 MB |
| `DOGEUSD` | `DOGEUSD.CRYPTO-1-MINUTE-LAST-EXTERNAL` | 2,439,592 | 2020-07-10 to 2026-02-14 | 3 | 0 | 17007 | 57.03 MB |
| `XRPUSD` | `XRPUSD.CRYPTO-1-MINUTE-LAST-EXTERNAL` | 3,827,835 | 2016-11-08 to 2026-02-14 | 2 | 0 | 25445 | 94.67 MB |
| `LINKUSD` | `LINKUSD.CRYPTO-1-MINUTE-LAST-EXTERNAL` | 2,275,282 | 2021-09-28 to 2026-02-14 | 2 | 0 | 22208 | 44.39 MB |
| `DOTUSD` | `DOTUSD.CRYPTO-1-MINUTE-LAST-EXTERNAL` | 2,379,184 | 2021-05-12 to 2026-02-14 | 2 | 0 | 5990 | 52.14 MB |

---

## Key Governance Decisions
1. **No Synthetic Fill**: For 24/7 crypto markets, zero-volume/missing intervals are logged in `defects.json` as natural market liquidity gaps or network outages, never forward-filled or fabricated.
2. **Nautilus Trader Compatibility**: Output partitioned under `catalog/bar/<bar_type>/<year>.parquet` with native `ts_event` (uint64 nanoseconds) and standard OHLCV float64 columns, allowing immediate zero-overhead ingestion via `ParquetDataCatalog.load_bars()`.
3. **Dual Access View**: Both `catalog/` (Nautilus Trader standard) and `by_symbol/` (standard quant research layout) are populated.

---

## Deliverables Generated
- **CLEAN_LOG**: `/home/da/quant-data/clean/crypto/CLEAN_LOG.md`
- **Defects List**: `/home/da/quant-data/clean/crypto/defects.json`
- **Sample Nautilus Parquet**: `/home/da/quant-data/clean/crypto/sample_nautilus_bars.parquet`
- **Clean Lake**: `/home/da/quant-data/clean/crypto/catalog`
