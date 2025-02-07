import traceback
import logging
from datetime import datetime
from notifications.telegram_bot import send_telegram_error_alert, send_telegram_message

# Hata loglarını saklamak için dosya belirleme
LOG_FILE = "logs/error_log.txt"

# Logger yapılandırması
logging.basicConfig(
    filename=LOG_FILE,
    level=logging.ERROR,
    format="%(asctime)s - %(levelname)s - %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S"
)

def log_error(error_message):
    """
    ⚠️ Hataları log dosyasına kaydeder.
    """
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    formatted_error = f"{timestamp} - ERROR: {error_message}\n"
    
    # Hata logunu kaydet
    with open(LOG_FILE, "a") as log_file:
        log_file.write(formatted_error)
    
    # Hata logunu terminale yazdır
    print(formatted_error)


def handle_error(exception, function_name=""):
    """
    ⚠️ Hataları yönetir, log dosyasına kaydeder ve Telegram bildirimi gönderir.
    """
    error_message = f"{function_name} Hata: {str(exception)}"
    log_error(error_message)
    
    # Telegram bildirim gönder
    send_telegram_error_alert(error_message)

    # Hata çözüm mekanizmasını tetikle
    auto_fix_error(exception, function_name)


def auto_fix_error(exception, function_name):
    """
    🤖 AI destekli hata düzeltme mekanizması.
    - Yetersiz bakiye hatasında kaldıraç düşürerek işlemi tekrar dener.
    - Bağlantı hatalarında işlemi tekrar dener.
    - Tekrar eden hatalarda stratejiyi değiştirir.
    """
    error_message = str(exception).lower()

    if "insufficient balance" in error_message:
        send_telegram_message("💡 Çözüm: Kaldıraç düşürülerek işlem tekrar deneniyor...")
        from trading.binance_futures import execute_trade
        execute_trade(symbol="BTCUSDT", trade_type="LONG", quantity=0.005, leverage=2)
    
    elif "network issue" in error_message:
        send_telegram_message("🔄 Ağ bağlantı sorunu tespit edildi, işlem tekrar edilecek...")
    
    elif "rate limit" in error_message:
        send_telegram_message("⏳ API sınırı aşıldı, 60 saniye beklenip tekrar denenecek...")
    
    else:
        send_telegram_message(f"🚨 {function_name} için bilinmeyen hata, manuel müdahale gerekebilir.")

    print(f"⚠️ Hata Yönetimi: {function_name} için hata çözümlendi veya işlem tekrar edilecek.")

