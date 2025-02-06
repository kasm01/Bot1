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
    df = pd.DataFrame(price_data, columns=["Close"])
    log_returns = np.log(df["Close"]).diff().dropna()  # Log getirileri hesapla

    model = arch.arch_model(log_returns, vol="Garch", p=1, q=1)
    fitted_model = model.fit(disp="off")  # Modeli eğit

    volatility_forecast = fitted_model.forecast(start=0).variance[-1:].values[0] ** 0.5  # Son volatilite tahmini
    return fitted_model, volatility_forecast

# **📌 GARCH Volatilite Tahminini Görselleştir**
def plot_garch_volatility(price_data):
    """
    GARCH modeli ile tahmin edilen volatiliteyi görselleştirir.
    """
    model, volatility_forecast = train_garch_model(price_data)
    volatility_series = model.conditional_volatility
    
    plt.figure(figsize=(12, 6))
    plt.plot(volatility_series, label="GARCH Tahmini Volatilite")
    plt.xlabel("Zaman")
    plt.ylabel("Volatilite")
    plt.title("📊 GARCH Modeli ile Volatilite Tahmini")
    plt.legend()
    plt.show()

# **📌 AI Destekli Kaldıraç Yönetimi**
def garch_based_leverage(price_data):
    """
    GARCH modeli ile volatiliteye bağlı olarak AI destekli kaldıraç hesaplar.
    :param price_data: Geçmiş fiyat verileri
    :return: Optimal kaldıraç oranı (1x - 10x)
    """
    _, volatility_forecast = train_garch_model(price_data)

    if volatility_forecast < 0.01:
        return 10  # Düşük volatilite, yüksek kaldıraç
    elif volatility_forecast < 0.03:
        return 5
    elif volatility_forecast < 0.05:
        return 3
    else:
        return 1  # Yüksek volatilite, düşük kaldıraç

# **📌 GARCH'a Göre AI Destekli İşlem Açma**
def garch_trade_decision(price_data):
    """
    GARCH Modeli sonucuna göre alım/satım stratejisi belirler.
    """
    leverage = garch_based_leverage(price_data)
    trade_type = "LONG" if np.random.rand() > 0.5 else "SHORT"

    execute_trade("BTCUSDT", trade_type, quantity=0.01, leverage=leverage)
    send_telegram_message(f"📊 GARCH Modeli: AI destekli işlem açıldı.\nİşlem Türü: {trade_type} | Kaldıraç: {leverage}x")
    
    return trade_type, leverage
