import telebot
import json
import os
import random
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton, ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove

TOKEN = "7304434908:AAFXo_YtZHpyWoOEPmTOLq0GNRWdkStI1i4"
bot = telebot.TeleBot(TOKEN)

DATA_FILE = "data.json"

def load_data():
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, "r") as f:
            return json.load(f)
    return {}

def save_data(data):
    with open(DATA_FILE, "w") as f:
        json.dump(data, f)

@bot.message_handler(commands=['start'])
def start(message):
    user_id = str(message.from_user.id)
    data = load_data()
    if user_id not in data:
        data[user_id] = {"tokens": 100, "cards": []}
        save_data(data)
        bot.reply_to(message, "👋 Salom! Sizga 100 token berildi.")
    else:
        bot.reply_to(message, "🔁 Siz allaqachon ro'yxatdan o'tgansiz.")

@bot.message_handler(commands=['balance'])
def balance(message):
    user_id = str(message.from_user.id)
    data = load_data()
    tokens = data.get(user_id, {}).get("tokens", 0)
    bot.reply_to(message, f"💰 Sizda {tokens} token bor.")

@bot.message_handler(commands=['giveto'])
def giveto(message):
    user_id = str(message.from_user.id)
    data = load_data()
    try:
        parts = message.text.split()
        if len(parts) != 3:
            raise ValueError("❗ Format: /giveto USER_ID MIQDOR")
        target_id = parts[1]
        amount = int(parts[2])
        if amount <= 0:
            raise ValueError("⚠️ Miqdor musbat bo‘lishi kerak.")
        if data.get(user_id, {}).get("tokens", 0) < amount:
            raise ValueError("💸 Sizda yetarli token yo‘q.")
        if target_id not in data:
            data[target_id] = {"tokens": 0, "cards": []}
        data[user_id]["tokens"] -= amount
        data[target_id]["tokens"] += amount
        save_data(data)
        bot.send_message(message.chat.id, f"✅ {amount} token {target_id} foydalanuvchiga yuborildi.")
    except Exception as e:
        bot.send_message(message.chat.id, str(e))

@bot.message_handler(commands=['packmenu'])
def pack_menu(message):
    markup = InlineKeyboardMarkup()
    markup.row(
        InlineKeyboardButton("📦 Rare (50💰)", callback_data="rare_pack"),
        InlineKeyboardButton("💎 Diamond (100💰)", callback_data="diamond_pack")
    )
    markup.row(
        InlineKeyboardButton("🔥 Legendary (200💰)", callback_data="legendary_pack"),
        InlineKeyboardButton("🌌 Mythic (300💰)", callback_data="mythic_pack")
    )
    markup.row(
        InlineKeyboardButton("🐐 GOAT (500💰)", callback_data="goat_pack")
    )
    bot.send_message(message.chat.id, "⬇ Qaysi packni ochmoqchisiz?", reply_markup=markup)

@bot.callback_query_handler(func=lambda call: call.data.endswith("_pack"))
def handle_pack(call):
    user_id = str(call.from_user.id)
    data = load_data()

    if user_id not in data:
        data[user_id] = {"tokens": 100, "cards": []}

    if len(data[user_id]["cards"]) >= 15:
        bot.answer_callback_query(call.id, "❌ Kolleksiya to‘la. Avval karta o‘chiring.", show_alert=True)
        return

    packs = {
        "rare_pack": {"price": 50, "cards": ["Zirkzee CF 81", "Eze AMF 81", "Isak CF 83", "David CF 81", "Grimaldo LB 81",
                                             "Doku RWF 83", "Kulusevski RWF 83", "Palhinha DMF 82", "Szoboszlai CMF 85",
                                             "João Pedro CF 83", "Paqueta AMF 84", "Emiliano GK 84", "Musiala AMF 86",
                                             "Mendy LB 84", "Beto CF 80"]},
        "diamond_pack": {"price": 100, "cards": ["Rodri DMF 86", "Saka RWF 85", "Odegaard AMF 85", "T. Hernandez LB 84",
                                                 "Alisson GK 86", "Valverde CMF 87", "Nkunku CF 86", "Bernardo Silva CMF 87",
                                                 "Kvaratskhelia LWF 87", "Maignan GK 86", "Gvardiol CB 86", "Trent RWB 86",
                                                 "De Jong CMF 85", "James RB 84", "Kane CF 87"]},
        "legendary_pack": {"price": 200, "cards": ["Mbappe CF 93", "Messi RWF 94", "Ronaldo CF 95", "Haaland CF 93",
                                                   "Neymar LWF 93", "Modric CMF 93", "De Bruyne AMF 92", "Vinicius Jr LWF 94",
                                                   "Bellingham CMF 94", "Griezmann SS 93", "Casemiro DMF 92", "Ter Stegen GK 93",
                                                   "Kimmich DMF 93", "Van Dijk CB 93", "Salah RWF 92"]},
        "mythic_pack": {"price": 300, "cards": ["Totti CF 98", "Pirlo CMF 98", "Iniesta CMF 97", "Xavi CMF 97",
                                                "Roberto Carlos LB 99", "R9 Ronaldo CF 99", "Ronaldinho AMF 100", "Zidane AMF 100",
                                                "Maldini CB 100", "Ibrahimovic CF 98", "Baggio AMF 98", "Schweinsteiger CMF 98",
                                                "Kaka AMF 100", "Cannavaro CB 99", "Puyol CB 99"]},
        "goat_pack": {"price": 500, "cards": ["🐐 Pelé CF 107", "🔱 Maradona AMF 106", "🧙‍♂️ Messi RWF 107", "🦁 Ronaldo CF 109",
                                              "👑 Zidane AMF 107", "⚡ R9 Ronaldo CF 106", "🎩 Ronaldinho AMF 107",
                                              "🛡️ Beckenbauer CB 106", "🌀 Cruyff SS 106", "🧠 Platini AMF 106",
                                              "🧭 Xavi CMF 105", "🎯 Iniesta CMF 105", "🚀 Roberto Carlos LB 106",
                                              "🧤 Lev Yashin GK 108", "🦅 George Best LWF 107"]}
    }

    selected = packs[call.data]
    if data[user_id]["tokens"] < selected["price"]:
        bot.answer_callback_query(call.id, "💸 Yetarli token yo‘q!", show_alert=True)
        return

    card = random.choice(selected["cards"])
    if card in data[user_id]["cards"]:
        bot.send_message(call.message.chat.id, f"🃏 {card} sizda allaqachon mavjud!")
    else:
        data[user_id]["cards"].append(card)
        data[user_id]["tokens"] -= selected["price"]
        save_data(data)
        bot.send_message(call.message.chat.id, f"🎴 Sizga {card} tushdi!")

    bot.answer_callback_query(call.id)

@bot.message_handler(commands=['collection'])
def collection(message):
    user_id = str(message.from_user.id)
    data = load_data()
    cards = data.get(user_id, {}).get("cards", [])
    if cards:
        text = "📚 Sizda yig'ilgan kartalar:\n" + "\n".join(f"- {c}" for c in cards)
    else:
        text = "📭 Sizda hali hech qanday karta yo‘q."
    bot.send_message(message.chat.id, text)

@bot.message_handler(commands=['remove'])
def remove_card(message):
    user_id = str(message.from_user.id)
    data = load_data()
    cards = data.get(user_id, {}).get("cards", [])
    if not cards:
        bot.reply_to(message, "📭 Sizda hech qanday karta yo‘q.")
        return
    markup = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    for c in cards:
        markup.add(KeyboardButton(c))
    msg = bot.send_message(message.chat.id, "🗑 Qaysi kartani o‘chirmoqchisiz?", reply_markup=markup)
    bot.register_next_step_handler(msg, process_remove_card, user_id)

def process_remove_card(message, user_id):
    card = message.text.strip()
    data = load_data()
    if card in data[user_id]["cards"]:
        data[user_id]["cards"].remove(card)
        save_data(data)
        bot.send_message(message.chat.id, f"✅ {card} o‘chirildi.", reply_markup=ReplyKeyboardRemove())
    else:
        bot.send_message(message.chat.id, "❌ Bunday karta topilmadi.", reply_markup=ReplyKeyboardRemove())

@bot.message_handler(commands=['match'])
def match_menu(message):
    user_id = str(message.from_user.id)
    data = load_data()
    if len(data[user_id].get("cards", [])) < 7:
        bot.reply_to(message, "⚠️ Kamida 7 ta karta kerak.")
        return
    markup = InlineKeyboardMarkup()
    markup.row(
        InlineKeyboardButton("⚽ Match 100 (yutuq: 100)", callback_data="match_100"),
        InlineKeyboardButton("🏆 Match 200 (yutuq: 200)", callback_data="match_200")
    )
    markup.row(
        InlineKeyboardButton("🔥 Match 500 (yutuq: 500)", callback_data="match_500")
    )
    bot.send_message(message.chat.id, "⚔ Qaysi matchni o‘ynaysiz?", reply_markup=markup)

@bot.callback_query_handler(func=lambda call: call.data.startswith("match_"))
def handle_match(call):
    user_id = str(call.from_user.id)
    data = load_data()

    prices = {"100": (0, 100), "200": (0, 200), "500": (200, 500)}
    mtype = call.data.split("_")[1]
    price, reward = prices.get(mtype, (0, 0))

    if len(data[user_id].get("cards", [])) < 7:
        bot.answer_callback_query(call.id, "❌ Kamida 7 ta karta kerak!", show_alert=True)
        return
    if data[user_id]["tokens"] < price:
        bot.answer_callback_query(call.id, "💸 Yetarli token yo‘q!", show_alert=True)
        return

    data[user_id]["tokens"] -= price
    win = random.choice([True, False])
    if win:
        data[user_id]["tokens"] += reward
        msg = f"🎉 G‘alaba! {reward} token yutdingiz!"
    else:
        msg = f"😓 Yutqazdingiz. {price} token ketdi."
    save_data(data)
    bot.send_message(call.message.chat.id, msg)
    bot.answer_callback_query(call.id, "Match yakunlandi.")

# === Botni ishga tushirish ===
print("✅ Bot ishga tushdi...")
bot.infinity_polling()