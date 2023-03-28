"""Utility functions for Euler problems"""

from typing import List


def is_arithmetic_progression(nums: List[int], common_diff: int) -> bool:
    """An arithmetic progression sequence should have length of at least 3"""
    if common_diff == 0 or len(nums) < 3:
        return False

    prev = nums[0]
    for num in nums[1:]:
        if num - prev != common_diff:
            return False
        prev = num
    return True


def compare(x, y: int) -> int:
    return (x > y) - (x < y)
