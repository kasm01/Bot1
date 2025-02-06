import os

# **🚀 Binance API Ayarları**
BINANCE_API_KEY = "YOUR_BINANCE_API_KEY"
BINANCE_API_SECRET = "YOUR_BINANCE_SECRET_KEY"

# **🚀 Telegram Bot API**
TELEGRAM_BOT_TOKEN = "AAHd5443YVlMYQzmZvVUT1NAOIqlMS45dQ0"
TELEGRAM_CHAT_ID = "+905455060646"

# **🚀 CryptoCompare API**
CRYPTOCOMPARE_API_KEY = "c27d77dfa312f637b17cbca43e75ca39d5f174994a7a516b75e469a64d078285"

# **🚀 CoinMarketCap API**
COINMARKETCAP_API_KEY = "e0aa7cc9-9e30-4c5c-8c33-d98bce804735"

# **🚀 Etherscan API**
ETHERSCAN_API_KEY = "AQCCV7EVH32599XDTKJYYHEW32B6BBHEGT"

# **🚀 Santiment API**
SANTIMENT_API_KEY = "ptwnjplj2x5c2lbt_y3ajkwmxg2wujqcf"

# **📌 Binance Testnet Modu (Gerçek işlem yapmaz, test ortamında çalışır)**
USE_TESTNET = True

# **📌 Telegram Bildirimleri Aç/Kapat**
ENABLE_TELEGRAM_NOTIFICATIONS = True

# **📌 İşlem Stratejileri (Kullanıcı tarafından değiştirilebilir)**
TRADE_STRATEGY = "AI_DYNAMIC"  # Seçenekler: "FIXED", "AI_DYNAMIC", "RISK_MANAGED"

# **📌 Kaldıraç Ayarları (Volatiliteye Göre AI tarafından belirlenir)**
MAX_LEVERAGE = 10  # AI en fazla 10x kaldıraç kullanabilir
MIN_LEVERAGE = 1   # En düşük kaldıraç 1x

# **📌 Stop-Loss ve Take-Profit Ayarları**
STOP_LOSS_PERCENTAGE = 0.02  # %2 Stop-Loss
TAKE_PROFIT_PERCENTAGE = 0.05  # %5 Take-Profit

# **📌 Veri Kaynağı Seçenekleri**
DATA_SOURCES = ["BinanceAPI", "CryptoCompare", "CoinMarketCap"]

# **📌 Risk Yönetimi ve Hedge Modülü**
ENABLE_HEDGE = True
HEDGE_THRESHOLD = 0.03  # %3 üzeri volatilite durumunda hedge işlemi açılır

# **📌 AI Model Güncellenme Zamanı**
MODEL_UPDATE_INTERVAL = "24h"  # Model her 24 saatte bir güncellenir

