from telegram import Update, KeyboardButton, ReplyKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes, ConversationHandler

# O'zgartiriladigan qism
BOT_TOKEN = "7781741863:AAG0wwifRXAV-n9lR0mOlJiKsv9_A-B-fAU"
ADMIN_ID = 6407669938  # bu yerga o‘zingning Telegram user ID'ingni yoz

# Bosqichlar
LANGUAGE, GET_CONTACT = range(2)

# /start komandasi
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.message.from_user

    if user.username:
        # Username mavjud — admin ga yubor
        await context.bot.send_message(
            chat_id=ADMIN_ID,
            text=f"Foydalanuvchi: @{user.username} (ID: {user.id})"
        )
        await update.message.reply_text("Raxmat, sizda username bor. Bot to‘xtadi.")
        return ConversationHandler.END
    else:
        # Username yo‘q — til tanlash
        buttons = [
            ["Uzbek"], ["English"], ["Russian"]
        ]
        markup = ReplyKeyboardMarkup(buttons, resize_keyboard=True, one_time_keyboard=True)
        await update.message.reply_text("Iltimos, tilni tanlang:", reply_markup=markup)
        return LANGUAGE

# Til tanlangach
async def choose_language(update: Update, context: ContextTypes.DEFAULT_TYPE):
    # Endi kontakt tugmasini yuboramiz
    contact_btn = KeyboardButton("Telefon raqamni yuborish", request_contact=True)
    markup = ReplyKeyboardMarkup([[contact_btn]], resize_keyboard=True, one_time_keyboard=True)
    await update.message.reply_text("Iltimos, telefon raqamingizni yuboring:", reply_markup=markup)
    return GET_CONTACT

# Kontakt qabul qilinadi
async def get_contact(update: Update, context: ContextTypes.DEFAULT_TYPE):
    contact = update.message.contact
    user = update.message.from_user

    phone_number = contact.phone_number
    first_name = user.first_name
    user_id = user.id

    # Admin ga yuborish
    await context.bot.send_message(
        chat_id=ADMIN_ID,
        text=f"Yangi foydalanuvchi:\nIsmi: {first_name}\nID: {user_id}\nTelefon: {phone_number}"
    )

    await update.message.reply_text("Raxmat! Ma'lumot qabul qilindi.")
    return ConversationHandler.END

# Noma'lum xabar
async def cancel(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Jarayon bekor qilindi.")
    return ConversationHandler.END

# Botni ishga tushirish
app = ApplicationBuilder().token(BOT_TOKEN).build()

conv_handler = ConversationHandler(
    entry_points=[CommandHandler("start", start)],
    states={
        LANGUAGE: [MessageHandler(filters.TEXT & ~filters.COMMAND, choose_language)],
        GET_CONTACT: [MessageHandler(filters.CONTACT, get_contact)],
    },
    fallbacks=[MessageHandler(filters.COMMAND, cancel)]
)

app.add_handler(conv_handler)
app.run_polling()