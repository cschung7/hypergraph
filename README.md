# Hypergraph Analysis

This repository contains simple scripts for fetching financial data with `yfinance` and building a correlation-based **hypergraph** of equities. The scripts report several network statistics – including the Fiedler value of the Laplacian – to help analyze market structure.

## Scripts

- `data_analysis.py` – downloads prices and fundamentals for up to 1000 large-cap US tickers, categorizes valuation ratios (PER, PBR, EPS, market cap) into top/bottom quartiles (+1/‑1/0), builds a correlation **hypergraph** of returns, and prints network statistics including the Fiedler value.
  It first creates a simple correlation graph where edges connect pairs with correlation above the threshold. Statistics are printed for this correlation graph and the clique-expanded hypergraph.
- `macro_analysis.py` – fetches macro market indicators such as equity indices, yield spreads and commodities.
  It downloads S&P 500, NASDAQ, VIX, JPY/USD, EURO/USD, gold, WTI and the 10Y-2Y and 10Y-3M Treasury spreads.

Both scripts require `yfinance`, `pandas`, `numpy`, and `networkx`.
Install them with:

```bash
pip install yfinance pandas numpy networkx
```

The list of dependencies is also available in `requirements.py` for reference.

The hypergraph is formed by clustering tickers that exhibit a correlation above a threshold (default ``0.7``) and expanding these groups into cliques. Fundamentals are classified using quartiles so PER, PBR, EPS and market capitalization each receive a label of ``+1`` (top 25%), ``-1`` (bottom 25%) or ``0``.
First, a simple correlation network is constructed using the same threshold.

Run a script with:

```bash
python3 data_analysis.py
python3 macro_analysis.py
```

The repository includes an `__init__.py` so the functions can be imported as a
package if desired.
