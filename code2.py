import discord
import asyncio
import time
import logging
import traceback

logging.getLogger("discord.http").setLevel(logging.ERROR)

TOKEN = "token"

CHANNEL_IDS = [
    1360600045757403237, 1380756408982831265, 1377406352342909090,
    1373427207191531600, 1380373801140879481, 1355719043243573420,
    1370046895208140860, 1308830998204780555, 1324603930310738001,
    1382722688027590676, 1376137193973747855, 1313314891129552956,
    1373951933026668655, 1373964866271842414, 1313503046755680278,
    1378402331875348561, 1338959641836781568
]

MESSAGE = (
    "# Looking for offers on most/all my accounts discord.gg/HdrHBw5E9S\n"
    "# Buying vip+s or better ranked mfas cheap or bulk idc also nons if cheap\n"
    "# Selling 3.2b+ networth, lvl 220+, ironman coop looking for offers"
)

COOLDOWN_SECONDS = 6 * 60 * 60  # 6 hours cooldown


class SelfBot(discord.Client):
    def __init__(self):
        super().__init__()
        self.channel_cooldowns = {}
        self.ad_task = None
        self.is_running = False

    async def on_ready(self):
        print(f"✅ Logged in as {self.user} ({self.user.id})")

    async def on_message(self, message):
        print(f"📩 Message received from {message.author} in #{message.channel}: {message.content}")

        if message.author.id != self.user.id:
            print("Ignoring message - not from self")
            return

        content = message.content.lower().strip()

        if content == "!startads":
            if self.is_running:
                await message.channel.send("Ad sending already running.")
                print("Ad sending already running.")
                return
            self.is_running = True
            await message.channel.send("Starting ad sending task...")
            print("Starting ad sending task...")
            self.ad_task = asyncio.create_task(self.send_loop())

        elif content == "!stopads":
            if not self.is_running:
                await message.channel.send("Ad sending is not running.")
                print("Ad sending is not running.")
                return
            self.is_running = False
            if self.ad_task:
                self.ad_task.cancel()
                self.ad_task = None
            await message.channel.send("Ad sending task stopped.")
            print("Ad sending task stopped.")

    async def send_loop(self):
        print("Entered send_loop task.")
        try:
            while self.is_running:
                now = time.time()
                print(f"Checking channels at {time.strftime('%X')}")

                for channel_id in CHANNEL_IDS:
                    print(f"Checking channel ID: {channel_id}")
                    cooldown_until = self.channel_cooldowns.get(channel_id, 0)
                    if now < cooldown_until:
                        remaining = int(cooldown_until - now)
                        print(f"⏳ Cooldown active on channel {channel_id}, skipping for {remaining}s")
                        continue

                    channel = self.get_channel(channel_id)
                    if channel is None:
                        print(f"Channel {channel_id} not in cache, fetching...")
                        try:
                            channel = await self.fetch_channel(channel_id)
                            print(f"Fetched channel #{channel.name} successfully.")
                        except Exception as e:
                            print(f"Failed to fetch channel {channel_id}: {e}")
                            continue
                    else:
                        print(f"Found channel in cache: #{channel.name} ({channel.id})")

                    try:
                        print(f"Attempting to send message to #{channel.name} ({channel.id})")
                        await asyncio.wait_for(channel.send(MESSAGE), timeout=10)
                        print(f"✅ Sent message to #{channel.name} ({channel.id})")
                        self.channel_cooldowns[channel_id] = time.time() + COOLDOWN_SECONDS

                    except asyncio.TimeoutError:
                        print(f"❌ Timeout when sending message to #{channel.name} ({channel.id})")

                    except discord.Forbidden:
                        print(f"🚫 Missing permission for #{channel.name}, skipping forever.")
                        self.channel_cooldowns[channel_id] = float("inf")

                    except discord.HTTPException as e:
                        if e.status == 429:
                            retry_after = getattr(e, "retry_after", 3600)
                            print(f"🚦 Rate limited in #{channel.name}, retry after {int(retry_after)} seconds.")
                            self.channel_cooldowns[channel_id] = time.time() + retry_after
                        else:
                            print(f"⚠️ HTTP error in #{channel.name}: {e}")

                    except Exception as e:
                        print(f"❌ Unexpected error when sending to #{channel.name}: {type(e).__name__}: {e}")
                        traceback.print_exc()

                    await asyncio.sleep(5)

                print("🔁 Cycle complete. Sleeping 5 minutes before next check...\n")
                await asyncio.sleep(300)

        except asyncio.CancelledError:
            print("Ad sending task cancelled.")
        except Exception as e:
            print(f"Error in send_loop: {e}")
            traceback.print_exc()


if __name__ == "__main__":
    client = SelfBot()
    client.run(TOKEN)
