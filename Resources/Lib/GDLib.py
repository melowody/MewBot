import asyncio, aiohttp, base64, html, discord

def rted(s):
    s = base64.b64decode(s.encode('utf-8')).decode()
    s2 = ""
    if (len(s) < 5):
        for i in range(len(s)):
            s2 = s2 + "26364"[i]
    elif (len(s) > 5):
        while (len(s2) < len(s)):
            s2 = s2 + "26364"
        while (len(s2) != len(s)):
            s2 = list(s2)
            s2.pop(-1)
            s2 = ''.join(s2)
    out = ''.join(chr(ord(a) ^ ord(b)) for a, b in zip(s, s2))
    return out

def rtee(s):
    s2 = ""
    if(len(s) >= 6):
        if(len(s) < 5):
            for i in range(len(s)):
                s2 = s2 + "26364"[i]
        elif(len(s) > 5):
            while(len(s2) < len(s)):
                s2 = s2 + "26364"
            while(len(s2) != len(s)):
                s2 = list(s2)
                s2.pop(-1)
                s2 = ''.join(s2)
        out = ''.join(chr(ord(a) ^ ord(b)) for a,b in zip(s,s2))
        out = base64.b64encode(out.encode('utf-8'))
        return out
    else:
        return 0

def gjpe(s):
    if(len(s) > 5):
        s2 = ""
        if(len(s) < 5):
            for i in range(len(s)):
                s2 = s2 + "37526"[i]
        elif(len(s) > 5):
            while(len(s2) < len(s)):
                s2 = s2 + "37526"
            while(len(s2) != len(s)):
                s2 = list(s2)
                s2.pop(-1)
                s2 = ''.join(s2)
        out = ''.join(chr(ord(a) ^ ord(b)) for a,b in zip(s,s2))
        out = base64.b64encode(out.encode('utf-8'))
        return out
    else:
        return 0

def gjpd(s):
    s = base64.b64decode(s.encode('utf-8')).decode()
    s2 = ""
    if (len(s) < 5):
        for i in range(len(s)):
            s2 = s2 + "37526"[i]
    elif (len(s) > 5):
        while (len(s2) < len(s)):
            s2 = s2 + "37526"
        while (len(s2) != len(s)):
            s2 = list(s2)
            s2.pop(-1)
            s2 = ''.join(s2)
    out = ''.join(chr(ord(a) ^ ord(b)) for a, b in zip(s, s2))
    return out

async def getdemoninfo(i):
    fin = []
    async with aiohttp.ClientSession(connector=aiohttp.TCPConnector(verify_ssl=False)) as cs:
        async with cs.get('https://pointercrate.com/api/v1/demons/' + str(i)) as f:
            r = await f.json()
    x = r['data']
    creators = [i['name'] for i in x['creators']]
    verifier = x['verifier']['name']
    video = x['video']
    name = x['name']
    async with aiohttp.ClientSession(connector=aiohttp.TCPConnector(verify_ssl=False)) as cs:
        async with cs.get('https://pointercrate.com/demonlist/' + str(i)) as f:
            r = str(await f.read())
    desc = html.unescape(r.split('<q>')[1].split('</q>')[0]) if '<q>' in r else '-'
    finalemb = discord.Embed(colour=0xf7b8cf)
    if(video == None):
        finalemb.set_author(name=name + " - #" + str(i))
    else:
        finalemb.set_author(name=name + " - #" + str(i), url=video)
    finalemb.add_field(name="Description", value=desc)
    finalemb.add_field(name="Creators", value='`' + ', '.join(creators) + '`')
    finalemb.add_field(name="Verifier", value=verifier)
    return finalemb

async def get_level_pass(lid):
    async with aiohttp.ClientSession(connector=aiohttp.TCPConnector(verify_ssl=False)) as cs:
        payload = {'gameVersion':'21', 'binaryVersion':'35', 'gdw':'0', 'levelID': lid, 'inc': '1', 'extras': '0', 'secret':'Wmfd2893gb7'}
        async with cs.post('http://www.boomlings.com/database/downloadGJLevel22.php', data=payload) as r:
            f = await r.text()
    return rted(f.split(':')[-1].split('#')[0])[1:] if f.split(':')[-1].split('#')[0] != "0" and f.split(':')[-1].split('#')[0] != "10" and f.split(':')[-1].split('#')[0] != "1" and f.split(':')[-1].split('#')[0] != "" and rted(f.split(':')[-1].split('#')[0])[1:] != "" else 0

async def get_level_info(inp):
    async with aiohttp.ClientSession(connector=aiohttp.TCPConnector(verify_ssl=False)) as cs:
        payload = {'gameVersion':'21', 'binaryVersion':'35', 'gdw':'0', 'type':'0', 'str': inp, 'diff':'-', 'len':'-', 'page':'0', 'total':'0', 'unCompleted':'0', 'onlycCompleted':'0', 'featured':'0', 'original':'0', 'twoPlayer':'0', 'coins':'0', 'epic':'0', 'demonFilter':'1', 'secret':'Wmfd2893gb7'}
        async with cs.post('http://www.boomlings.com/database/getGJLevels21.php', data=payload) as r:
            f = await r.text()
    if(f == "-1"):
        return None
    lid = f.split(':')[1]
    async with aiohttp.ClientSession(connector=aiohttp.TCPConnector(verify_ssl=False)) as cs:
        payload = {'gameVersion':'21', 'binaryVersion':'35', 'gdw':'0', 'type':'0', 'str': lid, 'diff':'-', 'len':'-', 'page':'0', 'total':'0', 'unCompleted':'0', 'onlycCompleted':'0', 'featured':'0', 'original':'0', 'twoPlayer':'0', 'coins':'0', 'epic':'0', 'demonFilter':'1', 'secret':'Wmfd2893gb7'}
        async with cs.post('http://www.boomlings.com/database/getGJLevels21.php', data=payload) as r:
            f = await r.text()
    return f

async def get_top10():
    data={"gameVersion": "21", "binaryVersion": "35", "gdw": "0", "type": "top", "count": "10", "secret": "Wmfd2893gb7"}
    async with aiohttp.ClientSession(connector=aiohttp.TCPConnector(verify_ssl=False)) as cs:
        async with cs.post('http://www.boomlings.com/database/getGJScores20.php', data=data) as f:
            r = await f.read()
    r = str(r)
    fin = []
    players = r.split('|')[:-1]
    for i in players:
        fin.append([i.split(':')[1], i.split(':')[23]])
    return fin

def get_difficulty(f):
    f = f.split(':')
    if(f[11] == "50"):
        if(f[21] == "1"):
            return "Extreme Demon"
        elif(f[25] == "1"):
            return "Auto"
        else:
            return "Insane"
    elif(f[11] == "40"):
        if(f[27] == "10"):
            return "Insane Demon"
        else:
            return "Harder"
    elif(f[11] == "30"):
        if(f[27] == "10"):
            return "Hard Demon"
        else:
            return "Hard"
    elif(f[11] == "20"):
        if(f[27] == "10"):
            return "Medium Demon"
        else:
            return "Normal"
    elif(f[11] == "10"):
        if(f[27] == "10"):
            return "Easy Demon"
        else:
            return "Easy"
    else:
        return "N/A"

async def get_user_info(x):
    async with aiohttp.ClientSession(connector=aiohttp.TCPConnector(verify_ssl=False)) as cs:
        async with cs.post('http://www.boomlings.com/database/getGJUsers20.php', data={"gameVersion": "21", "binaryVersion": "35", "gdw": "0", "str": x, "secret": "Wmfd2893gb7"}) as f:
            r = await f.read()
        async with cs.post('http://www.boomlings.com/database/getGJUserInfo20.php', data={"gameVersion": "21", "binaryVersion": "35", "gdw": "0", "targetAccountID": str(r).split(':')[21], "secret": "Wmfd2893gb7"}) as f:
            r = await f.text()
    r = str(r)
    user = User()
    user.name = r.split(':')[1]
    user.rank = int(r.split(':')[47])
    user.stars = int(r.split(':')[13])
    user.diamonds = int(r.split(':')[15])
    user.coins = int(r.split(':')[5])
    user.ucoins = int(r.split(':')[7])
    user.demons = int(r.split(':')[17])
    user.cp = int(r.split(':')[19])
    if(r.split(':')[-3] == "0"):
        user.mod = "None"
    elif(r.split(':')[-3] == "1"):
        user.mod = "Mod"
    else:
        user.mod = "Elder Mod"
    return user

class User:
    def __init__(self):
        self.name = ""
        self.rank = 0
        self.stars = 0
        self.diamonds = 0
        self.coins = 0
        self.ucoins = 0
        self.demons = 0
        self.cp = 0
        self.mod = ""

    @classmethod
    async def create(self, name):
        k = await get_user_info(name)
        self.name = k.name
        self.rank = k.rank
        self.stars = k.stars
        self.diamonds = k.diamonds
        self.coins = k.coins
        self.ucoins = k.ucoins
        self.demons = k.demons
        self.cp = k.cp
        self.mod = k.mod
        return self

class Level:
    def __init__(self):
        self.title = "N/A"
        self.id = ""
        self.desc = ""
        self.author = ""
        self.downloads = 0
        self.likes = 0
        self.epic = False
        self.featured = False
        self.difficulty = "N/A"
        self.stars = 0
        self.noc = 0
        self.password = 0

    @classmethod
    async def create(self, inp):
        self.info = await get_level_info(inp)
        if(self.info):
            self.title = self.info.split(':')[3]
            self.id = self.info.split(':')[1]
            self.desc = base64.b64decode(self.info.split(':')[35]).decode() if self.info.split(':')[35] != "" else "No Description Provided"
            self.author = (self.info.split('#')[1] if self.info.split('#')[1] != "" else ":-").split(':')[1]
            self.downloads = int(self.info.split(':')[13])
            self.likes = int(self.info.split(':')[19])
            self.epic = False if self.info.split(':')[31] == "0" else True
            self.featured = False if self.info.split(':')[29] == "0" else True
            self.difficulty = get_difficulty(self.info)
            self.stars = int(self.info.split(':')[27])
            self.noc = int(self.info.split(':')[43])
            self.password = int(await get_level_pass(self.id))
        else:
            self.title = "N/A"
            self.id = ""
            self.desc = ""
            self.author = ""
            self.downloads = 0
            self.likes = 0
            self.epic = False
            self.featured = False
            self.difficulty = "N/A"
            self.stars = 0
            self.noc = 0
            self.password = 0
        return self
