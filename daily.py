from discord import Embed, File, Color, User, TextChannel
from discord.ext import commands, tasks
from time import time, sleep
from io import BytesIO
import moviepy.editor as mp
from random import choice
import json
import os
import requests

day = 86400
wait_time = 3600

def load_data():
    with open( "daily_data.json", "r" ) as file:
        return json.loads( file.read() )

def load_data_by_id( id ):
    if ( not id in load_data() ):
        print( load_data() )
        return {}
    
    return load_data()[id]

def write_data( data ):
    with open( "daily_data.json", "w" ) as file:
        file.write( json.dumps( data, indent=4 ) )

def write_data_by_id( id, data ):
    d = load_data()
    d[id] = data
    write_data( d )


class Daily(commands.Cog):
    
    routine = None

    def __init__(self, bot):
        self.bot = bot
    
    @commands.Cog.listener()
    async def on_ready( self ):
        self.routine = Routine()
        self.routine.Start( self.bot )

    @commands.command( name = "setup_daily_cat" )
    async def SetupDailyCat( self, ctx, guild:int, channel:int, id:str ):
        pass
    
    @commands.command( name = "add_daily_cat" )
    async def StartDailyCat( self, ctx, id:str ):

        routine = load_data_by_id( "routine" )
        routine.append( id )
        write_data_by_id( "routine", routine )
        
        await ctx.send( f"{id} was added to daily" )
    
    @commands.command( name = "remove_daily_cat" )
    async def RemoveDailyCat( self, ctx, id:str ):

        routine = load_data_by_id( "routine" )
        routine.remove( id )
        write_data_by_id( "routine", routine )

        await ctx.send( f"{id} was removed from daily" )
    
    @commands.command( name = "start_daily_cat" )
    async def StartDailyCat( self, ctx ):
        self.routine = Routine()
        self.routine.Start( self.bot )

        await ctx.send( "started daily cats" )
    
    @commands.command( name = "stop_daily_cat" )
    async def StopDailyCat( self, ctx ):
        
        self.routine.Stop()
        self.routine = None

        await ctx.send( f"stoped daily cat posts" )
    

class Routine:

    bot = None

    def Start( self, bot ):
        self.bot = bot
        self.Run.start()
    
    def Stop( self ):
        self.Run.cancel()
    
    async def CatImage( self, guild, channel, data ):
        r = requests.get( "https://cataas.com/cat" )
                        
        if r.status_code != 200:
            await channel.send( f"https://http.cat/{r.status_code}" )
            return

        image = File( BytesIO(r.content), f"cat.png" )
        
        role = guild.get_role( data["role"] )
        message = data["message"]
        await channel.send( f"{role.mention} {message}", file = image )

        print( "did daily cat for channel " + channel.name )
    
    async def CatVideo( self, guild, channel, data ):
        r = requests.get( "https://cataas.com/cat/gif" )

        if r.status_code != 200:
            await channel.send( f"https://http.cat/{r.status_code}" )
            return
        
        async with channel.typing():
            with open( "pics/cat.gif" , 'wb' ) as file:
                for chunk in r:
                    file.write( chunk )
            
            clip = mp.VideoFileClip( "pics/cat.gif" )
            clip.resize( width = 240 )

            entries = os.listdir( "funny_sounds/" )
            
            audio = mp.AudioFileClip( f"funny_sounds/{choice(entries) }"  )

            if ( audio.duration > clip.duration ):
                audio = audio.cutout( clip.duration, audio.duration )

            clip = clip.set_audio( audio )
            
            clip.write_videofile( "pics/cat.mp4" )
            clip.close()
            audio.close()

            vid = File( "pics/cat.mp4", "cat.mp4" )
        
            role = guild.get_role( data["role"] )
            message = data["message"]
            await channel.send( f"{role.mention} {message}", file = vid )
    
    @tasks.loop(seconds=wait_time)
    async def Run( self ):

        print( "trying to run daily cat" )
            
        if ( not load_data_by_id( "last_time" ) + day < time() ):
            return
        
        print( "posting daily cat" )

        write_data_by_id( "last_time", int( time() ) )

        routine = load_data_by_id( "routine" )

        for guild in self.bot.guilds:
            for run in routine:

                data = load_data_by_id( run )

                if ( data["guild"] == guild.id ):

                    channel = guild.get_channel( data["channel"] )

                    if ( channel != None and isinstance( channel, TextChannel ) ):
                        match data["type"] :
                            case "picture":
                                await self.CatImage( guild, channel, data )
                            case "video":
                                await self.CatVideo( guild, channel, data )

                

