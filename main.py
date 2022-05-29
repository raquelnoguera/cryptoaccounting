'''!
This script get the current price for tokens.

The list of tokens can be specify in two ways:

1. via the tokens.json file in the root directory.
    In this case, the script will look for the prices of the tokens in this list and return a
2. providing an Ethereum compatible wallet address. In this case, the
'''

import sys
from mlogger import logger
from pathlib import Path
from apis import networks, PankakeSwap, CoinGecko, Scan
import json
import re

logger = logger.get_module_logger(__name__)


def isValidWalletAddress(_address):
    '''
    Check whether the format of _address corresponds to that of a valid Ethereum address
    :param _address: wallet address to check
    :return: boolean
    '''
    validAddrPattern = r"0x[0123456789ABCDEFabcdef]{40,40}"
    pattern = re.compile(validAddrPattern)
    return pattern.match(_address)

def parse_keys_file():
    '''! Parses the secrets.json file to retrieve all the keys for the different APIs.

    @return: Object that contains the list of API keys.
    '''
    logger.info("Parsing lists of API keys.")
    # The key is the token "api" field in each token inside tokens.json
    keyspath = Path.cwd() / "config/secrets.json"
    assert (keyspath.exists())
    with open(keyspath) as keysfile:
        keys = json.load(keysfile)
    logger.debug(f"API keys: {keys}")
    return keys

def get_tokenslist_per_api(tokens):
    token_lists = {}    # This object is filled with a list of tokens for each provider (pancakeswap, coingecko, etc).
                        # The key is the token "api" field in each token inside tokens.json
    for chain in tokens:
        for token in tokens[chain]:
            if tokens[chain][token]['api'] in token_lists:
                token_lists[tokens[chain][token]['api']].append(tokens[chain][token])
            else:
                token_lists[tokens[chain][token]['api']] = [tokens[chain][token]]
    return token_lists

def parse_tokens_file():
    '''! Parses tokens.json to build an object that contains a list for each api.

    @return: Object that contains one list of tokens for each api. I.e. one list for pancakeswap, one for coingecko,
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
    return get_tokenslist_per_api(tokens)

def format_token_info(token, isHeader=False):
    '''
    Formats the token information into a correct CSV pattern for storage in the file.
    :param token: token information previously retrieved from each API (coingecko, pancakeswap, etc.).
    :param isHeader: return the heading line
    :return: string with the token data in csv format
    '''
    if isHeader:
        line = "Symbol,Contract,Last Updated,Value in USD,Market cap in USD,Volume last 24h,Change last 24h"
    else:
        line = f"{token['name']},{token['address']},{token['last_updated_at']},{token['usd']},{token['usd_market_cap']},"
        line += f"{token['usd_24h_vol']},{token['usd_24h_change']}"
    return line

# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    logger.info("Starting CryptoAccounting lookups.")
    if(len(sys.argv) > 1):
        address = sys.argv[1]
        if isValidWalletAddress(sys.argv[1]):
            logger.debug(f"{address} matches the pattern of a wallet address")
            api_keys = parse_keys_file()
            tokens = {}
            # Iterate all the supported networks and retrieve the tokens that this address has in each one of them
            for network in networks:
                scan = Scan(networks[network], api_keys[network], address)
                tokens[network] = scan.getListTokens()
            logger.debug(f"List of scanned tokens: {tokens}")
            lists_of_tokens = get_tokenslist_per_api(tokens)
        else:
            logger.info(f"Invalid wallet address: {address}")
            print(f"Invalid wallet address: {address}")
            exit(-1)
    else:
        lists_of_tokens = parse_tokens_file()
        logger.debug(f"Retrieved list of tokens: {lists_of_tokens}\n")
    apis = lists_of_tokens.keys()
    logger.debug(f"apis = {apis}")
    tokens_prices = []
    for api in apis:
        if api == "coingecko":
            cg = CoinGecko(lists_of_tokens[api])
            tokens_prices.extend(cg.get_prices())
        elif api == "pancakeswap":
            pcs = PankakeSwap(lists_of_tokens[api])
            tokens_prices.extend(pcs.get_prices())
        ## else: # "none" case

    logger.debug(f"Prices retrieved: {tokens_prices}")
    with open('output.csv', 'w') as outfile:
        line = format_token_info("", True)
        outfile.write(line + '\n')
        for token_info in tokens_prices:
            line = format_token_info(token_info)
            # logger.debug(f"\nToken line: {line}\n")
            outfile.write(line + '\n')
