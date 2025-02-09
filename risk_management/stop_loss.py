import numpy as np

def calculate_stop_loss(entry_price, volatility, risk_factor=0.02):
    """
    AI destekli stop-loss hesaplama.
    
    :param entry_price: İşlem giriş fiyatı
    :param volatility: Piyasa volatilitesi (0.01 - 0.05 arası değerler önerilir)
    :param risk_factor: Maksimum risk oranı (Varsayılan: %2)
    :return: Stop-loss fiyatı
    """
    if entry_price <= 0:
        raise ValueError("⚠️ Hata: Giriş fiyatı negatif veya sıfır olamaz.")
    
    if not (0.01 <= volatility <= 0.05):
        print("⚠️ Uyarı: Volatilite değeri önerilen aralıkta değil! (0.01 - 0.05)")

    stop_loss_pct = np.interp(volatility, [0.01, 0.05], [0.005, risk_factor])
    stop_loss_price = entry_price * (1 - stop_loss_pct)

    return round(stop_loss_price, 2)

def calculate_take_profit(entry_price, volatility, reward_factor=0.04):
    """
    AI destekli take-profit hesaplama.
    
    :param entry_price: İşlem giriş fiyatı
    :param volatility: Piyasa volatilitesi
    :param reward_factor: Kar hedefi oranı (Varsayılan: %4)
    :return: Take-profit fiyatı
    """
    if entry_price <= 0:
        raise ValueError("⚠️ Hata: Giriş fiyatı negatif veya sıfır olamaz.")
    
    if not (0.01 <= volatility <= 0.05):
        print("⚠️ Uyarı: Volatilite değeri önerilen aralıkta değil! (0.01 - 0.05)")

    take_profit_pct = np.interp(volatility, [0.01, 0.05], [0.01, reward_factor])
    take_profit_price = entry_price * (1 + take_profit_pct)

    return round(take_profit_price, 2)

def calculate_trailing_stop(entry_price, current_price, trailing_percent=0.02):
    """
    AI destekli trailing stop-loss hesaplama.
    
    :param entry_price: İşlem giriş fiyatı
    :param current_price: Güncel fiyat
    :param trailing_percent: Trailing stop yüzdesi (Varsayılan: %2)
    :return: Yeni stop-loss seviyesi
    """
    if entry_price <= 0 or current_price <= 0:
        raise ValueError("⚠️ Hata: Fiyat değerleri negatif veya sıfır olamaz.")

    if current_price <= entry_price:
        print("⚠️ Uyarı: Güncel fiyat giriş fiyatından düşük! Trailing stop güncellenmiyor.")
        return round(entry_price * (1 - trailing_percent), 2)

    trailing_stop_price = current_price * (1 - trailing_percent)
    
    return round(trailing_stop_price, 2)


# 📌 **Test Amaçlı Çalıştırma**
if __name__ == "__main__":
    # 📌 Örnek işlem giriş fiyatı ve volatilite değeri
    entry_price = 35000
    current_price = 36000
    volatility = 0.03

    # 📌 Stop-Loss Hesaplama
    stop_loss = calculate_stop_loss(entry_price, volatility)
    print(f"🛑 Stop-Loss Fiyatı: {stop_loss} USDT")

    # 📌 Take-Profit Hesaplama
    take_profit = calculate_take_profit(entry_price, volatility)
    print(f"🎯 Take-Profit Fiyatı: {take_profit} USDT")

    # 📌 Trailing Stop-Loss Hesaplama
    trailing_stop = calculate_trailing_stop(entry_price, current_price)
    print(f"📉 Trailing Stop Fiyatı: {trailing_stop} USDT")
