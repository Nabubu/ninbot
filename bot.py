from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, ContextTypes, filters
from config import TELEGRAM_BOT_TOKEN
from logic import load_games, find_combination, suggest_topup

user_states = {}

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("👋 Привет! Введи свой регион (например: US, PL):")
    user_states[update.effective_user.id] = {"step": "awaiting_region"}

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    text = update.message.text.strip()
    state = user_states.get(user_id, {})

    if state.get("step") == "awaiting_region":
        state["region"] = text.upper()
        state["step"] = "awaiting_balance"
        await update.message.reply_text("💰 Введи свой баланс в формате 4.99:")

    elif state.get("step") == "awaiting_balance":
        try:
            balance = float(text.replace(",", "."))
            games = load_games(state["region"])
            result, leftover = find_combination(balance, games)

            if leftover == 0 and result:
                reply = "🎮 Игры, которые можно купить:\n"
                for game in result:
                    reply += f"- {game['title']} — ${game['price']} — [Ссылка]({game['url']})\n"
                reply += "\n✅ Баланс будет обнулен!"
                await update.message.reply_text(reply, parse_mode="Markdown")
            else:
                topup, combo = suggest_topup(balance, games)
                if topup:
                    reply = f"💡 Пополните на ${topup} и купите:\n"
                    for game in combo:
                        reply += f"- {game['title']} — ${game['price']} — [Ссылка]({game['url']})\n"
                    reply += "\n🎯 Баланс будет обнулен!"
                else:
                    reply = "🙁 Не удалось найти подходящие игры даже с пополнением."
                await update.message.reply_text(reply, parse_mode="Markdown")
        except ValueError:
            await update.message.reply_text("❗ Введи баланс в формате 4.99")

    user_states[user_id] = state

if __name__ == "__main__":
    app = ApplicationBuilder().token(TELEGRAM_BOT_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    app.run_polling()