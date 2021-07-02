import datetime
import discord
from dotenv import dotenv_values

TOKEN = dotenv_values(".env")["TOKEN"]


class Client(discord.Client):
    async def on_ready(self):
        members = getlist(self.guilds[0])
        votes = {}
        for member in members:
            votes[member] = 0
        for member in members:
            try:
                dm = await member.create_dm()
                messages = await dm.history(limit=5, oldest_first=False,
                                            after=datetime.datetime.now() - datetime.timedelta(
                                                days=2)).flatten()
                for message in messages:
                    message = message.content.split()
                    if message[0] == "!vote" and not members[int(message[1]) - 1] == member:
                        votes[members[int(message[1]) - 1]] += 1
                        break
            except Exception as e:
                print(repr(e))
        sortedvotes = sorted(votes, key=votes.get, reverse=True)
        msg = "@everyone The election has ended and the results are are:\n"
        for i, member in enumerate(sortedvotes):
            if i == 0:
                msg += f"{member.mention}: {votes[member]} votes\n"
            elif votes[member] > 1:
                msg += f"{member.name}: {votes[member]} votes\n"
            elif votes[member] == 1:
                msg += f"{member.name}: {votes[member]} vote\n"
            else:
                break
        await self.guilds[0].text_channels[0].send(msg)
        await sortedvotes[0].add_roles(self.guilds[0].get_role(810326558727602258))
        await self.close()


def getlist(guild):
    ids = open("./members.txt").readlines()
    return [guild.get_member(int(uid)) for uid in ids]


intents = discord.Intents.default()
intents.members = True
Client(intents=intents).run(TOKEN)
