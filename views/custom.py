from datetime import datetime

from app import app
from libraries import holidayapi
from sanic import Blueprint
from sanic.response import json

custom = Blueprint('custom')


@custom.route("/holidays")
async def holidays(request):
    params = {
        'country': 'US',
        'public': 1
    }
    hapi = holidayapi.v1(app.config['HOLIDAYAPI_KEY'], params)
    results = await hapi.last_5_year_holidays()
    return json({'holidays': results})
