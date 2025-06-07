import yfinance as yf
import pandas as pd
import numpy as np
import networkx as nx
from typing import List, Iterable, Set, Dict


def get_us_tickers(n: int = 1000) -> List[str]:
    """Return up to ``n`` US tickers ranked by market capitalization."""
    # Russell 1000 constituents generally represent the largest US companies.
    index = yf.Ticker("^RUI")
    try:
        tickers = list(index.constituents.keys())
    except Exception:
        # Fallback to S&P 500 if Russell constituents are unavailable.
        tickers = list(yf.Ticker("^GSPC").constituents.keys())
    return tickers[:n]


def fetch_ticker_data(tickers: List[str]) -> pd.DataFrame:
    """Fetch historical close prices and fundamentals for tickers."""
    data = yf.Tickers(tickers)
    price = data.history(period="1y")['Close']
    info = {t: data.tickers[t].info for t in tickers}
    fundamentals = pd.DataFrame(info).T
    price.columns = price.columns.droplevel(0)  # yfinance returns multiindex
    return price, fundamentals


def categorize_series(s: pd.Series) -> pd.Series:
    """Categorize values into quantiles."""
    q1 = s.quantile(0.25)
    q3 = s.quantile(0.75)
    return s.apply(lambda x: -1 if x <= q1 else (1 if x >= q3 else 0))


def build_correlation_hypergraph(price: pd.DataFrame, threshold: float = 0.7) -> nx.Graph:
    """Return a clique-expanded graph representing high-correlation groups.

    The function forms hyperedges by clustering tickers whose pairwise
    correlations exceed ``threshold``. Each hyperedge is expanded into a clique
    so that standard graph algorithms (e.g., Laplacian eigenvalues) can be
    applied.
    """
    returns = price.pct_change().dropna(how='all')
    corr = returns.corr().fillna(0)

    unvisited = set(corr.columns)
    hyperedges: List[Set[str]] = []

    while unvisited:
        node = unvisited.pop()
        group = {node}
        queue = [node]
        while queue:
            current = queue.pop()
            neighbors = set(corr.index[corr[current] >= threshold]) & unvisited
            group.update(neighbors)
            queue.extend(neighbors)
            unvisited -= neighbors
        if len(group) > 1:
            hyperedges.append(group)

    G = nx.Graph()
    G.add_nodes_from(corr.columns)

    for hedge in hyperedges:
        for a in hedge:
            for b in hedge:
                if a < b:
                    G.add_edge(a, b)

    return G


def fiedler_value(G: nx.Graph) -> float:
    L = nx.normalized_laplacian_matrix(G).todense()
    eigvals = np.linalg.eigvalsh(L)
    eigvals.sort()
    if len(eigvals) < 2:
        return 0
    return float(eigvals[1])


def network_statistics(G: nx.Graph) -> Dict[str, float]:
    """Compute several network statistics for the given graph."""
    stats = {
        "fiedler_value": fiedler_value(G),
        "num_nodes": float(G.number_of_nodes()),
        "num_edges": float(G.number_of_edges()),
        "avg_degree": float(sum(dict(G.degree()).values()) / G.number_of_nodes()) if G.number_of_nodes() > 0 else 0.0,
        "density": nx.density(G) if G.number_of_nodes() > 1 else 0.0,
        "avg_clustering": nx.average_clustering(G) if G.number_of_nodes() > 0 else 0.0,
    }
    return stats


def main():
    # Download up to 1000 large-cap US tickers
    tickers = get_us_tickers(1000)
    price, fundamentals = fetch_ticker_data(tickers)

    fundamentals['per_category'] = categorize_series(fundamentals['trailingPE'])
    fundamentals['pbr_category'] = categorize_series(fundamentals['priceToBook'])
    fundamentals['eps_category'] = categorize_series(fundamentals['trailingEps'])
    fundamentals['capsize_category'] = categorize_series(fundamentals['marketCap'])

    G = build_correlation_hypergraph(price)
    stats = network_statistics(G)

    print("Network statistics:")
    for k, v in stats.items():
        print(f"  {k}: {v}")
    print(fundamentals[['sector', 'industry', 'per_category', 'pbr_category', 'eps_category', 'capsize_category']].head())

if __name__ == "__main__":
    main()
