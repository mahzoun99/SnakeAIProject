from Games.Snake.Client.Python.World import *


def first_pos(world: World, bdy):
    head = world.get_self().get_head()

    bdy.append(head)

    if head == Vector2D(1, 3):
        bdy.append(Vector2D(1, 2))
        bdy.append(Vector2D(1, 1))

    elif head == Vector2D(1, 26):
        bdy.append(Vector2D(1, 27))
        bdy.append(Vector2D(1, 28))

    elif head == Vector2D(28, 3):
        bdy.append(Vector2D(28, 2))
        bdy.append(Vector2D(28, 1))

    elif head == Vector2D(28, 26):
        bdy.append(Vector2D(28, 27))
        bdy.append(Vector2D(28, 28))


def i_first_pos(world: World, bd):
    if (len(bd) == 0):
        first_pos(world, bd)


def translate(txt):
    if txt == 'u':
        return Vector2D(1, 0)
    elif txt == 'r':
        return Vector2D(0, 1)
    elif txt == 'd':
        return Vector2D(-1, 0)
    elif txt == 'l':
        return Vector2D(0, -1)


def updater(world: World, body, action):
    act = translate(action)
    n_pos = body[0] + act
    pos_id = world.board[n_pos.i][n_pos.j]
    if pos_id == world.goal_id:
        body.insert(0, world.goal_position)
    else:
        body.pop(len(body))
        body.insert(0, n_pos)


def evaluate(world: World, point, f_move, s_move):
    if (f_move.dist(world.goal_position) == 0):
        return 19
    elif (s_move.dist(world.goal_position) == 0):
        return 20
    else:

        dist = point.dist(world.goal_position)
        score = 17 - dist
        return score


def first_L(world: World):
    head_pos = world.get_self().get_head()

    okays = []

    next_head = []
    next_head.append(head_pos + Vector2D(1, 0))
    next_head.append(head_pos + Vector2D(0, 1))
    next_head.append(head_pos + Vector2D(-1, 0))
    next_head.append(head_pos + Vector2D(0, -1))

    next_move = []
    next_move.append(Vector2D(1, 0))
    next_move.append(Vector2D(0, 1))
    next_move.append(Vector2D(-1, 0))
    next_move.append(Vector2D(0, -1))

    next_head_ok = [True, True, True, True]
    h_number = 0
    for h in next_head:
        accident = False
        for s in world.snakes:

            if h in world.snakes[s].get_body():
                accident = True
                break

        if h in world.get_walls():
            accident = True

        if accident:
            next_head_ok[h_number] = False
        h_number += 1

    for i in range(4):
        if next_head_ok[i]:
            okays.append([next_move[i]])
    return okays


def scnd_L(world: World, first_L):
    for act in first_L:
        okays = []
        head_pos = (world.get_self().get_head() + act[0])

        next_head = []
        next_head.append(head_pos + Vector2D(1, 0))
        next_head.append(head_pos + Vector2D(0, 1))
        next_head.append(head_pos + Vector2D(-1, 0))
        next_head.append(head_pos + Vector2D(0, -1))

        next_move = []
        next_move.append(Vector2D(1, 0))
        next_move.append(Vector2D(0, 1))
        next_move.append(Vector2D(-1, 0))
        next_move.append(Vector2D(0, -1))

        next_head_ok = [True, True, True, True]
        h_number = 0
        for h in next_head:
            accident = False
            for s in world.snakes:

                if h in world.snakes[s].get_body():
                    accident = True
                    break

            if h in world.get_walls():
                accident = True

            if accident:
                next_head_ok[h_number] = False
            h_number += 1

        for i in range(4):
            if next_head_ok[i]:
                # score = evaluate(world,next_head[i])
                okays.append([next_move[i]])
        act.append(okays)


def thrd_L(world: World, first_L):
    for act_one in first_L:
        move_one = act_one[0]
        for act_two in act_one[1]:
            move_two = act_two[0]
            head = world.get_self().get_head()
            head_pos = ((world.get_self().get_head() + move_one) + move_two)
            okays = []
            next_head = []
            next_head.append(head_pos + Vector2D(1, 0))
            next_head.append(head_pos + Vector2D(0, 1))
            next_head.append(head_pos + Vector2D(-1, 0))
            next_head.append(head_pos + Vector2D(0, -1))

            next_move = []
            next_move.append(Vector2D(1, 0))
            next_move.append(Vector2D(0, 1))
            next_move.append(Vector2D(-1, 0))
            next_move.append(Vector2D(0, -1))

            next_head_ok = [True, True, True, True]
            h_number = 0
            for h in next_head:
                accident = False
                for s in world.snakes:

                    if h in world.snakes[s].get_body():
                        accident = True
                        break

                if h in world.get_walls():
                    accident = True
                if (h == (head + move_one)):
                    accident = True

                if accident:
                    next_head_ok[h_number] = False
                h_number += 1

            for i in range(4):
                if next_head_ok[i]:
                    score = evaluate(world, next_head[i], (move_one + head), head_pos)
                    okays.append([next_move[i], score])
            act_two.append(okays)


def find_max(World, wayz):
    best_action = Vector2D(0, 1)
    best = -100
    for act in wayz:
        action = act[0]
        for move_one in act[1]:
            for move_two in move_one[1]:
                if move_two[1] > best:
                    best = move_two[1]
                    best_action = action
    print(best)
    return best_action


def translator(txt):
    if txt == Vector2D(1, 0):
        return 'd'
    elif txt == Vector2D(0, 1):
        return 'r'
    elif txt == Vector2D(-1, 0):
        return 'u'
    elif txt == Vector2D(0, -1):
        return 'l'


# global body
# body = []
def get_action(world: World):
    head_pos = world.get_self().get_head()

    ways = first_L(world)
    scnd_L(world, ways)
    thrd_L(world, ways)
    print(ways)
    print(world.cycle)
    act = find_max(world, ways)
    action = translator(act)

    return action