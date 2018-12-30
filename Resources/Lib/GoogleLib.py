import asyncio, aiohttp, bs4, discord

async def get_google_images(search_query):
    fin = []
    headers = {
        'User-Agent': ('Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:61.0) '
                      'Gecko/20100101 Firefox/61.0'),
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8'
    }
    for i in range(0, 100, 20):
        url="http://images.google.com/search?safe=active&q="+search_query+"&tbm=isch&sout=1&start=" + str(i)
        async with aiohttp.ClientSession() as cs:
            async with cs.get(url, headers=headers) as f:
                soup = bs4.BeautifulSoup(await f.text(), "lxml")
        print(soup)
        for j in soup.find("div", {"id": "ires"}).find_all("a"):
            emb = (discord.Embed(color=0xf7b8cf))
            emb.set_author(name="Google Image Search - " + search_query)
            emb.set_image(url=j.img['src'])
            fin.append(emb)
    return fin
