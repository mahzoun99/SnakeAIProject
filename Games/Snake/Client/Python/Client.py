import socket
import random
from argparse import ArgumentParser
from Base.Message import *
from Games.Snake.Client.Python.World import *
import Games.Snake.Client.Python.ClientGreedy as c_greedy
import Games.Snake.Client.Python.ClientRandom as c_random
import Games.Snake.Client.Python.ClientSimpleCrashAvoid as c_sca
import Games.Snake.Client.Python.ClientBest as c_best
import signal
is_run = True


def signal_handler(sig, frame):
    global is_run
    print('You pressed Ctrl+C!')
    is_run = False


signal.signal(signal.SIGINT, signal_handler)


def run():
    parser = ArgumentParser()
    parser.add_argument("-n", "--name", dest="name", type=str, default='team_name' + str(random.randint(0, 10000)),
                        help="Client Name", metavar="NAME")
    parser.add_argument("-c", "--client", dest="client_type", type=str, default='auto',
                        help="greedy, sca, best, random, hand, auto", metavar="ClientType")
    args = parser.parse_args()
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.settimeout(1)
    server_address = ('localhost', 20002)
    world = World()
    message_snd = MessageClientConnectRequest(args.name).build()

    while is_run:
        sock.sendto(message_snd, server_address)
        try:
            message_rcv = sock.recvfrom(4096)
        except:
            continue
        message = parse(message_rcv[0])
        if message.type == 'MessageClientConnectResponse':
            print('my id is ' + str(message.id))
            world.set_id(message.id, message.ground_config['goal_id'])
            break

    while is_run:
        try:
            r = sock.recvfrom(4096)
        except:
            continue
        message = parse(r[0])
        if message.type == 'MessageClientDisconnect':
            break
        elif message.type == 'MessageClientWorld':
            world.update(message)
            world.print()

            if args.client_type == 'greedy' or (args.client_type == 'auto' and world.self_id == 1):
                action = c_greedy.get_action(world)
            elif args.client_type == 'random' or (args.client_type == 'auto' and world.self_id >= 2):
                action = c_random.get_action(world)
            elif args.client_type == 'sca':
                action = c_sca.get_action(world)
            elif args.client_type == 'best':
                action = c_best.get_action(world)
            elif args.client_type == 'hand':
                action = input('enter action (u or d or l or r:')

            sock.sendto(MessageClientAction(string_action=action).build(), server_address)

