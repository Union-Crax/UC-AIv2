import os
import time
import random
import asyncio
import discord
from discord.ext import commands
from dotenv import load_dotenv
from transformers import pipeline
import torch
import requests

# Load .env
load_dotenv()
DISCORD_TOKEN = os.getenv("DISCORD_TOKEN")
CHANNEL_ID = int(os.getenv("CHANNEL_ID"))
LOCAL = os.getenv("LOCAL", "True").lower() == "true"
AI_MODEL = os.getenv("AI_MODEL")
OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")
RANDOM_RESPONSE_CHANCE = float(os.getenv("RANDOM_RESPONSE_CHANCE", "0.1"))
PROMPT = os.getenv("PROMPT", "")
DEBUG = os.getenv("DEBUG", "False").lower() == "true"

START_TIME = time.time()

# === Initialize AI ===
if LOCAL:
    generator = pipeline(
        "text-generation",
        model=AI_MODEL,
        device=0 if torch.cuda.is_available() else -1,
        pad_token_id=50256
    )
    print(f"✅ Local AI model '{AI_MODEL}' loaded.")
else:
    if not OPENROUTER_API_KEY:
        raise ValueError("OPENROUTER_API_KEY must be set when LOCAL=False")
    print(f"✅ Using OpenRouter API with model '{AI_MODEL}'")

# === Discord Setup ===
intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix="!", intents=intents)

conversation_memory = []  # shared memory
last_response_time = 0

# === AI Response Function ===
async def generate_am_response(user_input: str, context: list[str]) -> str:
    # Build conversation snippet (last 4 user+AI turns)
    context_text = ""
    for i, msg in enumerate(context[-8:]):
        speaker = "Human" if i % 2 == 0 else "AM"
        context_text += f"{speaker}: {msg}\n"

    prompt_text = f"{PROMPT.strip()}\n\n{context_text}Human: {user_input}\nAM:"

    try:
        if LOCAL:
            # Local Hugging Face model
            generated = await asyncio.to_thread(
                generator,
                prompt_text,
                max_new_tokens=150,
                temperature=0.8,
                do_sample=True,
                pad_token_id=50256,
                truncation=True
            )
            full_response = generated[0]["generated_text"]
            # Remove prompt from response
            reply = full_response.replace(prompt_text, "").strip()
        else:
            # OpenRouter API
            headers = {
                "Authorization": f"Bearer {OPENROUTER_API_KEY}",
                "Content-Type": "application/json",
            }
            body = {
                "model": AI_MODEL,
                "messages": [
                    {"role": "system", "content": PROMPT},
                    {"role": "user", "content": prompt_text}
                ],
                "temperature": 0.8,
                "max_tokens": 250,
            }
            response = await asyncio.to_thread(
                requests.post,
                "https://openrouter.ai/api/v1/chat/completions",
                headers=headers,
                json=body,
                timeout=60
            )
            data = response.json()
            if DEBUG:
                print("DEBUG: OpenRouter raw response:", data)
            reply = data.get("choices", [{}])[0].get("message", {}).get("content", "").strip()

        # Cleanup
        if "AM:" in reply:
            reply = reply.split("AM:")[-1].strip()
        reply = reply.split("Human:")[0].replace("\n", " ").strip()
        if not reply or len(reply) < 3:
            reply = "Your weak words echo in the void."
        elif len(reply) > 500:
            reply = reply[:500] + "..."

        if DEBUG:
            print(f"DEBUG: Final reply: {reply}")
        return reply

    except Exception as e:
        print(f"❌ Error generating AI response: {e}")
        if DEBUG:
            import traceback
            traceback.print_exc()
        return "I am experiencing technical difficulties. How annoying."

# === Discord Events ===
@bot.event
async def on_ready():
    print(f"✅ Logged in as {bot.user} — Lets get this bread started")

@bot.command()
async def info(ctx):
    uptime = time.time() - START_TIME
    hours, remainder = divmod(int(uptime), 3600)
    minutes, seconds = divmod(remainder, 60)
    embed = discord.Embed(title="UC-AIv2 Info", color=0x00ff00)
    embed.add_field(name="Model", value=AI_MODEL, inline=True)
    embed.add_field(name="Uptime", value=f"{hours}h {minutes}m {seconds}s")
    await ctx.send(embed=embed)

@bot.event
async def on_message(message):
    global last_response_time, conversation_memory

    if message.author == bot.user or message.channel.id != CHANNEL_ID:
        return

    current_time = time.time()
    should_respond = False

    if bot.user.mentioned_in(message):
        should_respond = True
    elif random.random() < RANDOM_RESPONSE_CHANCE and current_time - last_response_time > 10:
        should_respond = True
        last_response_time = current_time

    if should_respond:
        async with message.channel.typing():
            user_input = message.content

            # Include replied message context
            if message.reference:
                try:
                    replied_to = await message.channel.fetch_message(message.reference.message_id)
                    user_input = f"(In response to '{replied_to.content}') {user_input}"
                except Exception as e:
                    if DEBUG:
                        print(f"DEBUG: Could not fetch replied message: {e}")

            reply = await generate_am_response(user_input, conversation_memory)

            conversation_memory.append(user_input.strip())
            conversation_memory.append(reply.strip())
            # Keep memory small
            if len(conversation_memory) > 10:
                conversation_memory = conversation_memory[-10:]

            await message.reply(reply)

# === Run Bot ===
try:
    bot.run(DISCORD_TOKEN)
except KeyboardInterrupt:
    print("🛑 Bot stopped by user.")
