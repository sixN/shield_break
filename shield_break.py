class hero():
    '''
    Note yet implemented, intended as parent class for an individual hero
    '''
    def __init__(self, clip_size, reload_time, shot_damage, shot_time, ability_damage, ability_cooldown):
        pass

class soldier():
    '''
    Soldier 76 implementation    
    '''
    CLIP_SIZE = 25
    RELOAD_TIME = 1.5
    SHOT_DAMAGE = 19
    SHOT_TIME = 1/9
    ABILITY_DAMAGE = 120
    ABILITY_COOLDOWN = 8

    def __init__(self, tick_rate = 0.001):
        self.ammo = soldier.CLIP_SIZE
        self.tick_rate = tick_rate
        self.ability_cd = 0
        self.state = []
        self.action = 'IDLE'


    def _shoot(self):
        if self.ammo <= 0:
            return False
        self.ammo -= 1
        action_length = soldier.SHOT_TIME/self.tick_rate
        actions = [('SHOOT',0)]*round(action_length+0.5)
        actions[0] = ('SHOOT',soldier.SHOT_DAMAGE)
        self.state += actions
        return True

    def _reload(self):
        if self.ammo >= soldier.CLIP_SIZE:
            return False
        self.ammo = soldier.CLIP_SIZE
        action_length = soldier.RELOAD_TIME/self.tick_rate
        actions = [('RELOAD',0)]*round(action_length+0.5)
        self.state += actions
        return True

    def _ability(self):
        if self.ability_cd > 0:
            return False
        self.ability_cd = soldier.ABILITY_COOLDOWN
        actions = [('ROCKET',soldier.ABILITY_DAMAGE)]
        self.state += actions
        return True

    def act(self):
        if len(self.state) == 0:
            if self._ability():
                pass
            elif self._shoot():
                pass
            elif self._reload():
                pass
            else:
                raise Exception("Unknown player state")
        self.ability_cd -= self.tick_rate
        return self.state.pop(0)

class hanzo():
    CLIP_SIZE = 1
    RELOAD_TIME = 0.5
    SHOT_DAMAGE = 125
    SHOT_TIME = 0.5
    ABILITY_DAMAGE = 70
    ABILITY_COOLDOWN = 8

    def __init__(self, tick_rate = 0.001):
        self.ammo = hanzo.CLIP_SIZE
        self.tick_rate = tick_rate
        self.ability_cd = 0
        self.state = []
        self.action = 'IDLE'

    def _shoot(self):
        if self.ammo <= 0:
            return False
        self.ammo -= 1
        action_length = hanzo.SHOT_TIME/self.tick_rate
        actions = [('SHOOT',0)]*round(action_length+0.5)
        actions[0] = ('SHOOT',hanzo.SHOT_DAMAGE)
        self.state += actions
        return True

    def _reload(self):
        if self.ammo >= hanzo.CLIP_SIZE:
            return False
        self.ammo = hanzo.CLIP_SIZE
        action_length = hanzo.RELOAD_TIME/self.tick_rate
        actions = [('RELOAD',0)]*round(action_length+0.5)
        self.state += actions
        return True

    def _ability(self):
        if self.ability_cd > 0:
            return False
        self.ability_cd = hanzo.ABILITY_COOLDOWN + 1.8
        actions = ([('STORM',hanzo.ABILITY_DAMAGE)] + [('STORM',0)]*(round(0.3/self.tick_rate+0.5)-1))*6
        self.state += actions
        return True

    def act(self):
        if len(self.state) == 0:
            if self._ability():
                pass
            elif self._shoot():
                pass
            elif self._reload():
                pass
            else:
                raise Exception("Unknown player state")
        self.ability_cd -= self.tick_rate
        return self.state.pop(0)

SIM_LENGTH = 45 #time in S to simulate
SIM_RATE = 0.001 #increment rate for simulation

# Writing to a file for now
fh = open(r'simdata.csv','w')

time = 0 #initialize time to 0
s = soldier(tick_rate = SIM_RATE) #create a soldier
h = hanzo(tick_rate = SIM_RATE) #create a hanzo
fh.write("{},{},{},{},{},{},{}\n".format("TIME","SOLDIER_ACTION","SOLDIER_DAMAGE","SOLDIER_DAMAGE_CUM","HANZO_ACTION","HANZO_DAMAGE","HANZO_DAMAGE_CUM"))
s_cum_dam = 0
h_cum_dam = 0
while time < SIM_LENGTH:  #run sim
    s_act, s_dam = s.act()
    h_act, h_dam = h.act()
    s_cum_dam += s_dam
    h_cum_dam += h_dam
    time += SIM_RATE
    fh.write("{},{},{},{},{},{},{}\n".format(time,s_act,s_dam,s_cum_dam,h_act,h_dam,h_cum_dam))
fh.close()
print('DONE')

