from viberbot import Api
from viberbot.api.bot_configuration import BotConfiguration
from flask import Flask, request, Response

bot_configuration = BotConfiguration(
	name='Bot',
	avatar='http://viber.com/avatar.jpg',
	auth_token='4dcd302d6067d205-3f0e50f0e864ac0f-41f04dd6cd3d5089'
)
viber = Api(bot_configuration)

app = Flask(__name__)

@app.route('/incoming', methods=['POST'])
def incoming():
	logger.debug("received request. post data: {0}".format(request.get_data()))
	# handle the request here
	return Response(status=200)

context = ('server.crt', 'server.key')
app.run(host='0.0.0.0', port=443, debug=True, ssl_context=context)

viber.set_webhook('https://:443/')