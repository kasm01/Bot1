import requests
import ccxt
from binance.client import Client
from config.config import BINANCE_API_KEY, BINANCE_API_SECRET

# Binance Testnet Bağlantısı
client = Client(BINANCE_API_KEY, BINANCE_API_SECRET, testnet=True)

# **📌 Binance API'den OHLCV Verisi Çek**
def get_binance_ohlcv(symbol="BTCUSDT", interval="1h", limit=100):
    """
    Binance API'den OHLCV (Açılış, Yüksek, Düşük, Kapanış, Hacim) verisi al.
    """
    API_URL = f"https://api.binance.com/api/v3/klines"
    params = {"symbol": symbol, "interval": interval, "limit": limit}
    response = requests.get(API_URL, params=params).json()
    
    return [{"timestamp": candle[0], "open": float(candle[1]), "high": float(candle[2]), 
             "low": float(candle[3]), "close": float(candle[4]), "volume": float(candle[5])} 
            for candle in response]

# **📌 Binance Futures'ta İşlem Aç**
def execute_trade(symbol, trade_type, quantity, leverage):
    """
    Binance Futures'ta işlem açar.
    :param symbol: İşlem çifti (BTCUSDT, ETHUSDT vb.)
    :param trade_type: "LONG" veya "SHORT"
    :param quantity: İşlem miktarı
    :param leverage: Kaldıraç oranı (1x - 10x arası AI destekli hesaplanır)
    """
    client.futures_change_leverage(symbol=symbol, leverage=leverage)
    side = "BUY" if trade_type == "LONG" else "SELL"

    order = client.futures_create_order(
        symbol=symbol,
        side=side,
        type="MARKET",
        quantity=quantity
    )

    print(f"🚀 {trade_type} Pozisyon Açıldı: {symbol}, Miktar: {quantity}, Kaldıraç: {leverage}x")
    return order

# **📌 Binance API'den Mevcut Açık Pozisyonları Al**
def get_open_positions():
    """
    Binance Futures'taki açık pozisyonları getirir.
    """
    positions = client.futures_account()["positions"]
    open_positions = [pos for pos in positions if float(pos["positionAmt"]) != 0]
    
    return open_positions

# **📌 Binance API'den Gerçek Zamanlı Piyasa Fiyatını Al**
def get_binance_price(symbol="BTCUSDT"):
    """
    Binance API'den gerçek zamanlı piyasa fiyatını alır.
    """
    ticker = client.futures_symbol_ticker(symbol=symbol)
    return float(ticker["price"])

# **📌 Binance API'den Kaldıraç Değişimi**
def change_leverage(symbol, leverage):
    """
    Binance Futures kaldıraç oranını değiştirir.
    """
    client.futures_change_leverage(symbol=symbol, leverage=leverage)
    print(f"🔧 {symbol} için Kaldıraç Değiştirildi: {leverage}x")

# **📌 Binance API'den Likidite Derinliği Çek**
def get_market_depth(symbol="BTCUSDT", limit=10):
    """
    Binance API'den emir defteri (order book) likidite derinliğini çeker.
    """
    depth = client.futures_order_book(symbol=symbol, limit=limit)
    return {"bids": depth["bids"], "asks": depth["asks"]}

# **📌 Binance API'den Fonlama Oranlarını Al**
def get_funding_rate(symbol="BTCUSDT"):
    """
    Binance API'den fonlama oranlarını alır.
    """
    funding_info = client.futures_funding_rate(symbol=symbol, limit=1)
    return float(funding_info[0]["fundingRate"])
