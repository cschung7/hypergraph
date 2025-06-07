# Hypergraph Analysis

This repository contains simple scripts for fetching financial data with `yfinance` and building a correlation-based graph of equities. The Fiedler value of the graph Laplacian is reported as a basic network statistic.

## Scripts

- `data_analysis.py` – downloads equity prices and fundamentals, categorizes them into quartiles, builds a correlation graph of returns, and prints the Fiedler value.
- `macro_analysis.py` – fetches macro market indicators such as equity indices and commodities.

Both scripts require `yfinance`, `pandas`, `numpy`, and `networkx`.

Run a script with:

```bash
python3 data_analysis.py
python3 macro_analysis.py
```
