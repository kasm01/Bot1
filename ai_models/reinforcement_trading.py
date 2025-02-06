import gym
import numpy as np
from stable_baselines3 import PPO, DQN, A2C
from trading.binance_futures import execute_trade
from notifications.telegram_bot import send_telegram_message

# 📌 **Özel Ticaret Ortamını Tanımla**
env = gym.make("TradingEnv-v0")

# 📌 **Farklı Reinforcement Learning Modellerini Eğit ve Kaydet**
ppo_model = PPO("MlpPolicy", env, verbose=1)
dqn_model = DQN("MlpPolicy", env, verbose=1)
a2c_model = A2C("MlpPolicy", env, verbose=1)

def train_models(total_timesteps=100000):
    """📈 PPO, DQN ve A2C modellerini eğit ve kaydet"""
    ppo_model.learn(total_timesteps=total_timesteps)
    dqn_model.learn(total_timesteps=total_timesteps)
    a2c_model.learn(total_timesteps=total_timesteps)

    ppo_model.save("models/ppo_trading_model")
    dqn_model.save("models/dqn_trading_model")
    a2c_model.save("models/a2c_trading_model")

    print("✅ Reinforcement Learning Modelleri Eğitildi ve Kaydedildi!")

# 📌 **PPO Modeli ile İşlem Aç**
def reinforcement_trade_ppo():
    """📊 PPO modeli ile AI destekli işlem açar"""
    action, _ = ppo_model.predict(env.observation_space.sample())
    trade_type = "LONG" if action == 1 else "SHORT"
    execute_trade(symbol="BTCUSDT", trade_type=trade_type, quantity=0.01, leverage=5)
    send_telegram_message(f"📈 PPO Modeli Kararı: {trade_type}")

# 📌 **DQN Modeli ile İşlem Aç**
def reinforcement_trade_dqn():
    """📊 DQN modeli ile AI destekli işlem açar"""
    action, _ = dqn_model.predict(env.observation_space.sample())
    trade_type = "LONG" if action == 1 else "SHORT"
    execute_trade(symbol="BTCUSDT", trade_type=trade_type, quantity=0.01, leverage=5)
    send_telegram_message(f"📈 DQN Modeli Kararı: {trade_type}")

# 📌 **A2C Modeli ile İşlem Aç**
def reinforcement_trade_a2c():
    """📊 A2C modeli ile AI destekli işlem açar"""
    action, _ = a2c_model.predict(env.observation_space.sample())
    trade_type = "LONG" if action == 1 else "SHORT"
    execute_trade(symbol="BTCUSDT", trade_type=trade_type, quantity=0.01, leverage=5)
    send_telegram_message(f"📈 A2C Modeli Kararı: {trade_type}")

# 📌 **Eğer bu dosya doğrudan çalıştırılırsa modeller eğitilir**
if __name__ == "__main__":
    train_models(total_timesteps=100000)
