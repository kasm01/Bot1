import numpy as np
import pandas as pd
import tensorflow as tf
from tensorflow.keras.models import Sequential, load_model
from tensorflow.keras.layers import LSTM, Dense, Dropout
from sklearn.preprocessing import MinMaxScaler
import os

# 📌 Model ve scaler için klasörü oluştur
MODEL_DIR = "models"
os.makedirs(MODEL_DIR, exist_ok=True)

# **📌 LSTM Modelini Eğitme Fonksiyonu**
def train_lstm_model(price_data, epochs=20, batch_size=32):
    """📈 LSTM modelini fiyat tahmini için eğit ve kaydet"""
    
    scaler = MinMaxScaler(feature_range=(0,1))
    scaled_data = scaler.fit_transform(np.array(price_data).reshape(-1, 1))

    X, y = [], []
    for i in range(60, len(scaled_data)):
        X.append(scaled_data[i-60:i, 0])
        y.append(scaled_data[i, 0])

    X, y = np.array(X), np.array(y)
    X = np.reshape(X, (X.shape[0], X.shape[1], 1))

    # **📌 LSTM Modeli**
    model = Sequential([
        LSTM(units=50, return_sequences=True, input_shape=(X.shape[1], 1)),
        Dropout(0.2),
        LSTM(units=50),
        Dropout(0.2),
        Dense(units=1)
    ])
    
    model.compile(optimizer="adam", loss="mse")
    model.fit(X, y, epochs=epochs, batch_size=batch_size, verbose=1)

    # 📌 **Modeli Kaydet**
    model.save(os.path.join(MODEL_DIR, "lstm_model.h5"))
    np.save(os.path.join(MODEL_DIR, "lstm_scaler.npy"), scaler)

    print("✅ LSTM modeli başarıyla eğitildi ve kaydedildi!")
    return model, scaler

# **📌 LSTM Modelini Yükleme Fonksiyonu**
def load_lstm_model():
    """Kaydedilmiş LSTM modelini ve scaler'ı yükler"""
    try:
        model = load_model(os.path.join(MODEL_DIR, "lstm_model.h5"))
        scaler = np.load(os.path.join(MODEL_DIR, "lstm_scaler.npy"), allow_pickle=True).item()
        print("✅ LSTM modeli ve scaler başarıyla yüklendi!")
        return model, scaler
    except Exception as e:
        print(f"⚠️ Model yüklenirken hata oluştu: {e}")
        return None, None

# **📌 LSTM Modeli ile Fiyat Tahmini**
def predict_price_lstm(model, scaler, last_60_prices):
    """📉 LSTM modeli ile fiyat tahmini yap"""
    if len(last_60_prices) < 60:
        print("⚠️ Yeterli veri yok! En az 60 fiyat verisi gerekli.")
        return None

    last_60_scaled = scaler.transform(np.array(last_60_prices).reshape(-1, 1))
    X_test = np.array([last_60_scaled])
    X_test = np.reshape(X_test, (X_test.shape[0], X_test.shape[1], 1))

    predicted_price = model.predict(X_test)
    return scaler.inverse_transform(predicted_price)[0][0]

# 📌 **Eğer bu dosya doğrudan çalıştırılırsa model eğitilir**
if __name__ == "__main__":
    # **Simüle edilen fiyat verileri (Binance API bağlandığında gerçek veriyle değiştirilir)**
    fake_price_data = np.cumsum(np.random.randn(500)) + 50000  # 50.000 seviyesinden simüle edilen fiyatlar

    # 📌 Modeli eğit ve kaydet
    trained_model, trained_scaler = train_lstm_model(fake_price_data)

    # 📌 Son 60 fiyatı kullanarak tahmin yap
    predicted_price = predict_price_lstm(trained_model, trained_scaler, fake_price_data[-60:])
    
    if predicted_price is not None:
        print(f"📊 AI Tahmini BTC/USDT Fiyatı: {predicted_price:.2f} USD")
