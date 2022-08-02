from discord import Embed, File, Color, User
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
        await ctx.send( f"{ctx.mention} nah", delete_after = 0.5 )
        sleep( 0.5 )
        await ctx.message.delete()

    @commands.command( name = "liza", description="Massive trol" )
    async def liza( self, ctx, *args ):

        if ( not self.CanTrol( ctx ) ):
            await self.RejectTrol( ctx )
            return

        message = ""
        for arg in args:
            message += " " + arg
        
        await ctx.channel.purge(limit=1)
        
        await ctx.send( message )
    
    @commands.command( name = "trol", description="Small trol" )
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

    @commands.command( name ="fakeban", description="ban someone" )
    async def fakeban( self, ctx, target : User, reason : str ):

        if ( not self.CanTrol( ctx ) ):
            await self.RejectTrol( ctx )
            return
        
        embed = Embed( title = f"Banned {target.display_name}", colour = Color.magenta(), description = f"{target.display_name} was banned for {reason}" )

        await ctx.send ( embed = embed )