import requests
import datetime
from config.config import SANTIMENT_API_KEY

SANTIMENT_API_URL = "https://api.santiment.net/graphql"

def get_santiment_data(query):
    """
    Santiment API'den veri çeken genel fonksiyon.
    :param query: GraphQL sorgusu (JSON formatında)
    :return: API yanıtı veya hata mesajı
    """
    if not SANTIMENT_API_KEY:
        print("⚠️ API Anahtarı Eksik! Lütfen .env dosyanızı kontrol edin.")
        return None

    headers = {"Authorization": f"Bearer {SANTIMENT_API_KEY}"}

    try:
        response = requests.post(SANTIMENT_API_URL, json=query, headers=headers)

        if response.status_code != 200:
            print(f"⚠️ API Hatası: {response.status_code} - {response.text}")
            return None

        data = response.json()
        return data.get("data", None)

    except requests.exceptions.RequestException as e:
        print(f"⚠️ API Bağlantı Hatası: {e}")
        return None

# **📌 Santiment API ile Büyük Kripto İşlemlerini Takip Et**
def get_whale_transactions(symbol="bitcoin"):
    """
    Santiment API ile büyük kripto işlemlerini takip et.
    """
    from_date = (datetime.datetime.utcnow() - datetime.timedelta(days=7)).isoformat()
    to_date = datetime.datetime.utcnow().isoformat()

    query = {
        "query": f"""
        {{
          whaleTransactions(
            slug: "{symbol}"
            from: "{from_date}"
            to: "{to_date}"
            limit: 5
          ) {{
            time
            transactionVolume
          }}
        }}
        """
    }

    data = get_santiment_data(query)
    return data.get("whaleTransactions", "⚠️ Veri çekilemedi, API anahtarınızı kontrol edin.") if data else None

# **📌 Santiment API ile Sosyal Medya Duyarlılığını Ölç**
def get_social_sentiment(symbol="bitcoin"):
    """
    Santiment API ile sosyal medya duyarlılığını ölç.
    """
    from_date = (datetime.datetime.utcnow() - datetime.timedelta(days=7)).isoformat()
    to_date = datetime.datetime.utcnow().isoformat()

    query = {
        "query": f"""
        {{
          sentimentVolumeConsumed(
            slug: "{symbol}"
            from: "{from_date}"
            to: "{to_date}"
            interval: "1d"
          ) {{
            datetime
            sentimentPositive
            sentimentNegative
          }}
        }}
        """
    }

    data = get_santiment_data(query)
    return data.get("sentimentVolumeConsumed", "⚠️ Veri çekilemedi, API anahtarınızı kontrol edin.") if data else None

# **📌 Santiment API ile Borsalara Giriş-Çıkış Verilerini Takip Et**
def get_exchange_flows(symbol="bitcoin"):
    """
    Santiment API ile borsalara giriş-çıkış verilerini takip et.
    """
    from_date = (datetime.datetime.utcnow() - datetime.timedelta(days=7)).isoformat()
    to_date = datetime.datetime.utcnow().isoformat()

    query = {
        "query": f"""
        {{
          exchangeFundsFlow(
            slug: "{symbol}"
            from: "{from_date}"
            to: "{to_date}"
            interval: "1d"
          ) {{
            datetime
            exchangeInflow
            exchangeOutflow
          }}
        }}
        """
    }

    data = get_santiment_data(query)
    return data.get("exchangeFundsFlow", "⚠️ Veri çekilemedi, API anahtarınızı kontrol edin.") if data else None

# 📌 **Test Amaçlı Çalıştırma**
if __name__ == "__main__":
    # 📌 Balina İşlemlerini Al
    whale_data = get_whale_transactions("bitcoin")
    print(f"🐋 Balina İşlemleri: {whale_data}")

    # 📌 Sosyal Medya Duyarlılığı Al
    sentiment_data = get_social_sentiment("bitcoin")
    print(f"💬 Sosyal Duyarlılık: {sentiment_data}")

    # 📌 Borsa Giriş-Çıkış Verilerini Al
    exchange_data = get_exchange_flows("bitcoin")
    print(f"🏦 Borsa Giriş-Çıkış Verileri: {exchange_data}")
