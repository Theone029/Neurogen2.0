#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import sys, os
# Bootstrap: add the root directory so modules in the root are importable.
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import discord
from discord.ext import commands
from context_injector import inject_context
from core.memory_store import MemoryStore

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix="!", intents=intents)
store = MemoryStore(collection_name="memories")

@bot.command(name="ask")
async def ask(ctx, *, query: str):
    """
    On !ask, retrieves context via context_injector,
    stores the interaction, and simulates a GPT response.
    """
    injected_prompt = inject_context(query)
    # Optionally store the query and a placeholder response in memory.
    store.store_memory(f"Query: {query}\nResponse: <placeholder>", tags=["discord", "ask"], source="discord")
    await ctx.send(f"Simulated GPT Response based on prompt:\n```Context:\n{injected_prompt}```")

@bot.command(name="context")
async def context(ctx, *, query: str):
    """
    On !context, retrieves and displays the injected context.
    """
    injected_prompt = inject_context(query)
    await ctx.send(f"Retrieved Context:\n```{injected_prompt}```")

@bot.event
async def on_ready():
    print(f"✅ Bot connected as {bot.user}")

if __name__ == "__main__":
    token = os.environ.get("DISCORD_TOKEN")
    if token is None:
        print("❌ DISCORD_TOKEN environment variable not set.")
    else:
        bot.run(token)
