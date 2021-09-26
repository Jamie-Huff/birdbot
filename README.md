# Thanks for checking out birdbot :)

birdbot is a discord bot that references riot api to provide helpful features to users.

# ** NOTE: THIS BOT IS IN PROGRESS AND DOES NOT HAVE FULL FUNCTIONALITY **

# How to get started with birdbot
1. head to: https://developer.riotgames.com/
2. Sign in to your riot account, and generate a new development API Key
  ** NOTE: DO NOT SHARE THIS WITH ANYONE. ITS FOR YOU AND YOU ALONE **
  the format should look like :
       
        RGAPI-11a1a1a1-aa11-11aa-111a-1aa1111a1aa1 with your own unique values.


3. replace the api_key variable at the top of main.py with your unique key
4. Head to https://replit.com/ , make an account, and create a new replit
5. Copy and paste the code into replit and click run to start the program.
6. Figure out on your own how to create a discord bot and get your api key from the bot
7. Replace the last line of the program
 `` bot.run(my_secret) ``
 with your bot specific key
`` bot.run('your discord bot key here') ``
8. Maybe it will work..?





# birdbot Commands

##  !stats:
    Provide a users ranked stats. Input: !stats player_name_string

      example input: "!stats nice rat"

      example output: Ranked stats for nice rat: 
                          Rank: PLATINUM II: 0LP 
                          Wins: 204 
                          Losses: 170 
                          Winrate: 54.5%

##  !game:
    Provides insights about the users most recent game. Input: !game player_name_string

      example input: "!game nice rat"

      example output: TO BE DETERMINED

##  !champ:
    Provides a list of all your champions abilities. Input: !champ champ_name_string

      example input: "!champ anivia"

      example output: 
      
          Champion: Anivia

                          Passive -- Rebirth: Upon taking fatal damage, Anivia reverts to an egg and is reborn with full health.

                          Q Ability -- Flash Frost: Anivia brings her wings together and summons a sphere of ice that flies towards her opponents, chilling and damaging anyone in its path. When the sphere explodes it does moderate damage in a radius, stunning anyone in the area.

                          W Ability -- Crystallize: Anivia condenses the moisture in the air into an impassable wall of ice to block all movement. The wall only lasts a short duration before it melts.

                          E Ability -- Frostbite: With a flap of her wings, Anivia blasts a freezing gust of wind at her target, dealing damage. If the target was recently hit by Flash Frost or damaged by a fully formed Glacial Storm, the damage they take is doubled.

                          Ultimate Ability -- Glacial Storm: Anivia summons a driving rain of ice and hail to damage her enemies and slow their advance.

##  !tips:
    Provides some helpful tips if you are new to a champion. Input: !tips champ_name_string

      example input: "!tips anivia"

      exampple output:

                          Timing Flash Frost with Frostbite can lead to devastating combinations.

                          Anivia is extremely reliant on Mana for Glacial Storm. Try getting items with Mana or going for a Crest of the Ancient Golem buff on Summoner's Rift.

                          It can be very difficult for enemy champions to kill her egg early in game. Seize the advantage by playing aggressively.

###  ** FOR DEVELOPERS **
##  !user:
    Provides the required information to get queries on a specific user. Input: !user name_string

      example input: "!user nice rat"

      example output: Player info for nice rat: 
                          Username: nice rat 
                          Account Id: CACHfHIA5MTNPDQNrVqDylS7Q_fMkgAlKLm3WG6x_KhMVFg 
                          puuid: qIMOa5zlengMPuWlb3r5Y78GF-90CM3AtsD-PxGrYJ7Skta8wCfjua8f5cGgA0vWAA1i77_BuFxApA 
                          Summoner Level: 165