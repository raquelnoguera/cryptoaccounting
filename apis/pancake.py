'''
Used to get the current value of a token from Pancake Swap.
'''

from mlogger import logger
from urllib.request import Request, urlopen
import json

logger = logger.get_module_logger(__name__)

BASE_URI = "https://api.pancakeswap.info/api/v2/tokens/"

class PancakeSwap(object):

    def __init__(self, tokens_list):
        self._baseuri = BASE_URI
        self._tokenslist = tokens_list

    def get_prices(self):
        prices = []
        for token in self._tokenslist:
            logger.debug(f"Quering token {token} in the list.\n")
            uri = self._baseuri + token['address']
            pcs = {
                "name": token['token'],
                "address": token['address'],
                "usd": 0,
                "usd_market_cap": 0,
                "usd_24h_vol": 0,
                "usd_24h_change": 0,
                "last_updated_at": 0
            }
            try:
                req = Request(uri)
                req.add_header('Accept',
                               'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8')
                req.add_header('User-Agent',
                               'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:95.0) Gecko/20100101 Firefox/95.0')
                response = urlopen(req).read()
                logger.debug(f"Response from Pancake {response}")
                quote = json.loads(response)

                if "data" in quote.keys():
                    pcs["name"] = quote['data']['symbol']
                    pcs["usd"] = quote['data']['price']
                    pcs["last_updated_at"] = quote['updated_at']
                    logger.info(f"Current price in USD for {quote['data']['symbol']} is {pcs}")
                else:
                    logger.info(f"Could not get current price for {token['token']} in Pancake Swap")
            except Exception as e:
                result = -1
                logger.error(f"Pancake returned exception: {e}")
            prices.append(pcs)
        logger.debug(f"\nPrices returned by PancakeSwap: {prices}\n")
        return prices