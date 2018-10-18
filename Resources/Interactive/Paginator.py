import discord, asyncio, Resources.Lib.CSGOLib as CSGOLib, Resources.Lib.GDLib as GDLib, concurrent.futures as futures

async def DemonlistPaginator(client, message):
    current = 1
    botmsg = await message.channel.send(embed=await GDLib.getdemoninfo(current))
    await botmsg.add_reaction("⏪")
    await botmsg.add_reaction("◀")
    await botmsg.add_reaction("▶")
    await botmsg.add_reaction("⏩")
    await botmsg.add_reaction("⏹")
    await botmsg.add_reaction("\U0001F522")

    def isNum(x):
        try:
            l = int(x)
            return True
        except ValueError:
            return False

    def check(m):
        return isNum(m.content) and m.author == message.author and m.channel == message.channel

    while(True):
        def change(reaction, user):
            return user == message.author
        try:
            reaction, user = await client.wait_for('reaction_add', timeout=60.0, check=change)
        except futures.TimeoutError:
            await botmsg.delete()
            break
        else:
            if(str(reaction.emoji) == "▶"):
                if(current < 100):
                    current += 1
                    await botmsg.edit(embed=await GDLib.getdemoninfo(current))
                    await botmsg.remove_reaction(reaction, message.guild.get_member(user.id))
                else:
                    current -= 1
                    await botmsg.remove_reaction(reaction, message.guild.get_member(user.id))
            elif(str(reaction.emoji) == "◀"):
                if(current > 0):
                    current -= 1
                    await botmsg.edit(embed=await GDLib.getdemoninfo(current))
                    await botmsg.remove_reaction(reaction, message.guild.get_member(user.id))
                else:
                    current += 1
                    await botmsg.remove_reaction(reaction, message.guild.get_member(user.id))
            elif(str(reaction.emoji) == "⏪"):
                current = 1
                await botmsg.edit(embed=await GDLib.getdemoninfo(current))
                await botmsg.remove_reaction(reaction, message.guild.get_member(user.id))
            elif(str(reaction.emoji) == "⏩"):
                current = 100
                await botmsg.edit(embed=await GDLib.getdemoninfo(current))
                await botmsg.remove_reaction(reaction, message.guild.get_member(user.id))
            elif(str(reaction.emoji) == "⏹"):
                await botmsg.delete()
                break
            elif(str(reaction.emoji) == "\U0001F522"):
                msg = await client.wait_for('message', check=check)
                current = int(msg.content)
                if(current > 100):
                    current = 100
                elif(current < 1):
                    current = 1
                await botmsg.edit(embed=await GDLib.getdemoninfo(current))
                await botmsg.remove_reaction(reaction, message.guild.get_member(user.id))
                await msg.delete()

async def ReactionPaginator(client, message, x):
    current = 0
    botmsg = await message.channel.send(embed=x[current])
    await botmsg.add_reaction("⏪")
    await botmsg.add_reaction("◀")
    await botmsg.add_reaction("▶")
    await botmsg.add_reaction("⏩")
    await botmsg.add_reaction("\U00002705")
    while(True):
        def change(reaction, user):
            return user == message.author

        try:
            reaction, user = await client.wait_for('reaction_add', timeout=60.0, check=change)
        except futures.TimeoutError:
            await botmsg.delete()
            break
        else:
            if(str(reaction.emoji) == "▶"):
                try:
                    current += 1
                    await botmsg.edit(embed=x[current])
                    await botmsg.remove_reaction(reaction, message.guild.get_member(user.id))
                except IndexError:
                    current -= 1
                    await botmsg.remove_reaction(reaction, message.guild.get_member(user.id))
            elif(str(reaction.emoji) == "◀"):
                if(current > 0):
                    current -= 1
                    await botmsg.edit(embed=x[current])
                    await botmsg.remove_reaction(reaction, message.guild.get_member(user.id))
                else:
                    current += 1
                    await botmsg.remove_reaction(reaction, message.guild.get_member(user.id))
            elif(str(reaction.emoji) == "⏪"):
                current = 0
                await botmsg.edit(embed=x[current])
                await botmsg.remove_reaction(reaction, message.guild.get_member(user.id))
            elif(str(reaction.emoji) == "⏩"):
                current = len(x) - 1
                await botmsg.edit(embed=x[current])
                await botmsg.remove_reaction(reaction, message.guild.get_member(user.id))
            elif(str(reaction.emoji) == "\U00002705"):
                await botmsg.delete()
                return x[current]

async def PaginatorNoSkip(client, message, x):
    current = 0
    botmsg = await message.channel.send(embed=x[current])
    await botmsg.add_reaction("⏪")
    await botmsg.add_reaction("◀")
    await botmsg.add_reaction("▶")
    await botmsg.add_reaction("⏩")
    await botmsg.add_reaction("⏹")
    while(True):
        def change(reaction, user):
            return user == message.author

        try:
            reaction, user = await client.wait_for('reaction_add', timeout=60.0, check=change)
        except futures.TimeoutError:
            await botmsg.delete()
            break
        else:
            if(str(reaction.emoji) == "▶"):
                try:
                    current += 1
                    await botmsg.edit(embed=x[current])
                    await botmsg.remove_reaction(reaction, message.guild.get_member(user.id))
                except IndexError:
                    current -= 1
                    await botmsg.remove_reaction(reaction, message.guild.get_member(user.id))
            elif(str(reaction.emoji) == "◀"):
                if(current > 0):
                    current -= 1
                    await botmsg.edit(embed=x[current])
                    await botmsg.remove_reaction(reaction, message.guild.get_member(user.id))
                else:
                    current += 1
                    await botmsg.remove_reaction(reaction, message.guild.get_member(user.id))
            elif(str(reaction.emoji) == "⏪"):
                current = 0
                await botmsg.edit(embed=x[current])
                await botmsg.remove_reaction(reaction, message.guild.get_member(user.id))
            elif(str(reaction.emoji) == "⏩"):
                current = len(x) - 1
                await botmsg.edit(embed=x[current])
                await botmsg.remove_reaction(reaction, message.guild.get_member(user.id))
            elif(str(reaction.emoji) == "⏹"):
                await botmsg.delete()
                break
            continue

async def Paginator(client, message, x):
    current = 0
    botmsg = await message.channel.send(embed=x[current])
    await botmsg.add_reaction("⏪")
    await botmsg.add_reaction("◀")
    await botmsg.add_reaction("▶")
    await botmsg.add_reaction("⏩")
    await botmsg.add_reaction("⏹")
    await botmsg.add_reaction("\U0001F522")
    while(True):
        def change(reaction, user):
            return user == message.author

        try:
            reaction, user = await client.wait_for('reaction_add', timeout=60.0, check=change)
        except futures.TimeoutError:
            await botmsg.delete()
            break
        else:
            if(str(reaction.emoji) == "▶"):
                try:
                    current += 1
                    await botmsg.edit(embed=x[current])
                    await botmsg.remove_reaction(reaction, message.guild.get_member(user.id))
                except IndexError:
                    current -= 1
                    await botmsg.remove_reaction(reaction, message.guild.get_member(user.id))
            elif(str(reaction.emoji) == "◀"):
                if(current > 0):
                    current -= 1
                    await botmsg.edit(embed=x[current])
                    await botmsg.remove_reaction(reaction, message.guild.get_member(user.id))
                else:
                    current += 1
                    await botmsg.remove_reaction(reaction, message.guild.get_member(user.id))
            elif(str(reaction.emoji) == "⏪"):
                current = 0
                await botmsg.edit(embed=x[current])
                await botmsg.remove_reaction(reaction, message.guild.get_member(user.id))
            elif(str(reaction.emoji) == "⏩"):
                current = len(x) - 1
                await botmsg.edit(embed=x[current])
                await botmsg.remove_reaction(reaction, message.guild.get_member(user.id))
            elif(str(reaction.emoji) == "⏹"):
                await botmsg.delete()
                break
            elif(str(reaction.emoji) == "\U0001F522"):
                msg = await client.wait_for('message', check=check)
                current = int(msg.content)
                if(current > 100):
                    current = 100
                elif(current < 1):
                    current = 1
                await botmsg.edit(embed=x[current])
                await botmsg.remove_reaction(reaction, message.guild.get_member(user.id))
                await msg.delete()
            continue
