import os
import discord
from discord.ext import commands
from openai import AsyncOpenAI

DISCORD_TOKEN = os.getenv("DISCORD_TOKEN")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

client = AsyncOpenAI(api_key=OPENAI_API_KEY)

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix="!", intents=intents)


@bot.event
async def on_ready():
    print(f"Bot online: {bot.user}")


@bot.event
async def on_message(message):
    # Bots ke messages ignore
    if message.author.bot:
        return

    # Sirf bot ko mention/tag kiya ho tab reply kare
    if bot.user not in message.mentions:
        await bot.process_commands(message)
        return

    # Bot ka mention message se remove karo
    user_message = message.content.replace(f"<@{bot.user.id}>", "")
    user_message = user_message.replace(f"<@!{bot.user.id}>", "").strip()

    # Sirf mention ho, koi message nahi
    if not user_message:
        user_message = "Hello!"

    try:
        async with message.channel.typing():
            response = await client.responses.create(
                model="gpt-5.6-luna",
                instructions=(
                    "You are a friendly Discord server AI assistant. "
                    "Reply naturally and briefly. "
                    "You can understand Hindi, Hinglish and English. "
                    "Match the user's language and tone."
                ),
                input=user_message,
                max_output_tokens=300
            )

        reply = response.output_text.strip()

        if reply:
            await message.reply(reply[:2000], mention_author=False)

    except Exception as e:
        print("AI Error:", e)

    await bot.process_commands(message)


bot.run(DISCORD_TOKEN)
