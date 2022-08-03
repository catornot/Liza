from discord import RawReactionActionEvent
from discord.utils import get
from discord.ext import commands
from time import time, sleep
from emoji import demojize
import json
import requests

def load_data():
    with open( "role_data.json", "r" ) as file:
        return json.loads( file.read() )

def load_data_by_id( id ):
    if ( not id in load_data() ):
        print( load_data() )
        return {}
    
    return load_data()[id]

def write_data( data ):
    with open( "role_data.json", "w" ) as file:
        file.write( json.dumps( data, indent=4 ) )

def write_data_by_id( id, data ):
    d = load_data()
    d[id] = data
    write_data( d )

class Roles(commands.Cog):

    def __init__(self, bot):
        self.bot = bot
    
    @commands.Cog.listener()
    async def on_raw_reaction_add( self, payload:RawReactionActionEvent ):

        if ( not payload.message_id in load_data_by_id( "messages_id" ) ):
            return
        
        data = load_data()

        if ( not demojize( payload.emoji.name ) in data ):
            return
        
        role_name = data[ demojize( payload.emoji.name ) ]
        
        guild = self.bot.get_guild( payload.guild_id )
        member = guild.get_member( payload.user_id )
        role = get( guild.roles, name = role_name )

        await member.add_roles( role, reason = "Cliked Emoji" )
    
    @commands.Cog.listener()
    async def on_raw_reaction_remove( self, payload:RawReactionActionEvent ):
        
        if ( not payload.message_id in load_data_by_id( "messages_id" ) ):
            return
        
        data = load_data()

        if ( not demojize( payload.emoji.name ) in data ):
            return
        
        role_name = data[ demojize( payload.emoji.name ) ]
        
        guild = self.bot.get_guild( payload.guild_id )
        member = guild.get_member( payload.user_id )
        role = get( guild.roles, name = role_name )

        await member.remove_roles( role, reason = "Cliked Emoji" )