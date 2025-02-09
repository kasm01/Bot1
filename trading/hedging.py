import numpy as np
from trading.binance_futures import execute_trade
from risk_management.leverage import determine_leverage
from notifications.telegram_bot import send_telegram_message

def delta_hedging(entry_price, volatility):
    """📉 AI destekli Delta Hedge stratejisi"""
    try:
        delta = np.random.uniform(-1, 1)  
        hedge_amount = abs(delta * volatility)

        if hedge_amount <= 0:
            print("⚠️ Delta Hedge için yetersiz miktar, işlem açılmadı.")
            return

        trade_type = "SHORT" if delta > 0 else "LONG"
        execute_trade("BTCUSDT", trade_type, quantity=hedge_amount, leverage=determine_leverage(volatility))

        message = f"📉 Delta Hedge Açıldı: Delta: {delta:.4f}, Hedge Miktarı: {hedge_amount:.4f}"
        print(message)
        send_telegram_message(message)

    except Exception as e:
        print(f"⚠️ Delta Hedge Hatası: {str(e)}")

def gamma_hedging(entry_price, gamma_value):
    """📊 AI destekli Gamma Hedge stratejisi"""
    try:
        hedge_amount = abs(gamma_value) * 0.1

        if hedge_amount <= 0:
            print("⚠️ Gamma Hedge için yetersiz miktar, işlem açılmadı.")
            return

        trade_type = "SHORT" if gamma_value > 0 else "LONG"
        execute_trade("BTCUSDT", trade_type, quantity=hedge_amount, leverage=1)

        message = f"📉 Gamma Hedge Açıldı: Gamma: {gamma_value:.4f}, Hedge Miktarı: {hedge_amount:.4f}"
        print(message)
        send_telegram_message(message)

    except Exception as e:
        print(f"⚠️ Gamma Hedge Hatası: {str(e)}")

def vega_hedging(volatility, vega_value):
    """📈 AI destekli Vega Hedge stratejisi"""
    try:
        hedge_amount = abs(vega_value) * volatility * 0.05

        if hedge_amount <= 0:
            print("⚠️ Vega Hedge için yetersiz miktar, işlem açılmadı.")
            return

        execute_trade("ETHUSDT", "SHORT", quantity=hedge_amount, leverage=1)

        message = f"📉 Vega Hedge Açıldı: Vega: {vega_value:.4f}, Hedge Miktarı: {hedge_amount:.4f}"
        print(message)
        send_telegram_message(message)

    except Exception as e:
        print(f"⚠️ Vega Hedge Hatası: {str(e)}")

def correlation_hedging():
    """🔄 BTC ve ETH fiyat korelasyonunu AI ile analiz ederek hedge işlemi açar."""
    try:
        btc_price = np.random.uniform(30000, 50000)  # Simüle edilmiş fiyat verisi (Gerçek fiyat API'den alınabilir)
        eth_price = np.random.uniform(1500, 4000)
        correlation = np.corrcoef([btc_price], [eth_price])[0, 1]

        if correlation > 0.8:
            message = "🔄 BTC ve ETH yüksek korelasyonlu, hedge açılıyor."
            execute_trade("ETHUSDT", "SHORT", quantity=0.01, leverage=1)
        else:
            message = "⚖️ Korelasyon düşük, hedge açılmıyor."

        print(message)
        send_telegram_message(message)

    except Exception as e:
        print(f"⚠️ Korelasyon Hedge Hatası: {str(e)}")

def dynamic_hedging(entry_price, volatility):
    """🛡️ AI destekli dinamik hedge stratejisi"""
    try:
        if volatility > 0.03:
            hedge_amount = np.random.uniform(0.01, 0.05)

            if hedge_amount <= 0:
                print("⚠️ Dinamik Hedge için yetersiz miktar, işlem açılmadı.")
                return

            execute_trade("BTCUSDT", "SHORT", quantity=hedge_amount, leverage=determine_leverage(volatility))
            message = f"📉 Hedge Açıldı: Miktar: {hedge_amount:.4f}, Volatilite: {volatility:.4f}"
        else:
            message = "⚠️ Hedge açılmadı. Volatilite düşük."

        print(message)
        send_telegram_message(message)

    except Exception as e:
        print(f"⚠️ Dinamik Hedge Hatası: {str(e)}")

# 📌 **Test Amaçlı Çalıştırma**
if __name__ == "__main__":
    # 📌 Delta Hedge Testi
    delta_hedging(entry_price=35000, volatility=0.02)

    # 📌 Gamma Hedge Testi
    gamma_hedging(entry_price=35000, gamma_value=0.5)

    # 📌 Vega Hedge Testi
    vega_hedging(volatility=0.02, vega_value=1.5)

    # 📌 Korelasyon Hedge Testi
    correlation_hedging()

    # 📌 Dinamik Hedge Testi
    dynamic_hedging(entry_price=35000, volatility=0.04)
