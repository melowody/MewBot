import discord, aiohttp, asyncio, datetime, sqlite3, itertools, Resources.Lib.ImgLib as ImgLib
from discord.ext import commands

class Money:
    def __init__(self, bot):
        self.bot = bot

    @commands.command(pass_context=True, description="Pay someone!", brief='mb!pay @EdgyBot 10')
    async def pay(self, ctx, *args):
        if(args != ()):
            s = args[0]
        else:
            s = "E"
        user1 = await self.bot.get_user_info(ctx.message.author.id)
        if (s[:2] == "<@" and s[-1] == ">"):
            if (s[:3] == "<@!"):
                x = s.split("<@!")[1].split(">")[0]
            else:
                x = s.split("<@")[1].split(">")[0]
        elif (s.isdigit()):
            x = s
        else:
            await ctx.send("You must mention someone to pay them!")
            return
        try:
            user2 = await self.bot.get_user_info(x)
        except:
            await ctx.send("You must mention someone to pay them!")
            return
        conn = sqlite3.connect('./Resources/Interactive/Economy.db')
        c = conn.cursor()
        c.execute('SELECT * FROM Bank')
        data = c.fetchall()
        u1p = -1
        u2p = -1
        for i in data:
            if(user1.id in i):
                u1p = data.index(i)
            if(user2.id in i):
                u2p = data.index(i)
        if(u1p == -1):
            await ctx.send("You don't have an account! Use `mb!money` to make one!")
            return
        elif(u2p == -1):
            await ctx.send(user2.name + " does not have an account! Tell them to make one with `mb!money`!")
            return
        elif(u1p == u2p):
            await ctx.send("You cannot pay yourself!")
            return
        else:
            if(len(args) == 1):
                await ctx.send("You need an amount to pay!")
                return
            else:
                amount = int(args[1])
                if(amount <= 0):
                    await ctx.send("You can't do that.")
                    return
                else:
                    c.execute("UPDATE Bank SET Balance=? WHERE ClientID=?", (data[u1p][1] - amount, user1.id))
                    c.execute("UPDATE Bank SET Balance=? WHERE ClientID=?", (data[u2p][1] + amount, user2.id))
        await ctx.send(user1.mention + " payed " + user2.mention + " $" + str(amount) + "!")
        conn.commit()
        c.close()
        conn.close()


    @commands.command(pass_context=True, description="Get the money of someone or yourself!", brief='mb!money @Bagles')
    async def money(self, ctx, *args):
        current = datetime.datetime.now()
        if (args == ()):
            x = ctx.message.author.id
            s = ""
        else:
            s = args[0]
        conn = sqlite3.connect('./Resources/Interactive/Economy.db')
        c = conn.cursor()
        c.execute('SELECT * FROM Bank')
        data = c.fetchall()
        if (s[:2] == "<@" and s[-1] == ">"):
            if (args[0][:3] == "<@!"):
                x = args[0].split("<@!")[1].split(">")[0]
            else:
                x = args[0].split("<@")[1].split(">")[0]
        elif (s.isdigit()):
            x = s
        else:
            x = ctx.message.author.id
        x = int(x)
        user = await self.bot.get_user_info(x)
        cpos = -1
        for i in data:
            if(x in i):
                cpos = data.index(i)
        if(cpos != -1):
            await ctx.send(user.name + " has $" + str(data[cpos][1]) + "!")
        else:
            if(user.id != ctx.message.author.id):
                await ctx.send(user.name + " does not have an account! Tell them to make one with `mb!money`!")
            else:
                c.execute("INSERT INTO Bank VALUES(?, ?, ?)", (x, 0, "New"))
                await ctx.send("You didn't have an account, so I made one for you! Current Balance: $0")
        conn.commit()
        c.close()
        conn.close()


    @commands.command(pass_context=True, description="Get your daily money!", brief='mb!daily')
    async def daily(self, ctx):
        current = datetime.datetime.now()
        x = ctx.message.author.id
        conn = sqlite3.connect('./Resources/Interactive/Economy.db')
        c = conn.cursor()
        c.execute('SELECT * FROM Bank')
        data = c.fetchall()
        cpos = -1
        for i in data:
            if(x in i):
                cpos = data.index(i)
        if(cpos != -1):
            ci = data[cpos]
            if(ci[2] == "New" or current > datetime.datetime.strptime(ci[2], '%b %d %Y %I:%M%p') + datetime.timedelta(days=1)):
                c.execute("UPDATE Bank SET Balance = ? WHERE ClientID = ?", (ci[1] + 50, x))
                c.execute("UPDATE Bank SET LastDaily = ? WHERE ClientID = ?", (current.strftime('%b %d %Y %I:%M%p'), x))
                conn.commit()
                c.close()
                conn.close()
                await ctx.send("Daily Reward Claimed: $50!")
            else:
                lastdaily = datetime.datetime.strptime(ci[2], '%b %d %Y %I:%M%p')
                tl = lastdaily + datetime.timedelta(days=1) - current
                tl = tl - datetime.timedelta(microseconds=tl.microseconds)
                await ctx.send("You have " + str(tl) + " left!")
        else:
            c.execute("INSERT INTO Bank VALUES(?, ?, ?)", (x, 50, current.strftime('%b %d %Y %I:%M%p')))
            conn.commit()
            c.close()
            conn.close()
            await ctx.send("You didn't have an account, so I made one for you! Current Balance: $50")

def setup(bot):
    bot.add_cog(Money(bot))
