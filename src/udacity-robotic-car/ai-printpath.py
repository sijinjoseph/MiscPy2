# ----------
# User Instructions:
#
# Modify the the search function so that it returns
# a shortest path as follows:
# 
# [['>', 'v', ' ', ' ', ' ', ' '],
#  [' ', '>', '>', '>', '>', 'v'],
#  [' ', ' ', ' ', ' ', ' ', 'v'],
#  [' ', ' ', ' ', ' ', ' ', 'v'],
#  [' ', ' ', ' ', ' ', ' ', '*']]
#
# Where '>', '<', '^', and 'v' refer to right, left, 
# up, and down motions. NOTE: the 'v' should be 
# lowercase.
#
# Your function should be able to do this for any
# provided grid, not just the sample grid below.
# ----------


# Sample Test case
grid = [[0, 0, 1, 0, 0, 0],
        [0, 0, 0, 0, 0, 0],
        [0, 0, 1, 0, 1, 0],
        [0, 0, 1, 0, 1, 0],
        [0, 0, 1, 0, 1, 0]]

init = [0, 0]
goal = [len(grid)-1, len(grid[0])-1]

delta = [[-1, 0 ], # go up
         [ 0, -1], # go left
         [ 1, 0 ], # go down
         [ 0, 1 ]] # go right

inv_delta = [[ 1,  0], # go down
             [ 0,  1], # go right
             [-1,  0], # go up
             [ 0, -1]] # go left
         
delta_name = ['^', '<', 'v', '>']

cost = 1

# ----------------------------------------
# modify code below
# ----------------------------------------

def search():
    closed = [[0 for row in range(len(grid[0]))] for col in range(len(grid))]
    closed[init[0]][init[1]] = 1
    expand = [[-1 for row in range(len(grid[0]))] for col in range(len(grid))]
    path = [[' ' for row in range(len(grid[0]))] for col in range(len(grid))]
    
    x = init[0]
    y = init[1]
    g = 0

    open = [[g, x, y]]

    found = False  # flag that is set when search is complete
    resign = False # flag set if we can't find expand
    nExpansions = 0
    
    while not found and not resign:
        if len(open) == 0:
            resign = True
            return 'fail'
        else:
            open.sort()
            open.reverse()
            next = open.pop()
            x = next[1]
            y = next[2]
            g = next[0]
            expand[x][y] = nExpansions
            nExpansions += 1
            
            if x == goal[0] and y == goal[1]:
                found = True
            else:
                for i in range(len(delta)):
                    x2 = x + delta[i][0]
                    y2 = y + delta[i][1]
                    if x2 >= 0 and x2 < len(grid) and y2 >=0 and y2 < len(grid[0]):
                        if closed[x2][y2] == 0 and grid[x2][y2] == 0:
                            g2 = g + cost
                            open.append([g2, x2, y2])
                            closed[x2][y2] = 1
    for i in range(len(expand)):
        print expand[i]
    
    path[goal[0]][goal[1]] = '*'
    cx = goal[0]
    cy = goal[1]
    while True:    
        min_expand = 10000000
        min_expand_index = -1
        for mi in range(len(inv_delta)):
            move = inv_delta[mi]
            nx = cx + move[0]
            ny = cy + move[1]
            
            if nx >= 0 and nx < len(grid) and ny >=0 and ny < len(grid[0]) and expand[nx][ny] != -1 and expand[nx][ny] < min_expand and path[nx][nx] == ' ':
                min_expand = expand[nx][ny]
                min_expand_index = mi
        
        if min_expand_index == -1:
            return 'fail'
            
        cx += inv_delta[min_expand_index][0]
        cy += inv_delta[min_expand_index][1]
        path[cx][cy] = delta_name[min_expand_index]
        
        if cx == init[0] and cy == init[1]:
            for i in range(len(path)):
                print path[i]
            return path

search()