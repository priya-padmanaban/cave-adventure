#Priya Padmanaban, Per. 1 Advincula
#APCS Final Project

from random import randint

#defines default stats for Person
#do_dam calculates how much damage is dealt
class Person:
  def __init__(self):
    self.name = ""
    self.hp = 1
    self.hp_max = 1
  def do_dam(self, foe):
    dam = min(
        max(randint(0, self.hp) - randint(0, foe.hp), 0),
        foe.hp)
    foe.hp = foe.hp - dam
    if dam == 0: print "%s evades %s's attack." % (foe.name, self.name)
    else: print "%s injures %s!" % (self.name, foe.name)
    return foe.hp <= 0

#defines enemy's stats (hp must be lower than player's hp)
class foe(Person):
  def __init__(self, player):
    Person.__init__(self)
    self.name = 'a scary bear'
    self.hp = randint(1, player.hp)
    
#creates a Player with default hp and max hp
class Player(Person):
  def __init__(self):
    Person.__init__(self)
    self.state = 'normal'
    self.hp = 10
    self.hp_max = 10
    
#quit command = endgame
  def quit(self):
    print "%s wandered and fought for years, but couldn't find the way out of the cave. The skeleton remains there to this day. \nRIP" % self.name
    self.hp = 0
#help command = print list of commands
  def help(self): print Commands.keys()
#status command = print hp/max hp
  def status(self): print "%s's hp: %d/%d" % (self.name, self.hp, self.hp_max)
#tired state = sets hp one point lower
  def tired(self):
    print "%s feels very tired." % self.name
    self.hp = max(1, self.hp - 1)
#sleep command = regains one hp, randomly encounters enemy
  def sleep(self):
    if self.state != 'normal': print "%s can't sleep now! This is definitely not the time." % self.name; self.foe_fights()
    else:
      print "%s sleeps and feels a little healthier." % self.name
      if randint(0, 1):
        self.foe = foe(self)
        print "%s wakes up to %s staring right at %s!" % (self.name, self.foe.name, self.name)
        self.state = 'fight'
        self.foe_fights()
      else:
        if self.hp < self.hp_max:
          self.hp = self.hp + 1
        else: print "%s slept way too much." % self.name; self.hp = self.hp - 1
#explore command = randomly encounters enemy
  def explore(self):
    if self.state != 'normal':
      print "%s is too busy right now!" % self.name
      self.foe_fights()
    else:
      print "%s explores a twisty passage." % self.name
      if randint(0, 1):
        self.foe = foe(self)
        print "%s encounters %s!" % (self.name, self.foe.name)
        self.state = 'fight'
      else:
        if randint(0, 1): self.tired()
#run command =  random, but high chance of escaping 
  def run(self):
    if self.state != 'fight': print "%s runs in circles for a while." % self.name; self.tired()
    else:
      if randint(1, self.hp + 5) > randint(1, self.foe.hp):
        print "%s runs from %s." % (self.name, self.foe.name)
        self.foe = None
        self.state = 'normal'
      else: print "%s couldn't escape from %s!" % (self.name, self.foe.name); self.foe_fights()
#fight command = has a chance to raise max hp
  def fight(self):
    if self.state != 'fight': print "%s pounds the wall, but nothing happens. There is nothing to fight here." % self.name; self.tired()
    else:
      if self.do_dam(self.foe):
        print "%s kills %s!" % (self.name, self.foe.name)
        self.foe = None
        self.state = 'normal'
        if randint(0, self.hp) < 10:
          self.hp = self.hp + 1
          self.hp_max = self.hp_max + 1
          print "%s feels stronger!" % self.name
      else: self.foe_fights()
  def foe_fights(self):
    if self.foe.do_dam(self): print "%s was slaughtered by %s!\nRIP" %(self.name, self.foe.name)

#list of commands        
Commands = {
  'quit': Player.quit,
  'help': Player.help,
  'status': Player.status,
  'sleep': Player.sleep,
  'explore': Player.explore,
  'run': Player.run,
  'fight': Player.fight,
  }

 
#starts the game    
p = Player()
p.name = raw_input("What is your name? ")
print "%s takes a step into a pitch black cave, armed with nothing, hoping to find adventure.\n" % p.name
print "(Type one of these commands to proceed:\n"
print "['status', 'quit', 'run', 'fight', 'explore', 'sleep']\n"
print "Type 'help' to see the full list of commands again.)"
 
#if hp is greater than 0, takes commands
#if command is not recognized, error statement is printed.
while(p.hp > 0):
  line = raw_input("> ")
  args = line.split()
  if len(args) > 0:
    commandExists = False
    for c in Commands.keys():
      if args[0] == c[:len(args[0])]:
        Commands[c](p)
        commandExists = True
        break
    if not commandExists:
      print "%s has no idea what you're talking about." % p.name


