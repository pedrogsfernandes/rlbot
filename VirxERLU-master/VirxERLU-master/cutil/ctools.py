from util.agent import VirxERLU, Vector
from util import utils
import math

def is_onside(agent, car):
    return not agent.ball.location.y > car.location.y*utils.side(car.team)

def distance_to_goal(agent):
    return (agent.me.location - agent.friend_goal.location).magnitude()

def shooting_angle(agent, car):
    ball_to_goal:Vector = agent.foe_goal.location - agent.ball.location
    ball_to_player:Vector = car.location - agent.ball.location
    return ball_to_goal.angle2D(ball_to_player)

def angle_car_ball_point(agent, car, point):
    ball_to_point:Vector = point.location - agent.ball.location
    ball_to_player:Vector = car.location - agent.ball.location
    return ball_to_point.angle2D(ball_to_player)

def ball_to_foe_goal(agent):
    return (agent.foe_goal.location - agent.ball.location).magnitude()

def get_pass_location(agent:VirxERLU):
    field_side = utils.sign(agent.me.location.x)
    if field_side == 0:
        field_side = 1
    new_target = agent.ball.location - (3500*field_side, 0,0)
    new_target.y = -utils.side(agent.team)*2500
    new_target.z = 300

    if angle_car_ball_point(agent, agent.me, new_target) < math.pi/2:
        return None
    else:
        pass

    

def all_onside(agent, foes = False):
    if foes:
        cars = agent.foes
    else:
        cars = agent.friends
    for car in cars:
        if not is_onside(agent, car):
            return False
    return True

def n_friends_attacking(agent):
    i = 0
    for car in (agent.friends + (agent.me,)):
        if car.location.y * utils.side(agent.team) < 0:
            i += 1
    return i

def all_offside(agent, foes = False):
    if foes:
        cars = agent.foes
    else:
        cars = agent.friends
    for car in cars:
        if is_onside(agent, car):
            return False
    return True


def get_closest_boost(agent, boosts):
    closest = boosts[0]
    for boost in boosts:
        if (boost.location - agent.me.location).magnitude() < (closest.location - agent.me.location).magnitude():
            closest = boost
    return closest

def any_friend_shooting(agent):
    for car in agent.friends:
        if car.shooting:
            return True
    return False

def is_friend_doing_action(agent, action):
    # For attacking, for example, action = ActionType.BALL
    for _, comm in list(agent.comms.values()):
        if comm.get('action') == action:
            return True
    return False

def is_friend_getting_boost(agent, index):
    # For attacking, for example, action = ActionType.BALL
    for _, comm in list(agent.comms.values()):
        if comm.get('action') == "BOOST" and comm.get('target') == index:
            return True
    return False

def distance_to(agent, point):
    return (agent.me.location - point.location).magnitude()


def is_closest_to(agent, point):
    my_distance = (agent.me.location - point.location).magnitude()
    for car in agent.friends:
        car_to_point = (car.location - point.location).magnitude()
        if car_to_point < my_distance:
            return False
    return True


def get_closest_friend_to_ball(agent):
    all_off = True
    closest_distance = 1000000
    closest_car = None
    for car in (agent.friends + (agent.me,)):
        distance_to_ball = (car.location - agent.ball.location).magnitude()
        onside = is_onside(agent, car)

        if (all_off or onside) and distance_to_ball < closest_distance:
            closest_distance = distance_to_ball
            closest_car = car
            if onside:
                all_off = False

    return closest_car, closest_distance, all_off


def get_furthest_friend_to_ball(agent):
    all_off = True
    longest_distance = -1
    longest_car = None
    for car in (agent.friends + [agent.me]):
        distance_to_ball = (car.location - agent.ball.location).magnitude()
        onside = is_onside(agent, car)

        if (all_off or onside) and distance_to_ball > longest_distance:
            longest_distance = distance_to_ball
            longest_car = car
            if onside:
                all_off = False

    return longest_car, longest_distance, all_off


def get_closest_foe_to_ball(agent):
    all_off = True
    closest_distance = 1000000
    closest_car = None
    for car in agent.foes:
        distance_to_ball = (car.location - agent.ball.location).magnitude()
        onside = is_onside(agent, car)

        if (all_off or onside) and distance_to_ball < closest_distance:
            closest_distance = distance_to_ball
            closest_car = car
            all_off = False

    return closest_car, closest_distance, all_off


def is_closest_to_ball(agent):
    friend, distance, all_off = get_closest_friend_to_ball(agent)
    return friend.index == agent.me.index, distance, all_off

def is_furthest_from_ball(agent):
    friend, distance, all_off = get_furthest_friend_to_ball(agent)
    return friend.index == agent.me.index, distance, all_off

def get_closest_foe_to_car(agent):
    closest_car = None
    closest_distance = 1000000
    for car in agent.foes:
        distance_to_me = (car.location - agent.me.location).magnitude()
        if distance_to_me < closest_distance:
            closest_distance = distance_to_me
            closest_car = car
    return closest_car, closest_distance