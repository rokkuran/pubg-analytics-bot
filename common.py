import yaml
import os

from pubg_python import PUBG, Shard


class API:
	""""""
	def __init__(self, shard=Shard.PC_OC):
		self.api = PUBG(os.environ['PUBG_API_KEY'], shard)


class Query(API):
	""""""
	def __init__(self):
		API.__init__(self)

	def get_last_match_id(self, username):
		players = self.api.players().filter(player_names=[username])
		return players[0].matches[0].id

	# def get_user_last_match(self, username):
	# 	players = self.api.players().filter(player_names=[username])
	# 	return self.api.matches().get(players[0].matches[0].id)

	

if __name__ in "__main__":
	pass