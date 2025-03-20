import threading
import discord
from discord.ext import commands
from flask import Flask

# Flask App
app = Flask(__name__)

@app.route('/')
def home():
    return "NEUROGEN API is running!"

def run_flask():
    app.run(host='0.0.0.0', port=8000)

# Run Flask in a separate thread
threading.Thread(target=run_flask, daemon=True).start()

# Discord Bot Setup
intents = discord.Intents.default()
intents.messages = True
intents.message_content = True

bot = commands.Bot(command_prefix="!", intents=intents)

@bot.event
async def on_ready():
    print(f"✅ Logged in as {bot.user}")

@bot.command()
async def ping(ctx):
    await ctx.send("Pong! 🚀")

@bot.command()
async def info(ctx):
    await ctx.send("This is the NEUROGEN Discord bot, now with integrated API.")

bot.run("MTMzNTQyNDQzNDk1MzI1Njk5MA.Gyzs-k.NPFNW_KlIfG7iOMdBMP2zkLzm62jxpoQJJK0eE")
