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
    try:
        synced = await bot.tree.sync()
        print(f"Synced {len(synced)} commands")
    except Exception as e:
        print(e)


@bot.tree.command(name="viral", description="Find a viral video and generate a remake script")
async def viral(interaction: discord.Interaction):
    await interaction.response.send_message("🔎 Finding viral content and creating an idea...")

    video = find_viral_video()
    result = generate_script(video)

    embed = discord.Embed(
        title="🔥 Viral Video Analysis",
        description=result[:4000],
        color=discord.Color.red()
    )

    embed.add_field(
        name="Original Video",
        value=f"[{video['title']}]({video['url']})",
        inline=False
    )

    await interaction.followup.send(embed=embed)


bot.run(DISCORD_TOKEN)
