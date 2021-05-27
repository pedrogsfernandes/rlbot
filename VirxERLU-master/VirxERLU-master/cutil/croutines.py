from util.agent import VirxERLU, Vector
from util import routines, utils

class back_to_midfield:
    def __init__(self, agent: VirxERLU):
        self.goto = routines.goto(Vector(0,0,0), agent.foe_goal.location)

    def run(self, agent):
        self.goto.run(agent)

class get_in_position:
    def __init__(self, agent:VirxERLU, target):
        self.goto = routines.goto(target + Vector(0, utils.side(agent.team)*400 , 0), target)
        agent.line(target, Vector(target.x, target.y, 0))

    def run(self, agent):
        self.goto.run(agent)