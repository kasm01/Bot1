import numpy as np

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

def calculate_trailing_take_profit(entry_price, current_price, trailing_percent=0.02):
    """
    AI destekli trailing take-profit hesaplama.
    
    :param entry_price: İşlem giriş fiyatı
    :param current_price: Güncel fiyat
    :param trailing_percent: Trailing stop yüzdesi (Varsayılan: %2)
    :return: Yeni take-profit seviyesi veya None (Eğer güncel fiyat giriş fiyatının altındaysa)
    """
    if entry_price <= 0 or current_price <= 0:
        raise ValueError("⚠️ Hata: Fiyat değerleri negatif veya sıfır olamaz.")

    if current_price <= entry_price:
        print("⚠️ Uyarı: Güncel fiyat giriş fiyatından düşük! Trailing take-profit uygulanmadı.")
        return None

    trailing_take_profit_price = current_price * (1 + trailing_percent)
    
    return round(trailing_take_profit_price, 2)


# 📌 **Test Amaçlı Çalıştırma**
if __name__ == "__main__":
    # 📌 Örnek işlem giriş fiyatı ve volatilite değeri
    entry_price = 35000
    current_price = 36000
    volatility = 0.03

    # 📌 Take-Profit Hesaplama
    take_profit = calculate_take_profit(entry_price, volatility)
    print(f"🎯 Take-Profit Fiyatı: {take_profit} USDT")

    # 📌 Trailing Take-Profit Hesaplama
    trailing_take_profit = calculate_trailing_take_profit(entry_price, current_price)
    if trailing_take_profit:
        print(f"📉 Trailing Take-Profit Fiyatı: {trailing_take_profit} USDT")
