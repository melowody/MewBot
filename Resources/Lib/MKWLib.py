import codecs, discord, asyncio, aiohttp, json, Resources.Interactive.Paginator as Paginator, datetime, pytz

async def get_top(client, message, track):
    track = track.lower()
    async with aiohttp.ClientSession() as cs:
        async with cs.get('http://tt.chadsoft.co.uk/original-track-leaderboards.json') as l:
            r = json.loads(str(await l.text())[1:])
        async with cs.get('http://tt.chadsoft.co.uk/ctgp-leaderboards.json') as l:
            ct = json.loads(str(await l.text())[1:])
    regs = ['luigi circuit', 'moo moo meadows', 'mushroom gorge', "toad's factory", 'mario circuit', 'coconut mall', 'dk summit', "wario's gold mine", 'daisy circuit', 'koopa cape', 'maple treeway', 'grumble volcano', 'dry dry ruins', 'moonview highway', "bowser's castle", 'rainbow road', 'gcn peach beach', 'ds yoshi falls', 'snes ghost valley 2', 'n64 mario raceway', 'n64 sherbet land', 'gba shy guy beach', 'ds delfino square', 'gcn waluigi stadium', 'ds desert hills', 'gba bowser castle 3', "n64 dk's jungle parkway", 'gcn mario circuit', 'snes mario circuit 3', 'ds peach gardens', 'gcn dk mountain', "n64 bowser's castle"]
    cts = [i['name'].lower() for i in ct['leaderboards']]
    controllerCodes = {"0": "Wii Wheel", "1": "Nunchuck", "2": "Classic Controller", "3": "GameCube"}
    if(track in regs):
        t = 1
    elif(track in cts):
        t = 2
    else:
        return 0
    if(t == 1):
        mto = True if len([i['name'].lower() for i in r['leaderboards'] if i['name'].lower() == track]) > 1 else False
        if(mto):
            lot = [i["categoryId"] for i in r['leaderboards'] if i['name'].lower() == track]
            categoryIds = {0: "Normal", 1: "Glitch", 2: "No-shortcut", 16: "Shortcut"}
            rci = {"Normal": 0, "Glitch": 1, "No-shortcut": 2, "Shortcut": 16}
            loc = [categoryIds[i] for i in lot]
            x = []
            for i in loc:
                emb = (discord.Embed(color=0xf7b8cf))
                emb.set_author(name=i)
                x.append(emb)
            y = await Paginator.ReactionPaginator(client, message, x)
            sci = rci[y.author.name]
            rn = [i['name'] for i in r['leaderboards'] if i['name'].lower() == track][0] + " - " + y.author.name
            l = "http://tt.chadsoft.co.uk" + ''.join([i["_links"]["item"]["href"] for i in r['leaderboards'] if i['name'].lower() == track and i['categoryId'] == sci])
        else:
            l = "http://tt.chadsoft.co.uk" + ''.join([i["_links"]["item"]["href"] for i in r['leaderboards'] if i['name'].lower() == track])
            rn = [i['name'] for i in r['leaderboards'] if i['name'].lower() == track][0]
        async with aiohttp.ClientSession() as cs:
            async with cs.get(l) as l:
                t = json.loads(str(await l.text())[1:])
        wr = t['ghosts'][0]
    elif(t == 2):
        rn = [i['name'] for i in ct['leaderboards'] if i['name'].lower() == track][0]
        mto = True if len([i['name'].lower() for i in ct['leaderboards'] if i['name'].lower() == track]) > 1 else False
        if(mto):
            lot = [i["categoryId"] for i in ct['leaderboards'] if i['name'].lower() == track]
            categoryIds = {0: "Normal", 1: "Glitch", 2: "No-shortcut", 16: "Shortcut"}
            rci = {"Normal": 0, "Glitch": 1, "No-shortcut": 2, "Shortcut": 16}
            loc = [categoryIds[i] for i in lot]
            x = []
            for i in loc:
                emb = (discord.Embed(color=0xf7b8cf))
                emb.set_author(name=i)
                x.append(emb)
            y = await Paginator.ReactionPaginator(client, message, x)
            sci = rci[y.author.name]
            rn = [i['name'] for i in ct['leaderboards'] if i['name'].lower() == track][0] + " - " + y.author.name
            l = "http://tt.chadsoft.co.uk" + ''.join([i["_links"]["item"]["href"] for i in ct['leaderboards'] if i['name'].lower() == track and i['categoryId'] == sci])
        else:
            l = "http://tt.chadsoft.co.uk" + ''.join([i["_links"]["item"]["href"] for i in ct['leaderboards'] if i['name'].lower() == track])
            rn = [i['name'] for i in ct['leaderboards'] if i['name'].lower() == track][0]
        async with aiohttp.ClientSession() as cs:
            async with cs.get(l) as l:
                t = json.loads(str(await l.text())[1:])
        wr = t['ghosts'][0]
    ft = wr['finishTimeSimple']
    player = wr['player']
    with open("./Resources/Sources/countryCodes.json", "r") as f:
        countryCodes = json.load(f)
    country = countryCodes[str(wr['country'])]
    controller = controllerCodes[str(wr['controller'])]
    with open("./Resources/Sources/driverCodes.json", "r") as f:
        driverCodes = json.load(f)
    driver = driverCodes[str(wr['driverId'])]
    with open("./Resources/Sources/vehicleCodes.json", "r") as f:
        vehicleCodes = json.load(f)
    vehicle = vehicleCodes[str(wr['vehicleId'])]
    dateSet = (datetime.datetime.strptime(wr['dateSet'], "%Y-%m-%dT%H:%M:%SZ") - datetime.timedelta(hours=5)).strftime("%m-%d-%Y %H:%M:%S EST")
    return [rn, ft, player, country, controller, driver, vehicle, dateSet]
