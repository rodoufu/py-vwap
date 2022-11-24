from moving_list import CachedCircularMovingList, MovingList


class VolumeWeightedAveragePrice(object):
	def __init__(
			self, size: int, numerator: MovingList = None, denominator: MovingList = None,
	):
		self.numerator = numerator or CachedCircularMovingList(size)
		self.denominator = denominator or CachedCircularMovingList(size)

	def update(self, price: float, quantity: float):
		"""
		Updates the VWAP with a new price and quantity.
		O(1) when using CachedCircularMovingList which is also O(1) for update.
		The formula is basically:
		VWAP = \frac{\sum_j{P_j . Q_j}}{\sum_j{Q_j}}
		:param price: The price P.
		:param quantity: The quantity Q.
		"""
		self.numerator.update(price * quantity)
		self.denominator.update(quantity)

	def value(self) -> float:
		"""
		Gets the current value for VWAP.
		O(1) when using CachedCircularMovingList which is also O(1) for sum.
		:return: Current VWAP.
		"""
		return self.numerator.sum() / self.denominator.sum()
