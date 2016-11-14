import requests
import RiotConsts as Consts


class RiotAPI(object):
    def __init__(self, api_key, static, region=Consts.REGIONS['north_america']):
        self.api_key = api_key
        self.region = region
        self.static = static

    def _request(self, api_url, params={}): #This private function makes the request to either the static or regional API
        args = {'api_key': self.api_key}
        for key, value in params.items():
            if key not in args:
                args[key] = value

        if(self.static ==False):
            response = requests.get(
                Consts.URL['base'].format( #Every regional request will have the same base which is stored as a constant in RiotConsts
                    proxy=self.region,     #The URL is formatted for specific purposes in later functions
                    region=self.region,
                    url=api_url
                ),
                params=args
            )
        else:
            response = requests.get(
                Consts.URL['static_base'].format( #Every static request will have the same base which is stored as a constant in RiotConsts
                    region=self.region,           #The URL is formatted for specific purposes in later functions
                    url=api_url
                ),
                params=args
            )
            #print response.url

       # if(response.status_code!=200):
          #  print 'ERROR: Summoner Not Found'
           # exit()

        return response.json()                   #The response is returned formatted in json so it can be used as a dictionary

    def get_summoner_by_name(self, name):
        api_url = Consts.URL['summoner_by_name'].format( #Subsequent functions all specialize the base URL with specified parameters
            version=Consts.API_VERSIONS['summoner'],     #and call _request on the new URL
            names=name
        )

        return self._request(api_url)

    def get_league_by_id(self, id):
        api_url = Consts.URL['league_by_summoner'].format(
            version=Consts.API_VERSIONS['league'],
            ids=id
        )
        return self._request(api_url)

    def get_stats_by_id(self, id):
        api_url = Consts.URL['ranked_stats_by_id'].format(
            version = Consts.API_VERSIONS['stats'],
            ids=id
        )
        return self._request(api_url)

    def get_champ_by_id(self, id):
        api_url = Consts.URL['champion_by_id'].format(
            version=Consts.API_VERSIONS['champion'],
            id=id
        )
        return self._request(api_url)
