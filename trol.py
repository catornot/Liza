from discord import Embed, File, Color, User, TextChannel, DMChannel, Message, HTTPException
from discord.ext import commands
from os import walk
from random import choice
from time import sleep

whitelist = [ 645370715922497589, 625796609804075070 ]

class Trol(commands.Cog):

    def CanTrol( self, ctx ):
        if ( ctx.author.id in whitelist ):
            return True
        return False
    
    async def RejectTrol( self, ctx ):
        await ctx.send( f"{ctx.mention} nah", delete_after = 1 )
        await ctx.message.delete()

    @commands.command( name = "liza" )
    async def liza( self, ctx, *args ):

        if ( not self.CanTrol( ctx ) ):
            await self.RejectTrol( ctx )
            return

        message = ""
        for arg in args:
            message += " " + arg
        
        await ctx.channel.purge(limit=1)
        
        await ctx.send( message )
    
    @commands.command( name = "trol" )
    async def trol( self, ctx ):

        if ( not self.CanTrol( ctx ) ):
            await self.RejectTrol( ctx )
            return
        
        trols = []
        for root, dirs, files in walk("pics"):
            for fl in files:
                if ( fl.startswith( "trol" ) ):
                    trols.append( fl )
        
        with open( f"pics/{ choice( trols ) }", "rb" ) as file:
            image = File( file, "image.png" )
        
        await ctx.message.delete()
        await ctx.send( file = image )

    @commands.command( name ="fakeban" )
    async def fakeban( self, ctx, target : User, reason : str ):

        if ( not self.CanTrol( ctx ) ):
            await self.RejectTrol( ctx )
            return
        
        embed = Embed( title = f"Banned {target.display_name}", colour = Color.magenta(), description = f"{target.display_name} was banned for {reason}" )
        
        await ctx.message.delete()
        await ctx.send ( embed = embed )

channel_id = 1004076238626902117

class Talk(commands.Cog):
    
    target = None

    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_command_error( self, ctx, error ):
        
        embed = Embed( description = error )
        
        if ( isinstance( error, HTTPException ) ):
            embed.set_image( f"https://http.cat/{error.code}" )

        await ctx.send( embed = embed )
    
    @commands.Cog.listener()
    async def on_message( self, message: Message ):
        content = message.content
        
        if ( content.startswith( "?" ) or message.author == self.bot.user ):
            return
            
        if ( self.target != None and message.channel.id == channel_id  ):
            await self.target.send( content )

        elif( isinstance( message.channel, DMChannel ) ):
            with open( "dms.txt", "a" ) as file:
                file.write( f"{message.author.display_name}:{message.content}\n" )


    @commands.command( name = "notarget" )
    async def notarget( self, ctx ):
        self.target = None
        await ctx.send( f"cleared target" )

    @commands.command( name = "target" )
    async def target( self, ctx, target:TextChannel ):
        await ctx.send( f"target channel is set to {target.name}" )
        self.target = target
        
    @commands.command( name = "dm" )
    async def dm( self, ctx, target:User ):
        await ctx.send( f"target user is set to {target.name}" )
        self.target = target
    
    @commands.command( name = "dms" )
    async def dms( self, ctx, user:User ):
        messages = ""
        with open( "dms.txt", "r" ) as file:
            messages = file.read()

        if ( messages == "" ):
            await ctx.send( "no dms :skull:" )
            return
        
        messages = messages.split("\n")
        
        embed = Embed( title = f"{user.display_name}'s dms with me" )
        
        for message in messages:
        
            if ( message == "" ):
                continue

            name, text = message.split(":")

            if ( user.display_name == name ):
                embed.add_field( name = "🟢", value = text, inline = False )
        
        await ctx.send( embed = embed )
    
    @commands.command( name = "cleardms" )
    async def cleardms( self, ctx, user:User ):
        messages = ""
        with open( "dms.txt", "r" ) as file:
            messages = file.read()

        if ( messages == "" ):
            await ctx.send( "no dms :skull:" )
            return
        
        messages = messages.split("\n")

        new_messages = ""
        
        for message in messages:
        
            if ( message == "" ):
                continue

            if ( user.display_name == message.split(":")[0] ):
                continue
            
            new_messages = f"{new_messages}\n{message}"
    
        
        with open( "dms.txt", "w" ) as file:
            file.write( new_messages )
        
        await ctx.send( f"cleared {user.display_name}'s dms" )

