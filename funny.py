from discord.ext import commands
from discord import Embed, File, User
from random import choice
from PIL import Image, ImageDraw, ImageFont
from io import BytesIO
import requests
import moviepy.editor as mp
import moviepy
import os

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
    "https://cdn.discordapp.com/attachments/920776187884732559/1003376757174456320/cta.mp4",
    "https://cdn.discordapp.com/attachments/1004446607762280491/1004858314712174653/MemeFeedBot_6-1.mp4",
    "https://cdn.discordapp.com/attachments/987730053439827998/1005539542830428180/rcYZgTyNUOCP42JW.mp4",
    "https://cdn.discordapp.com/attachments/951461326478262292/1007066855854329997/cta.mp4"
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
            image = File( file, f"cat.png" )
        
        await ctx.send( file = image )
    
    async def cat_movie( self, ctx, url, args ):
        
        r = requests.get( url )

        if r.status_code != 200:
            await ctx.send( f"https://http.cat/{r.status_code}" )
            return
        
        async with ctx.channel.typing():
            with open( "pics/cat.gif" , 'wb' ) as file:
                for chunk in r:
                    file.write( chunk )
            
            clip = mp.VideoFileClip( "pics/cat.gif" )
            clip.resize( width = 240 )

            entries = os.listdir( "funny_sounds/" )
            
            audio = mp.AudioFileClip( f"funny_sounds/{choice(entries) }"  )

            if ( audio.duration > clip.duration and "cut" in args ):
                audio = audio.cutout( clip.duration, audio.duration )

            clip = clip.set_audio( audio )
            
            clip.write_videofile( "pics/cat.mp4" )
            clip.close()
            audio.close()

            vid = File( "pics/cat.mp4", "cat.mp4" )
        
            await ctx.send( file = vid )
            

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
                    message = ""
                    for arg in args:
                        message += " " + arg
                    url = f"https://cataas.com/cat/says/{message}"
                case "movie":
                    args = list( args )
                    args.pop(0)
                    url = "https://cataas.com/cat/gif"
                    await self.cat_movie( ctx, url, args )
                    return
                case "tag":
                    url = f"https://cataas.com/cat/{args[1]}"
                case "new":
                    url = f"https://thiscatdoesnotexist.com/"
                    
        r = requests.get( url )
        
        if r.status_code == 200:
            image = File( BytesIO(r.content), f"cat.{end}" )
            await ctx.send( file = image )
        else:
            await ctx.send( f"https://http.cat/{r.status_code}" )
    
    @commands.command( name = "age" )
    async def age( self, ctx, target : User ):
        await ctx.send( target.created_at )
        

# TODO: https://thiscatdoesnotexist.com/
# video montage with these cats
        