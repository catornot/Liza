from discord.ext import commands

categories = [ 1004064554780721242 ]

class Adventure(commands.Cog):
    games = {}

    async def CreateGame( self, ctx ):
        if ( ctx.author.id in self.games ):
            return False
        
        c = None
        for category in ctx.guild.categories:
            if ( category in categories ):
                c = category
        
        if ( not c ):
            return
            
        channel = await c.create_text_channel( ctx.author.display_name + " gaming" )

        self.games[ ctx.author.id ] = channel
