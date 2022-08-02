import discord
from discord.ext import commands
from trol import Trol

with open( "secret.txt", "r" ) as file:
    secret = file.read()

# prefix 
bot = commands.Bot(command_prefix='?')

# adding cogs
bot.add_cog(Trol(bot))

# token and run
bot.run( secret )