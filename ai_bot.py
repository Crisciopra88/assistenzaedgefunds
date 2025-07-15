import os
import openai
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes

openai.api_key = os.getenv("OPENAI_API_KEY")
TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
ADMIN_USER_ID = int(os.getenv("ADMIN_USER_ID"))

async def ask_openai(message):
    try:
        response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": "Rispondi in modo calmo, cortese e ragionato. Se non hai abbastanza informazioni, scrivi: 'Questa domanda va rivolta al mio umano. Ti risponderemo presto.'"},
                {"role": "user", "content": message}
            ],
            temperature=0.3
        )
        return response['choices'][0]['message']['content'].strip()
    except Exception:
        return "Non sono ancora in grado di rispondere a questa domanda, contatto un operatore. Ti risponderà qualcuno il prima possibile"

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_message = update.message.text
    reply = await ask_openai(user_message)
    chat_id = update.effective_chat.id

    if "va rivolta al mio umano" in reply:
        await context.bot.send_message(chat_id=ADMIN_USER_ID,
            text=f"⚠️ DOMANDA da gestire manualmente:\n\n👤 {update.message.from_user.first_name}\n💬 {user_message}")

    await context.bot.send_message(chat_id=chat_id, text=reply)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Ciao! Sono il tuo assistente AI. Fammi una domanda.")

if __name__ == '__main__':
    app = ApplicationBuilder().token(TELEGRAM_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    print("🤖 Bot in funzione...")
    app.run_polling()
