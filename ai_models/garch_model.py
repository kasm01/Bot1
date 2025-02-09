import numpy as np
import pandas as pd
import arch  # GARCH modeli için
import matplotlib.pyplot as plt
from trading.binance_futures import execute_trade
from notifications.telegram_bot import send_telegram_message

# **📌 GARCH Modeli ile Volatilite Tahmini**
def train_garch_model(price_data):
    """
    GARCH(1,1) modelini eğit ve volatiliteyi tahmin et.
    :param price_data: Geçmiş fiyat verileri (numpy array)
    :return: Eğitilmiş model ve volatilite tahminleri
    """
    try:
        if len(price_data) < 30:
            raise ValueError("GARCH modeli için en az 30 veri noktası gereklidir.")

        df = pd.DataFrame(price_data, columns=["Close"])
        log_returns = np.log(df["Close"]).diff().dropna()  # Log getirileri hesapla

        model = arch.arch_model(log_returns, vol="Garch", p=1, q=1)
        fitted_model = model.fit(disp="off")  # Modeli eğit

        # Son volatilite tahmini
        forecast = fitted_model.forecast(horizon=1).variance.iloc[-1, 0] ** 0.5
        return fitted_model, forecast
    except Exception as e:
        print(f"⚠️ GARCH Modeli Hatası: {e}")
        send_telegram_message(f"⚠️ GARCH Modeli Hatası: {e}")
        return None, None

# **📌 GARCH Volatilite Tahminini Görselleştir**
def plot_garch_volatility(price_data):
    """
    GARCH modeli ile tahmin edilen volatiliteyi görselleştirir.
    """
    try:
        model, _ = train_garch_model(price_data)
        if model is None:
            return

        plt.figure(figsize=(12, 6))
        plt.plot(model.conditional_volatility, label="GARCH Tahmini Volatilite", color='blue')
        plt.xlabel("Zaman")
        plt.ylabel("Volatilite")
        plt.title("📊 GARCH Modeli ile Volatilite Tahmini")
        plt.legend()
        plt.grid(True)
        plt.show()
    except Exception as e:
        print(f"⚠️ Grafik çizim hatası: {e}")
        send_telegram_message(f"⚠️ GARCH Grafik Çizim Hatası: {e}")

# **📌 AI Destekli Kaldıraç Yönetimi**
def garch_based_leverage(price_data):
    """
    GARCH modeli ile volatiliteye bağlı olarak AI destekli kaldıraç hesaplar.
    :param price_data: Geçmiş fiyat verileri
    :return: Optimal kaldıraç oranı (1x - 10x)
    """
    try:
        _, volatility_forecast = train_garch_model(price_data)
        if volatility_forecast is None:
            return 1  # Varsayılan kaldıraç

        if volatility_forecast < 0.005:
            return 10  # Çok düşük volatilite, en yüksek kaldıraç
        elif volatility_forecast < 0.015:
            return 7
        elif volatility_forecast < 0.03:
            return 5
        elif volatility_forecast < 0.05:
            return 3
        else:
            return 1  # Yüksek volatilite, minimum kaldıraç
    except Exception as e:
        print(f"⚠️ Kaldıraç hesaplama hatası: {e}")
        send_telegram_message(f"⚠️ Kaldıraç hesaplama hatası: {e}")
        return 1  # Varsayılan kaldıraç

# **📌 GARCH'a Göre AI Destekli İşlem Açma**
def garch_trade_decision(price_data):
    """
    GARCH Modeli sonucuna göre alım/satım stratejisi belirler.
    """
    try:
        leverage = garch_based_leverage(price_data)
        trade_type = "LONG" if np.random.rand() > 0.5 else "SHORT"

        execute_trade("BTCUSDT", trade_type, quantity=0.01, leverage=leverage)
        send_telegram_message(f"📊 GARCH Modeli: AI destekli işlem açıldı.\nİşlem Türü: {trade_type} | Kaldıraç: {leverage}x")

        return trade_type, leverage
    except Exception as e:
        print(f"⚠️ İşlem açma hatası: {e}")
        send_telegram_message(f"⚠️ İşlem açma hatası: {e}")
        return None, None
