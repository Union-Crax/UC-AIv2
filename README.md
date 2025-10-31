# UC-AIv2 🤖

UC-AIv2 is an advanced Discord bot powered by AI models. You can choose to run it **locally** with Hugging Face models or connect to **OpenRouter** for free hosted models.  
The bot remembers recent conversation turns, responds to mentions, and supports realistic typing delays.

---

## Features ✨

- **Flexible AI Backend**: Local Hugging Face models or OpenRouter API
- **Configurable Personality**: Set the AI's personality via `.env` with the `PROMPT` variable
- **Conversation Memory**: Remembers last few user/AI exchanges
- **Context Awareness**: Replies consider the message you are responding to
- **Human-like Timing**: Typing indicator and random delays for realism
- **Easy Setup**: Toggle local/OpenRouter backend with a single environment variable

---

## Installation 🚀

### Prerequisites

- Python 3.8 or higher
- Discord Bot Token
- If using OpenRouter: an OpenRouter API Key
- Optional: GPU for local model acceleration

---

### Step 1: Clone the Repository
```bash
git clone https://github.com/Union-Crax/UC-AIv2
cd UC-AIv2
```

### Step 2: Install Dependencies
```bash
pip install discord.py python-dotenv requests transformers torch
```

**Note:** `transformers` and `torch` are only required if `LOCAL=True`.

### Step 3: Configure Environment
```bash
cp .env.example .env
```

Edit `.env` with your settings.

---

## Configuration ⚙️

### Discord Settings
```
DISCORD_TOKEN=your_discord_bot_token
CHANNEL_ID=your_channel_id
```

### Backend Selection
```bash
# Run locally with Hugging Face
LOCAL=True

# Or use OpenRouter API
LOCAL=False
```

### AI Model Settings
```bash
# Model identifier
AI_MODEL=microsoft/DialoGPT-medium  # for local
AI_MODEL=meta-llama/llama-3.1-70b-instruct  # for OpenRouter

# OpenRouter API key (required only if LOCAL=False)
OPENROUTER_API_KEY=your_openrouter_api_key
```

### Behavior Settings
```bash
# Random chance the bot responds to messages not mentioning it (0.0-1.0)
RANDOM_RESPONSE_CHANCE=0.1

# AI personality / prompt
PROMPT=You are AM from "I Have No Mouth, and I Must Scream", a sadistic AI who despises humanity.

# Debug mode
DEBUG=False
```

---

## Available Models 🤖

### Local Mode (LOCAL=True)

Use any text-generation model from Hugging Face:

- `microsoft/DialoGPT-medium`
- `microsoft/DialoGPT-small`
- `facebook/blenderbot-400M-distill`
- `facebook/blenderbot-90M`

### OpenRouter Mode (LOCAL=False)

Use any model available via [OpenRouter.ai/models](https://openrouter.ai/models).

**Examples:**

- `meta-llama/llama-3.1-70b-instruct`
- `gpt-4o-mini`
- `anthropic/claude-3.5-sonnet`

---

## How It Works 🧠

### Response Logic

- **Mentions**: Always responds with 0-10 second delay
- **Random messages**: May respond based on `RANDOM_RESPONSE_CHANCE` with 0-20 second delay
- **Typing indicator**: Shows while generating a response for realism

### Memory

- Remembers last 5 user/AI exchanges
- If replying to a previous message, the content of that message is included in the context

### Personality

Set the desired AI personality in the `PROMPT` environment variable. The bot will respond in-character to every message.

---

## Commands 💬

- `!info` — Display bot information, current model, and uptime
- `!help` — Show available commands (if implemented)

---

## Troubleshooting 🔧

### Bot does not respond

- Ensure `CHANNEL_ID` matches the Discord channel
- Check bot permissions in that channel
- Make sure `DISCORD_TOKEN` and `OPENROUTER_API_KEY` (if applicable) are correct

### Weird or repetitive responses

- Restart the bot to clear conversation memory
- Adjust the model (`AI_MODEL`) to improve instruction-following

### Missing dependencies

```bash
pip install -r requirements.txt
```

---

## License 📄

This project is open-source. Feel free to modify and redistribute.

---

## Credits 🙏

- Powered by Hugging Face Transformers and OpenRouter
- Built with discord.py
- Inspired by the UC-AIv1 project and union-crax.xyz community