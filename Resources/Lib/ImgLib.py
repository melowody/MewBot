import discord, asyncio, io, aiohttp, numpy as np
from PIL import Image

async def Blurplefy(im):
    im = im.convert("LA")
    x = im.load()
    [a, b] = im.size
    for i in range(a):
        for j in range(b):
            a1 = abs(x[i, j][0] - 0)
            a2 = abs(x[i, j][0] - 127)
            a3 = abs(x[i, j][0] - 255)
            if(a1 < a2 and a1 < a3):
                x[i, j] = (0, 255)
            elif(a2 < a1 and a2 < a3):
                x[i, j] = (127, 255)
            else:
                x[i, j] = (255, 255)
    im = im.convert("RGBA")
    data = np.array(im)
    red, green, blue, alpha = data.T
    black = (red == 0) & (blue == 0) & (green == 0) & (alpha == 255)
    data[..., :-1][black.T] = (78, 93, 148)
    grey = (red == 127) & (blue == 127) & (green == 127) & (alpha == 255)
    data[..., :-1][grey.T] = (114, 137, 218)
    im = Image.fromarray(data)
    return im

async def GetImage(client, ctx, args):
    if (args == ()):
        m = ctx.message
        if (m.attachments != []):
            x = m.attachments[0].url
        else:
            x = m.author.avatar_url
    elif (args[0][:2] == "<@" and args[0][-1] == ">"):
        if (args[0][:3] == "<@!"):
            y = args[0].split("<@!")[1].split(">")[0]
        else:
            y = args[0].split("<@")[1].split(">")[0]
        try:
            x = await client.get_user_info(y)
        except discord.errors.NotFound:
            return None
        x = x.avatar_url
    elif (args[0].isdigit()):
        try:
            x = await client.get_user_info(int(args[0]))
        except discord.errors.NotFound:
            return None
        x = x.avatar_url
    elif (args[0].startswith('http')):
        x = args[0]
    else:
        return None
    async with aiohttp.ClientSession(connector=aiohttp.TCPConnector(verify_ssl=False)) as aioclient:
        async with aioclient.get(x) as r:
            f = await r.read()
    if (x.split(".")[-1].split("?")[0].lower() == "webp"):
        return Image.open(io.BytesIO(f)).convert("RGB")
    else:
        return Image.open(io.BytesIO(f))
