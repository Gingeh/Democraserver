import discord
from random import shuffle
from dotenv import dotenv_values

TOKEN = dotenv_values(".env")["TOKEN"]


class Client(discord.Client):
    async def on_ready(self):
        members = [x for x in self.guilds[0].members if not x.bot]
        shuffle(members)
        savelist(members)
        msg = ("@everyone The election has begun, please send a DM to vote (`!vote <ID>`). "
               "Voting ends in 24 hours.\nThe candidate IDs are:\n")
        for i, member in enumerate(members):
            try:
                msg += f"{i + 1}. {member.name}\n"
                await member.remove_roles(self.guilds[0].get_role(810326558727602258))
                dm = await member.create_dm()
                await dm.send(
                    "Use `!vote <id>` to vote. (Only the latest message will be counted.)")
            except Exception as e:
                print(e)
        await self.guilds[0].text_channels[0].send(msg)
        await self.close()


def savelist(members):
    with open("./members.txt", "w+") as f:
        for member in members:
            f.write(str(member.id)+"\n")


intents = discord.Intents.default()
intents.members = True
client = Client(intents=intents)
client.run(TOKEN)
