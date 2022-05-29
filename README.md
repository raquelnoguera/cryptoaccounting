# Crypto Accounting

This is a small project that I have done to get the current value of a 
crypto investment portfolio.

It supports two uses:

* List the tokens of interest in the ***"tokens.json*** file
in the root folder and this script will retrieve the value of 
the tokens listed there.
* Pass a wallet address as a parameter and the script will scan for 
all the tokens inside this wallet on various chains. The following chains 
are scanned: BSC, Celo, Ethereum, Fantom, Moonriver and Polygon. 

Adding chains is quite simple if their scan API is compatible with the 
ones above. Have a look at the api module to add additional chains.

*ToDo:* 
1. *Retrive balance of chain coin (e.g. ETH for Ethereum, BNB for Binance,
MATIC for Polygon, etc.) for use 2 above.*
2. *Get the actual amount of each token for use 2 above (now it only gets
the token movements of the account).*




