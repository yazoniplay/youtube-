import discord
from discord.ext import commands
from config import DISCORD_TOKEN
from ai.gemini import generate_script
from youtube.scanner import find_viral_video

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix="!", intents=intents)

@bot.event
async def on_ready():
    print(f"Logged in as {bot.user}")

@bot.tree.command(name="viral", description="Find a viral video and generate a remake script")
async def viral(interaction: discord.Interaction):
    await interaction.response.send_message("🔎 Finding viral content...")

    video = find_viral_video()
    result = generate_script(video)

    await interaction.followup.send(result[:1900])

bot.run(DISCORD_TOKEN)
