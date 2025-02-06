import numpy as np
from trading.binance_futures import execute_trade
from notifications.telegram_bot import send_telegram_message

def dynamic_leverage(volatility):
    """📈 AI destekli dinamik kaldıraç hesaplama (1x-10x)"""
    if volatility < 0.01:
        leverage = 10  # Düşük volatilite, yüksek kaldıraç
    elif volatility < 0.03:
        leverage = 5
    elif volatility < 0.05:
        leverage = 3
    else:
        leverage = 1  # Yüksek volatilite, düşük kaldıraç
    
    message = f"🔧 AI Destekli Kaldıraç: {leverage}x (Volatilite: {volatility})"
    print(message)
    send_telegram_message(message)
    
    return leverage

def adjust_leverage(symbol, volatility):
    """🔄 Binance API ile AI destekli kaldıraç ayarlama"""
    leverage = dynamic_leverage(volatility)

    try:
        from binance.client import Client
        from config.config import BINANCE_API_KEY, BINANCE_API_SECRET

        client = Client(BINANCE_API_KEY, BINANCE_API_SECRET, testnet=True)
        client.futures_change_leverage(symbol=symbol, leverage=leverage)

        message = f"✅ {symbol} için kaldıraç {leverage}x olarak güncellendi."
    except Exception as e:
        message = f"⚠️ Kaldıraç ayarlanırken hata oluştu: {str(e)}"

    print(message)
    send_telegram_message(message)
    
    return leverage

def optimize_leverage_trade(symbol, trade_type, quantity, volatility):
    """🚀 AI destekli kaldıraç optimizasyonu ile işlem aç"""
    leverage = adjust_leverage(symbol, volatility)
    execute_trade(symbol=symbol, trade_type=trade_type, quantity=quantity, leverage=leverage)

    message = f"🚀 AI ile {trade_type} işlemi açıldı! {symbol} | Kaldıraç: {leverage}x"
    print(message)
    send_telegram_message(message)
