import asyncio, aiohttp, datetime, math

async def get_player_info(name):
    try:
        async with aiohttp.ClientSession(connector=aiohttp.TCPConnector(verify_ssl=False)) as cs:
            async with cs.get('https://api.hypixel.net/player?key=' + open("C:/TOKENS/HYPIXEL.txt").read() + '&name=' + name) as r:
                z = await r.json()
            async with cs.get('https://api.mojang.com/users/profiles/minecraft/' + name) as p:
                qp = await p.json()
        player = Player()
        out = z['player']
        player.name = out['displayname']
        rank = None
        if("prefix" in out.keys()):
            rank = out["prefix"].split('[')[1].split(']')[0]
        elif("rank" in out.keys()):
            rank = out["rank"]
        elif("packageRank" in out.keys() and "monthlyPackageRank" in out.keys() and (out["packageRank"] == "MVP_PLUS" or out['newPackageRank'] == 'MVP_PLUS') and out["monthlyPackageRank"] == "SUPERSTAR"):
            rank = "MVP_PLUS_PLUS"
        elif("newPackageRank" in out.keys()):
            rank = out["newPackageRank"]
        else:
            rank = ""
        if(rank != ""):
            rank = "[" + rank.replace('_PLUS', '+').replace('MODERATOR', 'MOD').replace('YOUTUBER', 'YOUTUBE') + "] "
        player.rank = rank
        player.xp = int(out['networkExp'])
        player.mrank = 1 + (-(10000 - 0.5 * 2500) / 2500) + math.sqrt((-(10000 - 0.5 * 2500) / 2500)**2 + 2 / 2500 * player.xp)
        player.level = math.floor(player.mrank)
        mult = 1
        if(player.level >= 5 and player.level <= 9):
            mult = 1.5
        elif(player.level >= 10 and player.level <= 14):
            mult = 2
        elif(player.level >= 15 and player.level <= 19):
            mult = 2.5
        elif(player.level >= 20 and player.level <= 24):
            mult = 3
        elif(player.level >= 25 and player.level <= 29):
            mult = 3.5
        elif(player.level >= 30 and player.level <= 39):
            mult = 4
        elif(player.level >= 40 and player.level <= 49):
            mult = 4.5
        elif(player.level >= 50 and player.level <= 99):
            mult = 5
        elif(player.level >= 100 and player.level <= 124):
            mult = 5.5
        elif(player.level >= 125 and player.level <= 149):
            mult = 6
        elif(player.level >= 150 and player.level <= 199):
            mult = 6.5
        elif(player.level >= 200 and player.level <= 249):
            mult = 7
        elif(player.level >= 250):
            mult = 8
        player.multiplier = mult
        player.karma = 0 if 'karma' not in out.keys() else int(out['karma'])
        player.apoints = 0 if 'achievementPoints' not in out.keys() else int(out['achievementPoints'])
        qc = 0
        if('quests' in out.keys()):
            for i in out['quests']:
                if "completions" in out['quests'][i].keys():
                    qc += len(out['quests'][i]["completions"])
        player.qcompleted = qc
        player.firstlogin = datetime.datetime.fromtimestamp(int(str(out['firstLogin'])[:10]))
        player.lastlogin = datetime.datetime.fromtimestamp(int(str(out['lastLogin'])[:10]))
        uuid = qp['id']
        async with aiohttp.ClientSession(connector=aiohttp.TCPConnector(verify_ssl=False)) as cs:
            async with cs.get("https://api.hypixel.net/friends?key=" + open("C:/TOKENS/HYPIXEL.txt").read() + "&uuid=" + uuid) as r:
                x = await r.json()
            async with cs.get('https://api.hypixel.net/findGuild?key=' + open("C:/TOKENS/HYPIXEL.txt").read() + '&byUuid=' + uuid) as f:
                p = await f.json()
                gid = p['guild']
            if(gid):
                async with cs.get('https://api.hypixel.net/guild?key=' + open("C:/TOKENS/HYPIXEL.txt").read() + '&id=' + gid) as l:
                    t = await l.json()
                    if('tag' in t['guild'].keys()):
                        tag = t['guild']['tag']
                        player.gtag = tag
                    else:
                        player.gtag = ""
            else:
                player.gtag = ""
        player.friends = len(x["records"])
    except:
        player = None
    return player

class Player:

    def __init__(self):
        self.name = ""
        self.rank = ""
        self.level = 0
        self.xp = 0
        self.multiplier = 0
        self.mrank = 0
        self.karma = 0
        self.apoints = 0
        self.qcompleted = 0
        self.firstlogin = None
        self.lastlogin = None
        self.friends = 0
        self.gtag = ""

    @classmethod
    async def create(self, name):
        player = await get_player_info(name)
        if(player):
            self.name = player.name
            self.rank = player.rank
            self.level = player.level
            self.xp = player.xp
            self.multiplier = player.multiplier
            self.mrank = player.mrank
            self.karma = player.karma
            self.apoints = player.apoints
            self.qcompleted = player.qcompleted
            self.firstlogin = player.firstlogin
            self.lastlogin = player.lastlogin
            self.friends = player.friends
            self.gtag = player.gtag
        else:
            self.name = ""
            self.rank = ""
            self.level = 0
            self.xp = 0
            self.multiplier = 0
            self.mrank = 0
            self.karma = 0
            self.apoints = 0
            self.qcompleted = 0
            self.firstlogin = None
            self.lastlogin = None
            self.friends = 0
            self.gtag = ""
        return self
