import requests
from requests.adapters import HTTPAdapter, Retry

s = requests.Session()
retries = Retry(total=3, backoff_factor=0.1, status_forcelist=[500, 502, 503, 504])
s.mount("http://", HTTPAdapter(max_retries=retries))

def _get(url, params=None, proxy=None):
    proxies = {"http": proxy, "https": proxy}
    return s.get(url, params=params, proxies=proxies, timeout=10)

def getAllChannels(base, username, password, proxy=None):
    try:
        r = _get(base.rstrip('/') + '/player_api.php',
                 {"username": username, "password": password, "action": "get_live_streams"}, proxy)
        data = r.json()
        channels = []
        for c in data:
            channels.append({
                "id": c.get("stream_id"),
                "name": c.get("name"),
                "number": c.get("num"),
                "tv_genre_id": c.get("category_id"),
                "cmd": base.rstrip('/') + '/live/' + username + '/' + password + '/' + str(c.get("stream_id")) + '.ts'
            })
        return channels
    except Exception:
        return None

def getGenreNames(base, username, password, proxy=None):
    try:
        r = _get(base.rstrip('/') + '/player_api.php',
                 {"username": username, "password": password, "action": "get_live_categories"}, proxy)
        data = r.json()
        return {str(c.get("category_id")): c.get("category_name") for c in data}
    except Exception:
        return None


