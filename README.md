Thanks for checking out birdbot :)

Birdbot is a discord bot that references riot api to provide helpful features to users.

** NOTE: THIS BOT IS IN PROGRESS AND DOES NOT HAVE FULL FUNCTIONALITY **

How to get started with birdbot:
1. head to: https://developer.riotgames.com/
2. Sign in to your riot account, and generate a new development API Key
  ** NOTE: DO NOT SHARE THIS WITH ANYONE. ITS FOR YOU AND YOU ALONE **
  the format should look like : RGAPI-11a1a1a1-aa11-11aa-111a-1aa1111a1aa1 with your own unique values.
3. replace the api_key variable at the top of main.py with your unique key
4. Head to https://replit.com/ , make an account, and create a new replit
5. Copy and paste the code into replit and click run to start the program.
6. Figure out on your own how to create a discord bot and get your api key from the bot
7. Replace the last line of the program
 `` bot.run(my_secret) ``
 with your bot specific key
`` bot.run('your discord bot key here') ``
8. Maybe it will work..?





some features available from birdbot:

  !stats:
    Provide a users ranked stats. Input: !stats name_string

      example input: "!stats nice rat"

      example output: Ranked stats for nice rat: 
                          Rank: PLATINUM II: 0LP 
                          Wins: 204 
                          Losses: 170 
                          Winrate: 54.5%

  !game:
    Provides insights about the users current game. Input: !game name_string

      example input: "!game nice rat"

      example output: TO BE DETERMINED

  ** FOR DEVELOPERS **
  !user:
    Provides the required information to get queries on a specific user. Input: !user name_string

      example input: "!user nice rat"

      example output: Player info for nice rat: 
                          Username: nice rat 
                          Account Id: CACHfHIA5MTNPDQNrVqDylS7Q_fMkgAlKLm3WG6x_KhMVFg 
                          puuid: qIMOa5zlengMPuWlb3r5Y78GF-90CM3AtsD-PxGrYJ7Skta8wCfjua8f5cGgA0vWAA1i77_BuFxApA 
                          Summoner Level: 165