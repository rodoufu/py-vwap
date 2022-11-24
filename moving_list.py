from typing import List, NoReturn


class MovingList(object):
	def __init__(self, size: int):
		"""
		Creates the MovingList.
		:param size: The fixed size.
		"""
		self.size = size
		if size < 0:
			raise IndexError(f"The size cannot be negative")
		self.values: List[int] = []

	def update(self, value: float) -> NoReturn:
		"""
		Adds a new value to the list.
		:param value: Value to be added.
		"""
		pass

	def sum(self) -> float:
		"""
		:return: The sum of all items in the list.
		"""
		pass

	def __repr__(self):
		"""
		Only used for debug.
		:return: The string representation of the list.
		"""
		return f"[{','.join(map(str, self.values))}]"


class SimpleMovingList(MovingList):
	"""
	Simple implementation, it can re-allocate memory on updates, and sums all the values every time.
	"""
	def __init__(self, size: int):
		super().__init__(size)
		self.values: List[float] = []

	def update(self, value: float):
		"""
		O(n)
		"""
		self.values.append(value)
		if len(self.values) > self.size:
			self.values = self.values[1:]

	def sum(self) -> float:
		"""
		O(n)
		"""
		return sum(self.values)


class CachedMovingList(SimpleMovingList):
	"""
	Caches the sum value so it does not need to add everyone.
	"""
	def __init__(self, size: int):
		super().__init__(size)
		self.sum_so_far = 0

	def update(self, value: float):
		"""
		O(n)
		"""
		self.values.append(value)
		self.sum_so_far += value
		if len(self.values) > self.size:
			self.sum_so_far -= self.values[0]
			self.values = self.values[1:]

	def sum(self) -> float:
		"""
		O(1)
		"""
		return self.sum_so_far


class CachedCircularMovingList(MovingList):
	"""
	Keeps a circular moving list, so it does not need to allocate new memory every time it is updated.
	It could also be implemented with a linked list.
	"""
	def __init__(self, size: int):
		super().__init__(size)
		self.values: List[float] = [0.0] * self.size
		self.sum_so_far = 0
		self.oldest: int = 0

	def update(self, value: float):
		"""
		O(1)
		"""
		self.sum_so_far -= self.values[self.oldest]
		self.sum_so_far += value
		self.values[self.oldest] = value
		self.oldest = (self.oldest + 1) % self.size

	def sum(self) -> float:
		"""
		O(1)
		"""
		return self.sum_so_far
