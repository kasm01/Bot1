import numpy as np
import pandas as pd
from scipy.stats import norm
from trading.binance_futures import execute_trade
from notifications.telegram_bot import send_telegram_message

# **📌 AI Destekli Volatilite Hesaplama**
def calculate_volatility(price_data, window=20):
    """Fiyat verilerinden volatilite hesaplar"""
    df = pd.DataFrame(price_data, columns=["Close"])
    df["returns"] = df["Close"].pct_change()
    df["volatility"] = df["returns"].rolling(window=window).std()
    return df["volatility"].iloc[-1]  # Son volatilite değeri

# **📌 Value at Risk (VaR) Hesaplama**
def calculate_var(price_data, confidence_level=0.95):
    """Monte Carlo Simülasyonu ile Value at Risk (VaR) hesaplar"""
    df = pd.DataFrame(price_data, columns=["Close"])
    daily_returns = df["Close"].pct_change().dropna()

    mean_return = daily_returns.mean()
    std_dev = daily_returns.std()

    var_value = norm.ppf(1 - confidence_level, mean_return, std_dev) * df["Close"].iloc[-1]
    return abs(var_value)

# **📌 AI Destekli Stop-Loss & Take-Profit Hesaplama**
def calculate_dynamic_stop_loss(entry_price, volatility):
    """Volatilite bazlı stop-loss hesaplama"""
    stop_loss_pct = np.interp(volatility, [0.01, 0.05], [0.005, 0.03])
    return round(entry_price * (1 - stop_loss_pct), 2)

def calculate_dynamic_take_profit(entry_price, volatility):
    """Volatilite bazlı take-profit hesaplama"""
    take_profit_pct = np.interp(volatility, [0.01, 0.05], [0.01, 0.06])
    return round(entry_price * (1 + take_profit_pct), 2)

# **📌 AI Destekli Hedge Mekanizması**
def optimized_hedging(entry_price, volatility, threshold=0.03):
    """Volatilite eşiğine göre hedge aç/kapat"""
    if volatility > threshold:
        hedge_amount = np.random.uniform(0.01, 0.05)  # Maksimum %5 hedge aç
        execute_trade("BTCUSDT", "SHORT", quantity=hedge_amount)
        send_telegram_message(f"📉 AI Hedge Açıldı: Miktar: {hedge_amount}, Volatilite: {volatility}")
    else:
        send_telegram_message("⚠️ Hedge açılmadı. Volatilite düşük.")

# **📌 AI Destekli Kaldıraç Yönetimi**
def dynamic_leverage(volatility):
    """AI destekli kaldıraç yönetimi (1x-10x)"""
    if volatility < 0.01:
        return 10
    elif volatility < 0.03:
        return 5
    elif volatility < 0.05:
        return 3
    else:
        return 1  # Yüksek volatilite, düşük kaldıraç

# **📌 Risk Yönetimi Fonksiyonları Bir Arada Kullanımı**
def risk_management(entry_price, price_data):
    """Risk yönetimi analizi ve hesaplamaları"""
    volatility = calculate_volatility(price_data)
    var = calculate_var(price_data)
    
    stop_loss = calculate_dynamic_stop_loss(entry_price, volatility)
    take_profit = calculate_dynamic_take_profit(entry_price, volatility)
    leverage = dynamic_leverage(volatility)

    optimized_hedging(entry_price, volatility)

    return {
        "volatility": volatility,
        "VaR": var,
        "stop_loss": stop_loss,
        "take_profit": take_profit,
        "leverage": leverage
    }
