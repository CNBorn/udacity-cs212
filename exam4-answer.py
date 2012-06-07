"""
UNIT 4: Search

Your task is to maneuver a car in a crowded parking lot. This is a kind of 
puzzle, which can be represented with a diagram like this:

| | | | | | | |  
| G G . . . Y |  
| P . . B . Y | 
| P * * B . Y @ 
| P . . B . . |  
| O . . . A A |  
| O . S S S . |  
| | | | | | | | 

A '|' represents a wall around the parking lot, a '.' represents an empty square,
and a letter or asterisk represents a car.  '@' marks a goal square.
Note that there are long (3 spot) and short (2 spot) cars.
Your task is to get the car that is represented by '**' out of the parking lot
(on to a goal square).  Cars can move only in the direction they are pointing.  
In this diagram, the cars GG, AA, SSS, and ** are pointed right-left,
so they can move any number of squares right or left, as long as they don't
bump into another car or wall.  In this diagram, GG could move 1, 2, or 3 spots
to the right; AA could move 1, 2, or 3 spots to the left, and ** cannot move 
at all. In the up-down direction, BBB can move one up or down, YYY can move 
one down, and PPP and OO cannot move.

You should solve this puzzle (and ones like it) using search.  You will be 
given an initial state like this diagram and a goal location for the ** car;
in this puzzle the goal is the '.' empty spot in the wall on the right side.
You should return a path -- an alternation of states and actions -- that leads
to a state where the car overlaps the goal.

An action is a move by one car in one direction (by any number of spaces).  
For example, here is a successor state where the AA car moves 3 to the left:

| | | | | | | |  
| G G . . . Y |  
| P . . B . Y | 
| P * * B . Y @ 
| P . . B . . |  
| O A A . . . |  
| O . . . . . |  
| | | | | | | | 

And then after BBB moves 2 down and YYY moves 3 down, we can solve the puzzle
by moving ** 4 spaces to the right:

| | | | | | | |
| G G . . . . |
| P . . . . . |
| P . . . . * *
| P . . B . Y |
| O A A B . Y |
| O . . B . Y |
| | | | | | | |

You will write the function

    solve_parking_puzzle(start, N=N)

where 'start' is the initial state of the puzzle and 'N' is the length of a side
of the square that encloses the pieces (including the walls, so N=8 here).

We will represent the grid with integer indexes. Here we see the 
non-wall index numbers (with the goal at index 31):

 |  |  |  |  |  |  |  |
 |  9 10 11 12 13 14  |
 | 17 18 19 20 21 22  |
 | 25 26 27 28 29 30 31
 | 33 34 35 36 37 38  |
 | 41 42 43 44 45 46  |
 | 49 50 51 52 53 54  |
 |  |  |  |  |  |  |  |

The wall in the upper left has index 0 and the one in the lower right has 63.
We represent a state of the problem with one big tuple of (object, locations)
pairs, where each pair is a tuple and the locations are a tuple.  Here is the
initial state for the problem above in this format:
"""

puzzle1 = (
 ('@', (31,)),
 ('*', (26, 27)), 
 ('G', (9, 10)),
 ('Y', (14, 22, 30)), 
 ('P', (17, 25, 33)), 
 ('O', (41, 49)), 
 ('B', (20, 28, 36)), 
 ('A', (45, 46)), 
 ('|', (0, 1, 2, 3, 4, 5, 6, 7, 8, 15, 16, 23, 24, 32, 39,
        40, 47, 48, 55, 56, 57, 58, 59, 60, 61, 62, 63)))

# A solution to this puzzle is as follows:

#     path = solve_parking_puzzle(puzzle1, N=8)
#     path_actions(path) == [('A', -3), ('B', 16), ('Y', 24), ('*', 4)]

# That is, move car 'A' 3 spaces left, then 'B' 2 down, then 'Y' 3 down, 
# and finally '*' moves 4 spaces right to the goal.

# Your task is to define solve_parking_puzzle:

N = 8

def solve_parking_puzzle(start, N=N):
    """Solve the puzzle described by the starting position (a tuple 
    of (object, locations) pairs).  Return a path of [state, action, ...]
    alternating items; an action is a pair (object, distance_moved),
    such as ('B', 16) to move 'B' two squares down on the N=8 grid."""
    return shortest_path_search(start, psuccessors, is_goal)

def psuccessors(state):
    from copy import deepcopy
    import itertools

    cars = {}
    walls = []
    cars_pos = []
    other_car_pos = {}
    for item_name, item_pos in state:
        if item_name not in ["@", "|"]:
            cars.setdefault(item_name, item_pos)
            cars_pos.extend(item_pos)
        if item_name == "|":
            walls.extend(item_pos)

    for car_name, _ in state:
        if car_name not in ["@", "|"]:
            other_car_pos.setdefault(car_name, [pos for pos in cars_pos if (pos not in cars[car_name] and pos not in walls)])
    #print cars

    def distant_to_boarder(car, one_direction_step):
        find_boarder = False
        current_pos = cars[car]
        
        if one_direction_step == 1:
            length_tweak = len(cars[car]) - 1
        else:
            length_tweak = 0

        if abs(one_direction_step) not in (1, N):
            raise

        if abs(one_direction_step) == N:
            v_find = True
        else:
            v_find = False

        if not v_find:
            start_pos = cars[car][0]
            while not find_boarder:
                start_pos += one_direction_step
                if start_pos in walls or start_pos in other_car_pos[car]:
                    find_boarder = True
            return start_pos - cars[car][0] - length_tweak - 1
        else:
            #vertical find
            results = []
            for pos in current_pos:
                v_pos = pos
                while not find_boarder:
                    v_pos += one_direction_step
                    if v_pos in walls or v_pos in other_car_pos[car]:
                        find_boarder = True
                results.append(v_pos - pos)
            return min(results)

    def has_clear_path_direction(car, one_direction, abs_step):

        near_by_grid_is_blocked = any((pos+(one_direction*abs_step) in walls or pos+(one_direction*abs_step) in other_car_pos[car] for pos in cars[car]))
        if near_by_grid_is_blocked:
            return False

        return True

        origin_car_pos = cars[car]
        if one_direction < 0:
            step = 0-abs_step
        else:
            step = abs_step

        #should not be one_direction+step, one_direction+step only searchs next grid
        other_car_in_the_path = any(((pos+grid) in other_car_pos[car] or (pos+grid) in walls for grid in xrange(0, distant_to_boarder(car, step), step) for pos in origin_car_pos[:1]))
        #other_car_in_the_path = any(((pos+grid) in other_car_pos[car] or (pos+grid) in walls for grid in xrange(0, one_direction+step, step) for pos in origin_car_pos[:1]))
        if other_car_in_the_path:
            return False
        return True

    def has_clear_path(car, move):
        #other_cars_pos = [pos for pos in cars_pos if (pos not in cars[car] or pos in walls)] #bottle neck?

        origin_car_pos = cars[car]
        one_direction = get_car_action(car, move)

        if one_direction % N == 0:
            step_unit = 8
        else:
            step_unit = 1
        if one_direction < 0:
            step = 0-step_unit
        else:
            step = step_unit

        other_car_in_the_path = any(((pos+grid) in other_car_pos[car] or (pos+grid) in walls for grid in xrange(0, one_direction+step, step) for pos in origin_car_pos[:1]))
        if other_car_in_the_path:
            return False

        return True

    def legible(car, move):
        if not has_clear_path(car, move):
            return False
        return True

    def get_car_action(car_name, moved_pos):
        origin_pos = cars[car_name]
        return moved_pos[0] - origin_pos[0]

    state_action_pair = {}

    #print distant_to_boarder("A", 1)
    #print distant_to_boarder("A", -8)
    
    for car, car_pos in cars.iteritems():

        #Only +-(N-car_pos) - 2, +-N*(N-1)
        h_directions = [d for d in [1,-1] if has_clear_path_direction(car, d, 1)]
        v_directions = [d for d in [1, -1] if has_clear_path_direction(car, d, N)]
        
        steps = [i*direction for i in range(1,N-1) for direction in h_directions if not any((p+(i*direction) in other_car_pos[car] or p+(i*direction) in walls for p in car_pos))]

        step_v = [i*direction for i in range(N, N*(N-1-2), N) for direction in v_directions if not any((p+(i*direction) in other_car_pos[car] or p+(i*direction) in walls for p in car_pos))]

        def filter_out_unconsective_steps(steps, n_step):

            results = []

            positive_steps = [s for s in steps if s > 0]
            if positive_steps:
                perfect_positive_steps = range(min(positive_steps), max(positive_steps), n_step)
                positive_break_points = set(positive_steps) ^ set(perfect_positive_steps)
                positive_break_point = min(positive_break_points)
                if positive_break_point:
                    results.extend([s for s in positive_steps if s < positive_break_point])
                else:
                    results.extend(positive_steps)
 

            negative_steps = [s for s in steps if s < 0]

            if negative_steps:
                perfect_negative_steps = range(max(negative_steps), min(negative_steps)-n_step, 0-n_step)
                
                negative_break_points = set(negative_steps) ^ set(perfect_negative_steps)

                if negative_break_points:
                    negative_break_point = min(negative_break_points)
                    results.extend([s for s in negative_steps if s < negative_break_point])
                else:
                    results.extend(negative_steps)
            return results

        #print car
        #print "+", filter_out_unconsective_steps(steps, 1)
        #print "v", filter_out_unconsective_steps(step_v, N)

        steps_r = steps + step_v
        #steps1 = filter_out_unconsective_steps(steps, 1) + filter_out_unconsective_steps(step_v, N)
        #print car, steps_r, steps1
        #exit(1)

        step_moved_pos = [tuple(((p + s) for p in car_pos if p+s not in other_car_pos[car] and p+s not in walls)) for s in steps_r]
        step_moved_pos = [s for s in step_moved_pos if s and len(s) == len(car_pos)]
        #filtered out all illegible destination pos
        
        #if car == "Y":
        #    print "car %s step_moved_pos" % car, step_moved_pos
        fesible_step_moved_pos = [move for move in step_moved_pos if legible(car, move)]
        #if car == "Y":
        #    print "car %s" % car, fesible_step_moved_pos

        def get_new_state_with_car_move(car_name, moved_pos):
            ret_state = list(state)
            ret = []
            for s_car_name, pos in ret_state:
                if s_car_name != car_name:
                    ret.append((s_car_name, pos))
                else:
                    ret.append((car_name, moved_pos)) 
            return tuple(ret)

        #return {state:action} pair
        for step in set(fesible_step_moved_pos):
            state_action_pair.setdefault(get_new_state_with_car_move(car, step), (car, get_car_action(car, step)))
        
    return state_action_pair


# But it would also be nice to have a simpler format to describe puzzles,
# and a way to visualize states.
# You will do that by defining the following two functions:

def locs(start, n, incr=1):
    "Return a tuple of n locations, starting at start and incrementing by incr."
    return tuple(start+i*incr for i in range(n))

def grid(cars, N=N):
    """Return a tuple of (object, locations) pairs -- the format expected for
    this puzzle.  This function includes a wall pair, ('|', (0, ...)) to 
    indicate there are walls all around the NxN grid, except at the goal 
    location, which is the middle of the right-hand wall; there is a goal
    pair, like ('@', (31,)), to indicate this. The variable 'cars'  is a
    tuple of pairs like ('*', (26, 27)). The return result is a big tuple
    of the 'cars' pairs along with the walls and goal pairs."""
    goals = ((N**2)//2 - 1,)
    walls = (locs(0, N) + locs(N*(N-1), N) + locs(N, N-2, N) 
             + locs(2*N-1, N-2, N))
    walls = tuple(w for w in walls if w not in goals)
    return cars + (('|', walls), ('@', goals))    

def show(state, N=N):
    "Print a representation of a state as an NxN grid."
    # Initialize and fill in the board.
    board = ['.'] * N**2
    for (c, squares) in state:
        for s in squares:
            board[s] = c
    # Now print it out
    for i,s in enumerate(board):
        print s,
        if i % N == N - 1: print

# Here we see the grid and locs functions in use:

puzzle1 = grid((
    ('*', locs(26, 2)),
    ('G', locs(9, 2)),
    ('Y', locs(14, 3, N)),
    ('P', locs(17, 3, N)),
    ('O', locs(41, 2, N)),
    ('B', locs(20, 3, N)),
    ('A', locs(45, 2))))

puzzle2 = grid((
    ('@', (31,)),
    ('*', locs(26, 2)),
    ('B', locs(20, 3, N)),
    ('P', locs(33, 3)),
    ('O', locs(41, 2, N)),
    ('Y', locs(51, 3))))

puzzle3 = grid((
    ('@', (31,)),
    ('*', locs(25, 2)),
    ('B', locs(19, 3, N)),
    ('P', locs(36, 3)),
    ('O', locs(45, 2, N)),
    ('Y', locs(49, 3))))

#print puzzle1 
#print show(puzzle1)
#print psuccessors(puzzle1)

#for state, action in psuccessors(puzzle1).iteritems():
#    print state
#    print action
    
def is_goal(state):
    d = dict(state)
    return set(d['*']) & set(d['@'])


# Here are the shortest_path_search and path_actions functions from the unit.
# You may use these if you want, but you don't have to.

def shortest_path_search(start, successors, is_goal):
    """Find the shortest path from start state to a state
    such that is_goal(state) is true."""
    if is_goal(start):
        return [start]
    explored = set() # set of states we have visited
    frontier = [ [start] ] # ordered list of paths we have blazed
    while frontier:
        path = frontier.pop(0)
        s = path[-1]
        for (state, action) in successors(s).items():
            if state not in explored:
                explored.add(state)
                path2 = path + [action, state]
                if is_goal(state):
                    return path2
                else:
                    frontier.append(path2)
    return []

def path_actions(path):
    "Return a list of actions in this path."
    return path[1::2]

print path_actions(solve_parking_puzzle(puzzle1))
for r in solve_parking_puzzle(puzzle1)[::2]:
    print show(r)

print path_actions(solve_parking_puzzle(puzzle2))
for r in solve_parking_puzzle(puzzle2)[::2]:
    print show(r)

print path_actions(solve_parking_puzzle(puzzle3))
for r in solve_parking_puzzle(puzzle3)[::2]:
    print show(r)

puzzle4 = grid((
    ('*', locs(25, 2)),
    ('B', locs(19, 2, N))))

puzzle5 = grid((
    ('*', locs(25, 2)),
    ('B', locs(19, 2, N)),
    ('Y', locs(41,6))))

puzzle6 = (('@', (14,)),(('*',(11,12))), ('|', (0, 1, 2, 3, 4, 5, 9, 10, 15, 19, 20, 21, 22, 23, 24)))

print path_actions(solve_parking_puzzle(puzzle4))
for r in solve_parking_puzzle(puzzle4)[::2]:
    print show(r)

print path_actions(solve_parking_puzzle(puzzle5))
for r in solve_parking_puzzle(puzzle5)[::2]:
    print show(r)

print path_actions(solve_parking_puzzle(puzzle5))
for r in solve_parking_puzzle(puzzle5)[::2]:
    print show(r)

import cProfile
cProfile.run('solve_parking_puzzle(puzzle1)')
