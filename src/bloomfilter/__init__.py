import bitarray
import math
import typing as t
from collections.abc import Callable

import mmh3


mmh3.hash64("1", seed=1, signed=False)


T = t.TypeVar("T")


class BloomFilter[T]:

    def __init__(self, approx_items_count: int, false_positive_rate: float) -> None:
        self.bits_count = 0
        self.hash_funcs = []

        self.calc_number_of_bits(approx_items_count, false_positive_rate)
        self.bits_array = bitarray.bitarray(self.bits_count)
        self.prepare_hash_functions(approx_items_count)

    def calc_number_of_bits(self, approx_items_count: int, false_positive_rate: float) -> None:
        self.bits_count = math.ceil(-approx_items_count * math.log(false_positive_rate) / math.log(2) ** 2)

    def prepare_hash_functions(self, approx_items_count: int) -> list[Callable[[T], int]]:
        k = math.ceil(approx_items_count / self.bits_count * math.log(2))
        for i in range(k):
            self.hash_funcs.append(
                lambda key: mmh3.hash128(str(key), seed=i, signed=False),
            )
        return self.hash_funcs

    def add(self, value: T) -> None:
        for hash_func in self.hash_funcs:
            self.bits_array[hash_func(value) % self.bits_count] = 1

    def contains(self, value: T) -> bool:
        return all(
            self.bits_array[hash_func(value) % self.bits_count] for hash_func in self.hash_funcs
        )


bf = BloomFilter[int](100, .01)



# print("adding < 50")
# for i in range(50):
#     bf.add(i)
#
# print("=="*50)
# print("checking > 50")
# for i in range(50, 100):
#     print(bf.contains(i))
#
#
# print("=="*50)
# print("checking < 50")
# for i in range(50):
#     print(bf.contains(i))


