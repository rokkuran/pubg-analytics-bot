import yaml
import os
# import io
# import urllib
# import base64

import numpy as np

import matplotlib.pyplot as plt

from pubg_python import PUBG, Shard


class API:
	""""""
	def __init__(self, shard=Shard.PC_OC):
		self.api = PUBG(os.environ['PUBG_API_KEY'], shard)


class Query(API):
	""""""
	def __init__(self):
		API.__init__(self)

	def get_players(self, username):
		return self.api.players().filter(player_names=[username])

	def get_last_match_id(self, username):
		players = self.get_players(username)
		return players[0].matches[0].id
	
	def get_player_id(self, username)
		players = self.get_players(username)
        return players[0].id
	
	def get_last_match_info(self, username):
		match = api.matches().get(self.get_last_match_id(username))
		
		match_info = {
			"game_mode": match.game_mode,
			"duration": match.duration,
			"map": match.map,
		} 

		return match_info
	
	# def test_plot(self, n):
	
	# 	plt.plot(range(n), np.random.normal(0, 1, n))
	# 	fig = plt.gcf()

	# 	buf = io.BytesIO()
	# 	fig.savefig(buf, format='png')
	# 	buf.seek(0)
	# 	string = base64.b64encode(buf.read())

	# 	uri = 'data:image/png;base64,' + urllib.parse.quote(string)
	# 	return uri

	# def get_user_last_match(self, username):
	# 	players = self.api.players().filter(player_names=[username])
	# 	return self.api.matches().get(players[0].matches[0].id)

	

if __name__ in "__main__":
	pass