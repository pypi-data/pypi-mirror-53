Hivatalos MDBL API wrapper Pythonhoz!

Példa
--------------

.. code:: py

    import mdbl
    import discord
    from discord.ext import commands
    import asyncio

    class MDBLAPI(commands.Cog):

        def __init__(self, bot):
            self.bot = bot
            self.mdbl = mdbl.Bot()

        @commands.command()
        async def link(self, ctx):
            mdbl_link = self.mdbl.botlink(bot.user.id)
            await ctx.send(mdbl_link)

    def setup(bot):
        bot.add_cog(MDBLAPI(bot))

