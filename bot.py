import discord
from openai import OpenAI
import asyncio

DISCORD_TOKEN = "SEU_TOKEN"
OPENAI_API_KEY = "SUA_API_KEY"

client_ai = OpenAI(api_key=OPENAI_API_KEY)

intents = discord.Intents.default()
intents.message_content = True

bot = discord.Client(intents=intents)

@bot.event
async def on_ready():
    print("Bot online:", bot.user)

@bot.event
async def on_message(message):

    if message.author.bot:
        return

    pergunta = message.content

    async with message.channel.typing():

        try:

            resposta = await asyncio.to_thread(
                client_ai.chat.completions.create,
                model="gpt-4.1-mini",
                messages=[{"role":"user","content":pergunta}]
            )

            texto = resposta.choices[0].message.content

        except Exception as e:

            print(e)
            await message.channel.send("Erro na IA")
            return

    await message.channel.send(texto)

bot.run()