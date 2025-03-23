#!/usr/bin/env python3
import sys, os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import discord
from discord.ext import commands
from context_pipeline import build_context
from memory_store import MemoryStore

intents = discord.Intents.default()
intents.message_content = True  # Required to read message content for commands

bot = commands.Bot(command_prefix="!", intents=intents)
store = MemoryStore(collection_name="memories")

@bot.command(name="ask")
async def ask_command(ctx, *, query: str):
    context = build_context(query)
    combined_prompt = f"Context:\n{context}\n\nUser Query: {query}"
    response = f"Simulated GPT Response based on prompt: {combined_prompt}"
    store.store_memory(f"Query: {query}\nResponse: {response}", tags=["discord", "ask"])
    await ctx.send(response)

@bot.command(name="context")
async def context_command(ctx, *, query: str):
    context = build_context(query)
    await ctx.send(f"Retrieved Context:\n{context}")

@bot.event
async def on_ready():
    print(f"✅ Bot connected as {bot.user}")

if __name__ == "__main__":
    token = os.environ.get("DISCORD_TOKEN")
    if token is None:
        print("❌ DISCORD_TOKEN environment variable not set.")
    else:
        bot.run(token)
