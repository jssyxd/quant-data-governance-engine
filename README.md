# Quant Data Governance Engine & Nautilus Trader Parquet Catalog

[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)
[![Python 3.10+](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/downloads/)
[![NautilusTrader](https://img.shields.io/badge/NautilusTrader-1.200+-orange.svg)](https://nautilustrader.io/)
[![Polars](https://img.shields.io/badge/Engine-Polars%20%7C%20DuckDB-yellow.svg)](https://pola.rs/)

> **生产级量化历史数据工程自动化体系**：覆盖超大规模（150GB+）多资产高频历史行情（Crypto 24/7、美股 US Equities、商品期货 Futures）的**高速断点采集、几何物理不变量审计、无前向填充缺口治理、双契约标准化分区**以及 **Nautilus Trader 事件驱动回测引擎原生 ParquetDataCatalog 的极速序列化与回测加载**。

本项目沉淀了完整的自动化工作流脚本、现场系统治理规范（1:1 Swap 固化、CIFS/SMB 文件锁兼容性补丁、国内镜像网络直连绕行）以及即插即用的 **Agent Skill (`quant-data-governance-engine`)**，支持日后零成本增量数据拉取与回测数据库无损重建。

---

## 目录
- [核心架构与设计哲学](#核心架构与设计哲学)
- [双契约标准数据模型](#双契约标准数据模型)
- [已验证治理入库资产（实机验证）](#已验证治理入库资产实机验证)
- [工程落地难点与核心解法](#工程落地难点与核心解法)
  - [1. 物理挂载与 CIFS/SMB 文件锁 (Errno 95) 补丁](#1-物理挂载与-cifssmb-文件锁-errno-95-补丁)
  - [2. 国内网络直连与海外代理自适应分流](#2-国内网络直连与海外代理自适应分流)
  - [3. 1:1 永久 Swap 内存固化](#3-11-永久-swap-内存固化)
- [快速上手指南](#快速上手指南)
  - [安装依赖](#安装依赖)
  - [步骤 1：高速容错拉取开源金融数据集](#步骤-1高速容错拉取开源金融数据集)
  - [步骤 2：日内多核高频 K 线清洗与审计](#步骤-2日内多核高频-k-线清洗与审计)
  - [步骤 3：注入 Nautilus Trader 原生 DataCatalog](#步骤-3注入-nautilus-trader-原生-datacatalog)
- [Agent Skill 规范与自动化工作流](#agent-skill-规范与自动化工作流)
- [项目结构](#项目结构)
- [开源许可证](#开源许可证)

---

## 核心架构与设计哲学

在严肃的事件驱动量化回测（如 Nautilus Trader）中，**“垃圾进，垃圾出 (Garbage In, Garbage Out)”** 和 **“前向偏误 / 价格幻觉 (Look-ahead Bias & Phantom Fills)”** 是导致实盘滑铁卢的核心根源：
1. **真实世界拒绝静默填充**：在 7x24 的加密货币市场中，缺乏流动性或交易所断连导致的无成交时段必须如实记录为客观缺口（Gaps），**严禁通过前向填充（Forward-fill）凭空伪造交易价格**。
2. **极速高并发处理**：采用 Rust 原生加速的 `Polars` 与 `DuckDB` 代替传统 Pandas 全量载入，数千万行 1 分钟级 OHLCV 秒级清洗与聚合。
3. **双契约落地 (Dual-Contract Lake)**：
   - **研究标准层 (`by_symbol/`)**：遵循量化研究通行标准的 UTC `timestamp`、浮点 OHLCV、年/月分区 Parquet。
   - **引擎原生层 (`catalog/`)**：内嵌 Nautilus Trader 要求的纳秒级无符号整数 `ts_event` / `ts_init`、全局唯一 `bar_type`（如 `BTCUSD.CRYPTO-1-MINUTE-LAST-EXTERNAL`），支持直接通过 `ParquetDataCatalog.bars()` 进行零损耗读取。

---

## 双契约标准数据模型

清洗管线输出的 Parquet 文件采用双契约复合结构：

```text
Field Name     | Data Type               | 说明
---------------+-------------------------+---------------------------------------------------
timestamp      | timestamp[us, tz=UTC]   | 标准人类/通用研究基准 UTC 时间戳
symbol         | Utf8 / string           | 标准标的代码 (如 BTCUSD, ETHUSD)
timeframe      | Utf8 / string           | 周期分辨率 (如 1m, 5m, 15m, 1h, 1d)
bar_type       | Utf8 / string           | Nautilus Trader 规范 BarType 唯一全名
ts_event       | UInt64                  | 纳秒级 UTC 时间戳（K线收盘刻度，撮合引擎判定依据）
ts_init        | UInt64                  | 纳秒级 UTC 时间戳（数据接收刻度，防未来函数）
open           | Float64                 | 开盘价
high           | Float64                 | 最高价 (严格满足 H >= max(O, C) 且 H >= L)
low            | Float64                 | 最低价 (严格满足 L <= min(O, C) 且 L <= H)
close          | Float64                 | 收盘价
volume         | Float64                 | 基础币种成交量 (严格满足 V >= 0)
```

---

## 已验证治理入库资产（实机验证）

本项目已在生产级环境完成首批核心加密资产（2013-2026 全历史 1 分钟级别）全流程清洗，产出质量日志 `CLEAN_LOG.md` 与缺陷清单 `defects.json`：

| 资产代码 | Nautilus BarType 标识符 | 验证有效K线行数 | 时间跨度 | 重复行去重 | 违规K线剔除 | 记录客观缺口 | 紧凑 Parquet 大小 |
|---|---|---|---|---|---|---|---|
| **BTCUSD** | `BTCUSD.CRYPTO-1-MINUTE-LAST-EXTERNAL` | **3,778,481** | 2013-01 至 2026-02 | 0 | 0 | 25,269 | 107.02 MB |
| **ETHUSD** | `ETHUSD.CRYPTO-1-MINUTE-LAST-EXTERNAL` | **3,850,009** | 2016-11 至 2026-02 | 3 | 0 | 13,121 | 101.01 MB |
| **SOLUSD** | `SOLUSD.CRYPTO-1-MINUTE-LAST-EXTERNAL` | **2,297,722** | 2021-09 至 2026-02 | 3 | 0 | 7,814 | 52.89 MB |
| **DOGEUSD**| `DOGEUSD.CRYPTO-1-MINUTE-LAST-EXTERNAL`| **2,439,592** | 2020-07 至 2026-02 | 3 | 0 | 17,007 | 57.03 MB |
| **XRPUSD** | `XRPUSD.CRYPTO-1-MINUTE-LAST-EXTERNAL` | **3,827,835** | 2016-11 至 2026-02 | 2 | 0 | 25,445 | 94.67 MB |
| **LINKUSD**| `LINKUSD.CRYPTO-1-MINUTE-LAST-EXTERNAL`| **2,275,282** | 2021-09 至 2026-02 | 2 | 0 | 22,208 | 44.39 MB |
| **DOTUSD** | `DOTUSD.CRYPTO-1-MINUTE-LAST-EXTERNAL` | **2,379,184** | 2021-05 至 2026-02 | 2 | 0 | 5,990 | 52.14 MB |
| **合计**   | **全量主流现货分钟级全景回测湖**        | **20,848,105** | **长达 13 年**     | **15**| **0**| **116,854** | **509.15 MB** |

> **回测适配性实测**：通过本仓库提供的 `examples/test_nautilus_load.py` 对治理后 Parquet 执行 Nautilus Trader 原生 `BarDataWrangler` 与 `ParquetDataCatalog.bars()` 实机测试，10,000 条样本数据解析成功率 **100%**，微秒/纳秒时间戳与高精度定点价格对齐零误差。

---

## 工程落地难点与核心解法

### 1. 物理挂载与 CIFS/SMB 文件锁 (Errno 95) 补丁
- **背景**：本地 SSD 空间有限，大规模量化湖常部署于 NAS / SMB / CIFS 共享存储。Linux GVFS/CIFS 挂载点**不支持 POSIX `fchmod`/`chmod` 和原生锁模式**。
- **解法**：`scripts/download_hf_dataset.py` 内置了对 `filelock._unix.UnixFileLock` 的运行时异常捕获与无害穿透处理（静默拦截 `[Errno 95] Operation not supported`），确保在外部网络共享盘上持续多线程断点写入不崩溃。

### 2. 国内网络直连与海外代理自适应分流
- **背景**：`hf-mirror.com` 国内镜像服务器位于大陆境内。当系统配置了全局海外代理（如 `192.168.1.5:7890`）时，对镜像的请求会经由海外节点绕行回国，导致严重的 SSL EOF 握手重置与连接中断。
- **解法**：下载引擎在检测到目标端点包含 `hf-mirror.com` 时，在子进程级自动剥离 `http_proxy` / `https_proxy` 变量，直连国内骨干网，保持百兆宽带满速吞吐；对 GitHub 仓库与 Hugging Face 鉴权请求则自适应保持海外代理。

### 3. 1:1 永久 Swap 内存固化
- **背景**：多线程并发解析十吉字节级压缩 Parquet / CSV 时易瞬时突破物理内存导致 OOM。
- **解法**：提供配套的 1:1 Linux Swap 固化配置（如 12GB 物理 RAM 配备 12GB `/swap.img`），并固化至 `/etc/fstab`，保障海量数据合并期间系统始终稳健。

---

## 快速上手指南

### 安装依赖
```bash
pip install polars duckdb pyarrow pandas huggingface_hub
# 若需要本地运行回测，请安装 nautilus_trader
pip install nautilus_trader
```

### 步骤 1：高速容错拉取开源金融数据集
```bash
# 自动绕过海外代理回环，支持断点续传与 SMB 共享盘挂载
python3 scripts/download_hf_dataset.py OMCHOKSI108/my-cloud-data-lake ./raw_data/ 4
```

### 步骤 2：日内多核高频 K 线清洗与审计
```bash
# 执行时间戳单调性去重、几何不变量剔除与客观缺口发现
python3 scripts/clean_crypto_bars.py \
    ./raw_data/ALL_TIME_DATA/1min_time/BTCUSD#_1min.parquet \
    ./clean_data/crypto \
    BTCUSD \
    1m
```

### 步骤 3：注入 Nautilus Trader 原生 DataCatalog
```bash
# 一键生成 Nautilus Trader 规范目录并进行实机加载验证
python3 scripts/nautilus_catalog_converter.py \
    ./clean_data/crypto/sample_nautilus_bars.parquet \
    ./nautilus_catalog \
    BTCUSD \
    CRYPTO
```

验证脚本测试：
```bash
python3 examples/test_nautilus_load.py
```

---

## Agent Skill 规范与自动化工作流

本项目已完整遵循 [Agent Skills 规范](https://github.com/vercel-labs/skills)，在 `skill-quant-data-governance-engine/` 目录下提供了可以直接导入 AI Agent（如 Claude Code, Pi, OpenCode, Cursor, Herdr）的元数据与操作指引：
- **`SKILL.md`**：定义了治理管线的意图触发词、自动化调用规范与上下文契约。
- **`scripts/`**：包含可直接调用的自动化 CLI。
- **`references/`**：提供详尽的量化审计不变量公式与 Nautilus Trader 集成范例。

---

## 项目结构

```text
quant-data-governance-engine/
├── README.md                              # 项目详细介绍与架构文档
├── LICENSE                                # MIT 开源许可证
├── skill-quant-data-governance-engine/    # 即插即用 Agent Skill 套件
│   ├── SKILL.md                           # Skill 规约与调用配置
│   ├── scripts/                           # Skill 工具集软链/副本
│   └── references/                        # 方法论与回测契约说明
├── scripts/                               # 核心工作流自动化生产脚本
│   ├── download_hf_dataset.py             # 容错多线程极速下载引擎
│   ├── clean_crypto_bars.py               # Polars 驱动的高速治理审计器
│   └── nautilus_catalog_converter.py      # Nautilus Trader 原生 Catalog 序列化器
├── docs/                                  # 架构文档与工程实践备忘
│   ├── methodology.md                     # 存储/内存/网络/数据不变量方法论
│   └── nautilus-integration.md            # Nautilus Trader 数据接口指南
└── examples/                              # 实机验证样本与测试代码
    ├── sample_nautilus_bars.parquet       # 包含 10,000 条已清洗验证的 K 线样本
    ├── sample_defects.json                # 样本缺口审计报告
    ├── sample_CLEAN_LOG.md                # 样本治理汇总日志
    └── test_nautilus_load.py              # Nautilus Trader 原生回测加载验证测试
```

---

## 开源许可证

本项目基于 [MIT 许可证](LICENSE) 开源。欢迎量化机构、研究员与自动化交易者在此基础上构建自己的自研数据中台！
