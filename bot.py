from viberbot import Api
from viberbot.api.bot_configuration import BotConfiguration
from flask import Flask, request, Response, logging
from viberbot.api.messages import TextMessage
from viberbot.api.viber_requests import ViberMessageRequest, ViberSubscribedRequest, ViberFailedRequest

logger = logging.getLogger()
logger.setLevel(logging.DEBUG)
handler = logging.StreamHandler()
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
handler.setFormatter(formatter)
logger.addHandler(handler)

bot_configuration = BotConfiguration(
	name='Bot',
	avatar='http://viber.com/avatar.jpg',
	auth_token='4dcd302d6067d205-3f0e50f0e864ac0f-41f04dd6cd3d5089'
)
viber = Api(bot_configuration)

app = Flask(__name__)

@app.route('/incoming', methods=['POST'])
def incoming():
	if not viber.verify_signature(request.get_data(), request.headers.get('X-Viber-Content-Signature')):
		return Response(status=403)

	# this library supplies a simple way to receive a request object

	viber_request = viber.parse_request(request.get_data())

	if isinstance(viber_request, ViberMessageRequest):
		message = viber_request.message
		viber.send_messages(viber_request.sender.id, [
			message
		])

	elif isinstance(viber_request, ViberSubscribedRequest):
		viber.send_messages(viber_request.user.id, [
			TextMessage(text="thanks for subscribing!")
		])

	elif isinstance(viber_request, ViberFailedRequest):
		logger.warn("client failed receiving message. failure: {0}".format(viber_request))

	return Response(status=200)

	# logger.debug("received request. post data: {0}".format(request.get_data()))
	# # handle the request here
	# return Response(status=200)

context = ('server.crt', 'server.key')
app.run(host='0.0.0.0', port=8443, debug=True, ssl_context=context)

viber.set_webhook('https://aqueous-tundra-56533.herokuapp.com')