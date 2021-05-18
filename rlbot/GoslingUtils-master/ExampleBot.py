from tools import *
from objects import *
from routines import *


# This file is for strategy

class ExampleBot(GoslingAgent):
    def run(agent):
        agent.debug_stack()

        # understand agent position in relation to ball
        my_goal_to_ball, my_ball_distance = (agent.ball.location - agent.friend_goal.location).normalize(True)
        goal_to_me = agent.me.location - agent.friend_goal.location
        my_distance = my_goal_to_ball.dot(goal_to_me)
        me_onside = my_distance - 200 < my_ball_distance

        # An example of pushing routines to the stack:
        left_field = Vector3(4200*-side(agent.team), agent.ball.location.y + (1000*-side(agent.team)), 0)
        right_field = Vector3(4200*side(agent.team), agent.ball.location.y + (1000*-side(agent.team)), 0)
        targets = {"goal": (agent.foe_goal.left_post, agent.foe_goal.right_post),"upfield": (left_field, right_field)}
        shots = find_hits(agent, targets)
        if len(agent.stack) < 1:
            if agent.kickoff_flag:
                agent.push(kickoff())
            elif len(shots["goal"]) > 0:
                agent.push(shots["goal"][0])
            elif len(shots["upfield"]) > 0:
                agent.push(shots["upfield"][0])
            elif not me_onside:  # get onside
                print("not_onside")
                relative_target = agent.friend_goal.location - agent.me.location
                angles = defaultPD(agent, agent.me.local(relative_target))
                defaultThrottle(agent, 2300)
                agent.controller.boost = False if abs(angles[1]) > 0.5 or agent.me.airborne else agent.controller.boost
                agent.controller.handbrake = True if abs(angles[1]) > 2.8 else False

            else:
                relative_target = agent.ball.location - agent.me.location
                local_target = agent.me.local(relative_target)
                defaultPD(agent, local_target)
                defaultThrottle(agent, 2300)
