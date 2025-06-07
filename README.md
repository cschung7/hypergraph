# Hypergraph Analysis

This repository contains simple scripts for fetching financial data with `yfinance` and building a correlation-based **hypergraph** of equities. The scripts report several network statistics – including the Fiedler value of the Laplacian – to help analyze market structure.

## Scripts

- `data_analysis.py` – downloads equity prices and fundamentals, categorizes them into quartiles, builds a correlation **hypergraph** of returns, and prints various network statistics (Fiedler value, average clustering, etc.).
- `macro_analysis.py` – fetches macro market indicators such as equity indices and commodities.

Both scripts require `yfinance`, `pandas`, `numpy`, and `networkx`.

The hypergraph is formed by clustering tickers that exhibit a correlation above
a threshold (default ``0.7``) and expanding these groups into cliques.

Run a script with:

```bash
python3 data_analysis.py
python3 macro_analysis.py
```
