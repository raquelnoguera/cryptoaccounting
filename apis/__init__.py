'''
These APIs are used to retrieve token information from different sources: coingecko, pancakeswap, etc.

All the APIs consume a list of token data to iterate and return a list of json objects (one per token) with the
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
'''

from .pancake import PankakeSwap
from .coingecko import CoinGecko
