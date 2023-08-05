class PUBGQuery:
    PUBG_HOST = 'https://api.pubg.com/'

    def get_host(self):
        return self.PUBG_HOST

    def get_domain(self):
        return ''

    def get_endpoint(self):
        return self.get_host() + self.get_domain()

class PUBGShardedQuery(PUBGQuery):
    def __init__(self, shard='steam'):
        self.shard = shard

    def get_host(self):
        return self.PUBG_HOST + 'shards/{}/'.format(self.shard)

class PlayerQuery(PUBGShardedQuery):
    def __init__(self, player_name, shard='steam'):
        self.player_name = player_name
        self.shard = shard

    def get_domain(self):
        return 'players?filter[playerNames]={}'.format(self.player_name)

class SeasonsQuery(PUBGShardedQuery):
    def __init__(self, shard='steam'):
        self.shard = shard

    def get_domain(self):
        return 'seasons'

class MatchesQuery(PUBGShardedQuery):
    def __init__(self, account_id, season_id, shard='steam'):
        self.account_id = account_id
        self.season_id = season_id
        self.shard = shard

    def get_domain(self):
        return 'players/{}/seasons/{}'.format(self.account_id, self.season_id)

class MatchQuery(PUBGShardedQuery):
    def __init__(self, match_id, shard='steam'):
        self.match_id = match_id
        self.shard = shard

    def get_domain(self):
        return 'matches/{}'.format(self.match_id)

class TelemetryQuery(PUBGQuery):
    def __init__(self, url):
        self.url = url

    def get_endpoint(self):
        return self.url
