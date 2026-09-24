import discord
from discord.ext import commands
from config import DISCORD_TOKEN
from ai.gemini import generate_script
from youtube.scanner import find_viral_video
from database.saves import save_video, get_saved_videos, get_video, delete_video

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix="!", intents=intents)


def make_embed(title, text, color=discord.Color.blue()):
    text = text or "No result generated."
    return discord.Embed(title=title, description=text[:4000], color=color)


class ViralButtons(discord.ui.View):
    def __init__(self, video, result):
        super().__init__(timeout=900)
        self.video = video
        self.result = result

    @discord.ui.button(label="🔄 Regenerate", style=discord.ButtonStyle.primary)
    async def regenerate(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.defer()
        try:
            result = generate_script(self.video, regenerate=True)
            await interaction.followup.send(embed=make_embed("🔄 New Version Generated", result), view=ViralButtons(self.video, result))
        except Exception as e:
            await interaction.followup.send(f"❌ Regeneration failed: {e}", ephemeral=True)

    @discord.ui.button(label="💾 Save", style=discord.ButtonStyle.success)
    async def save(self, interaction: discord.Interaction, button: discord.ui.Button):
        try:
            save_video(self.video, self.result)
            await interaction.response.send_message("✅ Saved to your viral library.", ephemeral=True)
        except Exception as e:
            await interaction.response.send_message(f"❌ Save failed: {e}", ephemeral=True)

    @discord.ui.button(label="🎬 Another Version", style=discord.ButtonStyle.secondary)
    async def another(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.defer()
        try:
            result = generate_script(self.video, regenerate=True)
            await interaction.followup.send(embed=make_embed("🎬 Another Version", result), view=ViralButtons(self.video, result))
        except Exception as e:
            await interaction.followup.send(f"❌ Failed: {e}", ephemeral=True)


@bot.event
async def on_ready():
    print(f"Logged in as {bot.user}")
    await bot.tree.sync()


@bot.tree.command(name="viral", description="Find viral content and generate a remake script")
async def viral(interaction: discord.Interaction):
    await interaction.response.send_message("🔎 Finding viral content...")
    try:
        video = find_viral_video()
        if not video:
            await interaction.followup.send("❌ No viral video found.")
            return

        result = generate_script(video)
        embed = make_embed("🔥 Viral Video Found", result, discord.Color.red())
        embed.add_field(name="Original Video", value=f"[{video['title']}]({video['url']})", inline=False)
        await interaction.followup.send(embed=embed, view=ViralButtons(video, result))
    except Exception as e:
        await interaction.followup.send(f"❌ Viral scan failed: {e}")


@bot.tree.command(name="saved", description="See saved viral ideas")
async def saved(interaction: discord.Interaction):
    videos = get_saved_videos()
    if not videos:
        await interaction.response.send_message("No saved videos yet.")
        return

    embed = discord.Embed(title="📚 Saved Viral Ideas", color=discord.Color.green())
    for video in videos[:10]:
        embed.add_field(name=f"#{video['id']} 🔥 {video['title']}", value=video['url'], inline=False)
    await interaction.response.send_message(embed=embed)


@bot.tree.command(name="view", description="View a saved viral idea")
async def view(interaction: discord.Interaction, id: int):
    video = get_video(id)
    if not video:
        await interaction.response.send_message("❌ Not found.")
        return
    embed = make_embed(f"📖 {video['title']}", video.get('result', 'No script saved.'))
    embed.add_field(name="Original Video", value=video['url'], inline=False)
    await interaction.response.send_message(embed=embed)


@bot.tree.command(name="delete", description="Delete a saved viral idea")
async def delete(interaction: discord.Interaction, id: int):
    delete_video(id)
    await interaction.response.send_message("🗑️ Deleted.")


@bot.event
async def on_command_error(ctx, error):
    await ctx.send(f"❌ Error: {error}")


bot.run(DISCORD_TOKEN)
