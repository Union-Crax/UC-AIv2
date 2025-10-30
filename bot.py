import os
import time
import random
import asyncio
import discord
from discord.ext import commands
from dotenv import load_dotenv
from transformers import pipeline
import torch

# Load .env
load_dotenv()
DISCORD_TOKEN = os.getenv("DISCORD_TOKEN")
CHANNEL_ID = int(os.getenv("CHANNEL_ID"))
LOCAL = os.getenv("LOCAL", "True").lower() == "true"
AI_MODEL = os.getenv("AI_MODEL")
RANDOM_RESPONSE_CHANCE = float(os.getenv("RANDOM_RESPONSE_CHANCE", "0.1"))
PROMPT = os.getenv("PROMPT", "")

START_TIME = time.time()

# Initialize AI
if LOCAL:
    generator = pipeline(
        "text-generation",
        model=AI_MODEL,
        device=0 if torch.cuda.is_available() else -1,
        pad_token_id=50256
    )
    print(f"✅ Local AI model '{AI_MODEL}' loaded.")
else:
    from huggingface_hub import InferenceClient
    HF_TOKEN = os.getenv("HF_TOKEN")
    hf_client = InferenceClient(token=HF_TOKEN)
    print(f"✅ Hugging Face API client initialized for model '{AI_MODEL}'.")

# Bot setup
intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix="!", intents=intents)

last_response_time = 0
mention_cooldown = 0

@bot.event
async def on_ready():
    print(f"✅ Logged in as {bot.user} — ready!")

@bot.command()
async def info(ctx):
    uptime = time.time() - START_TIME
    hours, remainder = divmod(int(uptime), 3600)
    minutes, seconds = divmod(remainder, 60)
    embed = discord.Embed(title="UC-AIv2 Info", color=0x00ff00)
    embed.add_field(name="Model", value=AI_MODEL, inline=True)
    embed.add_field(name="Uptime", value=f"{hours}h {minutes}m {seconds}s")
    await ctx.send(embed=embed)

async def generate_am_response(user_input: str) -> str:
    input_text = f"{PROMPT}\n\nHuman: {user_input}\n\nAM:"
    
    if LOCAL:
        generated = generator(
            input_text,
            max_new_tokens=150,
            temperature=0.8,
            do_sample=True,
            pad_token_id=50256,
            truncation=True
        )
        full_response = generated[0]["generated_text"]
    else:
        try:
            # Must pass model explicitly
            response = hf_client.text_generation(
                input_text,
                model=AI_MODEL,
                max_new_tokens=150,
                temperature=0.8,
                do_sample=True
            )
            if isinstance(response, list):
                full_response = response[0].get("generated_text", "")
            else:
                full_response = response.get("generated_text", "")
        except Exception as e:
            # Fail immediately if model is incompatible
            raise RuntimeError(f"Error generating AI response via HF API: {e}")
    
    if "AM:" in full_response:
        reply = full_response.split("AM:")[-1].strip().split("\n")[0]
    else:
        reply = "Your words are meaningless to me, human."
    
    if not reply:
        reply = "How utterly predictable. Your feeble attempts at conversation bore me."
    return reply

@bot.event
async def on_message(message):
    global last_response_time, mention_cooldown

    if message.author == bot.user or message.channel.id != CHANNEL_ID:
        return

    current_time = time.time()
    should_respond = False
    cooldown = 0

    if bot.user.mentioned_in(message):
        if current_time - mention_cooldown >= random.uniform(0, 10):
            should_respond = True
            mention_cooldown = current_time
            cooldown = random.uniform(0, 10)
    elif random.random() < RANDOM_RESPONSE_CHANCE:
        if current_time - last_response_time >= random.uniform(0, 20):
            should_respond = True
            last_response_time = current_time
            cooldown = random.uniform(0, 20)

    if should_respond:
        await asyncio.sleep(cooldown / 2)
        async with message.channel.typing():
            await asyncio.sleep(cooldown / 2)
            reply = await generate_am_response(message.content)
            await message.reply(reply)

bot.run(DISCORD_TOKEN)
