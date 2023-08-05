# pubg-toolbox

A set of APIs that are used for my personal projects. There are already a bunch of [awesome utils](https://pypi.org/search/?q=pubg), however they don't really fit my needs. Also made this one small and simple.

## How to Use

### Client
Creating a client is easy
```
client = PUBGClient('<API key>')
```

### Player
```
data = client.request(PlayerQuery('<id>', '<platform>'))
player = Player(data)
```

### Seasons
```
data = client.request(SeasonsQuery('<platform>'))
seasons = Seasons(data)
```

### Matches
```
data = client.request(MatchesQuery('<account id>', '<season is>'))
matches = Matches(data)
```

### Match
```
data = client.request(MatchQuery('<match id>'))
player = Player(data)
```

### Telemetry
Telemetry is a bit more complicated as you need get a match first.
With the Match object created from above, use `get_telemetry_url` to get the telemtry CDN url.
```
data = client.request(TelemetryQuery('<telemetry url>'))
```
Then use event class to deal with each telemetry.


