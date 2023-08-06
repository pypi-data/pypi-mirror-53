import requests
from dacite import from_dict
from giantbomb.dataclasses import Platform, Release, Game, SearchResult, Genre, Theme

__author__ = "Leandro Voltolino <xupisco@gmail.com>"
__author__ = "Hidde Jansen <hidde@hiddejansen.com>"
__version__ = "1.0.6"


class GiantBombError(Exception):
    def __init__(self, msg):
        self.msg = msg

    def __str__(self):
        return repr(self.msg)


class Api:
    def __init__(self, api_key, user_agent):
        self.api_key = api_key
        self.base_url = 'https://giantbomb.com/api/'
        self.headers = {'User-Agent': user_agent}
        self.default_parameters = {'api_key': self.api_key, 'format': 'json'}

    @staticmethod
    def defaultRepr(obj):
        return "<{}: {}>".format(obj.id, obj.name)

    def validate_response(self, resp):
        if resp['status_code'] == 1:
            return resp['results']
        else:
            raise GiantBombError('Error code {}: {}'.format(
                resp['status_code'],
                resp['error']
            ))

    def perform_request(self, url_path, parameters={}):
        url = self.base_url + url_path

        url_parameters = self.default_parameters.copy()
        url_parameters.update(parameters)

        response = requests.get(url, headers=self.headers,
                                params=url_parameters)

        return self.validate_response(response.json())

    def search(self, query, offset=0):
        url_path = 'search/'
        parameters = {
            'resources': 'game',
            'query': query,
            'offset': offset
        }
        results = self.perform_request(url_path, parameters)

        return [from_dict(data_class=SearchResult, data=x) for x in results]

    def get_game(self, id):
        if not type(id) is int:
            id = id.id
        url_path = 'game/' + str(id) + '/'
        parameters = {}
        results = self.perform_request(url_path, parameters)

        return from_dict(data_class=Game, data=results)

    def list_games(self, plat, offset=0):
        if not type(plat) is int:
            plat = plat.id

        url_path = 'games/'
        parameters = {
            'platforms': plat,
            'offset': offset
        }
        results = self.perform_request(url_path, parameters)

        return [from_dict(data_class=Game, data=x) for x in results]

    def get_platform(self, id):
        if not type(id) is int:
            id = id.id
        url_path = 'platform/' + str(id) + '/'
        parameters = {
            'field_list': ",".join([
                'id',
                'name',
                'abbreviation',
                'deck',
                'image',
                'install_base',
                'release_date',
                'description',
                'api_detail_url',
                'site_detail_url',
                'date_added',
                'date_last_updated'
            ])
        }

        results = self.perform_request(url_path, parameters)
        return from_dict(data_class=Platform, data=results)

    def list_platforms(self, offset=0):
        url_path = 'platforms/'
        parameters = {
            'field_list': ",".join([
                'id',
                'name',
                'abbreviation',
                'deck',
                'image',
                'install_base',
                'release_date',
                'description',
            ]),
            'offset': offset
        }
        results = self.perform_request(url_path, parameters)

        return [from_dict(data_class=SearchResult, data=x) for x in results]

    def get_release(self, id):
        if not type(id) is int:
            id = id.id
        url_path = 'release/' + str(id) + '/'
        parameters = {
            'field_list': ",".join([
                'id',
                'name',
                'deck',
                'description',
                'image',
                'region',
                'developers',
                'platform',
                'release_date',
                'api_detail_url',
                'site_detail_url',
                'date_added',
                'date_last_updated'
            ])
        }

        results = self.perform_request(url_path, parameters)
        return from_dict(data_class=Release, data=results)

    def list_genres(self, offset=0):
        url_path = 'genres/'
        parameters = {
            'offset': offset
        }
        results = self.perform_request(url_path, parameters)

        return [from_dict(data_class=Genre, data=x) for x in results]

    def list_themes(self, offset=0):
        url_path = 'themes/'
        parameters = {
            'offset': offset
        }
        results = self.perform_request(url_path, parameters)

        return [from_dict(data_class=Theme, data=x) for x in results]
