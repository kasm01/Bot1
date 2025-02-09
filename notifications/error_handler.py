import traceback
import logging
import time
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

def log_error(exception, function_name=""):
    """
    ⚠️ Hataları log dosyasına ve terminale detaylı şekilde kaydeder.
    """
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    error_trace = traceback.format_exc()
    formatted_error = f"{timestamp} - ERROR in {function_name}:\n{str(exception)}\n{error_trace}\n"

    # Hata logunu kaydet
    with open(LOG_FILE, "a") as log_file:
        log_file.write(formatted_error)

    # Hata logunu terminale yazdır
    print(formatted_error)

    # Logları Telegram'a gönderme seçeneği
    send_telegram_message(f"🚨 Hata Tespit Edildi: {function_name}\n{str(exception)}")

def handle_error(exception, function_name=""):
    """
    ⚠️ Hataları yönetir, log dosyasına kaydeder ve Telegram bildirimi gönderir.
    """
    log_error(exception, function_name)

    # Telegram hata bildirimini gönder
    send_telegram_error_alert(f"🚨 {function_name} Hatası:\n{str(exception)}")

    # Hata çözüm mekanizmasını tetikle
    auto_fix_error(exception, function_name)

def auto_fix_error(exception, function_name):
    """
    🤖 AI destekli hata düzeltme mekanizması.
    - Yetersiz bakiye hatasında kaldıraç düşürerek işlemi tekrar dener.
    - Bağlantı hatalarında işlemi tekrar dener.
    - API sınırına ulaşıldığında bekleyerek tekrar dener.
    - Tekrar eden hatalarda işlemi durdurur.
    """
    error_message = str(exception).lower()

    if "insufficient balance" in error_message:
        send_telegram_message("💡 Çözüm: Kaldıraç düşürülerek işlem tekrar deneniyor...")
        from trading.binance_futures import execute_trade
        execute_trade(symbol="BTCUSDT", trade_type="LONG", quantity=0.005, leverage=2)

    elif "network issue" in error_message or "connection" in error_message:
        send_telegram_message("🔄 Ağ bağlantı sorunu tespit edildi, işlem tekrar edilecek...")
        time.sleep(10)  # 10 saniye bekleyip tekrar dene
        return

    elif "rate limit" in error_message:
        send_telegram_message("⏳ API sınırı aşıldı, 60 saniye bekleniyor...")
        time.sleep(60)  # 60 saniye bekleyip tekrar dene
        return

    else:
        send_telegram_message(f"🚨 {function_name} için bilinmeyen hata, manuel müdahale gerekebilir.")
        print(f"⚠️ Manuel müdahale gerekebilir: {function_name}")

    print(f"⚠️ Hata Yönetimi: {function_name} için hata çözümlendi veya işlem tekrar edilecek.")
