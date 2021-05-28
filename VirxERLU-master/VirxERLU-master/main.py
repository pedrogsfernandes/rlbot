from util import routines, tools, utils
from cutil import ctools, croutines
from util.agent import Vector, VirxERLU, run_bot


class Bot(VirxERLU):

    def init(self):
        # This is a shot between the opponent's goal posts
        self.foe_goal_shot = (self.foe_goal.left_post, self.foe_goal.right_post)

    def run(self):
        #kickoff strategy
        if not self.kickoff_done:
            if self.is_clear() and ctools.is_closest_to(self, self.ball):
                self.push(routines.generic_kickoff())
                return

            elif self.is_clear() and ctools.is_closest_to(self, self.friend_goal):
                self.kickoff_done = True
                self.goto_nearest_boost()
                return

            elif self.is_clear():
                self.push(routines.generic_kickoff())
                return
        else:

            num_friends = len(self.friends)
            if ctools.all_offside(self,True): #if all foes are offside, shoot without regrets
                 shot = tools.find_shot(self, self.foe_goal_shot)
                 # If we found a  
                 if shot is not None:
                    # If the stack is clear
                    if self.is_clear():
                        # Shoot
                        self.push(shot)
                        return
                    else:
                        current_shot_name = self.stack[0].__class__.__name__
                        new_shot_name = shot.__class__.__name__

                        # If the shots are the same type
                        if new_shot_name is current_shot_name:
                            # Update the existing shot with the new information
                            self.stack[0].update(shot)
                        else:
                            self.clear()
                            self.push(shot)

                    return


            #If all friends are getting boost or offside
            if ctools.all_friends_occupied(self):
                if self.is_clear():
                    self.push(routines.retreat())

            if num_friends > 0 and self.me.boost < 36 and self.boost_amount != "no boost" \
                    and ctools.n_friends_offside(self) < 2 and not ctools.should_attack_ball(self) and not ctools.should_retreat(self):
                if self.is_clear():
                    self.goto_nearest_boost()

                if not self.is_clear():
                    return
          

            # if the stack is clear, then run the following - otherwise, if the stack isn't empty, then look for a shot every 4th tick while the other routine is running
            if self.is_clear() or self.odd_tick == 0:
                shot = None
                # If ball in attacking position
                if self.ball.location.y * utils.side(self.team) < 640 and not ctools.ball_being_targeted(self):
                    shot = tools.find_shot(self, self.foe_goal_shot)
                elif  self.ball.location.y * utils.side(self.team) < 640 and ctools.ball_being_targeted(self) and ctools.should_retreat(self):
                    if self.is_clear():
                        self.push(routines.shadow())
                        return
                elif self.ball.location.y * utils.side(self.team) < 640 and ctools.ball_being_targeted(self):
                    car, action = ctools.get_friend_shooting(self)
                    if car is not None:
                        _, target = ctools.get_pass_location(self, car)
                        if self.is_clear():
                            self.push(croutines.get_in_position(self, target, action.get('time')))
                            return 
                    elif self.is_clear():
                        self.push(croutines.get_in_position(self, Vector(0,util.side(self.team)*-500,0), 1))
                        return


                # if the ball is on our half, get it out
                if shot is None and self.ball.location.y * utils.side(self.team) > 1500\
                        and self.ball.location.x > -2500\
                        and self.ball.location.x < 2500:
                    shot = tools.find_shot(self,(self.friend_goal.right_post + Vector(utils.side(self.team) * 400, 0, 0), self.friend_goal.left_post + Vector(utils.side(self.team) * 400, 0, 0)))


                # If we're behind the ball and we couldn't find a shot on target
                if shot is None and self.ball.location.y * utils.side(self.team) < self.me.location.y * utils.side(self.team) and not ctools.ball_being_targeted(self) :
                    shot = tools.find_any_shot(self)

                # If we found a shot
                if shot is not None:
                    if self.is_clear():
                        self.push(shot)
                    else:
                        current_shot_name = self.stack[0].__class__.__name__
                        new_shot_name = shot.__class__.__name__

                        if new_shot_name is current_shot_name:
                            self.stack[0].update(shot)
                        else:
                            self.clear()
                            self.push(shot)

                    return
            
            if self.is_clear() and self.me.airborne:
                self.push(routines.recovery())

                return




            if self.is_clear():
                if self.ball.location.y * utils.side(self.team) > 640:
                    retreat_routine = routines.retreat()
                    if retreat_routine.is_viable(self):
                        self.push(retreat_routine)
                else:
                    shadow_routine = routines.shadow()
                    if shadow_routine.is_viable(self):
                        self.push(shadow_routine)


    def goto_nearest_boost(self):
        boosts = tuple(boost for boost in self.boosts if boost.active and boost.large)

        if len(boosts) > 0:
            closest_boost = min(boosts, key=lambda boost: boost.location.dist(self.me.location))
            if not ctools.is_friend_getting_boost(self, closest_boost) and (closest_boost.location.dist(self.me.location) < 3500):
                self.push(routines.goto_boost(closest_boost))



    def demolished(self):
        # NOTE This method is ran every tick that your bot it demolished

        # If the stack isn't clear
        if not self.is_clear():
            # Clear the stack
            self.clear()

    def handle_tmcp_packet(self, packet):
        if packet.get('team') is self.team:
            self.comms[packet.get('index')] = (self.time, packet)

    def handle_match_comm(self, msg):

        # All match comms are Python objects
        if msg.get('team') is self.team:
            self.print(msg)

    def handle_quick_chat(self, index, team, quick_chat):

        if self.team is team:
            self.print(quick_chat)


if __name__ == "__main__":
    run_bot(Bot)
