# import matplotlib
# matplotlib.use('Agg')  # tkinter backend not supported by heroku
# import matplotlib.pyplot as plt

import yaml
import os

from collections import Counter
from datetime import datetime
# import io
# import urllib
# import base64

# import numpy as np
import pandas as pd

import plotly
plotly.tools.set_credentials_file(username='rokkuran', api_key=os.environ['PLOTLY_API_KEY'])
import plotly.plotly as py
import plotly.graph_objs as go

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
		
	def get_player_id(self, username):
		players = self.get_players(username)
		return players[0].id
	
	def get_last_match_info(self, username):
		match = self.api.matches().get(self.get_last_match_id(username))
		
		match_info = {
			"game_mode": match.game_mode,
			"duration": match.duration,
			"map": match.map,
		} 

		return match_info

	def get_user_last_match(self, username):
		return self.api.matches().get(self.get_last_match_id(username))

	def _get_match(self, match_id):
		return self.api.matches().get(match_id)
	
	def _get_telemetry(self, match_id):
		return self.api.telemetry(self._get_match(match_id).assets[0].url)
		
	def _convert_timestamp(self, s):
		# return datetime.strptime(s, "%Y-%m-%dT%H:%M:%SZ")
		return datetime.strptime(s, "%Y-%m-%dT%H:%M:%S.%fZ")
	
	def _get_events(self, match_id, event_type):
		telemetry = self._get_telemetry(match_id)
		return telemetry.events_from_type(event_type)

	def get_player_kill_events(self, match_id):
		events = self._get_events(match_id, 'LogPlayerKill')
		return events
	
	def get_player_attack_events(self, match_id):
		return self._get_events(match_id, 'LogPlayerAttack')


	def get_player_attack_df(self, match_id):
		events = self.get_player_attack_events(match_id)

		attack_points_header = ["timestamp", "attack_id", "attacker_name", "attack_type", "weapon_vehicle"]
		attack_points = []

		for attack in events:
			
			if attack.weapon.name != "Undefined":
				attack_point = [
					self._convert_timestamp(attack.timestamp),
					attack.attack_id,
					attack.attacker.name,
					attack.attack_type,
					attack.weapon.name
				]

				attack_points.append(attack_point)
				
			if attack.vehicle.name != "Undefined":

				attack_point = [
					self._convert_timestamp(attack.timestamp),
					attack.attack_id,
					attack.attacker.name,
					attack.attack_type,
					attack.vehicle.name
				]
				
				attack_points.append(attack_point)
				

		return pd.DataFrame(attack_points, columns=attack_points_header)
	
	def plot_weapon_dmg(self, match_id):
		df = self.get_player_attack_df(match_id)

		weapon_dmg_counts = Counter(df.weapon_vehicle)

		data = [go.Bar(
			x=list(weapon_dmg_counts.keys()),
			y=[weapon_dmg_counts[k] for k in weapon_dmg_counts]
		)]

		url = py.plot(data, filename='basic-bar')
		url = url.replace('~', '%7E')  # discord embed fails with tilde in url: reported bug.
		return '{}.jpeg'.format(url)

	

	

if __name__ in "__main__":
	pass