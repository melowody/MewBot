import discord, aiohttp, asyncio, aiosqlite, traceback
from discord.ext.commands import Bot
from discord.ext import commands
from discord import *

bot_prefix = "mb!"
client = commands.Bot(command_prefix=bot_prefix)

client.remove_command('help')

@client.event
async def on_ready():
    print("Bot Online")
    print("Name: {}".format(client.user.name))
    print("ID: {}".format(client.user.id))


@client.event
async def on_message(message):
    async with aiosqlite.connect('./Resources/Interactive/Prefixes.db') as conn:
        c = await conn.execute("SELECT * FROM Prefixes")
        buffer = await c.fetchall()
        await c.close()
        await conn.close()
    user_id = message.author.id
    data = [i[0] for i in buffer]
    if(user_id in data):
        cprefix = buffer[data.index(user_id)][-1]
        if(message.content.startswith(cprefix) and not message.author.bot):
            message.content = "mb!" + message.content[len(cprefix):].split()[0].lower() + ' ' + ' '.join(message.content[len(cprefix):].split()[1:]) if len(message.content[len(cprefix):].split()) != 1 else "mb!" + message.content[len(cprefix):].split()[0].lower()
            game = discord.Game('for mb!help | Currently in ' + str(len(client.guilds)) + ' servers!', type=discord.ActivityType.watching)
            await client.change_presence(activity=game)
            payload = {"server_count": str(len(client.guilds))}
            x = 0
            for server in client.guilds:
                for user in server.members:
                    if(not user.bot):
                        x += 1
            async with aiohttp.ClientSession() as aioclient:
                #await aioclient.post('https://botsfordiscord.com/api/bot/' + str(client.user.id), data=payload, headers={"Authorization": open('C:/TOKENS/BFD.txt').read()})
                await aioclient.post("https://discordbots.org/api/bots/" + str(client.user.id) + "/stats", data=payload, headers={"Authorization": open("C:/TOKENS/DBL.txt").read()})
                await aioclient.post("https://discordbotlist.com/api/bots/" + str(client.user.id) + "/stats", data={"guilds": len(client.guilds), "users": x}, headers={"Authorization": open("C:/TOKENS/DBL2.txt").read()})
            if(message.content.split()[0] != "mb!ping"):
                await message.channel.trigger_typing()
            await client.process_commands(message)
    else:
        if(message.content.startswith("mb!") and not message.author.bot):
            game = discord.Game('for mb!help | Currently in ' + str(len(client.guilds)) + ' servers!', type=discord.ActivityType.watching)
            await client.change_presence(activity=game)
            payload = {"server_count": str(len(client.guilds))}
            x = 0
            for server in client.guilds:
                for user in server.members:
                    if(not user.bot):
                        x += 1
            async with aiohttp.ClientSession() as aioclient:
                #await aioclient.post('https://botsfordiscord.com/api/bot/' + str(client.user.id), data=payload, headers={"Authorization": open('C:/TOKENS/BFD.txt').read()})
                await aioclient.post("https://discordbots.org/api/bots/" + str(client.user.id) + "/stats", data=payload, headers={"Authorization": open("C:/TOKENS/DBL.txt").read()})
                await aioclient.post("https://discordbotlist.com/api/bots/" + str(client.user.id) + "/stats", data={"guilds": len(client.guilds), "users": x}, headers={"Authorization": open("C:/TOKENS/DBL2.txt").read()})
            if(message.content.split()[0] != "mb!ping"):
                await message.channel.trigger_typing()
            await client.process_commands(message)

@client.event
async def on_command_error(ctx, error):
    x = traceback.format_exception_only(type(error), error)[0]
    y = traceback.format_exception(type(error), error, error.__traceback__)
    if(isinstance(error, commands.CommandNotFound)):
        pass
    elif(isinstance(error, discord.ext.commands.errors.MissingRequiredArgument)):
        await ctx.send("It seems that you have not put in all the required arguments!")
    else:
        await ctx.send("It seems an error has occured. Use mb!sugg to tell me about it!")
        venom = client.get_user(190804082032640000)
        emb = (discord.Embed(color=0xff0000))
        emb.set_author(name="ERROR")
        emb.add_field(name="Command", value=ctx.message.content)
        emb.add_field(name="Traceback", value='```' + ''.join(y).split('The above exception was the direct cause')[0][:1000] + '```')
        await venom.send(embed=emb)

extensions = ["Resources.Modules.Fun", "Resources.Modules.Encryption", "Resources.Modules.Money", "Resources.Modules.Info", "Resources.Modules.Mod"]

for i in extensions:
    client.load_extension(i)
client.run(open("C:/TOKENS/TOKEN.txt").read())
