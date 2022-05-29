'''! Used to get the list of tokens that the wallet has in the network provided
The scan API is identical for BSC, ETHER, FTM and MOON and are defined in:

- BINANCE: https://docs.bscscan.com/api-endpoints
- CELO: https://celoscan.xyz/apis
- ETHEREUM: https://docs.etherscan.io/api-endpoints
- FANTOM: https://docs.ftmscan.com/api-endpoints
- MOONRIVER: https://moonriver.moonscan.io/apis
- POLYGON: https://docs.polygonscan.com/api-endpoints

We use the requests library (https://github.com/psf/requests) to send request to these API.
'''

from mlogger import logger
import requests

logger = logger.get_module_logger(__name__)

class Scan(object):
    def __init__(self, network, apikey, address):
        '''! Initialise the BscScan object.

        @param network: 'bsc' | 'eth' | 'ftm' | 'movr'
        @param apikey:  Key for the BscScan API
        @param address: wallet address of the BSC
        '''
        self.network = network
        self._key = apikey
        self._address = address

    def _getBalance(self):
        '''! Get the balance for the native token unit of this chain (e.g. wei for Ethereum)

        :return: Balance for native token
        '''
        payload = {
            'apikey': self._key,
            'module': 'account',
            'action': 'balance',
            'address': self._address
        }
        res = requests.get(self.network['api'], params=payload)
        logger.debug(f"Status code of response: {res.status_code}")
        if (res.status_code == requests.codes.ok):
            # Assume that the response is json and iterate the response
            try:
                resp = res.json()
                balance = resp["result"]
                logger.debug(f"Current balance: {balance}")
                return balance
            except requests.exceptions.JSONDecodeError:
                logger.error("Error parsing JSON.")
                logger.error(f"Response: {res.text}")
                return 0
        else:
            logger.error(f"Error - Status code returned by BscScan: {res.status_code}")
            return 0

    def getBalanceForNative(self):
        '''! Get the balance for this address for the native coin of this network (e.g. ETH for Ethereum)

        :return: string with the current balance in native coin (ETH, BNB, FTM or MOVR)
        '''
        balance = self._getBalance()
        if balance > 0:
            for _ in range(1, self.network['decimals']):
                balance = balance / 10
        return f"{balance} "

    def getListTokens(self):
        '''! Gets the list of transfers of BEP20 tokens for the current address and iterates it to retrieve the list
        of BEP20 tokens that this address has.

        @returns the list of BEP20 tokens for the current address.
        '''
        payload = {
            'apikey': self._key,
            'module': 'account',
            'action': 'tokentx',
            'address': self._address,
            'startblock': 0,
            'endblock': 999999999,
            'sort': 'asc'
        }
        res = requests.get(self.network['api'], params = payload)
        logger.debug(f"Status code of response: {res.status_code}")
        if(res.status_code == requests.codes.ok):
            # Assume that the response is json and iterate the response
            try:
                tokensTransfersList = res.json()
                tokensrcv = tokensTransfersList["result"]
                logger.debug(f"Number of token transfers: {len(tokensrcv)}")
                tokens = {}
                keys = []
                for token in tokensrcv:
                    if token["tokenSymbol"] in keys:
                        continue
                    else:
                        keys.append(token["tokenSymbol"])
                        tokens[token["tokenSymbol"]] = {
                                "token": token["tokenSymbol"],
                                "address": token["contractAddress"],
                                "api": "coingecko",
                                "chain_id": self.network['chain']
                            }
                return tokens
            except requests.exceptions.JSONDecodeError:
                logger.error("Error parsing JSON.")
                logger.error(f"Response: {res.text}")
                return {}
        else:
            logger.error(f"Error - Status code returned by {self.network['id']} scan: {res.status_code}")
            return {}  # empty object