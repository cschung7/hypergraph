"""List of modules required for running the hypergraph analysis scripts."""

REQUIRED_MODULES = [
    'yfinance',
    'pandas',
    'numpy',
    'networkx',
]

if __name__ == '__main__':
    print('\n'.join(REQUIRED_MODULES))
