from bs4 import BeautifulSoup
import requests
import re

URL = "http://eztv.it/"

class TVShowNotFound(Exception):
    def __init__(self, message, Errors):

        # Call the base class constructor with the parameters it needs
        Exception.__init__(self, message)
        self.Errors = Errors

class SeasonNotFound(Exception):
    def __init__(self, message, Errors):

        # Call the base class constructor with the parameters it needs
        Exception.__init__(self, message)
        self.Errors = Errors

class EpisodeNotFound(Exception):
    def __init__(self, message, Errors):

        # Call the base class constructor with the parameters it needs
        Exception.__init__(self, message)
        self.Errors = Errors


class eztvAPI(object):
    _instance = None
    _id_tv_show = None
    _season_and_episode = {}

    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super(eztvAPI, cls).__new__(
                                cls, *args, **kwargs)
        return cls._instance

    def TV_Show(self, name):
        global URL
        # all strings are in lowercase
        name = name.lower()
        terms = name.split(' ')

        req = requests.get(URL)
        found = False

        soup = BeautifulSoup(req.content)
        tv_shows =  str(soup('select', {'name': 'SearchString'})).split('</option>')
        for tv_show in tv_shows:
            tv_show = tv_show.lower()
            if all(x in tv_show for x in terms):
                # get the id of the show
                id_tv_show = re.search(r"\d+", tv_show)
                self._id_tv_show  = id_tv_show.group(0)
                found = True
                break

        if not found:
            raise TVShowNotFound('The TV Show "' + ' '.join(terms) + '" has not been found.', None)

        # load the tv show data
        self.load_tv_show_data()
        return self._instance

    def load_tv_show_data(self):
        url = "http://eztv.it/search/"
        payload = {'SearchString' : self._id_tv_show, 'SearchString1': '', 'search': 'Search'}

        req = requests.post(url, data=payload)
        soup = BeautifulSoup(req.content)
        
        episodes =  str(soup('a', {'class': 'magnet'})).split('</a>')
        for episode in episodes:
            regex = re.search(r"S(\d+)E(\d+)", episode)
            try:
                season_tv_show = regex.group(1)
                episode_tv_show = regex.group(2)
                regex = re.search(r"href=\"(.*)\" ", episode)
                magnet_link = regex.group(1)

                self.add_episode_and_season(season_tv_show, episode_tv_show, magnet_link)
            except:
                try:
                    regex = re.search(r"(\d+)x(\d+)", episode)
                    season_tv_show = regex.group(1)
                    episode_tv_show = regex.group(2)
                    regex = re.search(r"href=\"(.*)\" ", episode)
                    magnet_link = regex.group(1)

                    self.add_episode_and_season(season_tv_show, episode_tv_show, magnet_link)
                except:
                    pass
        return self._instance

    # insert into the dictionnary the season and the episode with the specific magnet link
    def add_episode_and_season(self, num_season, num_episode, magnet_link):
        num_season = int(num_season)
        num_episode = int(num_episode)

        if (num_season not in self._season_and_episode):
            self._season_and_episode[num_season] = {}

        if (num_episode not in self._season_and_episode[num_season]):
            self._season_and_episode[num_season][num_episode] = magnet_link

        return self._instance

    # specific episode
    def episode(self, num_season=None, num_episode=None):
        # specific episode
        if (num_season is not None and num_episode is not None):
            # verifiyng the season exist
            if (num_season not in self._season_and_episode):
                raise SeasonNotFound('The season ' + str(num_season) + ' does not exist.', None)

            # verifying the episode exists
            if (num_episode not in self._season_and_episode[num_season]):
                raise EpisodeNotFound('The episode ' + str(num_episode) + ' does not exist.', None)
            
            return self._season_and_episode[num_season][num_episode]
        return ""

    # specifc season
    def season(self, num_season=None):
        res = ""
        # specific season, all episodes
        if (num_season is not None):
            # verifiyng the season exist            
            if (num_season not in self._season_and_episode):
                raise SeasonNotFound('The season ' + str(num_season) + ' does not exist.', None)

            for episode in self._season_and_episode[num_season]:
                res = res + str(episode) + ": " + self._season_and_episode[num_season][episode] + "\n"
            pass

        # all seasons
        else:
            for season in self._season_and_episode:
                for episode in self._season_and_episode[season]:
                    res = res + "S" + str(season) + "E" + str(episode) + ": " + self._season_and_episode[season][episode] + "\n"
            pass
        return res

    # all season
    def seasons(self):
        return self.season()