colors = [['red', 'green', 'green', 'red' , 'red'],
          ['red', 'red', 'green', 'red', 'red'],
          ['red', 'red', 'green', 'green', 'red'],
          ['red', 'red', 'red', 'red', 'red']]

measurements = ['green', 'green', 'green' ,'green', 'green']
motions = [[0,0],[0,1],[1,0],[1,0],[0,1]]

sensor_right = 0.7

p_move = 0.8

def show(p):
    for i in range(len(p)):
        print p[i]

#DO NOT USE IMPORT
#ENTER CODE BELOW HERE
#ANY CODE ABOVE WILL CAUSE
#HOMEWORK TO BE GRADED
#INCORRECT

def index(row, col):
    return (total_cols * row) + col

def sense(p, Z):
    q = []
    for row in range(total_rows):
        for col in range(total_cols):
            hit = (colors[row][col] == Z)
            q.append(p[index(row, col)] * ((hit * sensor_right) + ((1 - hit) * (1 - sensor_right))))
        
    #Normalize
    total_sum = sum(q)
    for k in range(total_elements):
        q[k] = q[k] / total_sum 
        
    return q

def move(p, M):
    q = []
    for row in range(total_rows):
        for col in range(total_cols):
            q.append(((1 - p_move) * p[index(row, col)]) + (p_move * p[index((row - M[0]) % total_rows, (col - M[1]) % total_cols)]))
            
    return q

total_rows = len(colors)
total_cols = len(colors[0])
total_elements = total_rows * total_cols

p = [1.0 / total_elements] * total_elements
for k in range(len(measurements)):
    p = sense(p, measurements[k])
    p = move(p, motions[k])
        
#Your probability array must be printed 
#with the following code.

show(p)