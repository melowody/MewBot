import asyncio, aiohttp, discord, codecs, subprocess, aiosqlite
from discord.ext import commands

class Mod:

    def __init__(self, bot):
        self.bot = bot

    @commands.command(pass_context=True, description="Set the prefix that your server will use!", brief='mb!gprefix m!', aliases=['gprefix'])
    async def guildprefix(self, ctx, *args):
        if(ctx.message.author.guild_permissions.manage_guild):
            prefix = ' '.join(args)
            async with aiosqlite.connect("./Resources/Interactive/ServerPrefixes.db") as conn:
                c = await conn.execute("SELECT * FROM Prefixes")
                server_id = ctx.message.guild.id
                data = [i[0] for i in await c.fetchall()]
                if(server_id in data):
                    await conn.execute("UPDATE Prefixes SET Prefix = ? WHERE ServerID = ?", (prefix, server_id))
                    await conn.commit()
                    await c.close()
                    await conn.close()
                else:
                    await conn.execute("INSERT INTO Prefixes VALUES(?, ?)", (server_id, prefix))
                    await conn.commit()
                    await c.close()
                    await conn.close()
                await ctx.send("Server Prefix set to ***__" + prefix + "__***!")
        else:
            await ctx.send("You do not have the `Manage Guild` permission!")

    @commands.command(pass_context=True, aliases=["exec"], description="BOT OWNER ONLY: Execute some python code!", brief='mb!execute "print(\'Hello, world!\')"')
    async def execute(self, ctx, c):
        if(ctx.message.author.id == 190804082032640000):
            with codecs.open("./Resources/Interactive/thing.py", "w", encoding="utf8") as f:
                f.write(c)
            x = subprocess.check_output(["py", ".\\Resources\\Interactive\\thing.py"], shell=True)
            emb = (discord.Embed(color=0xf7b8cf))
            emb.add_field(name="Execute", value="```" + x.decode() + "```")
            await ctx.send(embed=emb)
        else:
            await ctx.send("You're not allowed.")

    @commands.command(pass_context=True, description="ADMIN: Kick someone from your server!", brief='mb!kick @Lemon')
    async def kick(self, ctx, *args):
        if(ctx.message.author.guild_permissions.kick_members):
            try:
                if(args[0].startswith('<@') and args[0].endswith('>')):
                    user = await self.bot.get_user_info(int(args[0].split('@')[1].split('>')[0]))
                elif(args[0].isdigit()):
                    user = await self.bot.get_user_info(int(args[0]))
                n = user.name
                d = user.discriminator
                await ctx.message.guild.kick(user)
                await ctx.send("Kicked " + str(n) + "#" + str(d) + "!")
            except:
                await ctx.send("I cannot kick that user! Either they do not exist or I don't have enough permissions!")
        else:
            await ctx.send("You do not have the `Kick Members` permission!")

    @commands.command(pass_context=True, description="ADMIN: Ban someone from your server!", brief='mb!ban @Orange')
    async def ban(self, ctx, user: discord.User):
        if (ctx.message.author.guild_permissions.ban_members):
            try:
                if(args[0].startswith('<@') and args[0].endswith('>')):
                    user = await self.bot.get_user_info(int(args[0].split('@')[1].split('>')[0]))
                elif(args[0].isdigit()):
                    user = await self.bot.get_user_info(int(args[0]))
                n = user.name
                d = user.discriminator
                await ctx.message.guild.ban(user)
                await ctx.send("Banned " + str(n) + "#" + str(d) + "!")
            except:
                await ctx.send("I cannot ban that user! Either they do not exist or I don't have enough permissions!")
        else:
            await ctx.send("You do not have the `Ban Members` permission!")

    @commands.command(pass_context=True, description="ADMIN: Purge the chat!", brief='mb!purge 5')
    async def purge(self, ctx, num: int):
        if(ctx.message.author.guild_permissions.manage_messages):
            await ctx.message.channel.purge(limit=num+1)
        else:
            await ctx.send("You do not have the `Manage Messages` permission!")

def setup(bot):
    bot.add_cog(Mod(bot))
