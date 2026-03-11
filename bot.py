import discord
from discord.ext import tasks
import datetime
import pytz
import requests
import os

TOKEN = os.getenv("TOKEN")
CHANNEL_ID = 1480505357687062629
USER_ID = 1070965951564107817
timezone = pytz.timezone("Europe/Paris")
intents = discord.Intents.default()
client = discord.Client(intents=intents)
rappel_valide = False

# ---------- CAT API ----------
def get_random_cat():
    try:
        r = requests.get("https://api.thecatapi.com/v1/images/search")
        data = r.json()
        return data[0]["url"]
    except:
        return None

# ---------- button ----------
class ValidationView(discord.ui.View):

    def __init__(self):
        super().__init__(timeout=None)

    @discord.ui.button(label="C'est fait", style=discord.ButtonStyle.success, emoji="✅")
    async def valider(self, interaction: discord.Interaction, button: discord.ui.Button):

        global rappel_valide

        if interaction.user.id != USER_ID:
            await interaction.response.send_message(
                "Ce rappel ne te concerne pas 👀",
                ephemeral=True
            )
            return

        rappel_valide = True

        embed = discord.Embed(
            title="✅ Validé",
            description="Mission accomplie UwU",
            color=discord.Color.green()
        )

        await interaction.response.send_message(embed=embed)

# ---------- display reminder ----------
async def envoyer_rappel(type_rappel):

    channel = client.get_channel(CHANNEL_ID)

    cat = get_random_cat()

    if type_rappel == "first":

        embed = discord.Embed(
            title="📌 Rappel quoti Genshin",
            description="Clique sur le bouton quand c'est fait.",
            color=discord.Color.orange()
        )

    else:

        embed = discord.Embed(
            title="⚠️ Rappel",
            description="Toujours pas validé 👀",
            color=discord.Color.red()
        )

    embed.add_field(
        name="Action à faire",
        value="Ton rappel du jour.",
        inline=False
    )

    if cat:
        embed.set_image(url=cat)

    view = ValidationView()

    await channel.send(f"<@{USER_ID}>", embed=embed, view=view)

# ---------- Main loop ----------
@tasks.loop(minutes=1)
async def check_rappels():

    global rappel_valide

    now = datetime.datetime.now(timezone)

    if now.hour == 0 and now.minute == 0:
        rappel_valide = False

    if now.hour == 19 and now.minute == 30:
        rappel_valide = False
        await envoyer_rappel("first")

    if now.hour == 20 and now.minute == 30 and rappel_valide is False:
        await envoyer_rappel("second")

# ---------- READY ----------
@client.event
async def on_ready():
    check_rappels.start()

client.run(TOKEN)
