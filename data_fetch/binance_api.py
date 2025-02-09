import requests
import ccxt
from binance.client import Client
from config.config import BINANCE_API_KEY, BINANCE_API_SECRET, BINANCE_TESTNET

# 📌 **Binance API Bağlantısını Kur**
binance_base_url = "https://testnet.binancefuture.com" if BINANCE_TESTNET else "https://fapi.binance.com"
client = Client(BINANCE_API_KEY, BINANCE_API_SECRET, testnet=BINANCE_TESTNET)

# **📌 Binance API'den OHLCV Verisi Çek**
def get_binance_ohlcv(symbol="BTCUSDT", interval="1h", limit=100):
    """
    Binance API'den OHLCV (Açılış, Yüksek, Düşük, Kapanış, Hacim) verisi al.
    """
    try:
        url = f"{binance_base_url}/fapi/v1/klines"
        params = {"symbol": symbol, "interval": interval, "limit": limit}
        response = requests.get(url, params=params)
        data = response.json()

        if "code" in data:  # API hatası varsa
            print(f"⚠️ Binance OHLCV Hatası: {data}")
            return None

        return [{"timestamp": candle[0], "open": float(candle[1]), "high": float(candle[2]), 
                 "low": float(candle[3]), "close": float(candle[4]), "volume": float(candle[5])} 
                for candle in data]
    
    except Exception as e:
        print(f"⚠️ Binance OHLCV Verisi Alınamadı: {e}")
        return None

# **📌 Binance Futures'ta İşlem Aç**
def execute_trade(symbol, trade_type, quantity, leverage):
    """
    Binance Futures'ta işlem açar.
    """
    try:
        client.futures_change_leverage(symbol=symbol, leverage=leverage)
        side = "BUY" if trade_type.upper() == "LONG" else "SELL"

        order = client.futures_create_order(
            symbol=symbol,
            side=side,
            type="MARKET",
            quantity=quantity
        )

        print(f"🚀 {trade_type} Pozisyon Açıldı: {symbol}, Miktar: {quantity}, Kaldıraç: {leverage}x")
        return order
    
    except Exception as e:
        print(f"⚠️ İşlem Hatası: {e}")
        return None

# **📌 Binance API'den Mevcut Açık Pozisyonları Al**
def get_open_positions():
    """
    Binance Futures'taki açık pozisyonları getirir.
    """
    try:
        positions = client.futures_account().get("positions", [])
        open_positions = [pos for pos in positions if float(pos["positionAmt"]) != 0]
        return open_positions
    
    except Exception as e:
        print(f"⚠️ Açık Pozisyonlar Alınamadı: {e}")
        return None

# **📌 Binance API'den Gerçek Zamanlı Piyasa Fiyatını Al**
def get_binance_price(symbol="BTCUSDT"):
    """
    Binance API'den gerçek zamanlı piyasa fiyatını alır.
    """
    try:
        ticker = client.futures_symbol_ticker(symbol=symbol)
        return float(ticker.get("price", 0.0))  # Hata durumunda 0.0 döndür
    
    except Exception as e:
        print(f"⚠️ Binance Fiyat Verisi Alınamadı: {e}")
        return None

# **📌 Binance API'den Kaldıraç Değişimi**
def change_leverage(symbol, leverage):
    """
    Binance Futures kaldıraç oranını değiştirir.
    """
    try:
        client.futures_change_leverage(symbol=symbol, leverage=leverage)
        print(f"🔧 {symbol} için Kaldıraç Değiştirildi: {leverage}x")
    
    except Exception as e:
        print(f"⚠️ Kaldıraç Değiştirme Hatası: {e}")

# **📌 Binance API'den Likidite Derinliği Çek**
def get_market_depth(symbol="BTCUSDT", limit=10):
    """
    Binance API'den emir defteri (order book) likidite derinliğini çeker.
    """
    try:
        depth = client.futures_order_book(symbol=symbol, limit=limit)
        return {"bids": depth.get("bids", []), "asks": depth.get("asks", [])}
    
    except Exception as e:
        print(f"⚠️ Piyasa Derinliği Alınamadı: {e}")
        return None

# **📌 Binance API'den Fonlama Oranlarını Al**
def get_funding_rate(symbol="BTCUSDT"):
    """
    Binance API'den fonlama oranlarını alır.
    """
    try:
        funding_info = client.futures_funding_rate(symbol=symbol, limit=1)
        return float(funding_info[0].get("fundingRate", 0.0))  # Hata durumunda 0.0 döndür
    
    except Exception as e:
        print(f"⚠️ Fonlama Oranı Alınamadı: {e}")
        return None

# 📌 **Test Amaçlı Çalıştırma**
if __name__ == "__main__":
    # 📌 Bitcoin fiyatını al
    btc_price = get_binance_price("BTCUSDT")
    print(f"💰 Bitcoin Fiyatı: {btc_price} USD")

    # 📌 OHLCV Verilerini al
    ohlcv_data = get_binance_ohlcv("BTCUSDT", "1h", 10)
    if ohlcv_data:
        print(f"📊 OHLCV İlk 3 Veri: {ohlcv_data[:3]}")

    # 📌 Açık pozisyonları al
    positions = get_open_positions()
    if positions:
        print(f"📈 Açık Pozisyonlar: {positions}")

    # 📌 Piyasa derinliği al
    depth = get_market_depth("BTCUSDT")
    if depth:
        print(f"📉 En İyi 3 Alım: {depth['bids'][:3]} | En İyi 3 Satış: {depth['asks'][:3]}")

    # 📌 Fonlama oranı al
    funding_rate = get_funding_rate("BTCUSDT")
    print(f"🔄 BTC Fonlama Oranı: {funding_rate * 100:.4f}%")
