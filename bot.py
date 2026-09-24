import discord
from discord.ext import commands
from config import DISCORD_TOKEN
from ai.gemini import generate_script
from youtube.scanner import find_viral_video
from database.saves import save_video, get_saved_videos, get_video, delete_video

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix="!", intents=intents)


class ViralButtons(discord.ui.View):
    def __init__(self, video, result):
        super().__init__(timeout=300)
        self.video = video
        self.result = result

    @discord.ui.button(label="🔄 Regenerate Idea", style=discord.ButtonStyle.primary)
    async def regenerate(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.send_message("🔄 Regenerating...")
        result = generate_script(self.video, regenerate=True)
        await interaction.followup.send(result[:4000])

    @discord.ui.button(label="💾 Save", style=discord.ButtonStyle.success)
    async def save(self, interaction: discord.Interaction, button: discord.ui.Button):
        save_video(self.video, self.result)
        await interaction.response.send_message("✅ Saved.", ephemeral=True)


@bot.event
async def on_ready():
    print(f"Logged in as {bot.user}")
    await bot.tree.sync()


@bot.tree.command(name="viral", description="Find viral content and generate a remake script")
async def viral(interaction: discord.Interaction):
    await interaction.response.send_message("🔎 Finding viral content...")

    video = find_viral_video()
    result = generate_script(video)

    embed = discord.Embed(
        title="🔥 Viral Video Found",
        description=result[:4000],
        color=discord.Color.red()
    )

    embed.add_field(name="Original Video", value=f"[{video['title']}]({video['url']})", inline=False)

    await interaction.followup.send(embed=embed, view=ViralButtons(video, result))


@bot.tree.command(name="saved", description="See saved viral ideas")
async def saved(interaction: discord.Interaction):
    videos = get_saved_videos()

    if not videos:
        await interaction.response.send_message("No saved videos yet.")
        return

    text = "📚 Saved Viral Ideas\n\n"
    for video in videos[:10]:
        text += f"#{video['id']} 🔥 {video['title']}\n{video['url']}\n\n"

    await interaction.response.send_message(text[:4000])


@bot.tree.command(name="view", description="View a saved viral idea")
async def view(interaction: discord.Interaction, id: int):
    video = get_video(id)

    if not video:
        await interaction.response.send_message("❌ Not found.")
        return

    await interaction.response.send_message(video['script'][:4000])


@bot.tree.command(name="delete", description="Delete a saved viral idea")
async def delete(interaction: discord.Interaction, id: int):
    delete_video(id)
    await interaction.response.send_message("🗑️ Deleted.")


bot.run(DISCORD_TOKEN)
