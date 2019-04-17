# aiohttp features excellent support of the HTTP protocol as well as for websockets, making it ideal for working with popular websocket
# libraries such as socket.io

# A RESTful API is an application program interface that uses HTTP requests to GET, PUT, POST and DELETE data
    # A RESTful API breaks down a transaction to create a series of small modules
    # Each module addresses a particular underlying part of the transaction

# Because the calls are stateless, REST is useful in cloud applications
    # Stateless componenets can be freely redeployed if something fails, and they can scale to accommodate load changes

# Stateful and stateless are adjectives to describe whether a computer of computer program is designed to note and remember one or more preceding
# events in a given sequence of interactions with a user/computer/device/outside element
    # Stateful means the computer or program keeps track of the state of interaction, usually by setting values in a storage field designated for that purpose
    # Stateless means there is no record of previous interactions and each interaction request has to be handled only with the info that comes with it

# The key part of the aiohttp framework is that it works in an asynchronous manner, and can concurrently handle hundreds of requests per
# second without too much hassle

# To begin writing a simple API you must write a handler function: async def handle(request): which returns a json based response whenever called

# We will then create an app object by calling app = web.Application() and then we will set up our app's router and add a GET request endpoint
# that calls handle whenever "/" is hit

# Finally we will call web.run_app(app) in order to kick off our newly defined aiohttp API

from aiohttp import web 
import json

async def handle(request):
    response_obj = {'status': 'success'}
    return web.Response(text=json.dumps(response_obj))

async def new_user(request):
    try:
        user = request.query['name']
        print("Creating new user with name: ", user)
        response_obj = {'status': 'success'}
        return web.Response(text=json.dumps(response_obj), status=200) # i.e. 'OK'
    except Exception as e:
        # bad path where name is not set 
        response_obj = {'status': 'failed', 'reason': str(e)}
        return web.Response(text=json.dumps(response_obj), status=500) # i.e. 'Server error'

app = web.Application()
app.router.add_get('/', handle)
app.router.add_post('/user', new_user)

web.run_app(app)


