#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import discord
from discord.ext import commands
from openai import OpenAI
import subprocess
import logging
from dotenv import load_dotenv

load_dotenv()
DISCORD_TOKEN = os.getenv("DISCORD_TOKEN")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

client = OpenAI(api_key=OPENAI_API_KEY)

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("NEUROGEN")

intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix="!", intents=intents)

@bot.event
async def on_ready():
    logger.info(f"Logged in as {bot.user}")
    print(f"✅ NEUROGEN Bot is live as {bot.user}")

@bot.command()
async def ask(ctx, *, question: str):
    try:
        await ctx.typing()
        response = client.chat.completions.create(
            model="gpt-4",
            messages=[{"role": "user", "content": question}],
            max_tokens=300
        )
        reply = response.choices[0].message.content
        await ctx.send(reply)
    except Exception as e:
        await ctx.send(f"⚠️ Error: {e}")
        logger.error("Error in ask", exc_info=e)

@bot.command()
async def restart(ctx, script: str):
    try:
        subprocess.run(["pkill", "-f", f"{script}.py"])
        subprocess.Popen(["nohup", "python3", f"{script}.py"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        await ctx.send(f"✅ Restarted `{script}.py`")
    except Exception as e:
        logger.error("Error in restart", exc_info=e)
        await ctx.send(f"❌ Failed to restart `{script}.py`: {e}")

@bot.command()
async def context(ctx, topic: str):
    await ctx.send(f"Context for `{topic}` is under construction...")

bot.run(DISCORD_TOKEN)
