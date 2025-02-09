import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
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
        simulation_results[sim, :] = simulated_prices[1:]

    return pd.DataFrame(simulation_results)

# **📌 Monte Carlo Sonuçlarını Görselleştir**
def plot_monte_carlo(simulation_results):
    """
    Monte Carlo simülasyon sonuçlarını grafikle gösterir.
    """
    plt.figure(figsize=(12, 6))
    
    # Bütün simülasyonları düşük opaklıkla göster
    plt.plot(simulation_results.T, alpha=0.05, color='blue')

    # Ortalama tahmin fiyat çizgisi
    mean_prediction = simulation_results.mean(axis=0)
    plt.plot(mean_prediction, color='red', label="Ortalama Tahmin")

    # Alt ve üst güven aralıkları
    lower_bound = np.percentile(simulation_results, 5, axis=0)
    upper_bound = np.percentile(simulation_results, 95, axis=0)
    plt.fill_between(range(len(mean_prediction)), lower_bound, upper_bound, color='gray', alpha=0.3, label="5%-95% Aralığı")

    plt.title("📈 Monte Carlo Simülasyonu - Fiyat Projeksiyonu")
    plt.xlabel("Gün")
    plt.ylabel("Fiyat")
    plt.legend()
    plt.grid(True)
    plt.show()

# **📌 AI Destekli Risk Analizi**
def monte_carlo_risk_analysis(price_data, num_simulations=1000, time_horizon=30):
    """
    Monte Carlo Simülasyonu ile AI destekli risk analizi yapar.
    :param price_data: Geçmiş fiyat verileri
    :return: Risk analizi raporu
    """
    simulation_results = monte_carlo_simulation(price_data, num_simulations, time_horizon)
    
    # 5% ve 95% seviyelerinde fiyat projeksiyonları
    lower_bound = np.percentile(simulation_results.values[:, -1], 5)
    upper_bound = np.percentile(simulation_results.values[:, -1], 95)
    
    # Risk değerlendirmesi
    expected_price = np.mean(simulation_results.values[:, -1])
    var_95 = np.percentile(simulation_results.values[:, -1], 5)  # 95% VaR (Value at Risk)

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

    current_price = price_data[-1]
    price_difference = (risk_report["expected_price"] - current_price) / current_price

    if price_difference > 0.01:  # Eğer tahmini fiyat %1'den fazla yukarıda ise LONG aç
        execute_trade("BTCUSDT", "LONG", quantity=0.01, leverage=3)
        send_telegram_message(
            f"📈 AI Monte Carlo: Yükseliş Bekleniyor! LONG açıldı."
            f"\nMevcut Fiyat: {current_price} USD | Tahmini Fiyat: {risk_report['expected_price']} USD"
        )
        return "LONG", risk_report

    elif price_difference < -0.01:  # Eğer tahmini fiyat %1'den fazla aşağıda ise SHORT aç
        execute_trade("BTCUSDT", "SHORT", quantity=0.01, leverage=3)
        send_telegram_message(
            f"📉 AI Monte Carlo: Düşüş Bekleniyor! SHORT açıldı."
            f"\nMevcut Fiyat: {current_price} USD | Tahmini Fiyat: {risk_report['expected_price']} USD"
        )
        return "SHORT", risk_report

    else:
        send_telegram_message(
            f"⚖️ AI Monte Carlo: Piyasa nötr durumda, işlem açılmadı."
            f"\nMevcut Fiyat: {current_price} USD | Tahmini Fiyat: {risk_report['expected_price']} USD"
        )
        return "NO TRADE", risk_report

# 📌 **Eğer bu dosya doğrudan çalıştırılırsa simülasyon yapılır**
if __name__ == "__main__":
    # **Simüle edilen fiyat verileri (Gerçek veriler Binance API ile entegre edilebilir)**
    fake_price_data = np.cumsum(np.random.randn(500)) + 50000  # 50.000 seviyesinden başlatılan simüle edilmiş fiyatlar

    # 📌 Monte Carlo Simülasyonu Çalıştır
    simulation_results = monte_carlo_simulation(fake_price_data)
    
    # 📌 Simülasyon Sonuçlarını Görselleştir
    plot_monte_carlo(simulation_results)

    # 📌 AI Destekli Risk Analizi Yap
    risk_report = monte_carlo_risk_analysis(fake_price_data)
    print(f"📊 AI Risk Analizi: {risk_report}")

    # 📌 AI Destekli İşlem Açma Kararı Ver
    trade_decision, final_risk_report = monte_carlo_trade_decision(fake_price_data)
    print(f"🚀 AI İşlem Kararı: {trade_decision}")
