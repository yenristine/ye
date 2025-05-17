class Solution:
    def knapsackRep(self, sacks, maxWeight): # sacks = list of [weight, value]
        # allows repetitions of each sack, of a weight and a value
        # dp[i] = max(dp[i], dp[i-wj]+vj), value with weight i allowed
        # wj and vj are weight and value of j-th sack
		
        # base: dp[0] = 0
        # TC O(n*maxWeight), SC O(maxWeight)
        dp = [0]*(1+maxWeight)
        for i in range(1, maxWeight+1):
            for w,v in sacks:
                if w <= i:
                    dp[i] = max(dp[i], dp[i-w] +v)
        return dp[-1]

    def knapsackNoRep(self, sacks, maxWeight): # sacks = list of [weight, value]
        # NO repetitions allowed, only ONE of each sack, of a weight and a value
        # dp[i][j] = max(d[i][j], dp[i-w[j-1] ][j-1] + v[j-1]), with weight i allowed and j sacks
		
        # base: dp[0][j] = dp[i][0] = 0
        # init dp[i][j] = dp[i][j-1] # as same weight allowed but one less sack
        # TC/SC O(n*maxWeight)
        n = len(sacks)
        dp = [[0]*(n+1) for _ in range(maxWeight+1)]
        for i in range(1, maxWeight+1):
            for j in range(1,n+1):
                dp[i][j] = dp[i][j-1]
				w, v = sacks[j-1]
                if w <= i:
                    dp[i][j] = max(dp[i][j], dp[i-w][j-1] +v)
        return dp[-1][-1]

sol = Solution()
maxWeight = 10
sacks = [[6,30], [3,14], [4,16], [2,9]]
print(sol.knapsackRep(sacks, maxWeight))
print(sol.knapsackNoRep(sacks, maxWeight))
