import os
import discord
from discord.ext import commands
from telegram import Update, Bot
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext

# Constants
DISCORD_TOKEN = os.environ["DISCORD_TOKEN"]
TELEGRAM_TOKEN = os.environ["TELEGRAM_TOKEN"]
DISCORD_CHANNEL_ID = int(os.environ["DISCORD_CHANNEL_ID"])
TELEGRAM_CHAT_ID = int(os.environ["TELEGRAM_CHAT_ID"])

# Discord bot setup
intents = discord.Intents.default()
intents.typing = False
intents.presences = False
bot = commands.Bot(command_prefix="!", intents=intents)

# Telegram bot setup
telegram_bot = Bot(token=TELEGRAM_TOKEN)
updater = Updater(token=TELEGRAM_TOKEN, use_context=True)

# Functions
async def send_to_telegram(content: str):
    telegram_bot.send_message(chat_id=TELEGRAM_CHAT_ID, text=content)

async def send_to_discord(content: str):
    channel = bot.get_channel(DISCORD_CHANNEL_ID)
    await channel.send(content)

# Discord events
@bot.event
async def on_ready():
    print(f"{bot.user} is connected to Discord!")

@bot.event
async def on_message(message):
    if message.author == bot.user or message.channel.id != DISCORD_CHANNEL_ID:
        return

    content = f"[Discord | {message.author}] {message.content}"
    await send_to_telegram(content)

# Telegram handlers
def handle_telegram_message(update: Update, context: CallbackContext):
    if update.message.chat_id != TELEGRAM_CHAT_ID:
        return

    content = f"[Telegram | {update.message.from_user.first_name}] {update.message.text}"
    context.bot.loop.create_task(send_to_discord(content))

message_handler = MessageHandler(Filters.text & ~Filters.command, handle_telegram_message)
updater.dispatcher.add_handler(message_handler)

# Start bots
if __name__ == "__main__":
    updater.start_polling()
    bot.run(DISCORD_TOKEN)
