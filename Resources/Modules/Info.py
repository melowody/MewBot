import discord, aiohttp, asyncio, Resources.Lib.HypixelLib as HypixelLib, Resources.Interactive.Paginator as Paginator, Resources.Lib.CSGOLib as CSGOLib, Resources.Lib.ImgLib as ImgLib, Resources.Lib.GDLib as GDLib, Resources.Lib.MKWLib as MKWLib, datetime, time, re, html, codecs, whois as wis, aiosqlite, pycountry, io
from PIL import Image
from discord.ext import commands
from mcstatus import MinecraftServer
from twitch import TwitchClient

dupt = datetime.datetime.now()

class Info:
    def __init__(self, bot):
        self.bot = bot

    @commands.command(pass_context=True, description="Graph an equation!", brief="mb!graph EQUATION", aliases=["eq", "equation", "eqgraph", "equationgraph"])
    async def graph(self, ctx, equation):
        async with aiohttp.ClientSession() as cs:
            async with cs.get("http://api.wolframalpha.com/v2/query?input=" + equation + "&appid=" + open("C:/TOKENS/WOLFRAM.txt").read()) as f:
                x = str(await f.read()).split("<pod title='Plot")[1].split('alt')[0].split("src='")[1].split("'")[0] if "<pod title='Plot" in str(await f.read()) else "None"
                r = html.unescape(x)
                if(r == "None"):
                    await ctx.send("That's not a vaild input!")
                    return
            async with cs.get(r) as f:
                x = await f.read()
        plot = Image.open(io.BytesIO(x)).convert("RGB")
        output_buffer = io.BytesIO()
        plot.save(output_buffer, "png")
        output_buffer.seek(0)
        await ctx.send(file=discord.File(output_buffer, filename="plot.png"))
        await ctx.send("Graph by *WolframAlpha*")

    @commands.command(pass_context=True, description="Get the top time for an MKW course!", brief="mb!mkwtop COURSE", aliases=["mkw", "ctgp", "top", "ctgptop", "mariokartwii", "mariokartwiitop", "customtrackgrandprix", "customtrackgrandprixtop"])
    async def mkwtop(self, ctx, *args):
        x = await MKWLib.get_top(self.bot, ctx.message, ' '.join(args))
        if(x != 0):
            emb = (discord.Embed(color=0xf7b8cf))
            emb.set_author(name=x[0])
            emb.add_field(name="Player", value=x[2])
            emb.add_field(name="Time", value=x[1])
            emb.add_field(name="Country", value=x[3])
            emb.add_field(name="Controller", value=x[4])
            emb.add_field(name="Character/Vehicle Combo", value=x[5] + ' - ' + x[6])
            emb.add_field(name="Time Set", value=x[7])
            await ctx.send(embed=emb)
        else:
            await ctx.send("This track does not exist!")

    @commands.command(pass_context=True, description="The help command!", brief="mb!help")
    async def help(self, ctx, *args):
        async with aiosqlite.connect('./Resources/Interactive/Prefixes.db') as conn:
            c = await conn.execute("SELECT * FROM Prefixes")
            buffer = await c.fetchall()
            await c.close()
            await conn.close()
        user_id = ctx.message.author.id
        data = [i[0] for i in buffer]
        prefix = "mb!"
        p = -1
        for j in range(len(data)):
            i = data[j]
            if(i == ctx.message.author.id):
                p = j
        if(p != -1):
            prefix = buffer[p][-1]
        if(args != ()):
            try:
                cmd = args[0]
                x = self.bot.get_command(cmd)
                emb = (discord.Embed(color=0xf7b8cf))
                emb.add_field(name=prefix + x.name, value=x.description)
                emb.add_field(name="Usage", value='`' + x.brief.replace('mb!', prefix) + '`' if not x.brief.startswith('`') else x.brief.replace('mb!', prefix))
                if(x.aliases != []):
                    emb.set_footer(text="Aliases: " + ', '.join(x.aliases))
                else:
                    emb.set_footer(text="Aliases: None")
                await ctx.send(embed=emb)
            except AttributeError:
                await ctx.send("It seems that is not a valid command! Type mb!help for a list of all commands!")
        else:
            cmds = list(self.bot.commands)
            loe = []
            for x in cmds:
                emb = (discord.Embed(color=0xf7b8cf))
                emb.add_field(name=prefix + x.name, value=x.description)
                emb.add_field(name="Usage", value='`' + x.brief.replace('mb!', prefix) + '`' if not x.brief.startswith('`') else x.brief.replace('mb!', prefix))
                if(x.aliases != []):
                    emb.set_footer(text="Aliases: " + ', '.join(x.aliases))
                else:
                    emb.set_footer(text="Aliases: None")
                loe.append(emb)
            await Paginator.PaginatorNoSkip(self.bot, ctx.message, loe)

    @commands.command(pass_context=True, aliases=["lookup", "domain"], description="Get the whois info of a website!", brief='mb!whois google.com')
    async def whois(self, ctx, website):
        try:
            wi = wis.whois(website)
            if(wi['domain_name'] == None):
                await ctx.send('Domain not found!')
            else:
                emb = (discord.Embed(color=0xf7b8cf))
                ud = wi['updated_date']
                emb.set_author(name=website, url=('http://' + website if not website.startswith('http') else website))
                if(wi['registrar']):
                    emb.add_field(name="Registrar", value=wi['registrar'])
                if(wi['creation_date']):
                    if(type(wi['creation_date']) != type([])):
                        emb.add_field(name="Creation Date", value=wi['creation_date'].strftime("%A, %b %d, %Y at %I:%M:%S %p UTC"))
                    else:
                        emb.add_field(name="Creation Date", value=wi['creation_date'][-1].strftime("%A, %b %d, %Y at %I:%M:%S %p UTC"))
                if(ud):
                    emb.add_field(name="Updated Date", value=(ud.strftime("%A, %b %d, %Y at %I:%M:%S %p UTC") if type(ud) != type([]) else ud[-1].strftime("%A, %b %d, %Y at %I:%M:%S %p UTC")))
                if(wi['expiration_date']):
                    emb.add_field(name="Expiration Date", value=(wi['expiration_date'].strftime("%A, %b %d, %Y at %I:%M:%S %p UTC") if type(wi['expiration_date']) != type([]) else wi['expiration_date'][-1].strftime("%A, %b %d, %Y at %I:%M:%S %p UTC")))
                if(wi['name']):
                    emb.add_field(name="Name", value=wi['name'])
                if(wi['org']):
                    emb.add_field(name="Organization", value=wi['org'])
                if(wi['address']):
                    emb.add_field(name="Address", value=wi['address'])
                try:
                    emb.add_field(name="Location", value=wi['city'] + ", " + wi['state'] + pycountry.countries.get(alpha_2=wi['country']).name + " " + ("" if len(wi['zipcode']) != 5 or zipcode == "00000" else wi['zipcode']))
                except:
                    ' '
                await ctx.send(embed=emb)
        except (socket.timeout, ConnectionResetError):
            await ctx.send('Timeout occurred when connecting to ' + website)

    @commands.command(pass_context=True, aliases=["up"], description="Get the uptime of MewBot!", brief='mb!uptime')
    async def uptime(self, ctx):
        global dupt
        y = str(datetime.datetime.now() - dupt).split('.')[0].split(":")
        y[0] += " hours"
        y[1] += " minutes"
        y[2] = "and " + y[2] + " seconds."
        if(y[-3] == "0 hours"):
            y.pop(-3)
        if (y[-2] == "00 minutes"):
            y.pop(-2)
        if (y[-1] == "and 00 seconds."):
            y.pop(-1)
        if(len(y) == 1):
            x = y[0].split("and ")[1]
            y[0] = x
        await ctx.send("MewBot has been online for " + ', '.join(y))

    @commands.command(pass_context=True, description="Get a Paginator of the current demonlist for Geometry Dash!", brief='mb!demonlist')
    async def demonlist(self, ctx):
        await Paginator.DemonlistPaginator(self.bot, ctx.message)

    @commands.command(pass_context=True, aliases=["mcserver", "minecraftserver"], description="Get the player count of a Minecraft server!", brief='mb!server mc.hypixel.net')
    async def server(self, ctx, host):
        if(":" not in host):
            server = MinecraftServer.lookup(host + ":25565")
        else:
            server = MinecraftServer.lookup(host)
        statushow = server.status()
        await ctx.send("There are " + str(statushow.players.online) + " people on " + host)

    @commands.command(pass_context=True, aliases=["twitchchannel"], description="Get the info on a twitch streamer!", brief='mb!twitch CarlSagan42')
    async def twitch(self, ctx, *args):
        x = args[0]
        cl = TwitchClient(client_id=open("C:/TOKENS/TWITCH.txt"))
        if(not x.isdigit()):
            async with aiohttp.ClientSession(connector=aiohttp.TCPConnector(verify_ssl=False)) as cs:
                async with cs.get("https://wind-bow.glitch.me/twitch-api/users/" + x) as r:
                    y = await r.read()
            x = str(y).split('_id":')[1].split(',')[0]
        s = cl.streams.get_stream_by_user(x)
        c = cl.users.get_by_id(int(x))
        emb = (discord.Embed(color=0xf7b8cf))
        emb.set_author(name=c.display_name, url="https://twitch.tv/" + c.name)
        emb.set_thumbnail(url=c.logo)
        emb.add_field(name="Bio", value=c.bio)
        emb.set_footer(text="Channel created at " + (c.created_at + datetime.timedelta(hours=-4)).strftime("%m-%d-%Y %H:%M:%S") + " EST")
        if(s == None):
            await ctx.send(embed=emb)
        else:
            await ctx.send(c.display_name + " is streaming!")
            emb.add_field(name="Followers", value=str(s.channel.followers))
            emb.add_field(name="Stream Name", value=s.channel.status)
            if(s.game == ''):
                game = "None"
            else:
                game = s.game
            emb.add_field(name="Game", value=game)
            emb.add_field(name="Viewers", value=str(s.viewers))
            st = (s.created_at + datetime.timedelta(hours=-4))
            y = str(datetime.datetime.now() - st).split('.')[0].split(":")
            y[0] += " hours"
            y[1] += " minutes"
            y[2] = "and " + y[2] + " seconds."
            if (y[-3] == "0 hours"):
                y.pop(-3)
            if (y[-2] == "00 minutes"):
                y.pop(-2)
            if (y[-1] == "and 00 seconds."):
                y.pop(-1)
            if (len(y) == 1):
                x = y[0].split("and ")[1]
                y[0] = x
            emb.add_field(name="Uptime", value=', '.join(y))
            emb.set_image(url="https://static-cdn.jtvnw.net/previews-ttv/live_user_" + c.name + "-320x180.jpg")
            await ctx.send(embed=emb)

    @commands.command(pass_context=True, description="Get the info on a Geometry Dash level!", brief='mb!level Windy Landscape')
    async def level(self, ctx, *args):
        level = await GDLib.Level.create(' '.join(args))
        emb = (discord.Embed(color=0xf7b8cf))
        emb.set_author(name="Level Info")
        emb.add_field(name="Level Name", value=level.title)
        emb.add_field(name="Level Author", value=level.author)
        emb.add_field(name="Level ID", value=level.id)
        emb.add_field(name="Downloads", value=str(level.downloads))
        emb.add_field(name="Likes", value=str(level.likes))
        emb.add_field(name="Epic?", value="Yes" if level.epic else "No")
        emb.add_field(name="Featured", value="Yes" if level.featured else "No")
        emb.add_field(name="Difficulty", value=(level.difficulty + " " + str(level.stars) + " Stars") if level.stars != 0 else level.difficulty)
        emb.add_field(name="Description", value=level.desc)
        if(level.noc != 0):
            emb.add_field(name="Number of Coins", value=str(level.noc))
        await ctx.send(embed=emb)

    @commands.command(pass_context=True, aliases=["inv"], description="Get the invite for MewBot!", brief='mb!invite')
    async def invite(self, ctx):
        emb = (discord.Embed(color=0xf7b8cf))
        emb.add_field(name="Invite Link", value="https://bit.ly/2wzmka1")
        emb.set_footer(text="Thanks for inviting MewBot!")
        await ctx.send(embed=emb)

    @commands.command(pass_context=True, aliases=["stats", "about", "info"], description="Get MewBot's info!", brief='mb!botinfo')
    async def botinfo(self, ctx):
        x = 0
        for server in self.bot.guilds:
            for user in server.members:
                if(not user.bot):
                    x += 1
        emb = (discord.Embed(color=0xf7b8cf))
        emb.set_author(name="Bot Info")
        emb.add_field(name="Bot Name", value=self.bot.user.name)
        emb.add_field(name="Server Count", value=str(len(self.bot.guilds)))
        emb.add_field(name="Users", value=str(x))
        emb.add_field(name="Developer", value="Venom#8068")
        emb.add_field(name="Library", value="discord.py")
        await ctx.send(embed=emb)

    @commands.command(pass_context=True, description="Get the information on a Geometry Dash player!", brief='mb!gdprof RobTop')
    async def gdprof(self, ctx, *args):
        user = await GDLib.User.create(' '.join(args))
        emb = (discord.Embed(color=0xf7b8cf))
        emb.set_author(name=user.name)
        emb.add_field(name="Rank", value=user.rank)
        emb.add_field(name="Stars", value=user.stars)
        emb.add_field(name="Diamonds", value=user.diamonds)
        emb.add_field(name="Coins", value=user.coins)
        emb.add_field(name="User Coins", value=user.ucoins)
        emb.add_field(name="Demons", value=user.demons)
        emb.add_field(name="Creator Points", value=user.cp)
        if(user.mod != "None"):
            emb.add_field(name="Mod Status", value=user.mod)
        await ctx.send(embed=emb)


    @commands.command(pass_context=True, aliases=["ytsearch", "youtubesearch", "youtube"], description="Search YouTube for a video!", brief='mb!ysearch Despacito')
    async def ysearch(self, ctx, *args):
        async with aiohttp.ClientSession(connector=aiohttp.TCPConnector(verify_ssl=False)) as cs:
            async with cs.get('https://www.youtube.com/results?search_query=' + ' '.join(args)) as r:
                f = await r.read()
            async with cs.get('https://www.youtube.com/watch?v='+ str(f).split('/watch?v=')[1].split('"')[0]) as p:
                page = await p.read()
        page = str(page)
        thumbnail = html.unescape(str(f).split('<span class="yt-thumb-simple">')[1].split('src="')[1].split('"')[0])
        title = html.unescape(page.split('<title>')[1].split(' - YouTube</')[0])
        desc = html.unescape(re.sub(re.compile('<.*?>'), r'\n', page.split('<p id="eow-description" class="" >')[1].split('</p')[0]))
        author = html.unescape(page.split(',"author":"')[1].split('","')[0])
        view = html.unescape(page.split('class="watch-view-count">')[1].split(' views')[0])
        likes = html.unescape(page.split('like this video along with ')[1].split(' other')[0])
        dislikes = html.unescape(page.split('dislike this video along with ')[1].split(' other')[0])
        emb = (discord.Embed(color=0xf7b8cf))
        emb.set_author(name=title, url='https://www.youtube.com/watch?v='+ str(f).split('/watch?v=')[1].split('"')[0])
        emb.add_field(name="Author", value=author)
        emb.add_field(name="Views", value=view)
        emb.add_field(name="Likes", value=likes)
        emb.add_field(name="Dislikes", value=dislikes)
        emb.add_field(name="Description", value=desc[:100].encode().decode('utf-8'))
        emb.set_image(url="https:" + thumbnail if not thumbnail.startswith("https:") else thumbnail)
        await ctx.send(embed=emb)

    @commands.command(pass_context=True, aliases=["user"], description="Get the information on a discord user!", brief='mb!userinfo @Zpicy')
    async def userinfo(self, ctx, *args):
        if(args == ()):
            user = self.bot.get_user(ctx.message.author.id)
        elif (args[0][:2] == "<@" and args[0][-1] == ">"):
            if (args[0][:3] == "<@!"):
                y = args[0].split("<@!")[1].split(">")[0]
            else:
                y = args[0].split("<@")[1].split(">")[0]
            user = await self.bot.get_user_info(y)
        elif(args[0].isdigit()):
            user = await self.bot.get_user_info(args[0])
        emb = (discord.Embed(color=0xf7b8cf))
        av = user.avatar_url
        member = ctx.message.guild.get_member(user_id=user.id)
        username = user.name
        nick = member.nick
        disc = user.discriminator
        stat = str(member.status)
        eyedee = str(user.id)
        cr = (member.created_at + datetime.timedelta(hours=-5)).strftime("%m-%d-%Y %H:%M:%S")
        if(member.activity):
            E = list(str(member.activity.type).split('.')[-1])
            E[0] = E[0].upper()
            E = ''.join(E)
        else:
            E = ""
        emb = (discord.Embed(color=0xf7b8cf))
        emb.set_thumbnail(url=av)
        emb.add_field(name="Username", value=str(username))
        if(nick != username):
            emb.add_field(name="Nickname", value=nick)
        emb.add_field(name="Discriminator (tag)", value=disc)
        emb.add_field(name="Status", value=stat)
        emb.add_field(name="User ID", value=eyedee)
        if(E != ""):
            emb.add_field(name=E, value=member.activity.name)
        emb.set_footer(text="Created on " + cr + " EST")
        await ctx.send(embed=emb)

    @commands.command(pass_context=True, description="Get MewBot's ping!", brief='mb!ping')
    async def ping(self, ctx):
        channel = ctx.message.channel
        t1 = time.perf_counter()
        await channel.trigger_typing()
        t2 = time.perf_counter()
        embed = discord.Embed(color=0xf7b8cf)
        embed.set_author(name="Ping")
        embed.add_field(name="{}".format(round((t2 - t1) * 1000)) + ".0 ms", value="{}".format(round(t2 - t1, 3)) + " sec")
        await ctx.send(embed=embed)

    @commands.command(pass_context=True, description="Get the top 10 GD Players right now!", brief='mb!top10')
    async def top10(self, ctx):
        emb = (discord.Embed(color=0xf7b8cf))
        emb.set_author(name="Top 10")
        p = 1
        for i in await GDLib.get_top10():
            emb.add_field(name="#" + str(p) + ": " + i[0], value=i[1])
            p += 1
        await ctx.send(embed=emb)

    @commands.command(pass_context=True, aliases=["csgoprice", "csprice", "counterstrikeglobaloffensiveprice"], description="Get the price of a CS:GO Skin!", brief='mb!csp')
    async def csp(self, ctx):
        finname = ""
        q1 = await ctx.send("Which Weapon will you choose?")
        low = ["Glock-18", "USP-S", "P2000", "P250", "Desert Eagle", "Dual Berettas", "Tec-9", "Five-SeveN", "CZ75-Auto", "R8 Revolver", "Nova", "XM1014", "Sawed-Off", "MAG-7", "MAC-10", "MP9", "MP7", "MP5-SD", "UMP-45", "PP-Bizon", "P90", "Galil-AR", "FAMAS", "AK-47", "M4A4", "M4A1-S", "SSG 08", "AUG", "SG 553", "AWP", "G3SG1", "SCAR-20"]
        lowe = []
        for i in low:
            emb = (discord.Embed(color=0xf7b8cf))
            emb.set_author(name=i)
            lowe.append(emb)
        x = await Paginator.ReactionPaginator(self.bot, ctx.message, lowe)
        await q1.delete()
        skins = await CSGOLib.get_weapon_skins(x.author.name)
        lose = []
        for i in skins:
            emb = (discord.Embed(color=0xf7b8cf))
            emb.set_author(name=i.replace("\\'", "'").replace("\\xe5\\xbc\\x90", "弐").replace("\\xe5\\xa3\\xb1", "壱").replace('\\xe9\\xbe\\x8d\\xe7\\x8e\\x8b', "龍王"))
            lose.append(emb)
        if(x):
            q2 = await ctx.send('Which Skin will you choose?')
            y = await Paginator.ReactionPaginator(self.bot, ctx.message, lose)
            await q2.delete()
            if(y):
                q3 = await ctx.send('Which Wear will you choose?')
                lof = ["Factory New", "Minimal Wear", "Field-Tested", "Well-Worn", "Battle-Scarred"]
                lofe = []
                for i in lof:
                    emb = (discord.Embed(color=0xf7b8cf))
                    emb.set_author(name=i)
                    lofe.append(emb)
                z = await Paginator.ReactionPaginator(self.bot, ctx.message, lofe)
                await q3.delete()
                if(z):
                    loc = ["StatTrak", "Souvenir", "None"]
                    loce = []
                    for i in loc:
                        emb = (discord.Embed(color=0xf7b8cf))
                        emb.set_author(name=i)
                        loce.append(emb)
                    q4 = await ctx.send("StatTrak, Souvenir, or None?")
                    a = await Paginator.ReactionPaginator(self.bot, ctx.message, loce)
                    await q4.delete()
                    if(a):
                        stattrak = a.author.name == "StatTrak"
                        souvenir = a.author.name == "Souvenir"
                        skin = await CSGOLib.WeaponSkin.create(x.author.name, y.author.name, z.author.name, stattrak=stattrak, souvenir=souvenir)
                        emb = (discord.Embed(color=0xf7b8cf))
                        emb.set_author(name=("StatTrak™ " if stattrak else "") + ("Souvenir " if souvenir else "") + x.author.name + " | " + y.author.name + " (" + z.author.name + ")")
                        emb.add_field(name="Price", value=(("$" + str(skin.price)) if skin.price != 0 else "This skin doesn't exist"))
                        await ctx.send(embed=emb)

    @commands.command(pass_context=True, aliases=["hypixel", "hypixels", "hstats", "hypixelstats"], description="Get the stats of a player on Hypixel!", brief='mb!hs pigpatty')
    async def hs(self, ctx, name):
        player = await HypixelLib.Player.create(name)
        text = player.rank + name + (" [" + player.gtag + "]\nMultiplier: Level " if player.gtag != "" else "\nMultiplier: Level ") + str(player.level) + " (x" + str(player.multiplier) + ")\nLevel: " + format(player.mrank, '.2f') + "\nKarma: " + ','.join(str(player.karma)[::-1][i:i+3] for i in range(0, len(str(player.karma)[::-1]), 3))[::-1] + "\nAchievement Points: " + str(player.apoints) + "\nQuests Completed: " + str(player.qcompleted) + "\nFirstlogin: " + datetime.datetime.strftime(player.firstlogin, "%Y-%m-%d %H:%M") + "\nLastlogin: " + datetime.datetime.strftime(player.lastlogin, "%Y-%m-%d %H:%M") + "\nFriends: " + str(player.friends) if player.name != "" else "This Player does not exist!"
        await ctx.send(text)

def setup(bot):
    bot.add_cog(Info(bot))
