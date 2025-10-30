# UC-AIv2 🤖

An advanced Discord bot powered by Hugging Face AI models with configurable personality. Choose between local model hosting or Hugging Face Inference API for dynamic, personality-driven responses.

## Features ✨

- **Flexible AI Backend**: Local models or Hugging Face Inference API
- **Configurable Personality**: Set any AI personality via environment variables
- **Realistic Timing**: Human-like response delays.
- **Smart Response Logic**: Always responds to mentions, occasionally to random messages
- **Easy Configuration**: Extensive .env configuration for all settings

## Installation 🚀

### Prerequisites
- Python 3.8+
- Discord Bot Token
- Hugging Face API Key (if using Inference API)

### Step 1: Clone & Setup
```bash
git clone <https://github.com/Union-Crax/UC-AIv2>
cd UC-AIv2
```

### Step 2: Install Dependencies
```bash
pip install discord.py python-dotenv transformers torch huggingface_hub
```

### Step 3: Configure Environment
```bash
cp .env.example .env
```

Edit `.env` with your settings (see Configuration section below).

### Step 4: Run the Bot
```bash
python bot.py
```

## Configuration ⚙️

### Discord Settings
```env
GUILD_ID=your_server_id_here
CHANNEL_ID=your_channel_id_here
DISCORD_TOKEN=your_bot_token_here
```

### AI Model Settings
```env
# Choose your AI model
AI_MODEL=microsoft/DialoGPT-medium

# Run AI locally (True) or use Hugging Face API (False)
LOCAL=True

# Hugging Face API token (only needed if LOCAL=False)
HF_TOKEN=your_huggingface_token_here
```

### Behavior Settings
```env
# Random response chance (0.0 = never, 1.0 = always respond to every message)
RANDOM_RESPONSE_CHANCE=0.1

# AI personality prompt (leave empty for default personality)
PROMPT=
```

## Available AI Models 🤖

Choose from any text-generation model available on Hugging Face:

### Recommended Models for local use:
- `microsoft/DialoGPT-medium` - Balanced conversational AI (~863MB download)
- `microsoft/DialoGPT-small` - Faster, less detailed (~117MB download)
- `microsoft/DialoGPT-large` - More detailed, slower (~1.7GB download)
- `facebook/blenderbot-400M-distill` - Good for conversations
- `facebook/blenderbot-90M` - Lightweight and fast

### For Local Mode (LOCAL=True):
Any model from: https://huggingface.co/models?pipeline_tag=text-generation&sort=downloads

### For API Mode (LOCAL=False):
Models available via: https://huggingface.co/docs/inference-endpoints/index

## How It Works 🧠

### Response Logic
- **Mentions**: Always responds with 0-10 second delay
- **Random Messages**: 10% chance to respond with 0-20 second delay
- **Typing Indicators**: Shows during AI generation for realism

### Humanizer System
The UC-AIv2 Humanizer creates realistic Discord interactions:
- Long delays (>5s) split time between waiting and typing
- Short delays (<5s) use full delay then show typing
- Maintains conversation flow that feels natural

### AI Personality
Set your desired personality in the PROMPT environment variable. The bot will respond in character to every message. Leave empty for a default conversational personality.

## Commands 💬

- `!info` - Display bot information, uptime, and current model
- `!help` - Show available commands

## Getting API Keys 🔑

### Discord Bot Token
1. Go to https://discord.com/developers/applications
2. Create a new application
3. Go to "Bot" section
4. Copy the token

### Hugging Face API Token (for API mode)
1. Go to https://huggingface.co/settings/tokens
2. Create a new token with "Read" permissions
3. Copy the token to `HF_TOKEN` in your .env

## Troubleshooting 🔧

### Bot doesn't respond
- Check that `CHANNEL_ID` matches your Discord channel
- Verify bot has proper permissions in your server
- Check console for error messages

### AI model errors
- For local mode: Ensure model name is correct and available for download
- For API mode: Ensure `HF_TOKEN` is correct and model is available via Inference API
- Check console for specific error messages

### Import errors
- Install missing dependencies: `pip install -r requirements.txt`
- Ensure Python 3.8+ is being used

## License 📄

This project is open source. Feel free to modify and distribute.

## Credits 🙏

- Powered by Hugging Face Transformers and Inference API
- Built with discord.py
- the community of union-crax.xyz for the original idea
- UC-AIv1 (stole some code heheh)