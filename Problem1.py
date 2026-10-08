# Problem1: Number Confused(https://leetcode.com/problems/confusing-number-ii/)
# Time Complexity: O(5^k), where k = number of digits in n. At each digit position we can pick one of 5 digits (0, 1, 6, 8, 9),so at most 5^k numbers are built.
# Space Complexity: O(k),Only the recursion stack uses extra memory. The deepest path adds one digit per call, so it is k calls deep.
# Approach:
# Only numbers made of the digits 0, 1, 6, 8, 9 can be confusing, because every other digit becomes invalid when rotated.
# So we do NOT check every number from 1 to n. We BUILD only the valid-digit numbers using DFS, one digit at a time.
# Start from 0 and add a digit at the end: 0 -> 1 -> 10, 11, 16, 18, 19 ...
# For each built number, check if it is confusing (rotated number != original).If yes, count it.
# Stop going deeper when the number becomes bigger than n, because adding more digits only makes it bigger.

class Solution:
    def __init__(self):
        # Rotation table: key = digit, value = what it becomes after 180 degree rotation.
        # Also used as the list of allowed digits to build numbers with.
        self.map = {0: 0, 1: 1, 6: 9, 8: 8, 9: 6}

        # Score counter: how many confusing numbers we found so far.
        self.count = 0

    def confusingNumberII(self, n: int) -> int:
        # Reset the score, so repeated calls do not add up.
        self.count = 0

        # Start building numbers from 0. dfs updates self.count as it goes.
        self.dfs(0, n)

        # After dfs finishes everything, count holds the final answer.
        return self.count

    def dfs(self, curr_num: int, n: int):
        # curr_num = the number built so far (our current position in the tree).

        # Step 1: check the number we are standing on.
        # If its rotated version is different, it is a confusing number, so score +1.
        # (For curr_num = 0 this is False, so the starting 0 is never counted.)
        if self.isconfusing(curr_num):
            self.count += 1

        # Step 2: try to extend this number by one more digit at the end.
        # Loop goes over the keys of the map: 0, 1, 6, 8, 9.
        for key in self.map:
            # Add the digit at the end. Example: curr_num = 1, key = 6 -> 16.
            new_num = curr_num * 10 + key

            # new_num != 0: from 0, adding digit 0 gives 0 again, which would
            #               recurse forever. So skip it.
            # new_num <= n: if it is already bigger than n, do not go deeper,
            #               since adding more digits only makes it bigger.
            if new_num != 0 and new_num <= n:
                # Go one level deeper. The new number gets checked and extended too.
                self.dfs(new_num, n)

    def isconfusing(self, num: int) -> bool:
        # Rotates num by 180 degrees and tells if the result is different.

        # Save the original, because num will be reduced to 0 in the loop below.
        temp = num

        # Will hold the rotated number, built digit by digit.
        result = 0

        # Repeat until all digits are used up.
        while num > 0:
            # Take the last digit. Example: 16 % 10 = 6.
            last_digit = num % 10

            # Rotate that digit using the map and attach it at the END of result.
            # Reading digits from right to left and appending is what reverses
            # the order, just like turning the number upside down.
            # Example for 16: result = 0*10 + 9 = 9, then 9*10 + 1 = 91.
            result = result * 10 + self.map[last_digit]

            # Remove the last digit, so the next round sees the next digit.
            # Example: 16 // 10 = 1.
            num = num // 10

        # True if rotated number differs from the original (confusing).
        # Example: 16 -> 91 is True, 11 -> 11 is False.
        return result != temp