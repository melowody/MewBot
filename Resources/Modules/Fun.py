import discord, aiohttp, asyncio, codecs, datetime, pytz, random, time, sys, io, Resources.Lib.ImgLib as ImgLib, Resources.Lib.GDLib as GDLib, Resources.Lib.NewgroundsLib as NewgroundsLib, Resources.Lib.MusicLib as MusicLib, Resources.Lib.PokeAPI as PokeAPI, Resources.Lib.GoogleLib as GoogleLib, Resources.Interactive.Paginator as Paginator, os, aiosqlite, PIL.ImageOps
from googletrans import Translator
from PIL import Image
from difflib import SequenceMatcher
from discord.ext import commands

class Fun:
    def __init__(self, bot):
        self.bot = bot

    @commands.command(pass_context=True, description="Google search for an image!", brief="mb!imagesearch Mew", aliases=["image", "gimage", "googleimage", "gimagesearch", "googleimagesearch"])
    async def imagesearch(self, ctx, *args):
        imgs = await GoogleLib.get_google_images(' '.join(args))
        await Paginator.PaginatorNoSkip(self.bot, ctx.message, imgs)

    @commands.command(pass_context=True, description="Convert to small letters!", brief="mb!smallletter Hello, world!")
    async def smallletter(self, ctx, *args):
        if(args != ()):
            sl = {'q': 'ᵠ', 'w': 'ʷ', 'e': 'ᵉ', 'r': 'ʳ', 't': 'ᵗ', 'y': 'ʸ', 'u': 'ᵘ', 'i': 'ᶦ', 'o': 'ᵒ', 'p': 'ᵖ', 'a': 'ᵃ', 's': 'ˢ', 'd': 'ᵈ', 'f': 'ᶠ', 'g': 'ᵍ', 'h': 'ʰ', 'j': 'ʲ', 'k': 'ᵏ', 'l': 'ˡ', 'z': 'ᶻ', 'x': 'ˣ', 'c': 'ᶜ', 'v': 'ᵛ', 'b': 'ᵇ', 'n': 'ⁿ', 'm': 'ᵐ', '1': '¹', '2': '²', '3': '³', '4': '⁴', '5': '⁵', '6': '⁶', '7': '⁷', '8': '⁸', '9': '⁹', '0': '⁰'}
            for i in range(len(args)):
                j = args[i]
                fin = ""
                for l in j:
                  if(l.isalpha() or l.isdigit()):
                    fin = fin + sl[l.lower()]
                  else:
                    fin = fin + "\\" + l
                args[i] = fin
            emb = (discord.Embed(color=0xf7b8cf))
            emb.add_field(name="Small Letter String", value=' '.join(args))
            await ctx.send(embed=emb)
        else:
            await ctx.send("You didn't enter a valid input!")
            

    @commands.command(pass_context=True, description="Invert an image!", brief="mb!invert @hellosarina")
    async def invert(self, ctx, *args):
        try:
            im = await ImgLib.GetImage(self.bot, ctx, args)
            if(im):
                im = im.convert('RGB')
                img = PIL.ImageOps.invert(im)
                output_buffer = io.BytesIO()
                img.save(output_buffer, "png")
                output_buffer.seek(0)
                await ctx.send(file=discord.File(output_buffer, filename="invert.png"))
            else:
                raise AttributeError("Not Valid.")
        except (AttributeError, OSError):
            await ctx.send("That is not a valid image or user!")

    @commands.command(pass_context=True, description="Set the prefix that you'll use!", brief='mb!setprefix m!')
    async def setprefix(self, ctx, *args):
        async with aiosqlite.connect('./Resources/Interactive/Prefixes.db') as conn:
            c = await conn.execute("SELECT * FROM Prefixes")
            user_id = ctx.message.author.id
            data = [i[0] for i in await c.fetchall()]
            if(user_id in data):
                await c.execute("UPDATE Prefixes SET Prefix = ? WHERE ClientID = ?", (' '.join(args), user_id))
                await conn.commit()
                await c.close()
                await conn.close()
            else:
                await c.execute("INSERT INTO Prefixes VALUES(?, ?)", (user_id, ' '.join(args)))
                await conn.commit()
                await c.close()
                await conn.close()
        await ctx.send("Prefix set to ***__" + ' '.join(args) + "__***!")

    @commands.command(pass_context=True, aliases=["8ball", "8b"], description="Try your luck with the 8ball!", brief='mb!8ball Is MewBot any good?')
    async def eightball(self, ctx, *args):
        out = ""
        out += ":8ball: " + str(ctx.message.author.mention) + ": " + ' '.join(args) + "\nMy Response: " + random.choice(["It is certain.", "It is decidedly so.", "Without a doubt.", "Yes - definitely.", "You may rely on it.", "As I see it, yes.", "Most likely.", "Outlook good.", "Yes.", "Signs point to yes.", "Reply hazy, try again", "Ask again later.", "Cannot predict now.", "Concentrate and ask again.", "Don't count on it.", "My reply is no.", "My sources say no", "Outlook not so good.", "Very doubtful"])
        await ctx.send(out)

    @commands.command(pass_context=True, aliases=["whosthatpokemon"], description="Play a game of Who's That Pokemon!", brief='mb!wtp')
    async def wtp(self, ctx, *args):
        if(args == ()):
            await ctx.message.channel.trigger_typing()
            async with aiosqlite.connect('./Resources/Interactive/WTP.db') as conn:
                c = await conn.execute("SELECT * FROM WTP")
                data = await c.fetchall()
                iii = False
                for i in data:
                    if(ctx.message.channel.id in i):
                        iii = True
                x = await PokeAPI.savepokemon(self.bot, ctx)
                file = x[0]
                output_buffer = io.BytesIO()
                file.save(output_buffer, "png")
                output_buffer.seek(0)
                await ctx.send(file=discord.File(output_buffer, filename="WTP.png"))
                if(not iii):
                    await c.execute("INSERT INTO WTP VALUES(?, ?)", (ctx.message.channel.id, x[1].replace('_', ' ').replace('-Overcast', '').replace('-Altered', '').replace('-Land', '').replace('-Spring', '').replace('-Baile', '').replace('-Solo', '')))
                else:
                    await c.execute("UPDATE WTP SET Pokemon=? WHERE Channel=?", (x[1].replace('_', ' ').replace('-Overcast', '').replace('-Altered', '').replace('-Land', '').replace('-Spring', '').replace('-Baile', '').replace('-Solo', ''), ctx.message.channel.id))
                await conn.commit()
                await c.close()
                await conn.close()
        else:
            p = ' '.join(args).replace('-Overcast', '').replace('-Altered', '').replace('-Land', '').replace('-Spring', '').replace('-Baile', '').replace('-Solo', '')
            async with aiosqlite.connect('./Resources/Interactive/WTP.db') as conn:
                c = await conn.execute('SELECT * FROM WTP')
                data = await c.fetchall()
                cpok = ""
                for i in data:
                    if(i[0] == ctx.message.channel.id):
                        cpok = i[1]
                if(cpok == ""):
                    await ctx.send("There isn't a game yet! Type mb!wtp to get one started!")
                else:
                    if(cpok.lower() == p.lower()):
                        await ctx.send("You got it!")
                        await c.execute("UPDATE WTP SET Pokemon=? WHERE Channel=?", ("", str(ctx.message.channel.id)))
                        await conn.commit()
                    else:
                        await ctx.send("That's not quite right, try again!")
                await c.close()
                await conn.close()

    @commands.command(pass_context=True, aliases=["shibe", "shiba", "shibainu", "inu"], description="Look at an adorable shibe!", brief='mb!shibe')
    async def shib(self, ctx):
        async with aiohttp.ClientSession(connector=aiohttp.TCPConnector(verify_ssl=False)) as cs:
            async with cs.get('http://shibe.online/api/shibes?count=1&urls=true&httpsUrls=true') as f:
                x = str(await f.read())
        url = x.split('"')[1]
        emb = (discord.Embed(color=0xf7b8cf))
        emb.set_image(url=url)
        emb.set_footer(text="Shibe API: http://shibe.online/")
        await ctx.send(embed=emb)

    @commands.command(pass_context=True, description="Get a random feature from iFunny!", brief='mb!ifunny')
    async def ifunny(self, ctx):
        async with aiohttp.ClientSession(connector=aiohttp.TCPConnector(verify_ssl=False)) as cs:
            async with cs.get('https://ifunny.co/feeds/shuffle') as f:
                page = str(await f.read())
            thumbnail = str(page.split('<img class="media__image" src="')[1].split('"')[0])
            async with cs.get("https://ifunny.co" + str(page.split('<img class="media__image" src="')[0].split('href="')[-1].split('"')[0].split('?galler')[0])) as f:
                x = str(await f.read())
        author = x.split('ontent_meta" href="/user/')[1].split('"')[0]
        tags = [i.split('<')[0] for i in x.split('"metapanel__copyright')[0].split('tag__name">')[1:]]
        likes = x.split('actionlink__text">')[1].split('<')[0]
        comments = x.split('actionlink__text">')[2].split('<')[0]
        emb = (discord.Embed(color=0xf7b8cf))
        emb.set_author(name="Random Feature", url="https://ifunny.co" + str(page.split('<img class="media__image" src="')[0].split('href="')[-1].split('"')[0].split('?galler')[0]))
        emb.add_field(name="Author", value=author)
        emb.add_field(name="Tags", value="`" + ', '.join(tags) + '`')
        emb.add_field(name="Comments", value=comments)
        emb.add_field(name="Likes", value=likes)
        emb.set_image(url=thumbnail)
        await ctx.send(embed=emb)

    @commands.command(pass_context=True, description="Translate a from one language to another!", brief='mb!translate en de Hello, world!')
    async def translate(self, ctx, lf, lt, *args):
        try:
            x = Translator()
            out = x.translate(' '.join(args), src=lf, dest=lt)
            emb = (discord.Embed(color=0xf7b8cf))
            emb.set_author(name="Google Translate")
            emb.add_field(name=lf + " -> " + lt, value=out.text)
            await ctx.send(embed=emb)
        except ValueError:
            await ctx.send("You put an invalid source or destination language!")

    @commands.command(pass_context=True, aliases=["levelpass"], description="Get the password of a Geometry Dash level!", brief='mb!lpass Cataclysm')
    async def lpass(self, ctx, *args):
        level = await GDLib.Level.create(' '.join(args))
        if(level.password != 0):
            emb = (discord.Embed(color=0xf7b8cf))
            emb.set_author(name=level.title)
            emb.add_field(name="Password:", value=level.password)
            await ctx.send(embed=emb)
        else:
            await ctx.send("There is no pass for the level __**" + level.title + "**__.")

    @commands.command(pass_context=True, aliases=["blurplefy"], description="Blurplefy an image!", brief='mb!blurple https://bit.ly/2RuKIDr')
    async def blurple(self, ctx, *args):
        im = await ImgLib.GetImage(self.bot, ctx, args)
        im = await ImgLib.Blurplefy(im)
        output_buffer = io.BytesIO()
        im.save(output_buffer, "png")
        output_buffer.seek(0)
        await ctx.send(file=discord.File(output_buffer, filename="blurple.png"))

    @commands.command(pass_context=True, aliases=["randomsong"], description="Get a random Newgrounds song!", brief='mb!rsong')
    async def rsong(self, ctx):
        while(True):
            async with aiohttp.ClientSession(connector=aiohttp.TCPConnector(verify_ssl=False)) as cs:
                async with cs.post('https://www.newgrounds.com/audio/browse/sort/date') as r:
                    f = await r.text()
            x = random.randint(0, int(f.split('//www.newgrounds.com/audio/listen/')[1].split('"')[0]))
            url = "https://www.newgrounds.com/audio/listen/" + str(x)
            song = await NewgroundsLib.Song.create(url)
            if(song.title != ""):
                break
        emb = (discord.Embed(color=0xf7b8cf))
        emb.set_author(name="Random Song")
        emb.add_field(name="Title", value=song.title)
        emb.add_field(name="ID", value=str(song.id))
        emb.add_field(name="Description", value=song.desc)
        emb.add_field(name="Genre", value=song.genre)
        await ctx.send(embed=emb)

    @commands.command(pass_context=True, aliases=["randomlevel"], description="Get a random Geometry Dash level!", brief='mb!rlevel')
    async def rlevel(self, ctx):
        while(True):
            payload = {'gameVersion':'21', 'binaryVersion':'35', 'gdw':'0', 'type':'4', 'str': "", 'diff':'-', 'len':'-', 'page':'0', 'total':'0', 'unCompleted':'0', 'onlycCompleted':'0', 'featured':'0', 'original':'0', 'twoPlayer':'0', 'coins':'0', 'epic':'0', 'demonFilter':'1', 'secret':'Wmfd2893gb7'}
            async with aiohttp.ClientSession(connector=aiohttp.TCPConnector(verify_ssl=False)) as cs:
                async with cs.post('http://www.boomlings.com/database/getGJLevels21.php', data=payload) as r:
                    f = await r.text()
            x = random.randint(0, int(f.split(':')[1]))
            level = await GDLib.Level.create(x)
            if(level.title != "N/A"):
                break
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

    @commands.command(pass_context=True, aliases=["saydelete"], description="Have MewBot say something, then delete your message!", brief='mb!sayd Hello, world!')
    async def sayd(self, ctx, *, args):
        try:
            if(args == ""):
                await ctx.send('You need to enter a message for me to say!')
            else:
                await ctx.message.delete()
                await ctx.send(args)
        except discord.errors.Forbidden:
            await ctx.send("I don't have the `Manage Messages` permission!")

    @commands.command(pass_context=True, description="Look at an adorable otter! (Credit to theeo)", brief='mb!otter')
    async def otter(self, ctx):
        o = ["https://goo.gl/q9g11B", "https://goo.gl/GKhkV9", "https://goo.gl/YcWLdH", "https://goo.gl/fxGaKW", "https://goo.gl/rRvqvW", "https://goo.gl/FEFi5P", "https://goo.gl/2EnR7P", "https://goo.gl/ZzF7hf", "https://goo.gl/P152Pw", "https://goo.gl/8A5dd2", "https://goo.gl/c4qTVG", "https://goo.gl/cvdkVx", "https://goo.gl/co1Sqv", "https://goo.gl/5Df5sA", "https://goo.gl/LFcmV4", "https://goo.gl/5j6LkW", "https://goo.gl/786Xme", "https://goo.gl/GLdoVf", "https://goo.gl/Z6PCFS", "https://goo.gl/jFnzZg", "https://goo.gl/ctMSFg", "https://goo.gl/PM7GS6", "https://goo.gl/EiYwHS", "https://goo.gl/MZG9Cf", "https://goo.gl/3dRpV4", "https://goo.gl/tqJXxE", "https://goo.gl/CDbqrS", "https://goo.gl/ZZXVaV", "https://goo.gl/QTsNEk", "https://goo.gl/ka5B6h", "https://goo.gl/sEpfXg", "https://goo.gl/z4dVLZ", "https://goo.gl/6ER4Av", "https://goo.gl/66RwD5", "https://goo.gl/bK5QGZ", "https://goo.gl/rsrsxz", "https://goo.gl/gs8BkV", "https://goo.gl/P6ksoT", "https://goo.gl/DCCR5F"]
        await ctx.message.channel.send(str(ctx.message.author.mention) + ", Here is your otter\n" + random.choice(o))

    @commands.command(pass_context=True, aliases=["deepfry"], description="Deepfry an image!", brief='mb!df https://bit.ly/2RuKIDr')
    async def df(self, ctx, *args):
        im = await ImgLib.GetImage(self.bot, ctx, args)
        if(im):
            factor = (259 * (255 + 255)) / (255 * (259 - 255))
            def contrast(c):
                return 128 + factor * (c-128)
            x = im.point(contrast)
            output_buffer = io.BytesIO()
            x.save(output_buffer, "png")
            output_buffer.seek(0)
            await ctx.send(file=discord.File(output_buffer, filename="df.png"))
        else:
            await ctx.send("Image Not Found!")

    @commands.command(pass_context=True, aliases=["emoji"], description="Turn a message into big letters!", brief='mb!bigletter Hello, world!')
    async def bigletter(self, ctx, *args):
        f = list(args)
        fin = ""
        for i in f:
            i = i.lower()
            if(i in list("abcdefghijklmnopqrstuvwxyz")):
                fin += ":regional_indicator_" + i + ":"
            elif(i in list("1234567890")):
                fin += ":" + i.replace('1', 'one').replace('2', 'two').replace('3', 'three').replace('4', 'four').replace('5', 'five').replace('6', 'six').replace('7', 'seven').replace('8', 'eight').replace('9', 'nine').replace('0', 'zero') + ":"
            else:
                fin += i
        emb = (discord.Embed(color=0xf7b8cf))
        emb.add_field(name="Emoji String", value=fin)
        await ctx.send(embed=emb)

    @commands.command(pass_context=True, description="Have MewBot say something!", brief='mb!say Hello, world!')
    async def say(self, ctx, *, args):
        if(args == ""):
            await ctx.send("You need to enter a message for me to say!")
        else:
            await ctx.send(args)

    @commands.command(pass_context=True, description="Duel someone!", brief='mb!duel @Monstahhh')
    async def duel(self, ctx, user: discord.User=None):
        if(user):
            x = str(ctx.message.author.mention)
            xx = str(user.mention)
            z = await ctx.send("{}".format(x) + " duels " + "{}".format(xx))
            await asyncio.sleep(1.5)
            y = await z.edit(content="⚔ Dueling.")
            await asyncio.sleep(.5)
            y = await z.edit(content="⚔ Dueling..")
            await asyncio.sleep(.5)
            y = await z.edit(content="⚔ Dueling...")
            await asyncio.sleep(.5)
            l = random.randint(1, 2)
            if(l == 1):
                await z.edit(content="{}".format(x) + " has won!")
            else:
                await z.edit(content="{}".format(xx) + " has won!")
        else:
            await ctx.send("You can't duel no one! Tag someone!")

    @commands.command(pass_context=True, description="Jeff someone!", brief='mb!jeff @File_34')
    async def jeff(self, ctx, *args):
        if(args):
            u = args[0]
            user = None
            if((u.startswith('<@') or u.isdigit()) and u.split('<@')[-1].split('>')[0].isdigit()):
                try:
                    user = await self.bot.get_user_info(int(u.split('<@')[-1].split('>')[0]))
                except discord.errors.NotFound:
                    await ctx.send("That is not a valid user, so I can't jeff them!")
                    return
            if(user):
                await ctx.send(file=discord.File(open("./Resources/Sources/jeff.jpg", "rb"), filename="jeff.jpg"))
                await ctx.send(str(user.mention) + ", You just got jeff'd by " + str(ctx.message.author.mention))
            else:
                await ctx.send("You have to mention someone to jeff them!")
        else:
            await ctx.send("You can't jeff yourself! Tag someone!")

    @commands.command(pass_context=True, aliases=["coin"], description="Flip a coin!", brief='mb!coinflip')
    async def coinflip(self, ctx):
        p = [1, 2]
        choic = random.choice(p)
        if(choic == 1):
            emb = (discord.Embed(color=0xf7b8cf))
            emb.add_field(name="Coinflip", value='You Got Tails!')
        else:
            emb = (discord.Embed(color=0xf7b8cf))
            emb.add_field(name="Coinflip", value='You Got Heads!')
        await ctx.send(embed=emb)

    @commands.command(pass_context=True, aliases=["suggest", "sg"], description="Suggest something for me to add to MewBot!", brief='mb!sugg There should be ____')
    async def sugg(self, ctx, *args):
        if(args != "SUGGESTION"):
            swears = ['anal', 'anus', 'arse', 'ass', 'ballsack', 'balls', 'bastard', 'bitch', 'biatch', 'bloody', 'blowjob', 'blow', 'bollock', 'bollok', 'boner', 'boob', 'bugger', 'bum', 'butt', 'buttplug', 'clitoris', 'cock', 'coon', 'crap', 'cunt', 'damn', 'dick', 'dildo', 'dyke', 'fag', 'feck', 'fellate', 'fellatio', 'felching', 'fuck', 'fudgepacker', 'packer', 'flange', 'goddamn', 'damn', 'hell', 'homo', 'jerk', 'jizz', 'knobend', 'knob', 'end', 'labia', 'lmao', 'lmfao', 'muff', 'nigger', 'nigga', 'omg', 'penis', 'piss', 'poop', 'porn', 'prick', 'pube', 'pussy', 'queer', 'scrotum', 'sex', 'shit', 'sh1t', 'slut', 'smegma', 'spunk', 'tit', 'tosser', 'turd', 'twat', 'vagina', 'wank', 'whore', 'wtf', 'negro', 'succ', 'retard', 'shiet', 'gay', 'dong', 'killyourself']
            x = ' '.join(args)
            count = 0
            for i in range(len(swears)):
                if(swears[i] in ''.join(args)):
                    count += 1
            with codecs.open("./Resources/Interactive/sugg.txt", "r", encoding="utf8") as f:
                a = "" if f.read() == "" else f.read().split(" - ")[0].replace('\n', '')
                if(SequenceMatcher(None, a, args).ratio() >= 0.8):
                    count += 1
            if(count > 0):
                await ctx.message.channel.send("Your suggestion looked like spam, so it wasn't sent!")
            else:
                f = codecs.open("./Resources/Interactive/sugg.txt", "a", encoding="utf-8")
                f.write(x + " - Suggested by " + str(ctx.message.author) + "\n")
                f.close()
                me = await self.bot.get_user_info(190804082032640000)
                emb = (discord.Embed(color=0xf7b8cf))
                emb.add_field(name=str(ctx.message.author), value=x)
                emb.timestamp = datetime.datetime.now(pytz.timezone('US/Eastern'))
                await me.send(embed=emb)
                await ctx.message.channel.send("Suggestion sent!")
        else:
            await ctx.send("No! You have to actually give a suggestion! For example, \"mb!sugg A better help command!\"")

def setup(bot):
    bot.add_cog(Fun(bot))
