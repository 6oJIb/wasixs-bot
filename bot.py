import asyncio
import os
import disnake
from disnake.ext import commands
import json

bot = commands.Bot(command_prefix="/", intents=disnake.Intents.all(), test_guilds=[1534901683690274916, 1385567845089542204])
active_voices = []

def channel_id_in_db(channel_id: int):
    with open("data/VC.json", "r", encoding="utf-8") as f:
        data = json.load(f)
    return str(channel_id) in data

def get_status_in_db(channel_id: int):
    with open("data/VC.json", "r", encoding="utf-8") as f:
        data = json.load(f)
    mode: str = data[str(channel_id)]
    with open("data/VCModes.json", "r", encoding="utf-8") as f:
        data = json.load(f)
    return data[mode]

def set_id_in_db(channel_id: int, mode: str):
    with open("data/VC.json", "r", encoding="utf-8") as f:
        data = json.load(f)
    data[str(channel_id)] = mode
    with open("data/VC.json", "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=4)

def get_voice_number(channel: disnake.VoiceChannel):
    numbers = []
    for ch in channel.category.channels:
        if ch.name.startswith(channel.name.split(" - ")[0]):
            try:
                num = int(ch.name.split(" - ")[1])
                numbers.append(num)
            except:
                pass
    return max(numbers) + 1 if len(numbers) > 0 else 1


@bot.event
async def on_ready():
    print(f"Logged in as {bot.user.name} ({bot.user.id})")
    print("--------------------------------------------------")


@bot.slash_command()
async def setvoicecategory(inter, channel: disnake.CategoryChannel):
    with open("data/config.json", "r", encoding="utf-8") as f:
        data = json.load(f)

    data["category_id"] = channel.id

    with open("data/config.json", "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=4)

    await inter.response.send_message(f"Voice category set to [{channel.mention}]!", ephemeral=True)


@bot.slash_command()
async def addvoicecreator(inter, channel: disnake.VoiceChannel, mode: str):
    if mode not in ["default", "vip", "admin"]:
        await inter.response.send_message(f"Invalid mode. Please choose from 'default', 'vip', or 'admin'.", ephemeral=True)
        return

    set_id_in_db(channel.id, mode)

    await inter.response.send_message(f"Voice creator set in [{channel.mention}] for mode [{mode}]!", ephemeral=True)


@bot.slash_command()
async def deletevoicecreator(inter, channel_id: str):
    try:
        channel_id = int(channel_id)
    except ValueError:
        await inter.response.send_message(f"Invalid channel ID: {channel_id}. Please provide a valid integer.", ephemeral=True)
        return
    if not channel_id_in_db(channel_id):
        await inter.response.send_message(f"No voice creator found in [{channel_id}].", ephemeral=True)
        return

    with open("data/VC.json", "r", encoding="utf-8") as f:
        data = json.load(f)

    del data[str(channel_id)]

    with open("data/VC.json", "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=4)

    await inter.response.send_message(f"Voice creator deleted in [{channel_id}]!", ephemeral=True)


@bot.slash_command()
async def listvoicecreators(inter):
    with open("data/VC.json", "r", encoding="utf-8") as f:
        data = json.load(f)

    if not data:
        await inter.response.send_message("No voice creators found.", ephemeral=True)
        return

    embed = disnake.Embed(title="Voice Creators", color=disnake.Color.blue())
    for channel_id, mode in data.items():
        channel = bot.get_channel(int(channel_id))
        if channel:
            embed.add_field(name=f"{channel.name} [{channel.id}]", value=f"Mode: {mode}", inline=False)

    await inter.response.send_message(embed=embed, ephemeral=True)


@bot.slash_command()
async def sendembed(inter, channel: disnake.TextChannel, name: str):
    try:
        with open(f"data/{name}.json", "r", encoding="utf-8") as f:
            message_data = json.load(f)

        if "content" in message_data:
            if message_data["content"] != "" and message_data["content"] is not None:
                await channel.send(message_data["content"])
        
        if "embeds" in message_data:
            for embed in message_data["embeds"]:
                await channel.send(embed=disnake.Embed.from_dict(embed))
        else:
            await channel.send(embed=disnake.Embed.from_dict(message_data))
            
        await inter.response.send_message(f"Embed [{name}] sent to [{channel.mention}]!", ephemeral=True)

    except FileNotFoundError:
        await inter.response.send_message(f"File [data/{name}.json] not found.", ephemeral=True)

    except json.JSONDecodeError:
        await inter.response.send_message(f"File [data/{name}.json] contains invalid JSON.", ephemeral=True)

    except Exception as e:
        await inter.response.send_message(f"An error occurred: {e}", ephemeral=True)


@bot.event
async def on_voice_state_update(member: disnake.Member, before, after: disnake.VoiceState):
    if before.channel is not None:
        if before.channel.id in active_voices:
            if len(before.channel.members) == 0:
                active_voices.remove(before.channel.id)
                try:
                    await before.channel.delete()
                except disnake.NotFound:
                    pass

    if after.channel is not None:
        ch: disnake.VoiceChannel = after.channel
        id: int = ch.id
        
        if channel_id_in_db(id):
            with open("data/config.json", "r", encoding="utf-8") as f:
                config = json.load(f)
            category: disnake.CategoryChannel = bot.get_channel(config["category_id"])
            if category is None:
                await member.send("The voice category is not found!")
                return
            new_channel = await after.channel.clone(
                category=category,
                name=f"{ch.name} - {get_voice_number(ch)}",
                user_limit=99,
                position=len(category.channels)
            )
            active_voices.append(new_channel.id)
            route = disnake.http.Route("PUT", "/channels/{channel_id}/voice-status", channel_id=new_channel.id)
            await bot.http.request(route, json={"status": get_status_in_db(id)})

            await asyncio.sleep(0.1)
            try:
                await member.move_to(new_channel)
            except:
                await asyncio.sleep(0.1)
                await member.move_to(new_channel)


@bot.event
async def on_guild_channel_delete(channel):
    if channel.id in active_voices:
        active_voices.remove(channel.id)         


TOKEN = os.getenv("BOT_TOKEN")
bot.run(TOKEN)