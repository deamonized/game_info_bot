import discord
from discord.ext import commands
from cassiopeia import riotapi
from cassiopeia.core import currentgameapi
import configparser

config = configparser.ConfigParser()
config.read(config.ini)

tokens = {'discord': config['DEFAULT']['DiscordToken'],
          'riot': config['DEFAULT']['RiotToken']}

riotapi.set_api_key(tokens['riot'])

command_prefix = config['DEFAULT']['CommandPrefix']
description = '''Idk this is memes or some shit'''

bot = commands.Bot(command_prefix=command_prefix, description=description)


@bot.event
async def on_ready():
    print('Logged in as')
    print(bot.user.name)
    print(bot.user.id)
    print('Connected to:')
    for server in bot.servers:
        print(server)
    print('------')


@bot.command(pass_context=True)
async def mythic_plus(ctx):
    await bot.say('%s This weeks affixes are: ' % ctx.message.author.mention)


@bot.command()
async def setgame(*, game: str):
    await bot.change_presence(game=discord.Game(name=game))
    await bot.say('Game set to "{game}"'.format(game=game))


@bot.command()
async def sim(region: str, realm: str, character: str):
    await bot.say('Simming %s on %s %s' % (character, realm, region.upper))


@bot.group(pass_context=True)
async def game(ctx):
    if ctx.invoked_subcommand is None:
        await bot.say('Try again with a region')


@game.command()
async def euw(*, summoner_name: str):
    await say_current_game(summoner_name, 'EUW')


@game.command()
async def na(*, summoner_name: str):
    await say_current_game(summoner_name, 'NA')


@game.command()
async def eune(*, summoner_name: str):
    await say_current_game(summoner_name, 'EUNE')


@game.command()
async def br(*, summoner_name: str):
    await say_current_game(summoner_name, 'BR')


@game.command()
async def jp(*, summoner_name: str):
    await say_current_game(summoner_name, 'JP')


@game.command()
async def kr(*, summoner_name: str):
    await say_current_game(summoner_name, 'KR')


@game.command()
async def lan(*, summoner_name: str):
    await say_current_game(summoner_name, 'LAN')


@game.command()
async def las(*, summoner_name: str):
    await say_current_game(summoner_name, 'LAS')


@game.command()
async def oce(*, summoner_name: str):
    await say_current_game(summoner_name, 'OCE')


@game.command()
async def ru(*, summoner_name: str):
    await say_current_game(summoner_name, 'RU')


@game.command()
async def tr(*, summoner_name: str):
    await say_current_game(summoner_name, 'TR')
    

@bot.group(pass_context=True)
async def rank(ctx):
    if ctx.invoked_subcommand is None:
        await bot.say('Try again with a region')


@rank.command()
async def euw(*, summoner_name: str):
    summoner, rank_info = get_rank_info(summoner_name, 'EUW')
    await say_rank_info(summoner, rank_info)


@rank.command()
async def na(*, summoner_name: str):
    summoner, rank_info = get_rank_info(summoner_name, 'NA')
    await say_rank_info(summoner, rank_info)


@rank.command()
async def eune(*, summoner_name: str):
    summoner, rank_info = get_rank_info(summoner_name, 'EUNE')
    await say_rank_info(summoner, rank_info)


@rank.command()
async def br(*, summoner_name: str):
    summoner, rank_info = get_rank_info(summoner_name, 'BR')
    await say_rank_info(summoner, rank_info)


@rank.command()
async def jp(*, summoner_name: str):
    summoner, rank_info = get_rank_info(summoner_name, 'JP')
    await say_rank_info(summoner, rank_info)


@rank.command()
async def kr(*, summoner_name: str):
    summoner, rank_info = get_rank_info(summoner_name, 'KR')
    await say_rank_info(summoner, rank_info)


@rank.command()
async def lan(*, summoner_name: str):
    summoner, rank_info = get_rank_info(summoner_name, 'LAN')
    await say_rank_info(summoner, rank_info)


@rank.command()
async def las(*, summoner_name: str):
    summoner, rank_info = get_rank_info(summoner_name, 'LAS')
    await say_rank_info(summoner, rank_info)


@rank.command()
async def oce(*, summoner_name: str):
    summoner, rank_info = get_rank_info(summoner_name, 'OCE')
    await say_rank_info(summoner, rank_info)


@rank.command()
async def ru(*, summoner_name: str):
    summoner, rank_info = get_rank_info(summoner_name, 'RU')
    await say_rank_info(summoner, rank_info)


@rank.command()
async def tr(*, summoner_name: str):
    summoner, rank_info = get_rank_info(summoner_name, 'TR')
    await say_rank_info(summoner, rank_info)


async def say_current_game(summoner_name, region):
    riotapi.set_region(region)
    summoner = riotapi.get_summoner_by_name(summoner_name)
    temp = await bot.say('Thinking... 🤔🤔🤔🤔')
    try:
        current_game = currentgameapi.get_current_game(summoner)
    except AttributeError:
        await bot.say("{name} is not in a game".format(name=summoner_name))
        await bot.delete_message(temp)
    summoners = []
    for participant in current_game.participants:
        summoners.append(participant.summoner)
    league_entries = riotapi.get_league_entries_by_summoner(summoners)
    for i, league_entry in enumerate(league_entries):
        message_string = 'Rank information for: {name}'.format(name=current_game.participants[i])
        if league_entry:
            league_entry = league_entry[0]
            message_string += '```Rank: {league} {division} {lp}LP\nWin rate: {win_rate}%, {games} games```'.format(
                league=league_entry.tier.value.title(),
                division=league_entry.entries[0].division.value,
                lp=league_entry.entries[0].league_points,
                win_rate='%.1f' % round((league_entry.entries[0].wins /
                                         (league_entry.entries[0].wins +
                                          league_entry.entries[0].losses)) * 100, 1),
                games=league_entry.entries[0].wins + league_entry.entries[0].losses)
        else:
            message_string += '```Rank: Unranked```'
        await bot.say(message_string)
    await bot.delete_message(temp)


async def say_rank_info(summoner, league_entry):
    temp = await bot.say('Looking up %s' % summoner.name)
    message_string = 'Rank information for: {name}'.format(name=summoner.name)
    if league_entry:
        message_string += '```Rank: {league} {division} {lp}LP\nWin rate: {win_rate}%, {games} games```'.format(
            league=league_entry['league'],
            division=league_entry['division'],
            lp=league_entry['lp'],
            win_rate=league_entry['win_rate'],
            games=league_entry['games'])
    else:
        message_string += '```Rank: Unranked```'
    await bot.edit_message(temp, message_string)


def get_rank_info(summoner_name: str, region: str):
    riotapi.set_region(region)
    summoner = riotapi.get_summoner_by_name(summoner_name)
    try:
        league_entry = riotapi.get_league_entries_by_summoner(summoner)[0]
    except:
        return summoner, None
    return summoner, {'league': league_entry.tier.value.title(),
                      'division': league_entry.entries[0].division.value,
                      'lp': league_entry.entries[0].league_points,
                      'win_rate': '%.1f' % round((league_entry.entries[0].wins /
                                                  (league_entry.entries[0].wins +
                                                   league_entry.entries[0].losses)) * 100, 1),
                      'games': league_entry.entries[0].wins + league_entry.entries[0].losses}

bot.run(tokens['discord'])
