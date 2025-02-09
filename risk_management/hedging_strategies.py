import numpy as np
from trading.binance_futures import execute_trade, get_binance_price
from risk_management.leverage_manager import dynamic_leverage

def delta_hedging(entry_price, volatility):
    """
    AI destekli Delta Hedge hesaplama.
    
    :param entry_price: İşlem giriş fiyatı
    :param volatility: Piyasa volatilitesi
    """
    try:
        delta = np.random.uniform(-1, 1)  # Simüle edilen delta değeri
        hedge_amount = abs(delta * volatility)

        if hedge_amount <= 0:
            print("⚠️ Delta Hedge için yetersiz miktar, işlem açılmadı.")
            return

        trade_type = "SHORT" if delta > 0 else "LONG"
        execute_trade("BTCUSDT", trade_type, quantity=hedge_amount, leverage=dynamic_leverage(volatility))

        print(f"📉 Delta Hedge Açıldı: Delta: {delta:.4f}, Miktar: {hedge_amount:.4f}")

    except Exception as e:
        print(f"⚠️ Delta Hedge Hatası: {str(e)}")


def gamma_hedging(entry_price, gamma_value):
    """
    Gamma Hedge stratejisi.
    
    :param entry_price: İşlem giriş fiyatı
    :param gamma_value: Gamma değeri
    """
    try:
        hedge_amount = abs(gamma_value) * 0.1

        if hedge_amount <= 0:
            print("⚠️ Gamma Hedge için yetersiz miktar, işlem açılmadı.")
            return

        trade_type = "SHORT" if gamma_value > 0 else "LONG"
        execute_trade("BTCUSDT", trade_type, quantity=hedge_amount, leverage=1)

        print(f"📉 Gamma Hedge Açıldı: Gamma: {gamma_value:.4f}, Miktar: {hedge_amount:.4f}")

    except Exception as e:
        print(f"⚠️ Gamma Hedge Hatası: {str(e)}")


def vega_hedging(volatility, vega_value):
    """
    Vega Hedge stratejisi.
    
    :param volatility: Piyasa volatilitesi
    :param vega_value: Vega değeri
    """
    try:
        hedge_amount = abs(vega_value) * volatility * 0.05

        if hedge_amount <= 0:
            print("⚠️ Vega Hedge için yetersiz miktar, işlem açılmadı.")
            return

        execute_trade("ETHUSDT", "SHORT", quantity=hedge_amount, leverage=1)

        print(f"📉 Vega Hedge Açıldı: Vega: {vega_value:.4f}, Miktar: {hedge_amount:.4f}")

    except Exception as e:
        print(f"⚠️ Vega Hedge Hatası: {str(e)}")


def correlation_hedging():
    """
    BTC-ETH fiyat korelasyonuna göre hedge stratejisi.
    """
    try:
        btc_price = get_binance_price("BTCUSDT")
        eth_price = get_binance_price("ETHUSDT")

        if btc_price is None or eth_price is None:
            print("⚠️ Fiyat verileri alınamadı, korelasyon hedge uygulanamadı.")
            return

        correlation = np.corrcoef([btc_price], [eth_price])[0, 1]

        if correlation > 0.8:
            print("🔄 BTC ve ETH yüksek korelasyonlu, hedge açılıyor.")
            execute_trade("ETHUSDT", "SHORT", quantity=0.01, leverage=1)
        else:
            print("⚖️ Korelasyon düşük, hedge açılmadı.")

    except Exception as e:
        print(f"⚠️ Korelasyon Hedge Hatası: {str(e)}")


def market_neutral_hedging():
    """
    AI destekli Market Neutral hedge stratejisi.
    """
    try:
        hedge_amount = 0.01  # Varsayılan miktar

        execute_trade("BTCUSDT", "LONG", quantity=hedge_amount, leverage=1)
        execute_trade("BTCUSDT", "SHORT", quantity=hedge_amount, leverage=1)

        print("⚖️ Market Neutral Hedge Stratejisi Uygulandı.")

    except Exception as e:
        print(f"⚠️ Market Neutral Hedge Hatası: {str(e)}")


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

    # 📌 Market Neutral Hedge Testi
    market_neutral_hedging()
