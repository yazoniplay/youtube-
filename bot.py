import discord
from discord.ext import commands
from config import DISCORD_TOKEN
from ai.gemini import generate_script
from youtube.scanner import find_viral_video
from database.saves import save_video, get_saved_videos

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix="!", intents=intents)

last_videos = {}


class ViralButtons(discord.ui.View):
    def __init__(self, video):
        super().__init__(timeout=300)
        self.video = video

    @discord.ui.button(label="🔄 Regenerate Idea", style=discord.ButtonStyle.primary)
    async def regenerate(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.send_message("🔄 Regenerating a new version...")
        result = generate_script(self.video, regenerate=True)
        await interaction.followup.send(result[:4000])

    @discord.ui.button(label="💾 Save", style=discord.ButtonStyle.success)
    async def save(self, interaction: discord.Interaction, button: discord.ui.Button):
        save_video(self.video)
        await interaction.response.send_message("✅ Saved to your viral ideas library.", ephemeral=True)


@bot.event
async def on_ready():
    print(f"Logged in as {bot.user}")
    await bot.tree.sync()


@bot.tree.command(name="viral", description="Find viral content and generate a complete remake script")
async def viral(interaction: discord.Interaction):
    await interaction.response.send_message("🔎 Finding viral content and creating script...")

    video = find_viral_video()
    result = generate_script(video)

    save_video(video)

    embed = discord.Embed(
        title="🔥 Viral Video Found",
        description=result[:4000],
        color=discord.Color.red()
    )

    embed.add_field(
        name="Original Video",
        value=f"[{video['title']}]({video['url']})",
        inline=False
    )

    await interaction.followup.send(embed=embed, view=ViralButtons(video))


@bot.tree.command(name="saved", description="See your saved viral ideas")
async def saved(interaction: discord.Interaction):
    videos = get_saved_videos()

    if not videos:
        await interaction.response.send_message("No saved videos yet.")
        return

    text = "📚 Saved Viral Ideas\n\n"
    for video in videos[:10]:
        text += f"🔥 {video['title']}\n{video['url']}\n\n"

    await interaction.response.send_message(text[:4000])


bot.run(DISCORD_TOKEN)
