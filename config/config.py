import os
from dotenv import load_dotenv

# .env dosyasını yükle
if not load_dotenv():
    print("⚠️ .env dosyası yüklenemedi! Ortam değişkenleri eksik olabilir.")

# 📌 **Binance API Bilgileri**
BINANCE_API_KEY = os.getenv("BINANCE_API_KEY")
BINANCE_API_SECRET = os.getenv("BINANCE_API_SECRET")
BINANCE_TESTNET = os.getenv("BINANCE_TESTNET", "True").strip().lower() == "true"

# 📌 **Telegram API Bilgileri**
TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
TELEGRAM_CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")

# 📌 **API Servisleri**
CRYPTOCOMPARE_API_KEY = os.getenv("CRYPTOCOMPARE_API_KEY")
COINMARKETCAP_API_KEY = os.getenv("COINMARKETCAP_API_KEY")
ETHERSCAN_API_KEY = os.getenv("ETHERSCAN_API_KEY")
SANTIMENT_API_KEY = os.getenv("SANTIMENT_API_KEY")

# 📌 **Varsayılan İşlem Ayarları**
try:
    DEFAULT_LEVERAGE = int(os.getenv("DEFAULT_LEVERAGE", 5))
except ValueError:
    print("⚠️ DEFAULT_LEVERAGE değeri geçersiz! Varsayılan olarak 5 ayarlandı.")
    DEFAULT_LEVERAGE = 5

try:
    STOP_LOSS_PERCENT = float(os.getenv("STOP_LOSS_PERCENT", 0.02))
except ValueError:
    print("⚠️ STOP_LOSS_PERCENT değeri geçersiz! Varsayılan olarak 0.02 ayarlandı.")
    STOP_LOSS_PERCENT = 0.02

try:
    TAKE_PROFIT_PERCENT = float(os.getenv("TAKE_PROFIT_PERCENT", 0.05))
except ValueError:
    print("⚠️ TAKE_PROFIT_PERCENT değeri geçersiz! Varsayılan olarak 0.05 ayarlandı.")
    TAKE_PROFIT_PERCENT = 0.05

# 📌 **Boş API Anahtarlarını Kontrol Et**
missing_keys = []

if not BINANCE_API_KEY or not BINANCE_API_SECRET:
    missing_keys.append("Binance API Keyleri")

if not TELEGRAM_BOT_TOKEN or not TELEGRAM_CHAT_ID:
    missing_keys.append("Telegram API Keyleri")

if missing_keys:
    print(f"⚠️ Eksik API Anahtarları: {', '.join(missing_keys)}! Lütfen .env dosyanızı kontrol edin.")

# 📌 **Ortam Değişkenlerini Yazdır**
print(f"""
✅ API Değerleri Yüklendi:
🔹 Binance Testnet: {'Aktif' if BINANCE_TESTNET else 'Kapalı'}
🔹 Varsayılan Kaldıraç: {DEFAULT_LEVERAGE}x
🔹 Stop Loss: %{STOP_LOSS_PERCENT * 100}
🔹 Take Profit: %{TAKE_PROFIT_PERCENT * 100}
""")
