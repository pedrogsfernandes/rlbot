from util.agent import VirxERLU, Vector
from util import routines, utils, tools
from cutil import ctools

class back_to_midfield:
    def __init__(self, agent: VirxERLU):
        self.goto = routines.goto(Vector(0,0,0), agent.foe_goal.location)

    def run(self, agent):
        self.goto.run(agent)

class get_in_position:
    def __init__(self, agent:VirxERLU, target, poptime):
        self.goto = routines.goto(target + Vector(0, utils.side(agent.team)*400 , 0), target)
        self.target = target
        if poptime == -1:
            self.poptime = 1
        else:
            self.poptime = poptime - agent.time
        print(poptime)
        self.deltatime = 0

    def run(self, agent:VirxERLU):
        target = self.target

        self.deltatime += agent.delta_time
        if self.deltatime >= self.poptime:
            agent.pop()
        else:
            self.goto.run(agent)

class no_defense_recovery:
    #its a recovery but not cancelable
    def __init__(self):
        self.retreat = routines.retreat()

    def run(self, agent):
        self.retreat.run(agent)
