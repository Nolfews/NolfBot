import discord
from discord.ext import tasks
import datetime
import os

print("TOKEN dans l'environnement :", os.getenv("TOKEN"))
TOKEN = os.getenv("TOKEN")
CHANNEL_ID = 1480505357687062629
USER_ID = 1070965951564107817

intents = discord.Intents.default()
intents.message_content = True
intents.reactions = True
intents.members = True

client = discord.Client(intents=intents)

message_rappel = None
rappel_valide = False


@client.event
async def on_ready():
    print(f"Bot connecté : {client.user}")
    rappel_19h30.start()
    rappel_20h30.start()


# 📌 Premier rappel
@tasks.loop(minutes=1)
async def rappel_19h30():
    global message_rappel, rappel_valide

    now = datetime.datetime.now()

    if now.hour == 19 and now.minute == 30:

        rappel_valide = False

        channel = client.get_channel(CHANNEL_ID)

        embed = discord.Embed(
            title="📌 Rappel quoti Genshin",
            description="Clique sur ✅ quand c'est fait.",
            color=discord.Color.orange()
        )

        embed.add_field(
            name="Action à faire",
            value="Ton rappel du jour.",
            inline=False
        )

        message_rappel = await channel.send(f"<@{USER_ID}>", embed=embed)

        await message_rappel.add_reaction("✅")


# 📌 Deuxième rappel
@tasks.loop(minutes=1)
async def rappel_20h30():
    global rappel_valide

    now = datetime.datetime.now()

    if now.hour == 20 and now.minute == 30:

        if rappel_valide is False:

            channel = client.get_channel(CHANNEL_ID)

            embed = discord.Embed(
                title="⚠️ Rappel",
                description="Toujours pas validé.",
                color=discord.Color.red()
            )

            embed.add_field(
                name="Action à faire",
                value="Pense à cliquer sur ✅ quand c'est fait.",
                inline=False
            )

            await channel.send(f"<@{USER_ID}>", embed=embed)


# 📌 Gestion des réactions
@client.event
async def on_reaction_add(reaction, user):
    global rappel_valide

    if user.bot:
        return

    if reaction.message.id == message_rappel.id:

        if str(reaction.emoji) == "✅":

            if user.id == USER_ID:

                rappel_valide = True

                embed = discord.Embed(
                    title="✅ Validé",
                    description="Mission accomplis UwU.",
                    color=discord.Color.green()
                )

                await reaction.message.reply(embed=embed)



client.run(TOKEN)
