import asyncio
from typing import Dict

from matches import CoinbaseProMatchesProvider
from vwap import VolumeWeightedAveragePrice


async def main():
	pairs = [
		"BTC-USD",
		"ETH-USD",
		"ETH-BTC",
	]
	vwaps: Dict[str, VolumeWeightedAveragePrice] = {
		pair: VolumeWeightedAveragePrice(200) for pair in pairs
	}
	async with CoinbaseProMatchesProvider(pairs=pairs) as matches_provider:
		async for match in matches_provider.matches():
			vwap = vwaps.get(match.pair)
			if vwap:
				vwap.update(match.price, match.quantity)
				print(f"VWAP for {match.pair}:{vwap.value()}")
			else:
				print(f"Unexpected pair: {match.pair}")


if __name__ == '__main__':
	asyncio.run(main())
