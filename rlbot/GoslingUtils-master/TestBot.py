from tools import *
from objects import *
from routines import *
from tmcp import TMCPHandler, TMCPMessage, ActionType


# This file is for strategy

class TestBot(GoslingAgent):
    def run(agent):

        if agent.team == 0:
            agent.debug_stack()

        close = (agent.me.location - agent.ball.location).magnitude() < 2000
        have_boost = agent.me.boost > 20
        # understand agent position in relation to ball

        me_onside = is_onside(agent, agent.me)
        foe_onside = is_onside(agent, agent.foes[0], is_foe=True)
        return_to_goal = False
        if len(agent.stack) < 1:
            if agent.kickoff_flag:
                agent.tmcp_handler.send_ball_action(0.0)
                agent.push(kickoff())
            elif (close and me_onside) or (not foe_onside and me_onside):
                # An example of pushing routines to the stack:
                left_field = Vector3(4200*-side(agent.team), agent.ball.location.y + (1000*-side(agent.team)), 0)
                right_field = Vector3(4200*side(agent.team), agent.ball.location.y + (1000*-side(agent.team)), 0)
                targets = {"goal": (agent.foe_goal.left_post, agent.foe_goal.right_post),"upfield": (left_field, right_field)}
                shots = find_hits(agent, targets)
                if len(shots["goal"]) > 0:
                    agent.tmcp_handler.send_ball_action(-2.0)
                    agent.push(shots["goal"][0])
                elif len(shots["upfield"]) > 0 and abs(agent.friend_goal.location.y - agent.ball.location.y) < 8490:
                    agent.tmcp_handler.send_ball_action(-3.0)
                    agent.push(shots["upfield"][0])
                else:
                    return_to_goal = True
            elif not me_onside and not have_boost:  # get onside
                boosts = [boost for boost in agent.boosts if boost.large and boost.active and abs(agent.friend_goal.location.y - boost.location.y) - 200 < abs(agent.friend_goal.location.y)]
                print("not_onside")
                if len(boosts) > 0:
                    boost = get_closest_boost(agent, boosts)
                    agent.tmcp_handler.send_boost_action(boost.index)
                    agent.push(goto_boost(boost,agent.friend_goal.location))
                else:
                    return_to_goal = True
            else:
                agent.tmcp_handler.send_ball_action(-1.0)
                agent.push(short_shot(agent.foe_goal.location))



        if return_to_goal:
                relative_target = agent.friend_goal.location - agent.me.location
                angles = defaultPD(agent, agent.me.local(relative_target))
                defaultThrottle(agent, 2300)
                agent.controller.boost = False if abs(angles[1]) > 0.5 or agent.me.airborne else agent.controller.boost
                agent.controller.handbrake = True if abs(angles[1]) > 2.8 else False
                agent.tmcp_handler.send_defend_action()
