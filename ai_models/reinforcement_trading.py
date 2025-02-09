import gym
import numpy as np
import os
from stable_baselines3 import PPO, DQN, A2C
from trading.binance_futures import execute_trade
from notifications.telegram_bot import send_telegram_message
from gym.envs.registration import register

# 📌 **Özel Ticaret Ortamını Kaydet ve Tanımla**
try:
    register(
        id="TradingEnv-v0",
        entry_point="trading_env:TradingEnv",
    )
except:
    print("⚠️ TradingEnv zaten kayıtlı!")

# 📌 **Ortamı Oluştur**
try:
    env = gym.make("TradingEnv-v0")
except Exception as e:
    print(f"⚠️ Ortam başlatılamadı: {e}")
    env = None

# 📌 **Model Dosyalarını Kaydetme ve Yükleme İşlemi**
MODEL_DIR = "models"
os.makedirs(MODEL_DIR, exist_ok=True)

def load_or_create_model(model_class, model_name):
    """Kaydedilmiş modeli yükler veya yeni model oluşturur."""
    model_path = os.path.join(MODEL_DIR, model_name)
    if os.path.exists(model_path + ".zip"):
        print(f"✅ {model_name} modeli yükleniyor...")
        return model_class.load(model_path, env=env)
    else:
        print(f"🔄 {model_name} modeli oluşturuluyor...")
        return model_class("MlpPolicy", env, verbose=1)

# 📌 **Modelleri Tanımla**
ppo_model = load_or_create_model(PPO, "ppo_trading_model")
dqn_model = load_or_create_model(DQN, "dqn_trading_model")
a2c_model = load_or_create_model(A2C, "a2c_trading_model")

def train_models(total_timesteps=100000):
    """📈 PPO, DQN ve A2C modellerini eğit ve kaydet"""
    if env is None:
        print("⚠️ Ortam başlatılamadı! Model eğitimi gerçekleştirilemiyor.")
        return
    
    print("🔄 PPO Modeli Eğitiliyor...")
    ppo_model.learn(total_timesteps=total_timesteps)
    ppo_model.save(os.path.join(MODEL_DIR, "ppo_trading_model"))

    print("🔄 DQN Modeli Eğitiliyor...")
    dqn_model.learn(total_timesteps=total_timesteps)
    dqn_model.save(os.path.join(MODEL_DIR, "dqn_trading_model"))

    print("🔄 A2C Modeli Eğitiliyor...")
    a2c_model.learn(total_timesteps=total_timesteps)
    a2c_model.save(os.path.join(MODEL_DIR, "a2c_trading_model"))

    print("✅ Reinforcement Learning Modelleri Eğitildi ve Kaydedildi!")

# 📌 **PPO Modeli ile İşlem Aç**
def reinforcement_trade_ppo():
    """📊 PPO modeli ile AI destekli işlem açar"""
    if env is None:
        print("⚠️ Ortam başlatılamadı! İşlem açılamıyor.")
        return

    obs = env.reset()
    action, _ = ppo_model.predict(obs)
    trade_type = "LONG" if action == 1 else "SHORT"
    execute_trade(symbol="BTCUSDT", trade_type=trade_type, quantity=0.01, leverage=5)
    send_telegram_message(f"📈 PPO Modeli Kararı: {trade_type}")

# 📌 **DQN Modeli ile İşlem Aç**
def reinforcement_trade_dqn():
    """📊 DQN modeli ile AI destekli işlem açar"""
    if env is None:
        print("⚠️ Ortam başlatılamadı! İşlem açılamıyor.")
        return

    obs = env.reset()
    action, _ = dqn_model.predict(obs)
    trade_type = "LONG" if action == 1 else "SHORT"
    execute_trade(symbol="BTCUSDT", trade_type=trade_type, quantity=0.01, leverage=5)
    send_telegram_message(f"📈 DQN Modeli Kararı: {trade_type}")

# 📌 **A2C Modeli ile İşlem Aç**
def reinforcement_trade_a2c():
    """📊 A2C modeli ile AI destekli işlem açar"""
    if env is None:
        print("⚠️ Ortam başlatılamadı! İşlem açılamıyor.")
        return

    obs = env.reset()
    action, _ = a2c_model.predict(obs)
    trade_type = "LONG" if action == 1 else "SHORT"
    execute_trade(symbol="BTCUSDT", trade_type=trade_type, quantity=0.01, leverage=5)
    send_telegram_message(f"📈 A2C Modeli Kararı: {trade_type}")

# 📌 **Eğer bu dosya doğrudan çalıştırılırsa modeller eğitilir**
if __name__ == "__main__":
    train_models(total_timesteps=100000)
