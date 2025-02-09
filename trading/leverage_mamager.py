import numpy as np
from trading.binance_futures import execute_trade
from notifications.telegram_bot import send_telegram_message
from binance.client import Client
from config.config import BINANCE_API_KEY, BINANCE_API_SECRET, USE_TESTNET

# **🚀 Binance API Bağlantısı**
client = Client(BINANCE_API_KEY, BINANCE_API_SECRET, testnet=USE_TESTNET)

def dynamic_leverage(volatility):
    """📈 AI destekli dinamik kaldıraç hesaplama (1x-10x)"""
    try:
        if volatility < 0.01:
            leverage = 10  # Düşük volatilite, yüksek kaldıraç
        elif volatility < 0.03:
            leverage = 5
        elif volatility < 0.05:
            leverage = 3
        else:
            leverage = 1  # Yüksek volatilite, düşük kaldıraç

        message = f"🔧 AI Destekli Kaldıraç: {leverage}x (Volatilite: {volatility:.4f})"
        print(message)
        send_telegram_message(message)

        return leverage
    except Exception as e:
        print(f"⚠️ Kaldıraç hesaplama hatası: {str(e)}")
        return 1  # Varsayılan olarak düşük kaldıraç döndür

def adjust_leverage(symbol, volatility):
    """🔄 Binance API ile AI destekli kaldıraç ayarlama"""
    try:
        leverage = dynamic_leverage(volatility)

        # Mevcut kaldıraç değerini kontrol et
        account_info = client.futures_account()
        current_leverage = None
        for position in account_info.get("positions", []):
            if position["symbol"] == symbol:
                current_leverage = int(position["leverage"])
                break

        # Eğer kaldıraç zaten aynıysa güncelleme yapma
        if current_leverage and current_leverage == leverage:
            message = f"⚡ {symbol} için kaldıraç zaten {leverage}x, değişiklik yapılmadı."
        else:
            client.futures_change_leverage(symbol=symbol, leverage=leverage)
            message = f"✅ {symbol} için kaldıraç {leverage}x olarak güncellendi."

        print(message)
        send_telegram_message(message)

        return leverage

    except Exception as e:
        message = f"⚠️ Kaldıraç ayarlanırken hata oluştu: {str(e)}"
        print(message)
        send_telegram_message(message)
        return 1  # Varsayılan olarak düşük kaldıraç döndür

def optimize_leverage_trade(symbol, trade_type, quantity, volatility):
    """🚀 AI destekli kaldıraç optimizasyonu ile işlem aç"""
    try:
        leverage = adjust_leverage(symbol, volatility)
        execute_trade(symbol=symbol, trade_type=trade_type, quantity=quantity, leverage=leverage)

        message = (
            f"🚀 AI ile {trade_type.upper()} işlemi açıldı!\n"
            f"📌 {symbol}\n"
            f"⚡ Kaldıraç: {leverage}x\n"
            f"💰 Miktar: {quantity} BTC"
        )
        print(message)
        send_telegram_message(message)

    except Exception as e:
        error_message = f"⚠️ İşlem Başarısız! Hata: {str(e)}"
        print(error_message)
        send_telegram_message(error_message)
