import os
import logging
from datetime import datetime, time
import pytz
from telegram import (
    Update, InlineKeyboardButton, InlineKeyboardMarkup, BotCommand
)
from telegram.ext import (
    Application, CommandHandler, MessageHandler,
    filters, ContextTypes, CallbackQueryHandler
)
from dotenv import load_dotenv

load_dotenv()

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

BOT_TOKEN = os.getenv('BOT_TOKEN')
ADMIN_ID = os.getenv('ADMIN_ID')
TIMEZONE = pytz.timezone('Asia/Phnom_Penh')  # Cambodia time

# Active hours (Cambodia Time)
ACTIVE_START = time(8, 0)
ACTIVE_END = time(23, 0)

user_data = {}

def is_active_hours():
    return ACTIVE_START <= datetime.now(TIMEZONE).time() <= ACTIVE_END

def now_str():
    return datetime.now(TIMEZONE).strftime("%d/%m/%Y • %I:%M %p")

# ---------- MENU ----------
async def main_menu():
    keyboard = [
        [InlineKeyboardButton("📅 ការប្រកួតថ្ងៃនេះ", callback_data='fights'),
         InlineKeyboardButton("🏆 ផ្សាយផ្ទាល់", callback_data='live')],
        [InlineKeyboardButton("📊 លទ្ធផល", callback_data='results'),
         InlineKeyboardButton("🎥 មើលផ្សាយផ្ទាល់", callback_data='watch')],
        [InlineKeyboardButton("💬 ចូលរួមក្រុម", callback_data='community'),
         InlineKeyboardButton("📞 ទំនាក់ទំនង", callback_data='contact')],
    ]
    return InlineKeyboardMarkup(keyboard)

# ---------- COMMANDS ----------
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    if user.id not in user_data:
        user_data[user.id] = {
            'name': user.first_name,
            'username': user.username,
            'joined': now_str()
        }

    text = f"""
🐓 *សូមស្វាគមន៍មកកាន់ SABONG24-បក្សីកីឡា!* 🐓

សួស្តី {user.first_name}! អ្នកបានភ្ជាប់ទៅកាន់មជ្ឈមណ្ឌលបក្សីកីឡាដ៏អស្ចារ្យ។

*អ្វីដែលអ្នកទទួលបាន:*
📅 កាលវិភាគប្រកួតប្រចាំថ្ងៃ
🏆 ព័ត៌មានផ្សាយផ្ទាល់
📊 លទ្ធផលភ្លាមៗ
🎥 តំណភ្ជាប់ផ្សាយផ្ទាល់
💬 ការចូលរួមក្រុម

🕐 *ស្ថានភាព:* {'🟢 កំពុងដំណើរការ' if is_active_hours() else '🟡 បើកនៅម៉ោង ៨:០០ ព្រឹក'}

សូមជ្រើសរើសជម្រើសខាងក្រោម 👇
"""
    await update.message.reply_text(
        text, reply_markup=await main_menu(), parse_mode='Markdown'
    )

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = """
📖 *ពាក្យបញ្ជា SABONG24-បក្សីកីឡា*

/start – ម៉ឺនុយមេ
/fights – ការប្រកួតថ្ងៃនេះ
/live – ផ្សាយផ្ទាល់
/results – លទ្ធផលចុងក្រោយ
/watch – តំណភ្ជាប់ផ្សាយ
/community – ចូលរួមក្រុម
/contact – ទំនាក់ទំនង
/help – ជំនួយ

💡 សូមចុចប៊ូតុងម៉ឺនុយបានគ្រប់ពេល!
"""
    await update.message.reply_text(text, parse_mode='Markdown')

async def fights(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = f"""
📅 *ការប្រកួតថ្ងៃនេះ*
_{now_str()}_

🏟️ *កម្មវិធីចម្បង — ពហុកីឡដ្ឋានភ្នំពេញ*
🕐 ១:០០ រសៀល — ដេរី ៥ ជុំ
🕐 ៤:០០ រសៀល — ជុំជើងឯក

🏟️ *កម្មវិធីបន្ថែម — ស្តាតអូឡាំពិក*
🕐 ២:៣០ រសៀល — ដេរី ៣ ជុំ

📌 កាលវិភាគធ្វើបច្ចុប្បន្នភាពរៀងរាល់ម៉ោង។
ចុច 🔔 ដើម្បីទទួលការជូនដំណឹង។
"""
    kb = [[InlineKeyboardButton("🔔 ជូនដំណឹងខ្ញុំ", callback_data='notify'),
           InlineKeyboardButton("🎥 មើល", callback_data='watch')],
          [InlineKeyboardButton("⬅️ ត្រឡប់", callback_data='menu')]]
    await update.message.reply_text(text, reply_markup=InlineKeyboardMarkup(kb), parse_mode='Markdown')

async def live(update: Update, context: ContextTypes.DEFAULT_TYPE):
    status = "🟢 កំពុងផ្សាយ" if is_active_hours() else "🟡 បិទផ្សាយ"
    text = f"""
🏆 *ការផ្សាយផ្ទាល់*

{status}

🔴 *ពហុកីឡដ្ឋានភ្នំពេញ* — ជុំទី ៣
👥 អ្នកទស្សនា ១២,៤០០ នាក់

🔴 *ស្តាតអូឡាំពិក* — កម្មវិធីចម្បង
👥 អ្នកទស្សនា ៨,២០០ នាក់

⚠️ ការផ្សាយបើក ១៥ នាទីមុនពេលប្រកួត។
"""
    kb = [[InlineKeyboardButton("🎥 មើលផ្សាយផ្ទាល់", callback_data='watch')],
          [InlineKeyboardButton("⬅️ ត្រឡប់", callback_data='menu')]]
    await update.message.reply_text(text, reply_markup=InlineKeyboardMarkup(kb), parse_mode='Markdown')

async def results(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = """
📊 *លទ្ធផលចុងក្រោយ*

🥇 *ប្រកួតទី ១២* — មាន់ក្រហម ឈ្នះ មាន់ខៀវ
⏱️ ជុំទី ២ • ៤:១២

🥇 *ប្រកួតទី ១១* — ផ្គរលាន់ ឈ្នះ ពស់ខ្មៅ
⏱️ ជុំទី ១ • ២:៤៥

🥇 *ប្រកួតទី ១០* — ឥន្ទ្រីមាស ឈ្នះ កញ្ជ្រោងប្រាក់
⏱️ ជុំទី ៣ • ៦:៣០

_បច្ចុប្បន្នភាពប៉ុន្មានវិនាទីមុន។_
"""
    kb = [[InlineKeyboardButton("🔄 ធ្វើបច្ចុប្បន្នភាព", callback_data='results')],
          [InlineKeyboardButton("⬅️ ត្រឡប់", callback_data='menu')]]
    await update.message.reply_text(text, reply_markup=InlineKeyboardMarkup(kb), parse_mode='Markdown')

async def watch(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = """
🎥 *មើលផ្សាយផ្ទាល់*

ជ្រើសរើសវេទិការបស់អ្នក:

▶️ [ផ្សាយ ១ – HD](https://example.com/stream1)
▶️ [ផ្សាយ ២ – បម្រុង](https://example.com/stream2)
▶️ [Facebook Live](https://facebook.com/example)
▶️ [YouTube Live](https://youtube.com/example)

📶 ដំបូន្មាន: ប្រើ Wi-Fi សម្រាប់ការមើលរលូន។
"""
    kb = [[InlineKeyboardButton("⬅️ ត្រឡប់", callback_data='menu')]]
    await update.message.reply_text(
        text, reply_markup=InlineKeyboardMarkup(kb),
        parse_mode='Markdown', disable_web_page_preview=True
    )

async def community(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = """
💬 *ចូលរួមក្រុមរបស់យើង*

• [ក្រុមមេ](https://t.me/yourgroup)
• [ឆានែលផ្សព្វផ្សាយ](https://t.me/yourchannel)
• [ទំព័រ Facebook](https://facebook.com/yourpage)

តាមដានរាល់ការប្រកួត! 🐓
"""
    kb = [[InlineKeyboardButton("⬅️ ត្រឡប់", callback_data='menu')]]
    await update.message.reply_text(
        text, reply_markup=InlineKeyboardMarkup(kb),
        parse_mode='Markdown', disable_web_page_preview=True
    )

async def contact(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = """
📞 *ទំនាក់ទំនង SABONG24-បក្សីកីឡា*

• ជំនួយ: @your_username
• អ៊ីមែល: support@sabong24.com
• ម៉ោង: ៨:០០ ព្រឹក – ១១:០០ យប់

យើងឆ្លើយតបក្នុងរយៈពេលប៉ុន្មាននាទី! ⚡
"""
    kb = [[InlineKeyboardButton("⬅️ ត្រឡប់", callback_data='menu')]]
    await update.message.reply_text(text, reply_markup=InlineKeyboardMarkup(kb), parse_mode='Markdown')

# ---------- TEXT HANDLER ----------
async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    msg = update.message.text.lower()

    if not is_active_hours():
        await update.message.reply_text(
            "🌙 *SABONG24-បក្សីកីឡា កំពុងសម្រាក។*\n\n"
            "យើងបើកម្តងទៀតនៅ *៨:០០ ព្រឹក*។\n"
            "សូមប្រើប៊ូតុងម៉ឺនុយដើម្បីមើលកាលវិភាគ និងលទ្ធផល។",
            parse_mode='Markdown'
        )
        return

    if any(w in msg for w in ['hi', 'hello', 'hey', 'សួស្តី', 'ជំរាបសួរ']):
        reply = "🐓 សូមស្វាគមន៍មកកាន់ SABONG24-បក្សីកីឡា! ចុច /start ដើម្បីមើលម៉ឺនុយ។"
    elif any(w in msg for w in ['fight', 'schedule', 'ប្រកួត', 'កាលវិភាគ']):
        reply = "📅 ពិនិត្យ /fights សម្រាប់ការប្រកួតថ្ងៃនេះ!"
    elif any(w in msg for w in ['live', 'watch', 'ផ្សាយ', 'មើល']):
        reply = "🎥 ចុច /watch សម្រាប់តំណផ្សាយផ្ទាល់។"
    elif any(w in msg for w in ['result', 'លទ្ធផល']):
        reply = "📊 ចុច /results សម្រាប់លទ្ធផលចុងក្រោយ។"
    elif any(w in msg for w in ['price', 'fee', 'តម្លៃ', 'ថ្លៃ']):
        reply = "💰 សម្រាប់តម្លៃ និងការចុះឈ្មោះ សូមទាក់ទង @your_username។"
    else:
        reply = (
            "🐓 ខ្ញុំបានទទួលសាររបស់អ្នក!\n\n"
            "សូមសាកល្បង /fights, /live, /results ឬ /watch។"
        )
    await update.message.reply_text(reply, parse_mode='Markdown')

# ---------- BUTTONS ----------
async def button_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    q = update.callback_query
    await q.answer()
    data = q.data

    if data == 'menu':
        await q.edit_message_text(
            "🐓 *ម៉ឺនុយមេ SABONG24-បក្សីកីឡា*\nសូមជ្រើសរើសជម្រើស 👇",
            reply_markup=await main_menu(), parse_mode='Markdown'
        )
    elif data == 'fights':
        await q.edit_message_text("📅 ប្រើ /fights សម្រាប់កាលវិភាគថ្ងៃនេះ។", parse_mode='Markdown')
    elif data == 'live':
        await q.edit_message_text("🏆 ប្រើ /live សម្រាប់ការផ្សាយបន្តបន្ទាប់។", parse_mode='Markdown')
    elif data == 'results':
        await q.edit_message_text("📊 ប្រើ /results សម្រាប់លទ្ធផលចុងក្រោយ។", parse_mode='Markdown')
    elif data == 'watch':
        await q.edit_message_text("🎥 ប្រើ /watch សម្រាប់ការផ្សាយ។", parse_mode='Markdown')
    elif data == 'community':
        await q.edit_message_text("💬 ប្រើ /community ដើម្បីចូលរួម។", parse_mode='Markdown')
    elif data == 'contact':
        await q.edit_message_text("📞 ប្រើ /contact សម្រាប់ជំនួយ។", parse_mode='Markdown')
    elif data == 'notify':
        await q.edit_message_text("🔔 អ្នកបានជាវ! អ្នកនឹងទទួលការជូនដំណឹងប្រកួត។", parse_mode='Markdown')

# ---------- ERROR ----------
async def error_handler(update, context):
    logger.warning(f"Update {update} caused error {context.error}")

# ---------- MAIN ----------
async def post_init(app: Application):
    await app.bot.set_my_commands([
        BotCommand("start", "🏠 ម៉ឺនុយមេ"),
        BotCommand("fights", "📅 ការប្រកួតថ្ងៃនេះ"),
        BotCommand("live", "🏆 ផ្សាយផ្ទាល់"),
        BotCommand("results", "📊 លទ្ធផលចុងក្រោយ"),
        BotCommand("watch", "🎥 មើលផ្សាយ"),
        BotCommand("community", "💬 ចូលរួមក្រុម"),
        BotCommand("contact", "📞 ទំនាក់ទំនង"),
        BotCommand("help", "📖 ជំនួយ"),
    ])

def main():
    app = (Application.builder()
           .token(BOT_TOKEN)
           .post_init(post_init)
           .build())

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("help", help_command))
    app.add_handler(CommandHandler("fights", fights))
    app.add_handler(CommandHandler("live", live))
    app.add_handler(CommandHandler("results", results))
    app.add_handler(CommandHandler("watch", watch))
    app.add_handler(CommandHandler("community", community))
    app.add_handler(CommandHandler("contact", contact))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    app.add_handler(CallbackQueryHandler(button_callback))
    app.add_error_handler(error_handler)

    logger.info("🐓 SABONG24-បក្សីកីឡា bot starting...")
    app.run_polling(allowed_updates=Update.ALL_TYPES)

if __name__ == '__main__':
    main()
