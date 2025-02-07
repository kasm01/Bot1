import requests
import json
from config.config import TELEGRAM_BOT_TOKEN, TELEGRAM_CHAT_ID

TELEGRAM_API_URL = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"

def send_telegram_message(message):
    """
    📢 Telegram API ile ücretsiz mesaj gönderir.
    """
    try:
        data = {"chat_id": TELEGRAM_CHAT_ID, "text": message, "parse_mode": "HTML"}
        response = requests.post(TELEGRAM_API_URL, data=data)
        
        if response.status_code != 200:
            print(f"⚠️ Telegram mesajı gönderilemedi: {response.text}")
    except Exception as e:
        print(f"⚠️ Telegram bağlantı hatası: {str(e)}")


def send_telegram_trade_alert(symbol, trade_type, quantity, leverage, price, stop_loss, take_profit):
    """
    📈 AI destekli alım-satım işlemi gerçekleştiğinde Telegram'a bildirim gönderir.
    """
    message = (
        f"🚀 <b>İŞLEM GERÇEKLEŞTİ!</b>\n"
        f"📌 <b>Parite:</b> {symbol}\n"
        f"📈 <b>İşlem:</b> {trade_type}\n"
        f"💰 <b>Miktar:</b> {quantity}\n"
        f"⚡ <b>Kaldıraç:</b> {leverage}x\n"
        f"💲 <b>Giriş Fiyatı:</b> {price}\n"
        f"🛑 <b>Stop-Loss:</b> {stop_loss}\n"
        f"🎯 <b>Take-Profit:</b> {take_profit}"
    )
    send_telegram_message(message)


def send_telegram_error_alert(error_message):
    """
    ⚠️ Bot hata aldığında Telegram'a bildirim gönderir.
    """
    message = f"⚠️ <b>BOT HATASI:</b>\n{error_message}"
    send_telegram_message(message)


def send_telegram_confirmation_request(action_type):
    """
    📩 Kullanıcıdan manuel işlem için onay ister (Alım/Satım veya Hata Düzeltme).
    """
    message = (
        f"📩 <b>ONAY GEREKLİ</b>\n"
        f"⚡ İşlem: {action_type}\n"
        f"✅ Kabul etmek için: /onayla\n"
        f"❌ Reddetmek için: /iptal"
    )
    send_telegram_message(message)


def send_telegram_daily_report(profit, loss, trade_count):
    """
    📊 Günlük kar-zarar raporunu Telegram'a gönderir.
    """
    message = (
        f"📅 <b>GÜNLÜK RAPOR</b>\n"
        f"💰 <b>Kâr:</b> {profit} USDT\n"
        f"🔻 <b>Zarar:</b> {loss} USDT\n"
        f"📊 <b>İşlem Sayısı:</b> {trade_count}"
    )
    send_telegram_message(message)


def send_telegram_weekly_report(profit, loss, trade_count):
    """
    📊 Haftalık kar-zarar raporunu Telegram'a gönderir.
    """
    message = (
        f"📅 <b>HAFTALIK RAPOR</b>\n"
        f"💰 <b>Kâr:</b> {profit} USDT\n"
        f"🔻 <b>Zarar:</b> {loss} USDT\n"
        f"📊 <b>İşlem Sayısı:</b> {trade_count}"
    )
    send_telegram_message(message)
