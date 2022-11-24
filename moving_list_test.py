import unittest
import random
from typing import List

from moving_list import MovingList, CachedCircularMovingList, CachedMovingList, SimpleMovingList


class MovingListTest(unittest.TestCase):
	def test_all_lists(self):
		size = 10
		moving_lists: List[MovingList] = [
			SimpleMovingList(size),
			CachedMovingList(size),
			CachedCircularMovingList(size),
		]

		values = range(1, 11)
		for moving_list in moving_lists:
			for value in values:
				moving_list.update(value)

		for moving_list in moving_lists:
			self.assertAlmostEqual(moving_list.sum(), sum(values), 3)

		values = range(1, 101)
		for moving_list in moving_lists:
			for value in values:
				moving_list.update(value)

		sum_of_lists = [x.sum() for x in moving_lists]
		for i in range(len(moving_lists) - 1):
			self.assertAlmostEqual(sum_of_lists[i], sum_of_lists[i + 1], 3)

	def test_random_lists(self):
		size = 10
		moving_lists: List[MovingList] = [
			SimpleMovingList(size),
			CachedMovingList(size),
			CachedCircularMovingList(size),
		]

		population = range(1_000_000)
		values = random.sample(population, 10)
		for moving_list in moving_lists:
			for value in values:
				moving_list.update(value)

		for moving_list in moving_lists:
			self.assertAlmostEqual(moving_list.sum(), sum(values), 3)

		values = random.sample(population, 100)
		for moving_list in moving_lists:
			for value in values:
				moving_list.update(value)

		sum_of_lists = [x.sum() for x in moving_lists]
		for i in range(len(moving_lists) - 1):
			self.assertAlmostEqual(sum_of_lists[i], sum_of_lists[i + 1], 3)


if __name__ == '__main__':
	unittest.main()
