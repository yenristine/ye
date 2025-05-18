# Given a matrix of integers (positive and negative numbers, and 0s), find the submatrix with the largest sum
# return the max sum, with left-top and right-bottom indices
# Example:
# [[-10, -2, -5, 1], 
#  [-4, 4, -2, 1],
#  [3, 10, 9, 3], 
#  [-8, -10, 2, -7]]
# (25, [((1,1),(2,3)), ((2,0),(2,3))])

class Solution:
    def SubMatSumMax1(self, A): # brute force, time O((mn)**3), space O(1)
        m, n = len(A), len(A[0])
        maxs = -float('inf')
        r = []
        for i in range(m):  # start of submatrix row
            for j in range(n):  # start of submatrix col
                for x in range(i,m):  # end of submatrix row
                    for y in range(j,n):  # end of submatrix col
                        # each submatrix takes time O(n*m)
                        subsum = sum([sum(A[k][j:y+1]) for k in range(i,x+1)])
                        if subsum>maxs:
                            maxs = subsum
                            r = [(i,j,x,y)]
                        elif subsum==maxs:
                            r.append((i,j,x,y))
        return maxs, r

    def SubMatSumMax2(self, A): # prefix sum, time O((mn)**2), space O(mn)
        m, n = len(A), len(A[0])
        maxs = -float('inf')
        r = []
        p = [[0]*n for _ in range(m)] # p[x][y] = prefix sum (0,0)~(x,y)-th row/col
        for x in range(m):  # end of submatrix row
            for y in range(n):  # end of submatrix col
                p[x][y] = (p[x][y-1] if y>0 else 0) +(p[x-1][y] if x>0 else 0) -(p[x-1][y-1] if x>0 and y>0 else 0) +A[x][y]
                for i in range(x+1):  # start of submatrix row
                    for j in range(y+1):  # start of submatrix col
                        subsum = p[x][y] -(p[x][j-1] if j>0 else 0) -(p[i-1][y] if i>0 else 0) +(p[i-1][j-1] if i>0 and j>0 else 0)
                        if subsum > maxs:
                            maxs = subsum
                            r = [(i,j,x,y)]
                        elif subsum==maxs:
                            r.append((i,j,x,y))
        return maxs, r

    def SubMatSumMax3(self, A): # time O(m**2 *n), space O(mn)
        # flatten each submatrix A[i~x,:] to arr, then need to find max subarr sum
        # then need to calc prefix sum from A[i~x][y] for each col y, = ps of A[i~x-1][y] +A[x][y]
        m, n = len(A), len(A[0])
        maxs = -float('inf')
        r = []
        for i in range(m):  # start of submatrix row
            colsum = [0]*n # array for flattened A[i~x,:], prefix sum of row i~x in each col
            for x in range(i,m):  # end of submatrix row
                # get max sum of subarray of colsum starting from each i-th row
                subsum = 0 # prefix sum of subarray of flattened A[i~x,:] up to each col y (including y)
                left = [] # left cols of the submatrix with max sum
                for y in range(n): # flatten A[i:x,:] by summing up each col
                    colsum[y] += A[x][y]
                    if subsum >0:
                        subsum += colsum[y]
                    else:
                        if subsum==0: # y can be another left col
                            left.append(y)
                        else: # new left cols
                            left = [y]
                        subsum = colsum[y]

                    if subsum > maxs:
                        maxs = subsum
                        r = [(i,j,x,y) for j in left]
                    elif subsum==maxs:
                        for j in left:
                            r.append((i,j,x,y))
        return maxs, r

# TEST:
sol = Solution()
import random, time
num_test = 10
for _ in range(num_test):
    m, n = random.randint(1,100), random.randint(1,100)
    A = [[0]*n for _ in range(m)]
    for i in range(m):
        for j in range(n):
            A[i][j] = random.randint(-10**8, 10**8)

    ts1 = time.time()
    ans1 = sol.SubMatSumMax1(A)
    te1 = time.time()
    ans1[1].sort()

    ts2 = time.time()
    ans2 = sol.SubMatSumMax2(A)
    te2 = time.time()
    ans2[1].sort()

    ts3 = time.time()
    ans3 = sol.SubMatSumMax3(A)
    te3 = time.time()
    ans3[1].sort()

    if te2==ts2:
        print('%d rows %d cols, Sol1 %f, Sol2 %f, Sol3 %f'
              % (n, m, te1-ts1, te2-ts2, te3-ts3))
    elif te3==ts3:
        print('%d rows %d cols, Sol1 %f, Sol2 %f (%.2f quicker), Sol3 %f'
              % (n, m, te1-ts1, te2-ts2, (te1-ts1)/(te2-ts2), te3-ts3))
    else:
        print('%d rows %d cols, Sol1 %f, Sol2 %f (%.2f quicker), Sol3 %f (%.2f quicker)'
              % (n, m, te1-ts1, te2-ts2, (te1-ts1)/(te2-ts2), te3-ts3, (te1-ts1)/(te3-ts3)))
    
    if ans1!=ans2 or ans1!=ans3 or ans2!=ans3:
        print(A)
        print(ans1)
        print(ans2)
        print(ans3)
