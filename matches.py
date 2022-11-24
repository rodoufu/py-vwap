import json
from types import TracebackType
from typing import AsyncIterable, Optional, Type, List

import websockets


class Match(object):
	def __init__(self, pair: str, price: float, quantity: float):
		self.pair = pair
		self.price = price
		self.quantity = quantity


class MatchesProvider(object):
	def __init__(self):
		self.keep_running = True

	async def matches(self) -> AsyncIterable[Match]:
		pass


class CoinbaseProMatchesProvider(MatchesProvider):
	def __init__(self, pairs: List[str]):
		super().__init__()
		self.url = "wss://ws-feed.pro.coinbase.com"
		self.connect = None
		self.websocket = None
		self.pairs = pairs

	async def __aenter__(self):
		self.connect = websockets.connect(self.url)
		self.websocket = await self.connect.__aenter__()
		await self.send({
			"type": "subscribe",
			"channels": [
				{"name": "heartbeat", "product_ids": self.pairs},
				{"name": "matches", "product_ids": self.pairs},
			],
		})
		return self

	async def __aexit__(
			self,
			exc_type: Optional[Type[BaseException]],
			exc_value: Optional[BaseException],
			traceback: Optional[TracebackType],
	) -> None:
		await self.connect.__aexit__(exc_type, exc_value, traceback)

	async def send(self, message: dict):
		await self.websocket.send(json.dumps(message))

	async def matches(self) -> AsyncIterable[Match]:
		while self.keep_running:
			msg_str = await self.websocket.recv()
			msg = json.loads(msg_str)
			msg_type = msg.get('type')
			if not msg_type:
				print(f"Unexpected message: {msg_str}")
			if msg_type == 'subscriptions':
				for channel in msg.get('channels'):
					print(f"Subscribed to {channel}")
			elif msg_type == "heartbeat":
				pass
			elif msg_type in ["last_match", "match"]:
				yield Match(msg.get("product_id"), float(msg.get("price")), float(msg.get("size")))
			elif msg_type == "error":
				print(f"Error from websocket: {msg_str}")
			else:
				print(f"Unexpected message type {msg_str}")
