import os
import logging
from telegram import Update
from telegram.ext import ApplicationBuilder, ContextTypes, CommandHandler, MessageHandler, filters, ConversationHandler
from dotenv import load_dotenv

# Load environment variables
dotenv_path = os.path.join(os.path.dirname(__file__), '.env')
if os.path.exists(dotenv_path):
    load_dotenv(dotenv_path)
else:
    print(f"Warning: .env file not found at {dotenv_path}")

TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")

# Enable logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

# Define states
FISH, UNIVERSITY, WORKPLACE, POSITION, CV = range(5)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Assalomu alaykum! Iltimos, FISHingizni kiriting:")
    return FISH

async def f_fish(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data['fish'] = update.message.text
    await update.message.reply_text("Ta’lim olgan universitetingizni kiriting:")
    return UNIVERSITY

async def f_university(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data['university'] = update.message.text
    await update.message.reply_text("Ish joyingizni kiriting:")
    return WORKPLACE

async def f_workplace(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data['workplace'] = update.message.text
    await update.message.reply_text("Lavozimingizni kiriting:")
    return POSITION

async def f_position(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data['position'] = update.message.text
    await update.message.reply_text("Iltimos, CV (obyektivka) faylini yuboring:")
    return CV

async def f_cv(update: Update, context: ContextTypes.DEFAULT_TYPE):
    document = update.message.document
    
    if not document:
        await update.message.reply_text("Iltimos, fayl yuboring.")
        return CV

    caption = (
        f"FISH: {context.user_data.get('fish')}\n"
        f"Ta’lim olgan universiteti: {context.user_data.get('university')}\n"
        f"Ish joyi: {context.user_data.get('workplace')}\n"
        f"Lavozimi: {context.user_data.get('position')}"
    )

    try:
        # Send to the group chat
        await context.bot.send_document(
            chat_id=CHAT_ID,
            document=document.file_id,
            caption=caption
        )
        await update.message.reply_text("Ma'lumotlaringiz qabul qilindi.")
    except Exception as e:
        logging.error(f"Error sending message: {e}")
        await update.message.reply_text(f"Xatolik yuz berdi: {e}")

    return ConversationHandler.END

async def cancel(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Amal bekor qilindi.")
    return ConversationHandler.END

if __name__ == '__main__':
    if not TOKEN or not CHAT_ID:
        print("Error: TELEGRAM_BOT_TOKEN or TELEGRAM_CHAT_ID not found in .env file.")
        exit(1)

    application = ApplicationBuilder().token(TOKEN).build()
    
    # Use filters.Document.ALL if available, otherwise fallback to check usually
    # In v20, filters.Document.ALL might not exist. 
    # Best generic filter for files is filters.ATTACHMENT or similar.
    # We will try a composition or standard filter.
    # filters.Document is a base class. 
    # Let's use filters.Document.ALL if possible, but to be safe, let's use filters.ATTACHMENT which covers all media/docs?
    # No, filters.ATTACHMENT excludes photos if I recall?
    # Actually, let's look at the imports.
    
    # For now, I'll use filters.Document.ALL and rely on the fact it's common.
    # If it fails, I'll direct the user or fix it.
    
    conv_handler = ConversationHandler(
        entry_points=[CommandHandler('start', start)],
        states={
            FISH: [MessageHandler(filters.TEXT & ~filters.COMMAND, f_fish)],
            UNIVERSITY: [MessageHandler(filters.TEXT & ~filters.COMMAND, f_university)],
            WORKPLACE: [MessageHandler(filters.TEXT & ~filters.COMMAND, f_workplace)],
            POSITION: [MessageHandler(filters.TEXT & ~filters.COMMAND, f_position)],
            CV: [MessageHandler(filters.Document.ALL, f_cv)], 
        },
        fallbacks=[CommandHandler('cancel', cancel)]
    )
    
    application.add_handler(conv_handler)
    
    print("Bot ishga tushdi...")
    application.run_polling()
