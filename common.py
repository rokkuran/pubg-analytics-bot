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

import numpy as np
import pandas as pd

import plotly
plotly.tools.set_credentials_file(username='rokkuran', api_key=os.environ['PLOTLY_API_KEY'])
import plotly.plotly as py
import plotly.graph_objs as go
# import cmocean

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

	def get_player_matches(self, username):
		players = self.get_players(username)
		return players[0].matches
	
	def get_player_match_ids(self, username):
		return [x.id for x in self.get_player_matches(username)]
	
	def get_player_nth_match_id(self, username, n):
		return self.get_player_match_ids(username)[int(n)]

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
	
	def plot_test(self, N):
		random_x = np.linspace(0, 1, N)
		random_y = np.random.randn(N)

		# Create a trace
		trace = go.Scatter(
			x = random_x,
			y = random_y
		)

		data = [trace]

		url = py.plot(data, filename='basic-line')
		url = url.replace('~', '%7E')  # discord embed fails with tilde in url: reported bug.
		return '{}.jpeg'.format(url)

	def plot_weapon_dmg(self, match_id):
		df = self.get_player_attack_df(match_id)

		weapon_dmg_counts = Counter(df.weapon_vehicle)
		y = [weapon_dmg_counts[k] for k in weapon_dmg_counts]

		data = [go.Bar(
			x=list(weapon_dmg_counts.keys()),
			y=y,
			marker=dict(
				cmin=0,
				cmax=max(y),
				color=y,
				colorscale="Viridis",
				reversescale=True
			)
		)]

		layout = go.Layout(
			title='Match Damage Breakdown',
			xaxis=dict(
		#         title='Weapon/Vehicle',
				titlefont=dict(
					size=14,
				),
				showline=True,
				mirror='ticks',
				zerolinewidth=1,
				linewidth=1,
				linecolor='lightgrey',
				tickangle=90,
			),
			yaxis=dict(
				title='Damage',
				titlefont=dict(
					size=14,
				),
				showline=True,
				mirror='ticks',
				zerolinewidth=1,
				linecolor='lightgrey',
				linewidth=1,
			),
			autosize=False,
			width=1000,
			height=600,
			margin=dict(
				l=60,
				r=50,
				b=120,
				t=50,
				pad=0
			),
		)

		fig = go.Figure(data=data, layout=layout)
		url = py.plot(fig, filename='plot_weapon_dmg_{}'.format(match_id))

		return fix_plot_url(url)

	def plot_all_weapon_dmg_for_user_match(self, username, n):
		return self.plot_weapon_dmg(self.get_player_nth_match_id(username, n))


class Transform(Query):
	""""""
	def __init__(self):
		Query.__init__(self)

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





def fix_plot_url(url):
	"""
	Discord embed fails with tilde (~) in url, hence replacement. 
	This is a reported bug.
	"""
	return '{}.jpeg'.format(url.replace('~', '%7E'))



if __name__ in "__main__":
	pass