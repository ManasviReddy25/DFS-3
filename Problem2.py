# Problem2: Matchsticks to Square (https://leetcode.com/problems/matchsticks-to-square/)
# Time Complexity: O(4^n),n is the number of sticks. Each stick can go into up to 4 sides, so in the worst case we try 4 choices for each of the n sticks. Sorting costs O(n log n), but that is small compared to 4^n.
# Space Complexity: O(n),The recursion goes as deep as the number of sticks (one call per stick). The square list has a fixed size of 4, so it is O(1).
# Approach:
# Add up all sticks. If the total is not divisible by 4, a square is impossible.
# The target length of one side is total // 4. If any stick is longer than one side, it can never fit, so return False.
# Sort sticks from big to small, so big sticks fail early and we skip bad paths fast.
# Keep 4 buckets (the 4 sides). For each stick, try placing it in each bucket if it does not go over the target.
# Place the stick, move to the next stick. If that fails, remove the stick (backtrack) and try the next bucket.
# If all sticks are placed, every side equals the target, so return True.

class Solution:
    def makesquare(self, matchsticks: list[int]) -> bool:
        sum = 0                      # total length of all sticks
        max_length = 0               # longest single stick

        for i in matchsticks:
            sum += i                 # add each stick to the total
            max_length = max(max_length, i)   # keep track of the longest stick
        
        length_of_each_side = sum // 4   # target length for one side

        if sum % 4 != 0:             # total cannot be split into 4 equal parts
            return False
        if max_length > length_of_each_side:   # longest stick cannot fit in any side
            return False
        
        matchsticks.sort()           # sort small to big
        matchsticks.reverse()        # now big to small, so hard sticks are placed first

        square = [0] * 4             # current length of each of the 4 sides

        def helper(index):           # tries to place the stick at position index
            if index == len(matchsticks):   # all sticks are placed
                return True          # no side went over the target, so all sides are equal
            
            for i in range(4):       # try each of the 4 sides for this stick
                if square[i] + matchsticks[index] <= length_of_each_side:   # only place if it does not overflow
                    square[i] += matchsticks[index]    # place the stick on side i
                    if helper(index + 1):              # try to place the next stick
                        return True                    # everything worked, pass True up
                    square[i] -= matchsticks[index]    # next sticks failed, so remove it (backtrack)
            return False             # this stick fits nowhere, so go back and change an earlier choice
        return helper(0)             # start with the first stick