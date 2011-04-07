import random

class CoinflipHandler:
	def __init__(self):
		
	def privmsg(self, user, channel, msg):
		return random.choice(["heads","tails"])
