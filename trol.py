from discord import Embed, File, Color, User, TextChannel
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
    
    @commands.Cog.listener()
    async def on_command_error( ctx, error ):
        await ctx.send( error )

    @commands.command( name = "target" )
    async def target( self, ctx, target : TextChannel ):
        pass
