'''
Used to get the current value of a token from Coingecko.

The coingecko API is defined in https://www.coingecko.com/en/api/documentation
Here, we use the python client of coingecko to request all the pricing information available for each token.

Among the APIs I had a look at, the Coingecko one is the one that supports most tokens.

'''

from mlogger import logger
from pycoingecko import CoinGeckoAPI

logger = logger.get_module_logger(__name__)

class CoinGecko(object):

    def __init__(self, tokens_list):
        self._chains = {}
        self._api = CoinGeckoAPI()
        self._parse_list(tokens_list)

    def _parse_list(self, tokens_list):
        '''
        Iterates the list of tokens and builds one list for each chain_id inside the _chains internal variable
        :param tokens_list: list of tokens to retrieve from coingecko
        :return: void
        '''
        for token in tokens_list:
            if token['chain_id'] in self._chains:
                self._chains[token['chain_id']].append(token)
            else:
                self._chains[token['chain_id']] = [token]

    def get_prices(self):
        prices = []
        logger.debug(f"\nList of chains to query in CoinGecko: {self._chains}\n")
        for chain in self._chains:
            token_list_for_chain = ""
            for token in self._chains[chain]:
                logger.debug(f"Including token {token} in the list.\n")
                token_list_for_chain += token['address'] + ','
            if len(token_list_for_chain) > 0:
                token_list_for_chain = token_list_for_chain[:-1]    # remove last comma
                logger.info(f"Requesting CoinGecko to provide prices in {token['chain_id']} chain "
                            f"for {token_list_for_chain}\n")
                pcs = self._api.get_token_price(id=token['chain_id'],
                                          contract_addresses=token_list_for_chain,
                                          vs_currencies='usd',
                                          include_market_cap=True,
                                          include_24hr_vol=True,
                                          include_24hr_change=True,
                                          include_last_updated_at=True)
                i = 0
                for item in pcs:
                    pcs[item]['address'] = item
                    pcs[item]['name'] = self._chains[chain][i]['token']
                    i += 1
                    prices.append(pcs[item])
        logger.debug(f"\nPrices returned by CoinGecko: {prices}\n")
        return prices