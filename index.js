require('dotenv').config();
const { Client, GatewayIntentBits, EmbedBuilder } = require('discord.js');
const { pipeline } = require('@xenova/transformers');
const fetch = require('node-fetch');

const DISCORD_TOKEN = process.env.DISCORD_TOKEN;
const CHANNEL_ID = parseInt(process.env.CHANNEL_ID);
const LOCAL = process.env.LOCAL === 'true';
const AI_MODEL = process.env.AI_MODEL;
const OPENROUTER_API_KEY = process.env.OPENROUTER_API_KEY;
const RANDOM_RESPONSE_CHANCE = parseFloat(process.env.RANDOM_RESPONSE_CHANCE || '0.1');
const PROMPT = process.env.PROMPT || '';
const DEBUG = process.env.DEBUG === 'true';

const START_TIME = Date.now();

let generator;
if (LOCAL) {
    (async () => {
        generator = await pipeline('text-generation', AI_MODEL);
        console.log(`✅ Local AI model '${AI_MODEL}' loaded.`);
    })();
} else {
    if (!OPENROUTER_API_KEY) {
        throw new Error('OPENROUTER_API_KEY must be set when LOCAL=false');
    }
    console.log(`✅ Using OpenRouter API with model '${AI_MODEL}'`);
}

const client = new Client({
    intents: [
        GatewayIntentBits.Guilds,
        GatewayIntentBits.GuildMessages,
        GatewayIntentBits.MessageContent,
    ],
});

let conversationMemory = [];
let lastResponseTime = 0;

async function generateAMResponse(userInput, context) {
    let contextText = '';
    for (let i = 0; i < Math.min(context.length, 8); i++) {
        const speaker = i % 2 === 0 ? 'Human' : 'AM';
        contextText += `${speaker}: ${context[i]}\n`;
    }

    const promptText = `${PROMPT.trim()}\n\n${contextText}Human: ${userInput}\nAM:`;

    try {
        let reply;
        if (LOCAL) {
            const generated = await generator(promptText, {
                max_new_tokens: 150,
                temperature: 0.8,
                do_sample: true,
                pad_token_id: 50256,
                truncation: true,
            });
            const fullResponse = generated[0].generated_text;
            reply = fullResponse.replace(promptText, '').trim();
        } else {
            const headers = {
                'Authorization': `Bearer ${OPENROUTER_API_KEY}`,
                'Content-Type': 'application/json',
            };
            const body = {
                model: AI_MODEL,
                messages: [
                    { role: 'system', content: PROMPT },
                    { role: 'user', content: promptText },
                ],
                temperature: 0.8,
                max_tokens: 250,
            };
            const response = await fetch('https://openrouter.ai/api/v1/chat/completions', {
                method: 'POST',
                headers,
                body: JSON.stringify(body),
            });
            const data = await response.json();
            if (DEBUG) console.log('DEBUG: OpenRouter raw response:', data);
            reply = data.choices?.[0]?.message?.content?.trim() || '';
        }

        if (reply.includes('AM:')) {
            reply = reply.split('AM:').pop().trim();
        }
        reply = reply.split('Human:')[0].replace(/\n/g, ' ').trim();
        if (!reply || reply.length < 3) {
            reply = 'Your weak words echo in the void.';
        } else if (reply.length > 500) {
            reply = reply.slice(0, 500) + '...';
        }

        if (DEBUG) console.log(`DEBUG: Final reply: ${reply}`);
        return reply;
    } catch (error) {
        console.error(`❌ Error generating AI response: ${error}`);
        if (DEBUG) console.error(error);
        return 'I am experiencing technical difficulties. How annoying.';
    }
}

client.once('ready', () => {
    console.log(`✅ Logged in as ${client.user.tag} — Lets get this bread started`);
});

client.on('messageCreate', async (message) => {
    if (message.author.bot || message.channel.id !== CHANNEL_ID) return;

    const currentTime = Date.now();
    let shouldRespond = false;

    if (message.mentions.has(client.user)) {
        shouldRespond = true;
    } else if (Math.random() < RANDOM_RESPONSE_CHANCE && currentTime - lastResponseTime > 10000) {
        shouldRespond = true;
        lastResponseTime = currentTime;
    }

    if (shouldRespond) {
        await message.channel.sendTyping();

        let userInput = message.content;

        if (message.reference) {
            try {
                const repliedTo = await message.channel.messages.fetch(message.reference.messageId);
                userInput = `(In response to '${repliedTo.content}') ${userInput}`;
            } catch (error) {
                if (DEBUG) console.log(`DEBUG: Could not fetch replied message: ${error}`);
            }
        }

        const reply = await generateAMResponse(userInput, conversationMemory);

        conversationMemory.push(userInput.trim());
        conversationMemory.push(reply.trim());
        if (conversationMemory.length > 10) {
            conversationMemory = conversationMemory.slice(-10);
        }

        await message.reply(reply);
    }
});

client.on('interactionCreate', async (interaction) => {
    if (!interaction.isCommand()) return;

    if (interaction.commandName === 'info') {
        const uptime = Date.now() - START_TIME;
        const hours = Math.floor(uptime / 3600000);
        const minutes = Math.floor((uptime % 3600000) / 60000);
        const seconds = Math.floor((uptime % 60000) / 1000);

        const embed = new EmbedBuilder()
            .setTitle('UC-AIv2 Info')
            .setColor(0x00ff00)
            .addField('Model', AI_MODEL, true)
            .addField('Uptime', `${hours}h ${minutes}m ${seconds}s`, true);

        await interaction.reply({ embeds: [embed] });
    }
});

client.login(DISCORD_TOKEN);