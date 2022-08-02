import discord
from discord.ext import commands

with open( "secret.txt", "r" ) as file:
    secret = file.read()

bot = commands.Bot(command_prefix='?')

@bot.command()
async def test(ctx):
    await ctx.send( "test" )


bot.run( secret )