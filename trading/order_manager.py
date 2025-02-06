from binance.client import Client
from config.config import BINANCE_API_KEY, BINANCE_API_SECRET
from risk_management.leverage_manager import adjust_leverage
from risk_management.stop_loss import calculate_dynamic_stop_loss, calculate_dynamic_take_profit
from notifications.telegram_bot import send_telegram_message

# Binance API bağlantısı
client = Client(BINANCE_API_KEY, BINANCE_API_SECRET, testnet=True)

def place_market_order(symbol, trade_type, quantity, volatility):
    """📈 AI destekli market order (anlık alım-satım) işlemi"""
    leverage = adjust_leverage(symbol, volatility)
    side = "BUY" if trade_type == "LONG" else "SELL"

    try:
        order = client.futures_create_order(
            symbol=symbol,
            side=side,
            type="MARKET",
            quantity=quantity
        )

        message = f"🚀 Market {trade_type} işlemi açıldı! {symbol} | Miktar: {quantity} | Kaldıraç: {leverage}x"
        print(message)
        send_telegram_message(message)
        
        return order
    except Exception as e:
        error_message = f"⚠️ Market Order Hatası: {str(e)}"
        print(error_message)
        send_telegram_message(error_message)

def place_limit_order(symbol, trade_type, quantity, limit_price):
    """📊 AI destekli limit emir (belirlenen fiyattan işlem açma)"""
    side = "BUY" if trade_type == "LONG" else "SELL"

    try:
        order = client.futures_create_order(
            symbol=symbol,
            side=side,
            type="LIMIT",
            price=limit_price,
            quantity=quantity,
            timeInForce="GTC"
        )

        message = f"🟢 Limit {trade_type} emri girildi! {symbol} | Fiyat: {limit_price} | Miktar: {quantity}"
        print(message)
        send_telegram_message(message)

        return order
    except Exception as e:
        error_message = f"⚠️ Limit Order Hatası: {str(e)}"
        print(error_message)
        send_telegram_message(error_message)

def place_trailing_stop_order(symbol, trade_type, quantity, activation_price, callback_rate):
    """🔄 AI destekli trailing stop-loss (otomatik stop seviyesi)"""
    side = "SELL" if trade_type == "LONG" else "BUY"

    try:
        order = client.futures_create_order(
            symbol=symbol,
            side=side,
            type="TRAILING_STOP_MARKET",
            activationPrice=activation_price,
            callbackRate=callback_rate,
            quantity=quantity
        )

        message = f"🔄 Trailing Stop {trade_type} ayarlandı! {symbol} | Aktivasyon: {activation_price} | Callback: {callback_rate}%"
        print(message)
        send_telegram_message(message)

        return order
    except Exception as e:
        error_message = f"⚠️ Trailing Stop Order Hatası: {str(e)}"
        print(error_message)
        send_telegram_message(error_message)

def place_stop_loss_order(symbol, trade_type, quantity, entry_price, volatility):
    """🛑 AI destekli stop-loss işlemi (dinamik)"""
    stop_loss_price = calculate_dynamic_stop_loss(entry_price, volatility)
    side = "SELL" if trade_type == "LONG" else "BUY"

    try:
        order = client.futures_create_order(
            symbol=symbol,
            side=side,
            type="STOP_MARKET",
            stopPrice=stop_loss_price,
            quantity=quantity
        )

        message = f"🛑 Stop-Loss {trade_type} ayarlandı! {symbol} | Stop-Loss: {stop_loss_price}"
        print(message)
        send_telegram_message(message)

        return order
    except Exception as e:
        error_message = f"⚠️ Stop-Loss Order Hatası: {str(e)}"
        print(error_message)
        send_telegram_message(error_message)

def place_take_profit_order(symbol, trade_type, quantity, entry_price, volatility):
    """🎯 AI destekli take-profit işlemi (dinamik)"""
    take_profit_price = calculate_dynamic_take_profit(entry_price, volatility)
    side = "SELL" if trade_type == "LONG" else "BUY"

    try:
        order = client.futures_create_order(
            symbol=symbol,
            side=side,
            type="TAKE_PROFIT_MARKET",
            stopPrice=take_profit_price,
            quantity=quantity
        )

        message = f"🎯 Take-Profit {trade_type} ayarlandı! {symbol} | Take-Profit: {take_profit_price}"
        print(message)
        send_telegram_message(message)

        return order
    except Exception as e:
        error_message = f"⚠️ Take-Profit Order Hatası: {str(e)}"
        print(error_message)
        send_telegram_message(error_message)
