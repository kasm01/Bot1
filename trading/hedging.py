import numpy as np
from trading.binance_futures import execute_trade
from risk_management.leverage import determine_leverage
from notifications.telegram_bot import send_telegram_message

def delta_hedging(entry_price, volatility):
    """📉 AI destekli Delta Hedge stratejisi"""
    delta = np.random.uniform(-1, 1)  
    hedge_amount = abs(delta * volatility)

    if delta > 0:
        execute_trade("BTCUSDT", "SHORT", quantity=hedge_amount)
    else:
        execute_trade("BTCUSDT", "LONG", quantity=hedge_amount)

    message = f"📉 Delta Hedge Açıldı: Delta: {delta}, Hedge Miktarı: {hedge_amount}"
    print(message)
    send_telegram_message(message)

def gamma_hedging(entry_price, gamma_value):
    """📊 AI destekli Gamma Hedge stratejisi"""
    hedge_amount = abs(gamma_value) * 0.1
    if gamma_value > 0:
        execute_trade("BTCUSDT", "SHORT", quantity=hedge_amount)
    else:
        execute_trade("BTCUSDT", "LONG", quantity=hedge_amount)

    message = f"📉 Gamma Hedge Açıldı: Gamma: {gamma_value}, Hedge Miktarı: {hedge_amount}"
    print(message)
    send_telegram_message(message)

def vega_hedging(volatility, vega_value):
    """📈 AI destekli Vega Hedge stratejisi"""
    hedge_amount = abs(vega_value) * volatility * 0.05
    execute_trade("ETHUSDT", "SHORT", quantity=hedge_amount)

    message = f"📉 Vega Hedge Açıldı: Vega: {vega_value}, Hedge Miktarı: {hedge_amount}"
    print(message)
    send_telegram_message(message)

def correlation_hedging():
    """🔄 BTC ve ETH fiyat korelasyonunu AI ile analiz ederek hedge işlemi açar."""
    btc_price = np.random.uniform(30000, 50000)  # Simüle edilmiş fiyat verisi
    eth_price = np.random.uniform(1500, 4000)
    correlation = np.corrcoef([btc_price], [eth_price])[0, 1]

    if correlation > 0.8:
        message = "🔄 BTC ve ETH yüksek korelasyonlu, hedge açılıyor."
        execute_trade("ETHUSDT", "SHORT", quantity=0.01)
    else:
        message = "⚖️ Korelasyon düşük, hedge açılmıyor."

    print(message)
    send_telegram_message(message)

def dynamic_hedging(entry_price, volatility):
    """🛡️ AI destekli dinamik hedge stratejisi"""
    if volatility > 0.03:  
        hedge_amount = np.random.uniform(0.01, 0.05)
        execute_trade("BTCUSDT", "SHORT", quantity=hedge_amount)
        message = f"📉 Hedge Açıldı: Miktar: {hedge_amount}, Volatilite: {volatility}"
    else:
        message = "⚠️ Hedge açılmadı. Volatilite düşük."

    print(message)
    send_telegram_message(message)
