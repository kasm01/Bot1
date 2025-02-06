import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from scipy.stats import norm
from trading.binance_futures import execute_trade
from notifications.telegram_bot import send_telegram_message

# **📌 Monte Carlo Simülasyonu ile Fiyat Tahmini**
def monte_carlo_simulation(price_data, num_simulations=1000, time_horizon=30):
    """
    Monte Carlo simülasyonu ile gelecek fiyat tahmini yapar.
    :param price_data: Geçmiş fiyat verileri (numpy array)
    :param num_simulations: Çalıştırılacak simülasyon sayısı (default=1000)
    :param time_horizon: Simülasyon süresi (gün olarak)
    :return: Simülasyon sonuçları (DataFrame)
    """
    df = pd.DataFrame(price_data, columns=["Close"])
    daily_returns = df["Close"].pct_change().dropna()

    mean_return = daily_returns.mean()
    std_dev = daily_returns.std()

    last_price = df["Close"].iloc[-1]
    
    simulation_results = np.zeros((num_simulations, time_horizon))

    for sim in range(num_simulations):
        simulated_prices = [last_price]
        for _ in range(time_horizon):
            simulated_price = simulated_prices[-1] * (1 + np.random.normal(mean_return, std_dev))
            simulated_prices.append(simulated_price)
        simulation_results[sim] = simulated_prices[1:]

    return pd.DataFrame(simulation_results)

# **📌 Monte Carlo Sonuçlarını Görselleştir**
def plot_monte_carlo(simulation_results):
    """
    Monte Carlo simülasyon sonuçlarını grafikle gösterir.
    """
    plt.figure(figsize=(12, 6))
    plt.plot(simulation_results.T, alpha=0.1, color='blue')
    plt.title("Monte Carlo Simülasyonu - Fiyat Projeksiyonu")
    plt.xlabel("Gün")
    plt.ylabel("Fiyat")
    plt.show()

# **📌 AI Destekli Risk Analizi**
def monte_carlo_risk_analysis(price_data):
    """
    Monte Carlo Simülasyonu ile AI destekli risk analizi yapar.
    :param price_data: Geçmiş fiyat verileri
    :return: Risk analizi raporu
    """
    simulation_results = monte_carlo_simulation(price_data)
    
    # 5% ve 95% seviyelerinde fiyat projeksiyonları
    lower_bound = np.percentile(simulation_results.iloc[:, -1], 5)
    upper_bound = np.percentile(simulation_results.iloc[:, -1], 95)
    
    # Risk değerlendirmesi
    expected_price = np.mean(simulation_results.iloc[:, -1])
    var_95 = np.percentile(simulation_results.iloc[:, -1], 5)  # 95% VaR (Value at Risk)

    risk_report = {
        "expected_price": round(expected_price, 2),
        "lower_bound": round(lower_bound, 2),
        "upper_bound": round(upper_bound, 2),
        "VaR_95": round(var_95, 2)
    }

    return risk_report

# **📌 Monte Carlo'ya Göre AI Destekli İşlem Açma**
def monte_carlo_trade_decision(price_data):
    """
    Monte Carlo Simülasyonu sonucuna göre alım/satım stratejisi belirler.
    """
    risk_report = monte_carlo_risk_analysis(price_data)

    if risk_report["expected_price"] > price_data[-1]:
        execute_trade("BTCUSDT", "LONG", quantity=0.01, leverage=3)
        send_telegram_message(f"📈 AI Monte Carlo: Yükseliş Bekleniyor! LONG açıldı.\nTahmini Fiyat: {risk_report['expected_price']} USD")
    else:
        execute_trade("BTCUSDT", "SHORT", quantity=0.01, leverage=3)
        send_telegram_message(f"📉 AI Monte Carlo: Düşüş Bekleniyor! SHORT açıldı.\nTahmini Fiyat: {risk_report['expected_price']} USD")

    return risk_report
