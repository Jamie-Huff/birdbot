import os
import discord
from discord.ext import commands
import csv
import random
import pandas as pd
import riotwatcher as riotwatcher
from riotwatcher import LolWatcher, ApiError
from pprint import pprint
#useful https://towardsdatascience.com/how-to-use-riot-api-with-python-b93be82dbbd6

# Needs riotAPI api_key from https://developer.riotgames.com/
api_key = 'RGAPI-******'
watcher = LolWatcher(api_key)
my_region = 'na1'

# init data dragon info
current_version = watcher.data_dragon.versions_for_region(my_region)['v']
champions = watcher.data_dragon.champions(current_version)

#
def id_to_champ_name(champ_id):
  champ_id = str(champ_id)
  champ_name = [k for k, v in champions['data'].items() if v['key'] == champ_id][0]
  return champ_name


# list of features to implement
 # !counter
 # !runes
 # !build
phrases = []
with open("phrases.csv") as csv_file:
    csv_reader = csv.reader(csv_file, delimiter=',')
    for row in csv_reader:
        phrases.append(row[1])


class Info(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def join(self, ctx, *, channel: discord.VoiceChannel):
        """Joins a voice channel"""

        if ctx.voice_client is not None:
            return await ctx.voice_client.move_to(channel)

        await channel.connect()


    @commands.command()
    async def greet(self, ctx):
        return await ctx.send('thanks for saying hi!')

    @commands.command()
    async def user(self, ctx, *message):
        name = ' '.join(message)
        # join our string back together, with no spaces and the proper values
        # user_web_syntax = "".join(user_web_syntax)
        me = watcher.summoner.by_name(my_region, name)

        response = watcher.summoner.by_name(my_region, name)

        return await ctx.send(f"Player info for {name}: \n   Username: {response['name']} \n   Account Id: {response['accountId']} \n   puuid: {response['puuid']} \n   Summoner Level: {response['summonerLevel']}")

    @commands.command()
    async def game(self, ctx, *message):
        name = ' '.join(message)
        me = watcher.summoner.by_name(my_region, name)
        my_matches = watcher.match.matchlist_by_account(my_region, me['accountId'])
        last_match = my_matches['matches'][0]
        match_detail = watcher.match.by_id(my_region, last_match['gameId'])
        # I can use this to vie all of the indivdual keys from my result
        matchkeys = list(match_detail.keys())
        print(matchkeys)
        # pprint(match_detail['participants'][0]['championName'])
        pprint(watcher.data_dragon.versions_for_region('na1')['v'])
        # pprint(watcher.data_dragon.champions())
    # i need to add the users information to this
    # for example each users id or puuid
        participants = []
        for row in match_detail['participants']:
            participants_row = {}
            participants_row['champion'] = id_to_champ_name(row['championId'])
            participants_row['spell1'] = row['spell1Id']
            participants_row['spell2'] = row['spell2Id']
            participants_row['win'] = row['stats']['win']
            participants_row['kills'] = row['stats']['kills']
            participants_row['deaths'] = row['stats']['deaths']
            participants_row['assists'] = row['stats']['assists']
            participants_row['totalDamageDealt'] = row['stats']['totalDamageDealt']
            participants_row['goldEarned'] = row['stats']['goldEarned']
            participants_row['champLevel'] = row['stats']['champLevel']
            participants_row['totalMinionsKilled'] = row['stats']['totalMinionsKilled']
            participants_row['item0'] = row['stats']['item0']
            participants_row['item1'] = row['stats']['item1']
            participants.append(participants_row)
        # df = pd.DataFrame(participants)
        # df
        pprint(participants)
        return await ctx.send(participants[0])

    @commands.command()
    async def runes(self, ctx, *message):

        return await ctx.send(message)

    @commands.command()
    async def stats(self, ctx, *message):
        name = ' '.join(message)
        me = watcher.summoner.by_name(my_region, name)
        my_ranked_stats = watcher.league.by_summoner(my_region, me['id'])[0]

        winrate = round(((my_ranked_stats['wins'] / (my_ranked_stats['wins'] + my_ranked_stats['losses'])) * 100), 1)

        # winrate = wins / wins + losses
        return await ctx.send(f"Ranked stats for {name}: \n   Rank: {my_ranked_stats['tier']} {my_ranked_stats['rank']}: {my_ranked_stats['leaguePoints']}LP \n   Wins: {my_ranked_stats['wins']} \n   Losses: {my_ranked_stats['losses']} \n   Winrate: {winrate}% ")

    # @commands.command()
    # async def thought(self, ctx):
    #     response = phrases[random.randint(0, len(phrases) - 1)]
    #     return await ctx.send(response)

#when ever someone uses the ! before a message in the chat, 
#the program looks for a function that follows the text after it.
bot = commands.Bot(
    command_prefix=commands.when_mentioned_or("!"),
    description='A leauge of legends discord bot'
)


@bot.event
async def on_ready():
    print(f'Logged in as {bot.user} (ID: {bot.user.id})')
    print('------')


bot.add_cog(Info(bot))
bot.run()
