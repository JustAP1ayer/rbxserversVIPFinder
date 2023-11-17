import discord
from discord.ext import commands
import requests
import datetime
import re
# copy pasted imports from my discord bot got lazy
intents = discord.Intents.all()
bot = commands.Bot(command_prefix=str(open("command.txt", "r").read().strip()), intents=intents)

@bot.event
async def on_ready():
    print(f"Logged in as {bot.user}")

@bot.command()
@commands.cooldown(1, num(open("delay.txt", "r").read().strip()), commands.BucketType.user)

async def game2vips(ctx, game_id1: str):
    try:
        if "games/" in game_id1:
            game_id = game_id1.split("/games/")[1].split("/")[0]
        else:
            game_id = game_id1

        url = f'https://rbxservers.xyz/games/{game_id}'
        response = requests.get(url)

        if response.status_code == 200:
            content = response.content.decode('utf-8')  
            matches = re.finditer(r'/servers/', content)

            vip_links = []  

            if matches:
                for match in matches:
                    start_index = match.end() 
                    end_index = content.find('"', start_index) 
                    if end_index != -1:
                        server_id = content[start_index:end_index]
                        server_url = f'https://rbxservers.xyz/servers/{server_id}'

                        server_response = requests.get(server_url)
                        if server_response.status_code == 200:
                            server_content = server_response.content.decode('utf-8')
                            vip_matches = re.finditer(r'https://www\.roblox\.com/\S+', server_content)
                            if vip_matches:
                                for vip_match in vip_matches:
                                    vip_link = vip_match.group()
                                    if vip_link.endswith('"'):
                                        vip_link = vip_link[:-1]
                                    vip_links.append(vip_link) 
                            else:
                                ctx.send('No Vips Found')
                        else:
                            ctx.send('No Vips Found')
            if vip_links:
                embed = discord.Embed(title=f"Vip Servers Found (rbxservers.xyz web scraping)", description='```' + '\n'.join(vip_links) + '```' + '\n', color=7419530)
                embed.timestamp = datetime.datetime.utcnow()
                embed.set_footer(text='nyaa~w redblue was here ^~^',icon_url="https://i.imgur.com/hWCLhIZ.png")
                await ctx.send(embed=embed)
            else:
                ctx.send('No Vips Found')
        else:
            ctx.send('Failed to fetch content for the specified game ID')
    except Exception as e:
        print(e)
        await ctx.send("An error occurred while getting VIPs.")

@game2vips.error
async def game2vips_error(ctx, error):
    if isinstance(error, commands.CommandOnCooldown):
        em = discord.Embed(title=f"Slow down!", description=f"Try again in {error.retry_after:.2f}s.", color=15548997)
        em.timestamp = datetime.datetime.utcnow()
        em.set_footer(text='nyaa~w redblue was here ^~^',icon_url="https://i.imgur.com/hWCLhIZ.png")
        await ctx.send(embed=em)

bot.run(str(open("token.txt", "r").read().strip()))
