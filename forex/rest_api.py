from forex.db import get_data
import falcon
import json
import time

ONE_HOUR = 1000 * 60 * 60


class ForexRates:

    def on_get(self, request, response):

        currency = request.get_param('currency')
        start = request.get_param('start')
        end = request.get_param('end')

        if not end:
            end = int(time.time() * 1000)
        if not start:
            start = end - ONE_HOUR

        data = get_data(currency, start, end)

        data = dict(
            datapoints=data
        )
        response.body = json.dumps(data)


api = falcon.API()
api.add_route('/forex', ForexRates())
