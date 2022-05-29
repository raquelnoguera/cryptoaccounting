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
        logger.debug(f"List of chains to query in CoinGecko: {self._chains}")
        for chain in self._chains:
            token_list_for_chain = ""
            for token in self._chains[chain]:
                # logger.debug(f"Including token {token} in the list.")
                token_list_for_chain += token['address'] + ','
            if len(token_list_for_chain) > 1:
                token_list_for_chain = token_list_for_chain[:-1]    # remove last comma
                logger.info(f"Requesting CoinGecko to provide prices in {token['chain_id']} chain "
                            f"for {token_list_for_chain}")
                cgk = self._api.get_token_price(id=token['chain_id'],
                                          contract_addresses=token_list_for_chain,
                                          vs_currencies='usd',
                                          include_market_cap=True,
                                          include_24hr_vol=True,
                                          include_24hr_change=True,
                                          include_last_updated_at=True)
                logger.debug(f"Response from Coingecko: {cgk}")
                i = 0
                for key in cgk:
                    # logger.debug(f"Iteration for key: {key}")
                    cgk[key]['address'] = key
                    # skip all the tokens that did not get a quote from coingecko
                    for j in range(0, len(self._chains[chain]) - 1):
                        # logger.debug(f"(i, j) = ({i}, {j}) - Comparing {key} to {self._chains[chain][j]['address']}")
                        if key.upper() != self._chains[chain][j]['address'].upper():
                            # logger.debug(f"value of j = {j} ignored")
                            continue
                        else:
                            # logger.debug(f"value of i = {j}")
                            i = j
                            break
                    cgk[key]['name'] = self._chains[chain][i]['token']
                    prices.append(cgk[key])
        logger.debug(f"Prices returned by CoinGecko: {prices}")
        return prices