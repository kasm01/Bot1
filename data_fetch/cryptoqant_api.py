import requests
from config.config import CRYPTOQUANT_API_KEY

CRYPTOQUANT_API_URL = "https://api.cryptoquant.com/v1"

def get_whale_transactions(symbol="BTC"):
    """
    CryptoQuant API ile büyük balina işlemlerini takip et.
    :param symbol: "BTC", "ETH", "BNB" gibi kripto para simgeleri
    """
    endpoint = f"{CRYPTOQUANT_API_URL}/whale-transactions?symbol={symbol}"
    headers = {"Authorization": f"Bearer {CRYPTOQUANT_API_KEY}"}

    response = requests.get(endpoint, headers=headers).json()
    
    if "data" in response:
        return response["data"]
    else:
        return {"error": "Veri çekilemedi, API anahtarınızı kontrol edin."}

def get_exchange_flows(symbol="BTC"):
    """
    CryptoQuant API ile borsalara giriş-çıkışları takip et.
    :param symbol: "BTC", "ETH", "BNB" gibi kripto para simgeleri
    """
    endpoint = f"{CRYPTOQUANT_API_URL}/exchange-flows?symbol={symbol}"
    headers = {"Authorization": f"Bearer {CRYPTOQUANT_API_KEY}"}

    response = requests.get(endpoint, headers=headers).json()
    
    if "data" in response:
        return response["data"]
    else:
        return {"error": "Veri çekilemedi, API anahtarınızı kontrol edin."}

def get_onchain_indicators(symbol="BTC"):
    """
    CryptoQuant API ile on-chain metrikleri al.
    :param symbol: "BTC", "ETH", "BNB" gibi kripto para simgeleri
    """
    endpoint = f"{CRYPTOQUANT_API_URL}/onchain-indicators?symbol={symbol}"
    headers = {"Authorization": f"Bearer {CRYPTOQUANT_API_KEY}"}

    response = requests.get(endpoint, headers=headers).json()
    
    if "data" in response:
        return response["data"]
    else:
        return {"error": "Veri çekilemedi, API anahtarınızı kontrol edin."}
