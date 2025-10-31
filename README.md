## Adding the Bot to Your Discord Server

### Step 1: Create a Discord Application
1. Go to the [Discord Developer Portal](https://discord.com/developers/applications)
2. Click "New Application" and give it a name (e.g., "UC-AI Bot")
3. Go to the "Bot" section in the left sidebar

### Step 2: Create and Configure the Bot
1. Click "Add Bot" to create your bot user
2. Under "Token", click "Copy" to get your bot token (keep this secret!)
3. Scroll down to "Privileged Gateway Intents"
4. Enable the following intents:
   - **Message Content Intent** (required for reading message content)
   - **Server Members Intent** (optional, for member-related features)

### Step 3: Generate Invite Link
1. Go to the "OAuth2" section, then "URL Generator"
2. Under "Scopes", select:
   - `bot`
   - `applications.commands` (for slash commands)
3. Under "Bot Permissions", select:
   - `Send Messages`
   - `Use Slash Commands`
   - `Read Message History`
   - `Mention Everyone` (optional)
   - `Use External Emojis` (optional)
4. Copy the generated URL at the bottom

### Step 4: Invite the Bot
1. Paste the invite URL into your browser
2. Select your server from the dropdown
3. Click "Authorize" and complete the CAPTCHA

### Step 5: Get Channel ID
1. In Discord, right-click on the channel you want the bot to respond in
2. Click "Copy ID" (if you don't see this option, enable Developer Mode in User Settings > Advanced)
3. This is your `CHANNEL_ID`

### Step 6: Configure Environment Variables
Create a `.env` file in your project root with:
```
DISCORD_TOKEN=your_bot_token_here
CHANNEL_ID=your_channel_id_here
LOCAL=true  # or false for OpenRouter
AI_MODEL=microsoft/DialoGPT-medium  # or any model
# OPENROUTER_API_KEY=your_key_here  # only if LOCAL=false
```

### Step 7: Run the Bot
```bash
npm install
npm start
```

The bot should now be online and respond to mentions and commands in your specified channel!