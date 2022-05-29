To use the CoinMarketCap API you will need to:

1. Follow the instructions in [CoinMarketCap](https://coinmarketcap.com/api/) 
to get an API key.
2. Create a file in this folder named **"secrets.json"** with the following 
content:

```
{
  "coinmarketcap_apikey": "your_coinmarketcap_key_here",
  "bscscan_apikey": "your_bscscan_key_here",
  "etherscan_apikey": "your_etherscan_key_here",
  "ftmscan_apikey": "your_ftmscan_key_here",
  "moonriverscan_apikey": "your_moonriverscan_key_here",
  "polygonscan_apikey": "your_plygonscan_key_here"
}
```

After this, the CoinMarketCap API in the **apis** directory should work 
correctly.
