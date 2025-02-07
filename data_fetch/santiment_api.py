import requests
from config.config import SANTIMENT_API_KEY

SANTIMENT_API_URL = "https://api.santiment.net/graphql"

def get_whale_transactions(symbol="bitcoin"):
    """
    Santiment API ile büyük kripto işlemlerini takip et.
    :param symbol: "bitcoin", "ethereum", "binancecoin" gibi kripto para ismi
    """
    query = {
        "query": f"""
        {{
          whaleTransactions(
            slug: "{symbol}"
            from: "utc_now-7d"
            to: "utc_now"
            limit: 5
          ) {{
            time
            transactionVolume
          }}
        }}
        """
    }
    headers = {"Authorization": f"Bearer {SANTIMENT_API_KEY}"}
    response = requests.post(SANTIMENT_API_URL, json=query, headers=headers).json()
    
    return response["data"]["whaleTransactions"]

def get_social_sentiment(symbol="bitcoin"):
    """
    Santiment API ile sosyal medya duyarlılığını ölç.
    :param symbol: "bitcoin", "ethereum", "binancecoin" gibi kripto para ismi
    """
    query = {
        "query": f"""
        {{
          sentimentVolumeConsumed(
            slug: "{symbol}"
            from: "utc_now-7d"
            to: "utc_now"
            interval: "1d"
          ) {{
            datetime
            sentimentPositive
            sentimentNegative
          }}
        }}
        """
    }
    headers = {"Authorization": f"Bearer {SANTIMENT_API_KEY}"}
    response = requests.post(SANTIMENT_API_URL, json=query, headers=headers).json()
    
    return response["data"]["sentimentVolumeConsumed"]

def get_exchange_flows(symbol="bitcoin"):
    """
    Santiment API ile borsalara giriş-çıkış verilerini takip et.
    :param symbol: "bitcoin", "ethereum", "binancecoin" gibi kripto para ismi
    """
    query = {
        "query": f"""
        {{
          exchangeFundsFlow(
            slug: "{symbol}"
            from: "utc_now-7d"
            to: "utc_now"
            interval: "1d"
          ) {{
            datetime
            exchangeInflow
            exchangeOutflow
          }}
        }}
        """
    }
    headers = {"Authorization": f"Bearer {SANTIMENT_API_KEY}"}
    response = requests.post(SANTIMENT_API_URL, json=query, headers=headers).json()
    
    return response["data"]["exchangeFundsFlow"]
