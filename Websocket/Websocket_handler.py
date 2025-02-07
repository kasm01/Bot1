import websocket
import json
import threading
from trading.binance_futures import execute_trade
from risk_management.leverage_manager import dynamic_leverage
from risk_management.stop_loss import calculate_dynamic_stop_loss, calculate_dynamic_take_profit
from ai_models.reinforcement_trading import reinforcement_trade
from notifications.telegram_bot import send_telegram_message

BINANCE_WS_URL = "wss://fstream.binance.com/ws/btcusdt@aggTrade"

def on_message(ws, message):
    """
    WebSocket mesajlarını işleyerek botun işlem stratejisini uygular.
    """
    data = json.loads(message)
    price = float(data["p"])  # Güncel işlem fiyatı

    # AI destekli işlem kararı
    trade_decision = reinforcement_trade()

    # AI destekli kaldıraç yönetimi
    volatility = abs(price - float(data["p"])) / price
    leverage = dynamic_leverage(volatility)

    # AI destekli stop-loss & take-profit hesaplama
    stop_loss = calculate_dynamic_stop_loss(price, volatility)
    take_profit = calculate_dynamic_take_profit(price, volatility)

    if trade_decision == "LONG":
        execute_trade("BTCUSDT", "LONG", quantity=0.01, leverage=leverage)
    elif trade_decision == "SHORT":
        execute_trade("BTCUSDT", "SHORT", quantity=0.01, leverage=leverage)

    send_telegram_message(
        f"📈 AI İşlem Kararı: {trade_decision} | Fiyat: {price} | Kaldıraç: {leverage}x"
        f"\n🛑 Stop-Loss: {stop_loss} | 🎯 Take-Profit: {take_profit}"
    )

def on_error(ws, error):
    """
    WebSocket bağlantısı sırasında hata oluşursa Telegram'a bildirir.
    """
    print(f"⚠️ WebSocket Hatası: {error}")
    send_telegram_message(f"⚠️ WebSocket Hatası: {error}")

def on_close(ws, close_status_code, close_msg):
    """
    WebSocket bağlantısı kesildiğinde log kaydı yapar ve tekrar başlatır.
    """
    print("🔌 WebSocket Bağlantısı Kapandı. Tekrar bağlanıyor...")
    send_telegram_message("🔄 WebSocket Bağlantısı Kapandı! Tekrar başlatılıyor...")
    start_websocket()

def on_open(ws):
    """
    WebSocket bağlantısı başarılı olursa log kaydı yapar.
    """
    print("✅ Binance WebSocket Bağlantısı Açıldı")
    send_telegram_message("✅ Binance WebSocket Bağlantısı Açıldı!")

def start_websocket():
    """
    Binance WebSocket bağlantısını başlatır ve sürekli çalışmasını sağlar.
    """
    while True:
        try:
            ws = websocket.WebSocketApp(
                BINANCE_WS_URL,
                on_message=on_message,
                on_error=on_error,
                on_close=on_close
            )
            ws.on_open = on_open
            ws.run_forever()
        except Exception as e:
            print(f"⚠️ WebSocket Yeniden Başlatılıyor... Hata: {e}")
            send_telegram_message(f"⚠️ WebSocket Yeniden Başlatılıyor... Hata: {e}")

# WebSocket'i ayrı bir thread içinde çalıştır
ws_thread = threading.Thread(target=start_websocket)
ws_thread.start()
