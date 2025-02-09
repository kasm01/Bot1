import requests

COINGECKO_API_URL = "https://api.coingecko.com/api/v3"

def get_coingecko_price(symbol="bitcoin"):
    """
    CoinGecko API ile ücretsiz kripto fiyat verisi al.
    :param symbol: "bitcoin", "ethereum", "binancecoin" gibi kripto para ismi
    :return: Kripto paranın USD fiyatı veya None (Hata durumunda)
    """
    try:
        url = f"{COINGECKO_API_URL}/simple/price"
        params = {"ids": symbol, "vs_currencies": "usd"}
        response = requests.get(url, params=params)

        if response.status_code != 200:
            print(f"⚠️ API Hatası: {response.status_code}")
            return None

        data = response.json()
        return data.get(symbol, {}).get("usd", None)
    
    except Exception as e:
        print(f"⚠️ CoinGecko Fiyat Verisi Alınamadı: {e}")
        return None

def get_market_data(symbol="bitcoin"):
    """
    CoinGecko API ile piyasa verilerini getir.
    :param symbol: "bitcoin", "ethereum", "binancecoin" gibi kripto para ismi
    :return: Piyasa verisi (dict) veya None (Hata durumunda)
    """
    try:
        url = f"{COINGECKO_API_URL}/coins/markets"
        params = {"vs_currency": "usd", "ids": symbol, "order": "market_cap_desc"}
        response = requests.get(url, params=params)

        if response.status_code != 200:
            print(f"⚠️ API Hatası: {response.status_code}")
            return None

        data = response.json()
        return data[0] if data else None  # İlk sonucu döndür (kripto hakkında detaylı bilgi)
    
    except Exception as e:
        print(f"⚠️ CoinGecko Piyasa Verisi Alınamadı: {e}")
        return None

def get_historical_prices(symbol="bitcoin", days=30):
    """
    CoinGecko API ile geçmiş fiyatları getir.
    :param symbol: "bitcoin", "ethereum", "binancecoin" gibi kripto para ismi
    :param days: Kaç günlük veriyi almak istiyorsun (1, 7, 30, 90 vb.)
    :return: [(timestamp, price), ...] formatında liste veya None (Hata durumunda)
    """
    try:
        url = f"{COINGECKO_API_URL}/coins/{symbol}/market_chart"
        params = {"vs_currency": "usd", "days": days, "interval": "daily"}
        response = requests.get(url, params=params)

        if response.status_code != 200:
            print(f"⚠️ API Hatası: {response.status_code}")
            return None

        data = response.json()
        return data.get("prices", None)  # Fiyat tarihçesini döndür
    
    except Exception as e:
        print(f"⚠️ CoinGecko Geçmiş Fiyat Verisi Alınamadı: {e}")
        return None

def get_trending_coins():
    """
    CoinGecko API ile trend olan kripto paraları getir.
    :return: [Coin Adları] listesi veya None (Hata durumunda)
    """
    try:
        url = f"{COINGECKO_API_URL}/search/trending"
        response = requests.get(url)

        if response.status_code != 200:
            print(f"⚠️ API Hatası: {response.status_code}")
            return None

        data = response.json()
        trending_coins = [coin["item"]["name"] for coin in data.get("coins", [])]

        return trending_coins if trending_coins else None

    except Exception as e:
        print(f"⚠️ CoinGecko Trend Kripto Verisi Alınamadı: {e}")
        return None

# 📌 **Test Amaçlı Çalıştırma**
if __name__ == "__main__":
    # 📌 Bitcoin fiyatını al
    btc_price = get_coingecko_price("bitcoin")
    print(f"💰 Bitcoin Fiyatı: {btc_price} USD")

    # 📌 Ethereum piyasa verilerini al
    eth_market = get_market_data("ethereum")
    if eth_market:
        print(f"📊 Ethereum Piyasa Verileri: {eth_market}")

    # 📌 Son 30 günlük fiyatları al
    historical_prices = get_historical_prices("bitcoin", days=30)
    if historical_prices:
        print(f"📉 Son 30 Günlük Bitcoin Fiyatları: {historical_prices[:5]} ...")  # İlk 5 veriyi göster

    # 📌 Trend olan coinleri al
    trending = get_trending_coins()
    if trending:
        print(f"🚀 Trend Olan Coinler: {', '.join(trending)}")
