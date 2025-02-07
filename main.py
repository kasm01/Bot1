import threading
import numpy as np
from websocket.websocket_handler import start_websocket
from data_fetch.binance_api import get_binance_ta
from ai_models.lstm_model import train_lstm_model, predict_price_lstm
from ai_models.reinforcement_trading import reinforcement_trade
from ai_models.sentiment_analysis import get_news_sentiment
from risk_management.stop_loss import calculate_stop_loss
from risk_management.take_profit import calculate_take_profit
from risk_management.leverage_manager import dynamic_leverage
from risk_management.hedging_strategies import optimized_hedging
from trading.binance_futures import execute_trade_safe
from notifications.telegram_bot import send_telegram_message
from error_handler import handle_error

if __name__ == "__main__":
    print("🚀 AI Destekli Binance Futures Botu Başlatılıyor...")

    # WebSocket işlemini başlat
    ws_thread = threading.Thread(target=start_websocket)
    ws_thread.start()

    try:
        # Binance API'den piyasa verilerini al
        prices = get_binance_ta()
        entry_price = prices[-1]
        market_volatility = np.random.uniform(0.01, 0.05)  # Simüle edilen volatilite

        # AI destekli fiyat tahmini
        lstm_model, lstm_scaler = train_lstm_model(prices)
        predicted_price = predict_price_lstm(lstm_model, lstm_scaler, prices[-60:])

        # AI destekli piyasa analizi (Reinforcement Learning)
        ai_trade_decision = reinforcement_trade()

        # Piyasa duyarlılığı analizi (Sentiment Analysis)
        sentiment = get_news_sentiment()

        # AI destekli stop-loss & take-profit hesapla
        stop_loss = calculate_stop_loss(entry_price, market_volatility)
        take_profit = calculate_take_profit(entry_price, market_volatility)

        # AI destekli kaldıraç yönetimi
        leverage = dynamic_leverage(market_volatility)

        # AI destekli hedge mekanizması
        optimized_hedging(entry_price, market_volatility)

        # AI destekli işlem açma
        trade_type = "LONG" if ai_trade_decision == "Bullish" else "SHORT"
        execute_trade_safe(symbol="BTCUSDT", trade_type=trade_type, quantity=0.01, leverage=leverage)

        # Telegram bildirimleri
        send_telegram_message(
            f"📈 AI Tahmini: {predicted_price} USD | AI Kararı: {trade_type} | Sentiment: {sentiment} | "
            f"Kaldıraç: {leverage}x | SL: {stop_loss} USD | TP: {take_profit} USD"
        )

    except Exception as e:
        handle_error(e, function_name="main.py")

