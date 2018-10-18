import asyncio, aiohttp

async def get_song_info(url):
    fin = None
    async with aiohttp.ClientSession(connector=aiohttp.TCPConnector(verify_ssl=False)) as cs:
        async with cs.get(url) as r:
            f = await r.text()
    if("No Audio Project exists" not in str(f) and "This audio was removed" not in str(f)):
        fin = []
        fin.append(f.split('title>')[1].split('<')[0])
        fin.append(url.split('/')[-1])
        fin.append(f.split('"artist":"')[1].split('"')[0])
        fin.append(f.split('id="author_comments">')[1].split('</div>')[0].replace('</p>', '').replace('<p>', '')[1:].replace('<br>', ''))
        fin.append(f.split('href="/audio/browse/genre/')[1].split('<')[0].split('>')[1])
    return fin

class Song:
    def __init__(self):
        self.info = ""
        self.title = ""
        self.id = 0
        self.author = ""
        self.desc = ""
        self.genre = ""

    @classmethod
    async def create(self, url):
        self.info = await get_song_info(url)
        if(self.info):
            self.title = self.info[0]
            self.id = self.info[1]
            self.author = self.info[2]
            self.desc = self.info[3]
            self.genre = self.info[4]
        else:
            self.info = ""
            self.title = ""
            self.id = 0
            self.author = ""
            self.desc = ""
            self.genre = ""
        return self
