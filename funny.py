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
    "https://cdn.discordapp.com/attachments/920776187884732559/1003376701130154074/cat_look_away.png",
    "https://cdn.discordapp.com/attachments/920776187884732559/1003376704770809896/cat_furniture.jpeg",
    "https://cdn.discordapp.com/attachments/920776187884732559/1003376704183603241/cat_above.mp4",
    "https://cdn.discordapp.com/attachments/920776187884732559/1003376703692877945/cat_and_guns.mp4",
    "https://cdn.discordapp.com/attachments/920776187884732559/1003376703323775146/cat_2.mp4",
    "https://cdn.discordapp.com/attachments/920776187884732559/1003376702858203207/cat_expl.mp4",
    "https://cdn.discordapp.com/attachments/920776187884732559/1003376702522667120/cat.mp4",
    "https://cdn.discordapp.com/attachments/920776187884732559/1003376702166147153/catt.mp4",
    "https://cdn.discordapp.com/attachments/920776187884732559/1003376701838987334/cats_halflife.mp4",
    "https://cdn.discordapp.com/attachments/920776187884732559/1003376701495062698/cat_real_or_fake.mp4",
    "https://cdn.discordapp.com/attachments/920776187884732559/1003376756494975006/music_cta.mp4",
    "https://cdn.discordapp.com/attachments/920776187884732559/1003376756868264116/ctamf.mp4",
    "https://cdn.discordapp.com/attachments/920776187884732559/1003376757174456320/cta.mp4"
]

class Cat(commands.Cog):

    @commands.command( name = "cta" )
    async def cta( self, ctx, *index ):
        
        link = choice( CTAs )

        if ( len( index ) != 0 and int( index[0] ) > -1 and int( index[0] ) < len(CTAs) ):
            link = CTAs[ int( index[0] ) ]

        await ctx.send( link )
    
    async def cat_title( self, ctx, url, args ):

        message = ""
        for arg in args:
            message += " " + arg
        
        r = requests.get( url )

        if r.status_code == 200:
            img = Image.open(BytesIO(r.content))

            draw = ImageDraw.Draw(img)

            # fnt = ImageFont.truetype("Pillow/Tests/fonts/FreeMono.ttf", 40)

            draw.text( (img.size[0] * 0.5, img.size[1] * 0.15), message, ( 255, 255, 255 ) )
            img.save( "pics/cat.png" )
        else:
            await ctx.send( f"https://http.cat/{r.status_code}" )
            return
        
        with open( "pics/cat.png" , 'rb' ) as file:
            image = image = File( file, f"cat.png" )
        
        await ctx.send( file = image )
    
    async def cat_movie( self, ctx, url ):
        
        r = requests.get( url )

        if r.status_code == 200:
            
            with open( f"pics/cat.{end}" , 'wb' ) as file:
                for chunk in r:
                    file.write( chunk )

            img = Image.open(BytesIO(r.content))
            img.save( "pics/cat." )
        else:
            await ctx.send( f"https://http.cat/{r.status_code}" )
            return
        
        with open( "pics/cat.png" , 'rb' ) as file:
            image = image = File( file, f"cat.png" )
        
        await ctx.send( file = image )

    @commands.command( name = "cat" )
    async def cat( self, ctx, *args ):
        
        end = "png"
        url = "https://cataas.com/cat"

        if ( len( args ) != 0 ):
            match args[0]:
                case "gif":
                    end = "gif"
                    url = "https://cataas.com/cat/gif"
                case "title":
                    args = list( args )
                    args.pop(0)
                    await self.cat_title( ctx, url, args )
                    return
                case "movie":
                    await self.cat_movie( ctx, url )
                    return
                    
        r = requests.get( url )
        
        if r.status_code == 200:
            image = File( BytesIO(r.content), f"cat.{end}" )
            await ctx.send( file = image )
        else:
            await ctx.send( f"https://http.cat/{r.status_code}" )
            return
        

        