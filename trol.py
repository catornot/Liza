from discord import Embed, File, Color
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
        await ctx.send( "<@{}> nah".format( ctx.author.id  ), delete_after = 0.5 )
        sleep( 0.5 )
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