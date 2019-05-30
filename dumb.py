import discord
from botutils import Clock
client = discord.Client()

@client.event
async def on_ready():
	print("Dumby bot initialized")

@client.event
async def on_message(message):
	c = Clock()
	wt = 2
	if message.content == "!ce":
		await message.channel.send("!createEvent")
		await client.wait_for("message")
		c.wait(wt)
		await message.channel.send("test")
		await client.wait_for("message")
		c.wait(wt)
		await message.channel.send("test")
		await client.wait_for("message")
		c.wait(wt)
		await message.channel.send("0")
		await client.wait_for("message")
		c.wait(wt)
		await message.channel.send("0")
		await client.wait_for("message")
	elif message.content == "!kick-me":
		await message.channel.send("!kick")
		await client.wait_for("message")
		c.wait(wt)
		await message.channel.send("test")
		await client.wait_for("message")
		c.wait(wt)
		await message.channel.send("reddeadeye")
		c.wait(wt)

client.run("NTYyMjYwMTIwMTIyNDI1MzU1.XKIMiQ.tAhxbaNNtFHasU14wDBhHqqs5Ys")
