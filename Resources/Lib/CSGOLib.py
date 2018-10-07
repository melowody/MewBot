import asyncio, aiohttp

async def get_weapon_skins(name):
    async with aiohttp.ClientSession() as cs:
        async with cs.get('https://csgostash.com/weapon/' + name) as f:
            r = await f.read()
    r = str(r)
    return [ i.split('</a')[0].split('>')[1] for i in r.split('.com/family/') ][1:]

async def get_skin_info(weapon, name, wear, stattrak=False, souvenir=False):
    fin = ("StatTrak™ " if stattrak else "") + ("Souvenir " if souvenir else "") + weapon + " | " + name + " (" + wear + ")"
    ws = WeaponSkin(weapon, name, wear, stattrak=stattrak, souvenir=souvenir)
    async with aiohttp.ClientSession() as cs:
        async with cs.get('https://steamcommunity.com/market/priceoverview/?appid=730&currency=1&market_hash_name=' + fin) as sapi:
            p = await sapi.json()
            if(p['success']):
                ws.price = float(p['lowest_price'][1:])
            else:
                ws.price = 0
    return ws

class Weapon:

    def __init__(self, name):
        self.name = name
        self.skins = []

    @classmethod
    async def create(self, name):
        self.name = name
        try:
            self.skins = await get_weapon_skins(name)
        except:
            self.skins = []
        return self

class WeaponSkin:

    def __init__(self, weapon, name, wear, stattrak=False, souvenir=False):
        self.name = ""
        self.weapon = ""
        self.price = 0
        self.wear = ""
        self.stattrak = False
        self.souvenir = False

    @classmethod
    async def create(self, weapon, name, wear, stattrak=False, souvenir=False):
        ws = await get_skin_info(weapon, name, wear, stattrak=stattrak, souvenir=souvenir)
        self.name = ws.name
        self.weapon = ws.weapon
        self.price = ws.price
        self.wear = ws.wear
        self.stattrak = stattrak
        self.souvenir = souvenir
        return self
