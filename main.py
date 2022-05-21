# This is a sample Python script.

from mlogger import logger
from pathlib import Path
from apis import PankakeSwap, CoinGecko
import json

logger = logger.get_module_logger(__name__)

def parse_tokens_file():
    '''
    Parses tokens.json to build an object that contains a list for each api.
    :return: Object that contains one list of tokens for each api. I.e. one list for pancakeswap, one for coingecko,
    and so on. The keys used for this object are the "api" name defined for each token.
    '''
    logger.info("Parsing lists of tokens.")
    token_lists = {}    # This object is filled with a list of tokens for each provider (pancakeswap, coingecko, etc).
                        # The key is the token "api" field in each token inside tokens.json
    tokenspath = Path.cwd() / "tokens.json"
    assert (tokenspath.exists())
    tokens = {}
    with open(tokenspath) as tokensfile:
        tokens = json.load(tokensfile)
    tokenkeys = tokens.keys()
    for token in tokenkeys:
        if tokens[token]['api'] in token_lists:
            token_lists[tokens[token]['api']].append(tokens[token])
        else:
            token_lists[tokens[token]['api']] = [tokens[token]]
    return token_lists

def format_token_info(token):
    '''
    Formats the token information into a correct CSV pattern for storage in the file.
    :param token: token information previously retrieved from each API (coingecko, pancakeswap, etc.).
    :return: string with the token data in csv format
    '''
    line = f"{token['name']},{token['address']},{token['last_updated_at']},{token['usd']},{token['usd_market_cap']},"
    line += f"{token['usd_24h_vol']},{token['usd_24h_change']}"
    return line

# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    logger.info("Starting CryptoAccounting lookups.")
    lists_of_tokens = parse_tokens_file()
    logger.debug(f"Retrieved list of tokens: {lists_of_tokens}\n")
    apis = lists_of_tokens.keys()
    tokens_prices = []
    for api in apis:
        if api == "coingecko":
            cg = CoinGecko(lists_of_tokens[api])
            tokens_prices.extend(cg.get_prices())
        else: # pancakeswap
            pcs = PankakeSwap(lists_of_tokens[api])
            tokens_prices.extend(pcs.get_prices())
    logger.debug(f"Prices retrieved: {tokens_prices}")
    with open('output.csv', 'w') as outfile:
        for token_info in tokens_prices:
            line = format_token_info(token_info)
            logger.debug(f"\nToken line: {line}\n")
            outfile.write(line + '\n')




