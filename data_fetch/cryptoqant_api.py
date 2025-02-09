import requests
from config.config import CRYPTOQUANT_API_KEY

CRYPTOQUANT_API_URL = "https://api.cryptoquant.com/v1"

def get_cryptoquant_data(endpoint, symbol="BTC"):
    """
    CryptoQuant API'den veri çekme fonksiyonu (Genelleştirilmiş).
    :param endpoint: API uç noktası (ör. "whale-transactions")
    :param symbol: Kripto para simgesi ("BTC", "ETH", "BNB" vb.)
    :return: API yanıtı (dict) veya None (hata durumunda)
    """
    if not CRYPTOQUANT_API_KEY:
        print("⚠️ API Anahtarı Eksik! Lütfen .env dosyanızı kontrol edin.")
        return None

    url = f"{CRYPTOQUANT_API_URL}/{endpoint}?symbol={symbol}"
    headers = {"Authorization": f"Bearer {CRYPTOQUANT_API_KEY}"}

    try:
        response = requests.get(url, headers=headers)

        if response.status_code != 200:
            print(f"⚠️ API Hatası: {response.status_code} - {response.text}")
            return None

        data = response.json()
        return data.get("data", None)

    except requests.exceptions.RequestException as e:
        print(f"⚠️ API Bağlantı Hatası: {e}")
        return None

# **📌 CryptoQuant API ile Büyük Balina İşlemlerini Takip Et**
def get_whale_transactions(symbol="BTC"):
    """
    CryptoQuant API ile büyük balina işlemlerini takip et.
    """
    data = get_cryptoquant_data("whale-transactions", symbol)
    return data if data else "⚠️ Veri çekilemedi, API anahtarınızı kontrol edin."

# **📌 CryptoQuant API ile Borsalara Giriş-Çıkışları Takip Et**
def get_exchange_flows(symbol="BTC"):
    """
    CryptoQuant API ile borsalara giriş-çıkışları takip et.
    """
    data = get_cryptoquant_data("exchange-flows", symbol)
    return data if data else "⚠️ Veri çekilemedi, API anahtarınızı kontrol edin."

# **📌 CryptoQuant API ile On-Chain Metrikleri Al**
def get_onchain_indicators(symbol="BTC"):
    """
    CryptoQuant API ile on-chain metrikleri al.
    """
    data = get_cryptoquant_data("onchain-indicators", symbol)
    return data if data else "⚠️ Veri çekilemedi, API anahtarınızı kontrol edin."

# 📌 **Test Amaçlı Çalıştırma**
if __name__ == "__main__":
    # 📌 Balina İşlemlerini Al
    whale_data = get_whale_transactions("BTC")
    print(f"🐋 Balina İşlemleri: {whale_data}")

    # 📌 Borsa Giriş-Çıkış Verilerini Al
    exchange_data = get_exchange_flows("BTC")
    print(f"🏦 Borsa Giriş-Çıkış Verileri: {exchange_data}")

    # 📌 On-Chain Metrikleri Al
    onchain_data = get_onchain_indicators("BTC")
    print(f"🔗 On-Chain Metrikler: {onchain_data}")
