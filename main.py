import os
import discord
from discord.ext import commands
import csv
import random
import pandas as pd
import riotwatcher as riotwatcher
from riotwatcher import LolWatcher, ApiError
from pprint import pprint
import requests
#useful https://towardsdatascience.com/how-to-use-riot-api-with-python-b93be82dbbd6

api_key = 'RGAPI-*******************'
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
        matchkeys = list(match_detail.keys())

        participant_names = []
        for row in match_detail['participantIdentities']:
          participant_names.append(row['player']['summonerName'])

        counter = 0
        participants = []
        team1 = []
        team2 = []
        for row in match_detail['participants']:
            participants_row = {}
            participants_row['champion'] = id_to_champ_name(row['championId'])
            participants_row['player_id'] = row['participantId']
            participants_row['name'] = participant_names[counter]
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
            if counter >= 5:
              team1.append(participants_row['name'])
            elif counter >= 10 and counter < 5:
              team2.append(participants_row['name'])
            counter += 1
            participants.append(participants_row)

        my_stats = []
        for row in participants:
          if row['name'].lower() == name.lower():
            my_stats = row

        # can change these strings for custom win / loss messages
        win_strings = ['You won the game, good job', 'You conqoured the other teams booties, nice', 'Your team showed the enemies who the real chad was. Nice']
        lose_strings = ['You lost that one, loser idiot head', 'Your team got stomped', 'Not even Justin could of carried that one, another loss for the books', 'You probably had Dalton on your team, feels bad']

        #pprint(participants)
        if my_stats['win'] == True:
          game_comment = win_strings[random.randint(0, len(win_strings) - 1)]
        elif my_stats['win'] == False:
          game_comment = lose_strings[random.randint(0, len(lose_strings) - 1)]
        
        return await ctx.send(f"Last game you played {my_stats['champion']} with a score of {my_stats['kills']}/{my_stats['deaths']}/{my_stats['assists']}. {game_comment}.")

    @commands.command()
    async def runes(self, ctx, *message):

        return await ctx.send(message)

    @commands.command()
    async def stats(self, ctx, *message):
        name = ' '.join(message)
        me = watcher.summoner.by_name(my_region, name)
        my_ranked_stats = watcher.league.by_summoner(my_region, me['id'])[0]

        winrate = round(((my_ranked_stats['wins'] / (my_ranked_stats['wins'] + my_ranked_stats['losses'])) * 100), 1)

        return await ctx.send(f"Ranked stats for {name}: \n   Rank: {my_ranked_stats['tier']} {my_ranked_stats['rank']}: {my_ranked_stats['leaguePoints']}LP \n   Wins: {my_ranked_stats['wins']} \n   Losses: {my_ranked_stats['losses']} \n   Winrate: {winrate}% ")
    
    @commands.command()
    async def tips(self, ctx, *message):
      champ_syntaxed = []
      for split_champion_name in message:
        string = split_champion_name.capitalize()
        champ_syntaxed.append(string)
      
      champ_syntaxed = ''.join(champ_syntaxed)
      r = requests.get(f'http://ddragon.leagueoflegends.com/cdn/11.19.1/data/en_US/champion/{champ_syntaxed}.json')

      try: 
        r.raise_for_status()
      except requests.exceptions.HTTPError:
          return await ctx.send(f"ERROR Champion: {champ_syntaxed}, does not exist. Are you sure you are spelling it right?")

      champ_info = r.json()
      champ_tips = champ_info['data'][champ_syntaxed]['allytips']
      tips_string = ''
      for tip in champ_tips:
        tips_string = tips_string + tip + '\n\n'
      return await ctx.send(tips_string)

    @commands.command()
    async def champ(self, ctx, *message):
      champ_syntaxed = []
      for split_champion_name in message:
        string = split_champion_name.capitalize()
        champ_syntaxed.append(string)
      
      champ_syntaxed = ''.join(champ_syntaxed)

      r = requests.get(f'http://ddragon.leagueoflegends.com/cdn/11.19.1/data/en_US/champion/{champ_syntaxed}.json')

      try: 
        r.raise_for_status()
      except requests.exceptions.HTTPError:
          return await ctx.send(f"ERROR Champion: {champ_syntaxed}, does not exist. Are you sure you are spelling it right?")

      champ_info = r.json()
      pprint(champ_info['data'][champ_syntaxed])

      blurb = champ_info['data'][champ_syntaxed]['blurb']
      passive_desc = champ_info['data'][champ_syntaxed]['passive']['description']
      passive_name = champ_info['data'][champ_syntaxed]['passive']['name']
      q_desc = champ_info['data'][champ_syntaxed]['spells'][0]['description']
      q_name = champ_info['data'][champ_syntaxed]['spells'][0]['name']
      w_desc = champ_info['data'][champ_syntaxed]['spells'][1]['description']
      w_name = champ_info['data'][champ_syntaxed]['spells'][1]['name']
      e_desc = champ_info['data'][champ_syntaxed]['spells'][2]['description']
      e_name = champ_info['data'][champ_syntaxed]['spells'][2]['name']
      r_desc = champ_info['data'][champ_syntaxed]['spells'][3]['description']
      r_name = champ_info['data'][champ_syntaxed]['spells'][3]['name']
      champ_tips = champ_info['data'][champ_syntaxed]['allytips']
      counter_tips = champ_info['data'][champ_syntaxed]['enemytips']

      return await ctx.send(f"Champion: {champ_syntaxed}\n\nPassive -- {passive_name}: {passive_desc}\n\nQ Ability -- {q_name}: {q_desc}\n\nW Ability -- {w_name}: {w_desc}\n\nE Ability -- {e_name}: {e_desc}\n\nUltimate Ability -- {r_name}: {r_desc}")


bot = commands.Bot(
    command_prefix=commands.when_mentioned_or("!"),
    description='Relatively simple music bot example'
)


@bot.event
async def on_ready():
    print(f'Logged in as {bot.user} (ID: {bot.user.id})')
    print('------')

bot.add_cog(Info(bot))
bot.run(my_secret)

