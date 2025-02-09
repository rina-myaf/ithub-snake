import random

LEFT = 0
RIGHT = 1
UP = 2
DOWN = 3

CELL_EMPTY = 0
CELL_OPPONENT = 1

def handle_move(game_state: dict) -> dict:
    #              left right up  down
    move_chance = [100, 100, 100, 100]
    move_str = ['left', 'right', 'up', 'down']
    
    me = game_state["you"]
    my_head = me["body"][0]  
    my_neck = me["body"][1]

    my_id = None
    is_autotest = True

    if 'id' in me:
        my_id = me["id"]
        is_autotest = False

    #print('id =', game_state)

    head_x = my_head['x']
    head_y = my_head['y']
    neck_x = my_neck['x']
    neck_y = my_neck['y']

    if neck_x < head_x:  
        #print('neck no left')
        move_chance[LEFT] = 0
    elif neck_x > head_x:  
        move_chance[RIGHT] = 0
    elif neck_y > head_y:  
        move_chance[UP] = 0
    elif neck_y < head_y:  
        move_chance[DOWN] = 0

    board = game_state['board']
    board_width = board['width']
    board_height = board['height']

    my_body = game_state['you']['body']

    matrix = []
    for i in range(board_height):
        mt = []
        for j in range(board_width):
            mt.append(CELL_EMPTY)
        matrix.append(mt)

    if head_x + 1 >= board_width:
        move_chance[RIGHT] = 0
    elif head_x - 1 < 0:
        #print('board no left')
        move_chance[LEFT] = 0

    if head_y + 1 >= board_height:
        move_chance[UP] = 0
    elif head_y - 1 < 0:
        move_chance[DOWN] = 0
    
    if {'x': head_x - 1, 'y': head_y} in my_body:
        #print('my body no left')
        move_chance[LEFT] = 0
    
    if {'x': head_x + 1, 'y': head_y} in my_body:  
        move_chance[RIGHT] = 0
    
    if {'x': head_x, 'y': head_y - 1} in my_body:  
        move_chance[DOWN] = 0
    
    if {'x': head_x, 'y': head_y + 1} in my_body:  
        move_chance[UP] = 0

    opponents = game_state['board']['snakes']

    for opp in opponents:
        if is_autotest:
            if opp['name'] == 'us': continue
        else:
            if opp['id'] == my_id: continue

        for pt in opp['body']:
            px = pt['x']
            py = pt['y']
            matrix[py][px] = CELL_OPPONENT

            if head_x - 1 == px and head_y == py:
                #print(px, py)
                #print('opp no left')
                move_chance[LEFT] = 0
            if head_x + 1 == px and head_y == py:
                move_chance[RIGHT] = 0
            if head_y + 1 == py and head_x == px:
                move_chance[UP] = 0
            if head_y - 1 == py and head_x == px:
                move_chance[DOWN] = 0
        
        hx = opp['head']['x']
        hy = opp['head']['y']

        if head_x - 1 == hx:
            #print('1!!!')
            move_chance[LEFT] = 0
        if head_x + 1 == hx:
            #print('2!!!')
            move_chance[RIGHT] = 0
        if head_y + 1 == hy:
            #print('3!!!')
            move_chance[UP] = 0
        if head_y - 1 == hy:
            #print('4!!!')
            move_chance[DOWN] = 0

    if not is_autotest:
        if me['health'] > 30:
            for fd in board['food']:
                px = fd['x']
                py = fd['y']

                if move_chance[LEFT] > 0 and head_x - 1 == px and head_y == py:
                    move_chance[LEFT] = 75
                if move_chance[RIGHT] > 0 and head_x + 1 == px and head_y == py:
                    move_chance[RIGHT] = 75
                if move_chance[UP] > 0 and head_y + 1 == py and head_x == px:
                    move_chance[UP] = 75
                if move_chance[DOWN] > 0 and head_y - 1 == py and head_x == px:
                    move_chance[DOWN] = 75

    max_chance = max(move_chance)
    print('bm', max_chance, move_chance)

    if max_chance <= 0:
        print('OP', max_chance)
        return {'move': 'down'}

    psbl_moves = []
    for i in range(len(move_chance)):
        if move_chance[i] == max_chance:
            psbl_moves.append(move_str[i])

    print('am', psbl_moves, move_chance)

    if len(psbl_moves) == 1:
        return {"move": psbl_moves[0]}
    else:
        next_move = random.choice(psbl_moves)

    print(f"MOVE {game_state.get('turn', '')}: {next_move}")
    return {"move": next_move}