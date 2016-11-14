#This file contains different formatted URL's to be used in the RiotAPI class as well as other constant values


KEY = 'RGAPI-42ee3ede-f853-4412-95fd-ec912ab55c0d'

URL = {
    'base': 'https://{proxy}.api.pvp.net/api/lol/{region}/{url}',
    'static_base': 'https://global.api.pvp.net/api/lol/static-data/{region}/{url}',
    'summoner_by_name': 'v{version}/summoner/by-name/{names}',
    'league_by_summoner': 'v{version}/league/by-summoner/{ids}/entry',
    'ranked_stats_by_id': 'v{version}/stats/by-summoner/{ids}/ranked',
    'champion_by_id': 'v{version}/champion/{id}'

}

API_VERSIONS = {
    'summoner': '1.4',
    'league': '2.5',
    'stats': '1.3',
    'champion': '1.2'
}


REGIONS = {
    'north_america': 'na',
    'brazil': 'br',
    'korea': 'kr',
    'europe_west': 'euw',
    'europe_nordic_and_east': 'eune'
}
