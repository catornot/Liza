import discord
from discord.ext import commands
from trol import Trol, Talk
from events import Adventure
from funny import Cat

with open( "secret.txt", "r" ) as file:
    secret = file.read()

# prefix 
bot = commands.Bot( command_prefix = "?" )

@bot.event
async def on_ready():
    print(f"{bot.user} is ready and online!")
    await bot.change_presence(
        status=discord.Status.online,
        activity=discord.Game( "Titanfall 2" )
    )

# adding cogs
bot.add_cog( Trol( bot ) )
bot.add_cog( Talk( bot ) )
# bot.add_cog( Adventure( bot ) )
bot.add_cog( Cat( bot ) )

# token and run
bot.run( secret )