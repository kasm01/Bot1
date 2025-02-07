import numpy as np

def calculate_take_profit(entry_price, volatility, reward_factor=0.04):
    """
    AI destekli take-profit hesaplama.
    
    :param entry_price: İşlem giriş fiyatı
    :param volatility: Piyasa volatilitesi
    :param reward_factor: Kar hedefi oranı (Varsayılan: %4)
    :return: Take-profit fiyatı
    """
    take_profit_pct = np.interp(volatility, [0.01, 0.05], [0.01, reward_factor])
    take_profit_price = entry_price * (1 + take_profit_pct)
    return round(take_profit_price, 2)

def calculate_trailing_take_profit(entry_price, current_price, trailing_percent=0.02):
    """
    AI destekli trailing take-profit hesaplama.
    
    :param entry_price: İşlem giriş fiyatı
    :param current_price: Güncel fiyat
    :param trailing_percent: Trailing stop yüzdesi (Varsayılan: %2)
    :return: Yeni take-profit seviyesi
    """
    trailing_take_profit_price = current_price * (1 + trailing_percent)
    return round(trailing_take_profit_price, 2)
