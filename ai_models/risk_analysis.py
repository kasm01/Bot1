import numpy as np
import pandas as pd
from scipy.stats import norm
from trading.binance_futures import execute_trade
from notifications.telegram_bot import send_telegram_message

# **📌 AI Destekli Volatilite Hesaplama**
def calculate_volatility(price_data, window=20):
    """Fiyat verilerinden volatilite hesaplar"""
    if len(price_data) < window:
        print("⚠️ Yetersiz veri! Volatilite hesaplanamıyor.")
        return None
    
    df = pd.DataFrame(price_data, columns=["Close"])
    df["returns"] = df["Close"].pct_change().dropna()
    df["volatility"] = df["returns"].rolling(window=window).std()
    
    return df["volatility"].dropna().iloc[-1]  # Son volatilite değeri

# **📌 Value at Risk (VaR) Hesaplama**
def calculate_var(price_data, confidence_level=0.95):
    """Monte Carlo Simülasyonu ile Value at Risk (VaR) hesaplar"""
    if len(price_data) < 30:  
        print("⚠️ Yetersiz veri! VaR hesaplanamıyor.")
        return None

    df = pd.DataFrame(price_data, columns=["Close"])
    daily_returns = df["Close"].pct_change().dropna()

    mean_return = daily_returns.mean()
    std_dev = daily_returns.std()

    if std_dev == 0:
        print("⚠️ Standart sapma sıfır! VaR hesaplanamıyor.")
        return None

    var_value = norm.ppf(confidence_level, mean_return, std_dev) * df["Close"].iloc[-1]
    return abs(var_value)

# **📌 AI Destekli Stop-Loss & Take-Profit Hesaplama**
def calculate_dynamic_stop_loss(entry_price, volatility):
    """Volatilite bazlı stop-loss hesaplama"""
    if volatility is None:
        return None

    stop_loss_pct = np.interp(volatility, [0.01, 0.05], [0.005, 0.03])
    return round(entry_price * (1 - stop_loss_pct), 2)

def calculate_dynamic_take_profit(entry_price, volatility):
    """Volatilite bazlı take-profit hesaplama"""
    if volatility is None:
        return None

    take_profit_pct = np.interp(volatility, [0.01, 0.05], [0.01, 0.06])
    return round(entry_price * (1 + take_profit_pct), 2)

# **📌 AI Destekli Hedge Mekanizması**
def optimized_hedging(entry_price, volatility, threshold=0.03):
    """Volatilite eşiğine göre hedge aç/kapat"""
    if volatility is None:
        print("⚠️ Volatilite hesaplanamadı! Hedge açılmıyor.")
        return
    
    if volatility > threshold:
        hedge_amount = round(np.random.uniform(0.01, 0.05), 4)  # Maksimum %5 hedge aç
        execute_trade("BTCUSDT", "SHORT", quantity=hedge_amount)
        send_telegram_message(f"📉 AI Hedge Açıldı: Miktar: {hedge_amount} BTC | Volatilite: {volatility:.4f}")
    else:
        send_telegram_message("⚠️ Hedge açılmadı. Volatilite düşük.")

# **📌 AI Destekli Kaldıraç Yönetimi**
def dynamic_leverage(volatility):
    """AI destekli kaldıraç yönetimi (1x-10x)"""
    if volatility is None:
        return 1

    if volatility < 0.005:
        return 10  # Çok düşük volatilite, en yüksek kaldıraç
    elif volatility < 0.015:
        return 7
    elif volatility < 0.03:
        return 5
    elif volatility < 0.05:
        return 3
    else:
        return 1  # Yüksek volatilite, düşük kaldıraç

# **📌 Risk Yönetimi Fonksiyonları Bir Arada Kullanımı**
def risk_management(entry_price, price_data):
    """Risk yönetimi analizi ve hesaplamaları"""
    if len(price_data) < 30:
        print("⚠️ Yetersiz fiyat verisi! Risk yönetimi yapılamıyor.")
        return None

    volatility = calculate_volatility(price_data)
    var = calculate_var(price_data)

    if volatility is None or var is None:
        print("⚠️ Gerekli metrikler hesaplanamadı! Risk yönetimi yapılamıyor.")
        return None

    stop_loss = calculate_dynamic_stop_loss(entry_price, volatility)
    take_profit = calculate_dynamic_take_profit(entry_price, volatility)
    leverage = dynamic_leverage(volatility)

    optimized_hedging(entry_price, volatility)

    risk_report = {
        "volatility": round(volatility, 4),
        "VaR": round(var, 2),
        "stop_loss": stop_loss,
        "take_profit": take_profit,
        "leverage": leverage
    }

    print(f"📊 Risk Analizi: {risk_report}")
    send_telegram_message(f"📊 AI Risk Yönetimi: {risk_report}")

    return risk_report

# 📌 **Eğer bu dosya doğrudan çalıştırılırsa test edilir**
if __name__ == "__main__":
    # **Simüle edilen fiyat verileri (Gerçek veriler Binance API ile entegre edilebilir)**
    fake_price_data = np.cumsum(np.random.randn(500)) + 50000  # 50.000 seviyesinden başlatılan simüle edilmiş fiyatlar

    # 📌 Test için giriş fiyatı
    entry_price = fake_price_data[-1]

    # 📌 Risk Yönetimi Testi
    risk_report = risk_management(entry_price, fake_price_data)
    print(f"🚀 AI Risk Yönetimi Sonuçları: {risk_report}")
