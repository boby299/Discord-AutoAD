import discord
from discord.ext import tasks
import asyncio
import random

TOKEN = "token"

CHANNEL_IDS = [
    1394028546304905310,
    1387979168964411523,
    1380756408982831265,
    1373427207191531600,
    1355719043243573420,
    1370046895208140860,
    1324603930310738001,
    1313314891129552956,
    1373951933026668655,
    1338959641836781568,
    1384557489504256134,
]

MESSAGE = (
    "# Looking for offers on most/all my accounts ❤️\n"
    "# Buying vip+s or better ranked mfas cheap or bulk idc also nons if cheap\n"
    "# Selling MFAs, Skyblock accounts, Coins and much more\n"
    "# Just created New server Join up discord.gg/sstzcdsTaq"
)

class SelfBot(discord.Client):
    async def on_ready(self):
        print(f"✅ Logged in as {self.user}")
        self.send_message_task.start()

    @tasks.loop(minutes=60)  # Check every 60 minutes
    async def send_message_task(self):
        now = asyncio.get_event_loop().time()

        for channel_id in CHANNEL_IDS:
            # Check if it's time to send again
            if self.last_sent.get(channel_id, 0) + self.cooldown <= now:
                channel = self.get_channel(channel_id)
                if channel:
                    try:
                        message = MESSAGE
                        await channel.send(message)
                        self.last_sent[channel_id] = now
                        print(f"[✔] Sent to {channel.name} ({channel.id})")
                        await asyncio.sleep(random.randint(30, 60))  # Delay between messages
                    except discord.HTTPException as e:
                        print(f"[✖] Rate limited or failed: {e}")
                        await asyncio.sleep(60)  # Wait 1 minute if error
                else:
                    print(f"[!] Channel {channel_id} not found")

    @send_message_task.before_loop
    async def before_sending(self):
        await self.wait_until_ready()
        self.cooldown = 6 * 60 * 60 + random.randint(0, 1800)  # ~6–6.5 hours
        self.last_sent = {}  # Channel ID to last sent timestamp

client = SelfBot()
client.run(TOKEN)

