from discord.ext import commands
from discord import Embed, File
from random import choice
import requests

CTAs = [ 
    "https://cdn.discordapp.com/attachments/920776187884732559/1003376008486977626/cta_cute.mp4",
    "https://cdn.discordapp.com/attachments/920776187884732559/1003807644877848636/cta2.mp4",
    "https://cdn.discordapp.com/attachments/920776187884732559/1003806722546221076/ctabnuuy.mo4.mp4",
    "https://cdn.discordapp.com/attachments/920776187884732559/1003806603180515418/bnuuyandcat.mp4",
    "https://cdn.discordapp.com/attachments/920776187884732559/1003421957968109568/cat2.mp4",
]

class Cat(commands.Cog):

    @commands.command( name = "cta" )
    async def cta( self, ctx ):
        await ctx.send( choice( CTAs ) )

    @commands.command( name = "cat" )
    async def cat( self, ctx, *args ):
        
        end = "png"
        url = "https://cataas.com/cat"

        if ( len( args ) != 0 ):
            match args[0]:
                case "gif":
                    end = "gif"
                    url = "https://cataas.com/cat/gif"
                    

        r = requests.get( url )
        
        if r.status_code == 200:
            with open( f"pics/cat.{end}" , 'wb' ) as file:
                for chunk in r:
                    file.write( chunk )
        
        with open( f"pics/cat.{end}" , 'rb' ) as file:
            image = image = File( file, f"cat.{end}" )
        
        await ctx.send( file = image )
        

        