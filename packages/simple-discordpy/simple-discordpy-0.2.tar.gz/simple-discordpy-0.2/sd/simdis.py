import discord
import queue
import asyncio
from threading import Thread

loop = asyncio.get_event_loop()
q = queue.Queue()

class MyClient(discord.Client):
    async def on_ready(self):
        print('Logged on as', self.user)

    async def on_message(self, message):
        if message.author == self.user:
            return

        q.put(message.content)

    async def send_msg(self, message):
        for ch in self.get_all_channels():
            if isinstance(ch, discord.TextChannel):
                await ch.send(message)

client = MyClient()

def f(loop, token):
    asyncio.set_event_loop(loop)
    loop.run_until_complete(client.start(token))

def sdinput():
    return q.get()

def sdstart(token):
    Thread(target=f, args=(loop, token)).start()

def sdstop():
    asyncio.run_coroutine_threadsafe(client.close(), loop)

def sdprint(*values):
    asyncio.run_coroutine_threadsafe(client.send_msg(' '.join([str(value) for value in values])), loop).result()


