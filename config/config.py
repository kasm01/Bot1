import os
from dotenv import load_dotenv

# .env dosyasını yükle
load_dotenv()

# Binance API Bilgileri
BINANCE_API_KEY = os.getenv("BINANCE_API_KEY")
BINANCE_API_SECRET = os.getenv("BINANCE_API_SECRET")
BINANCE_TESTNET = os.getenv("BINANCE_TESTNET", "True").lower() == "true"

# Telegram API Bilgileri
TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
TELEGRAM_CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")

# API Servisleri
CRYPTOCOMPARE_API_KEY = os.getenv("CRYPTOCOMPARE_API_KEY")
COINMARKETCAP_API_KEY = os.getenv("COINMARKETCAP_API_KEY")
ETHERSCAN_API_KEY = os.getenv("ETHERSCAN_API_KEY")
SANTIMENT_API_KEY = os.getenv("SANTIMENT_API_KEY")

# Varsayılan İşlem Ayarları
DEFAULT_LEVERAGE = int(os.getenv("DEFAULT_LEVERAGE", 5))
STOP_LOSS_PERCENT = float(os.getenv("STOP_LOSS_PERCENT", 0.02))
TAKE_PROFIT_PERCENT = float(os.getenv("TAKE_PROFIT_PERCENT", 0.05))
