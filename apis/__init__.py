'''
These APIs are used to:

 - coingecko and pancake: retrieve token information.
    They consume a list of token data to iterate and return a list of json objects (one per token) with the
    following schema, inspired in the coingecko API:

        {
            "name": "string",
            "address": "string",
            "usd": "number",
            "usd_market_cap": "number",
            "usd_24h_vol": "number",
            "usd_24h_change": "number",
            "last_updated_at": "integer"
        }

- tokenscan: retrieve the list of tokens / coins for the provided wallet / contract address
'''

from .pancake import PancakeSwap
from .coingecko import CoinGecko
from .tokenscanner import Scan

# Supported Networks
networks = {
    'avalanche': {
        'id': 'avalanche',
        'symbol': 'AVAX',
        'decimals': 18,
        'chain': 'avalanche',
        'api': 'https://api.snowtrace.io/api'
    },
    'binance': {
        'id': 'binance',
        'symbol': 'BNB',
        'decimals': 18,
        'chain': 'binance-smart-chain',
        'api': 'https://api.bscscan.com/api'
    },
    'celo': {
        'id': 'celo',
        'symbol': 'CELO',
        'decimals': 18,
        'chain': 'celo',
        'api': 'https://api.celoscan.xyz/api'
    },
    'ethereum': {
        'id': 'ethereum',
        'symbol': 'ETH',
        'decimals': 18,
        'chain': 'ethereum',
        'api': 'https://api.etherscan.io/api'
    },
    'fantom': {
        'id': 'fantom',
        'symbol': 'FTM',
        'decimals': 18,
        'chain': 'fantom',
        'api': "https://api.ftmscan.com/api"
    },
    'moonriver': {
        'id': 'moonriver',
        'symbol': 'MOVR',
        'decimals': 18,
        'chain': 'moonriver',
        'api': "https://api-moonriver.moonscan.io/api"
    },
    'polygon': {
        'id': 'polygon',
        'symbol': 'MATIC',
        'decimals': 18,
        'chain': 'polygon-pos',
        'api': "https://api.polygonscan.com/api"
    }
}