import discord
from discord.ext import tasks
import asyncio

TOKEN = "Token"  # Replace with your actual token
CHANNEL_IDS = [1380756408982831265, 1377406352342909090, 1373427207191531600, 1380373801140879481, 1355719043243573420, 1370046895208140860, 1308830998204780555, 1324603930310738001, 1382722688027590676]  # Replace with your channel IDs
MESSAGE = (
    "# Looking for offers on most/all my accounts discord.gg/HdrHBw5E9S\n"
    "# Buying vip+s or better ranked mfas cheap or bulk idc also nons if cheap\n"
    "# Selling 3.2b+ networth, lvl 220+, ironman coop looking for offers"
)


class SelfBot(discord.Client):
    async def on_ready(self):
        print(f"Logged in as {self.user}")
        self.send_message_task.start()

    @tasks.loop(hours=6, minutes=30)
    async def send_message_task(self):
        for channel_id in CHANNEL_IDS:
            channel = self.get_channel(channel_id)
            if channel:
                try:
                    await channel.send(MESSAGE)
                    print(f"Sent message to {channel.name}")
                except Exception as e:
                    print(f"Error sending message: {e}")
                await asyncio.sleep(10)
            else:
                print(f"Channel {channel_id} not found.")

    @send_message_task.before_loop
    async def before_sending(self):
        await self.wait_until_ready()

# Do NOT pass intents when using discord.py-self
client = SelfBot()
client.run(TOKEN)
