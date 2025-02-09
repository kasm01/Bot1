from binance.client import Client
from config.config import BINANCE_API_KEY, BINANCE_API_SECRET, USE_TESTNET
from risk_management.stop_loss import calculate_stop_loss, calculate_take_profit
from trading.leverage_manager import determine_leverage
from notifications.telegram_bot import send_telegram_message

# **🚀 Binance API Bağlantısı**
client = Client(BINANCE_API_KEY, BINANCE_API_SECRET, testnet=USE_TESTNET)

def execute_trade(symbol, trade_type, quantity):
    """Binance Futures'ta işlem açar ve stop-loss/take-profit belirler."""
    try:
        if quantity <= 0:
            raise ValueError("⚠️ Hata: İşlem miktarı sıfır veya negatif olamaz.")

        # **📌 AI Destekli Kaldıraç Yönetimi**
        leverage = determine_leverage()
        client.futures_change_leverage(symbol=symbol, leverage=leverage)

        # **📌 Piyasa Fiyatı Alma**
        mark_price_info = client.futures_mark_price(symbol=symbol)
        entry_price = float(mark_price_info["markPrice"]) if mark_price_info else None

        if entry_price is None:
            raise ValueError(f"⚠️ {symbol} için piyasa fiyatı alınamadı!")

        # **📌 Stop-Loss & Take-Profit Hesaplama**
        stop_loss = calculate_stop_loss(entry_price)
        take_profit = calculate_take_profit(entry_price)

        if stop_loss is None or take_profit is None:
            raise ValueError("⚠️ Stop-loss veya Take-profit hesaplanamadı!")

        # **📌 İşlem Tipini Belirleme**
        side = "BUY" if trade_type.upper() == "LONG" else "SELL"

        # **📌 Market Order Aç**
        order = client.futures_create_order(
            symbol=symbol,
            side=side,
            type="MARKET",
            quantity=quantity
        )

        # **📌 Stop-Loss Order Aç**
        client.futures_create_order(
            symbol=symbol,
            side="SELL" if trade_type.upper() == "LONG" else "BUY",
            type="STOP_MARKET",
            stopPrice=stop_loss,
            quantity=quantity
        )

        # **📌 Take-Profit Order Aç**
        client.futures_create_order(
            symbol=symbol,
            side="SELL" if trade_type.upper() == "LONG" else "BUY",
            type="TAKE_PROFIT_MARKET",
            stopPrice=take_profit,
            quantity=quantity
        )

        message = (
            f"🚀 {trade_type.upper()} Pozisyon Açıldı: {symbol}\n"
            f"📌 Miktar: {quantity} BTC\n"
            f"⚡ Kaldıraç: {leverage}x\n"
            f"💲 Giriş Fiyatı: {entry_price} USDT\n"
            f"🛑 Stop-Loss: {stop_loss} USDT\n"
            f"🎯 Take-Profit: {take_profit} USDT"
        )
        print(message)
        send_telegram_message(message)

        return order
    except Exception as e:
        error_message = f"⚠️ İşlem Başarısız! Hata: {str(e)}"
        print(error_message)
        send_telegram_message(error_message)
        return None

def close_position(symbol):
    """Açık pozisyonları kapatır."""
    try:
        positions = client.futures_position_information()
        for pos in positions:
            if pos["symbol"] == symbol and float(pos["positionAmt"]) != 0:
                client.futures_create_order(
                    symbol=symbol,
                    side="SELL" if float(pos["positionAmt"]) > 0 else "BUY",
                    type="MARKET",
                    quantity=abs(float(pos["positionAmt"]))
                )
                send_telegram_message(f"🔴 {symbol} Pozisyon Kapatıldı!")
                return
        print(f"⚠️ {symbol} için açık pozisyon bulunamadı.")
    except Exception as e:
        send_telegram_message(f"⚠️ Pozisyon kapatma başarısız: {str(e)}")

def place_limit_order(symbol, trade_type, quantity, limit_price):
    """Limit emir oluşturur."""
    try:
        if quantity <= 0 or limit_price <= 0:
            raise ValueError("⚠️ Hata: İşlem miktarı veya limit fiyatı negatif olamaz.")

        side = "BUY" if trade_type.upper() == "LONG" else "SELL"
        order = client.futures_create_order(
            symbol=symbol,
            side=side,
            type="LIMIT",
            price=limit_price,
            quantity=quantity,
            timeInForce="GTC"
        )
        send_telegram_message(f"📌 Limit Order Açıldı: {symbol}, Fiyat: {limit_price} USDT")
        return order
    except Exception as e:
        send_telegram_message(f"⚠️ Limit Order Hatası: {str(e)}")

def place_trailing_stop_order(symbol, trade_type, quantity, callback_rate=1.0):
    """AI Destekli Trailing Stop Mekanizması."""
    try:
        if quantity <= 0 or callback_rate <= 0:
            raise ValueError("⚠️ Hata: İşlem miktarı veya callback oranı negatif olamaz.")

        side = "SELL" if trade_type.upper() == "LONG" else "BUY"
        order = client.futures_create_order(
            symbol=symbol,
            side=side,
            type="TRAILING_STOP_MARKET",
            quantity=quantity,
            callbackRate=callback_rate
        )
        send_telegram_message(f"🚀 Trailing Stop Açıldı: {symbol}, Callback Rate: {callback_rate}%")
        return order
    except Exception as e:
        send_telegram_message(f"⚠️ Trailing Stop Hatası: {str(e)}")
