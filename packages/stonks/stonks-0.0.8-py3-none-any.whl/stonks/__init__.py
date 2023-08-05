import aiohttp
import asyncio
import json

class NotLoggedIn(BaseException): pass


class User():
	__slots__ = ('username', 'display_name', 'net_worth', 'worth', 'id')
	def __init__(
		self,
		username,
		display_name,
		net_worth,
		worth,
		balance,
		id,
		avatar_url=None
	):
		self.username = username
		self.display_name = display_name
		self.net_worth = int(net_worth)
		self.worth = int(worth)
		self.id = int(id)

	def __str__(self):
		return self.display_name

	def __repr__(self):
		return self.display_name

class Leaderboard():
	def __init__(self, raw_users, total_in_circulation):
		self.total_in_circulation = total_in_circulation
		self.__raw_users = raw_users
	
	def __iter__(self):
		self.__i = -1
		return self
	
	def __next__(self):
		self.__i += 1
		user = User(**self.__raw_users[self.__i])
		if self.__i + 1 >= len(self.__raw_users):
			raise StopIteration()
		return user

	async def __anext__(self):
		return self.__next__()

	def __repr__(self):
		return '[' + ', '.join(map(str, (user for user in self))) + ']'


class Bot():
	__base_url = 'https://stonks.matdoes.dev/api'
	def __init__(self, token=None, loop=None):
		self.token = token
		if token:
			self.s = aiohttp.ClientSession(headers={
				'Authorization': token
			})
		else:
			self.s = aiohttp.ClientSession()


	async def close(self):
		await self.s.close() # close aiohttp session

	async def __request(self, path, params={}):
		r = await self.s.get(
			f'{self.__base_url}/{path}',
			params=params
		)
		json_data = json.loads(await r.text())
		if 'error' in json_data:
			raise Exception(json_data['error'])
		return json_data

	async def __request_post(self, path, params={}, data={}):
		r = await self.s.post(
			f'{self.__base_url}/{path}',
			params=params,
			data=data
		)
		json_data = json.loads(await r.text())
		if 'error' in json_data:
			raise Exception(json_data['error'])
		return json_data


	async def get_investors(self, user_id):
		json_data = await self.__request(
			f'investors/{user_id}'
		)
		return json_data

	async def get_portfolio(self, user_id):
		json_data = await self.__request(
			f'portfolio/{user_id}'
		)
		return json_data


	async def get_history(self, user_id, hours=24):
		json_data = await self.__request(
			f'history/{user_id}', 
			params={'limit': hours}
		)
		return json_data
 
	async def whoami(self):
		json_data = await self.__request('whoami')
		self.id = int(json_data['id'])
		self.display_name = json_data['display_name']
		return json_data


	async def get_leaderboard(self, limit=20):
		json_data = await self.__request(
			'leaderboard',
			params={'limit': limit}
		)
		raw_users = json_data[0]
		
		return Leaderboard(raw_users, json_data[1])
			
		# def __aiter__(self, limit=20):
		# 	json_data = await self.__request(
		# 		'leaderboard',
		# 		params={'limit': limit}
		# 	)
		# 	raw_users = json_data[0]
		# 	return Leaderboard(raw_users, json_data[1])

	async def get_average(self, user_id, hours=24):
		json_data = await self.__request(
			f'average/{user_id}',
			params={'limit': hours}
		)
		return json_data

	async def get_user(self, user_id):
		json_data = await self.__request(
			f'user/{user_id}',
		)
		return User(**json_data)

	async def buy(self, user_id, amount):
		if not self.token:
			raise NotLoggedIn('You are not logged in!')
		json_data = await self.__request_post(
			'buy',
			data={
				'user_id': user_id,
				'amount': amount
			}
		)
		return json_data

	async def sell(self, user_id, amount):
		if not self.token:
			raise NotLoggedIn('You are not logged in!')
		json_data = await self.__request_post(
			'sell',
			data={
				'user_id': user_id,
				'amount': amount
			}
		)
		return json_data

	async def get_profit(self, user_id, amount):
		if not self.token:
			raise NotLoggedIn('You are not logged in!')
		json_data = await self.__request_post(
			'profit',
			data={
				'user_id': user_id
			}
		)
		return json_data['profit_percent']
