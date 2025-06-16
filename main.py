import discord
from discord.ext import tasks
import asyncio

TOKEN = "token"  # Replace with your actual token
CHANNEL_IDS = [1317155322292338837, 1317155322292338837]  # Replace with your channel IDs
MESSAGE = "Test"  # Replace with your message

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
