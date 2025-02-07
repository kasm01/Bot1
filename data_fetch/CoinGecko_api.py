import requests

COINGECKO_API_URL = "https://api.coingecko.com/api/v3"

def get_coingecko_price(symbol="bitcoin"):
    """
    CoinGecko API ile ücretsiz kripto fiyat verisi al.
    :param symbol: "bitcoin", "ethereum", "binancecoin" gibi kripto para ismi
    """
    url = f"{COINGECKO_API_URL}/simple/price"
    params = {"ids": symbol, "vs_currencies": "usd"}
    response = requests.get(url, params=params).json()
    
    return response[symbol]["usd"]

def get_market_data(symbol="bitcoin"):
    """
    CoinGecko API ile piyasa verilerini getir.
    :param symbol: "bitcoin", "ethereum", "binancecoin" gibi kripto para ismi
    """
    url = f"{COINGECKO_API_URL}/coins/markets"
    params = {"vs_currency": "usd", "ids": symbol, "order": "market_cap_desc"}
    response = requests.get(url, params=params).json()
    
    return response[0]  # İlk sonucu döndür (kripto hakkında detaylı bilgi)

def get_historical_prices(symbol="bitcoin", days=30):
    """
    CoinGecko API ile geçmiş fiyatları getir.
    :param symbol: "bitcoin", "ethereum", "binancecoin" gibi kripto para ismi
    :param days: Kaç günlük veriyi almak istiyorsun (1, 7, 30, 90 vb.)
    """
    url = f"{COINGECKO_API_URL}/coins/{symbol}/market_chart"
    params = {"vs_currency": "usd", "days": days, "interval": "daily"}
    response = requests.get(url, params=params).json()
    
    return response["prices"]  # Fiyat tarihçesini döndür

def get_trending_coins():
    """
    CoinGecko API ile trend olan kripto paraları getir.
    """
    url = f"{COINGECKO_API_URL}/search/trending"
    response = requests.get(url).json()
    
    trending_coins = [coin["item"]["name"] for coin in response["coins"]]
    return trending_coins
