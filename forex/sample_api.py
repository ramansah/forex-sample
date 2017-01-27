import falcon
import json


class ForexRates:

    def on_get(self, request, response):
        data = dict(
            name='Raman Sah',
            age=22
        )
        response.body = json.dumps(data)


api = falcon.API()
api.add_route('/forex', ForexRates())
