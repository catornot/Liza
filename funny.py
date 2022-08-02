from discord.ext import commands
from discord import Embed, File
from random import choice
from PIL import Image, ImageDraw, ImageFont
from io import BytesIO
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
    
    async def cat_title( self, ctx, url, *args ):

        message = ""
        for arg in args:
            message += " " + arg
        
        r = requests.get( url )

        if r.status_code == 200:
            img = Image.open(BytesIO(r.content))

            draw = ImageDraw.Draw(img)

            fnt = ImageFont.truetype("Pillow/Tests/fonts/FreeMono.ttf", 40)

            draw.text( (img.size[0] * 0.5, img.size[1] * 0.15), message, font = fnt( 255, 255, 255 ) )
            img.save( "pics/cat.png" )
        else:
            await ctx.send( f"https://http.cat/{r.status_code}" )
            return
        
        with open( "pics/cat.png" , 'rb' ) as file:
            image = image = File( file, f"cat.png" )
        
        await ctx.send( file = image )

    @commands.command( name = "cat" )
    async def cat( self, ctx, *args:list ):
        
        end = "png"
        url = "https://cataas.com/cat"

        if ( len( args ) != 0 ):
            match args[0]:
                case "gif":
                    end = "gif"
                    url = "https://cataas.com/cat/gif"
                case "title":
                    args.pop(0)
                    await self.cat_title( ctx, url, args )
                    return
                    

        r = requests.get( url )
        
        if r.status_code == 200:
            with open( f"pics/cat.{end}" , 'wb' ) as file:
                for chunk in r:
                    file.write( chunk )
        else:
            await ctx.send( f"https://http.cat/{r.status_code}" )
            return
        
        with open( f"pics/cat.{end}" , 'rb' ) as file:
            image = image = File( file, f"cat.{end}" )
        
        await ctx.send( file = image )
        

        