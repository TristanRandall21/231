#Tristan Randall ID:30038238
#imports and game variables
import math
import time
import turtle
import random
import engine
W=640
H=480
L=[]
count=0 #count for rockets
county=0 #accounts for rocket pairs if 2 rocket1's are destroyed otherwise/
         #allows for 3 rocket2's and 1 rocket1 as the four on screen rockets.

#Alot of parallax star stuff(creating list, iterate list, make new star class,/
#make default stars with list star class)
def starList():
    global L
    for i in range(150):
        x=random.randint(-320, 320)
        y=random.randint(-80, 240)
        c=random.choice(['#ffffff','#eaebed'])
        if c == '#ffffff':
            dx=-2
        elif c == '#eaebed':
            dx=-0.8
        dy=0  
        s=None
        L.append(x)
        L.append(y)
        L.append(dx)
        L.append(dy)
        L.append(s)
        L.append(c)    
    return L

def starIteration(L):
    for i in range(150):
        x=L[6*i]
        y=L[6*i+1]
        dx=L[6*i+2]
        dy=L[6*i+3]
        s=L[6*i+4]
        c=L[6*i+5]
        star1=_star(x,y,dx,dy,s,c)
        engine.add_obj(star1)
    
def newStar():
    y=random.randint(-80, 240)
    c=random.choice(['#ffffff','#eaebed'])
    if c == '#ffffff':
        dx=-2
    elif c == '#eaebed':
        dx=-0.8
    dy=0  
    s=None
    star2=_star(320,y,dx,dy,s,c)
    engine.add_obj(star2)
       
class _starstuff(engine.GameObject):
    def __init__(self,a,b):
        turtle.register_shape('star',((a,b),(a,a),(b,a),(b,b)))
        super().__init__(320,320,0,-1,'star','black')
          
class _star(engine.GameObject):
    def __init__(self,x,y,dx,dy,s,c):
        super().__init__(x,y,dx,dy,'star',c)
               
#static ground class   
class _ground(engine.GameObject):
    def __init__(self,a,b,c,d):
        turtle.register_shape('ground',((a,b),(a,c),(d,c),(d,b)))        
        super().__init__(0,0,0,0,'ground','light yellow')
    def isstatic(self):
        return True

#buggy and buggy jumping//movement based off of/
#https://sites.google.com/site/samicsemist/change-the-banner/cpsc231win17 week12 
class _buggy(engine.GameObject):
    def __init__(self,a,b,c,d,e,f):
        turtle.register_shape('buggy',((a,d),(a,e),(b,e),(b,f),(c,f),(c,d)))
        super().__init__(0,-120,0,0,'buggy','orange')
        self.count=0
    def heading(self):
        return (self.x+self.deltax)
    def move(self):
            if self.deltay == 5:
                self.y = self.y + self.deltay
                self.count = self.count + 1
            if self.deltay == -5:
                self.y = self.y + self.deltay
                self.count = self.count - 1
            if self.count == 20:
                self.deltay = -5
            if self.deltay == -5 and self.count == 0:
                self.deltay = 0            
            global jumping
            if self.count !=0:
                jumping=True
            else:
                jumping=False               
    def getxy(self):
	    return self.x,self.y
    def getx(self):
            return self.x
    def gety(self):
            return self.y
    def intersect(self,x,y):#5 units short of objects x on either side
        if self.x-35 <= x <= self.x+25 and self.y <= y <= self.y+40:
                return True
        return False
    def delete(self):
        super().delete()
        
buggy1=_buggy(-20,-40,0,-40,0,20)

#All the collisions 
def collbr(buggy1,rock1):
    if buggy1.intersect(rock1.getx(),rock1.gety()):
        engine.del_obj(buggy1)
        engine.add_obj(Boom(0,-120,20))

def collrb(rock1,buggy1):
    return collbr(buggy1,rock1)

#Only need to check for buggy hole collisions not vise versa but added/
#for futur implementations
def collbh(buggy1,hole1):
    if buggy1.intersect(hole1.getx(),hole1.gety()):
        engine.del_obj(buggy1)
        engine.add_obj(Boom(0,-120,20))

def collhb(hole1,buggy1):
    return collbh(buggy1,hole1)

#from http://devmag.org.za/2009/04/13/basic-collision-detection-in-2d-part-1/
#checking for intersection
def iscoll(obj1,obj2):
    x1,y1,r1=obj1.get_bc()
    x2,y2,r2=obj2.get_bc()
    d = math.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2)
    return d < (r1 + r2)

def collrtr(rocket1,rock1):
    if iscoll(rocket1,rock1):
        x1,y1,r1=rocket1.get_bc()
        x2,y2,r2=rock1.get_bc()
        engine.del_obj(rocket1)
        engine.del_obj(rock1)
        engine.add_obj(Boom(x1,y1,r1))
        engine.add_obj(Boom(x2,y2,r2))
        global count #score update and rocket counter
        count=count-1
        points()

def collrrt(rock1,rocket1):
    return collrtr(rocket1,rock1)
    
#rocketx then rockety classes
class _rocket(engine.GameObject):
    def __init__(self):
        super().__init__(20,-110,8,0,'triangle','red')
    def getx(self):
        return self.x
    def get_bc(self):
        return self.x,self.y,10
    def move(self):
        global count
        self.x=self.x+self.deltax
        if self.x>320:
            count=count-1

#Vert rocket moves faster for playability(they leave screen close to when horz/
#rockets do)
class _rocket2(engine.GameObject):
    def __init__(self):
        super().__init__(20,-110,0,10,'triangle','red')
    def gety(self):
        return self.y
    def move(self):
        global count
        global county
        self.y=self.y+self.deltay
        if self.y>240:
            count=count-1
            county=county-1
    
#Key input 
def inputs(key):
    global count
    global county
    if key == 'Q' or key == 'q':
        engine.exit_engine()       
    if key == 'space':
        if buggy1.deltay==0:
            buggy1.deltay=5
    if key =='Return' and jumping==False and count !=3 and count<4 and county<2:
        county=county+1
        count=count+2
        rocket1=_rocket()
        rocket2=_rocket2()
        engine.add_obj(rocket2)
        engine.add_obj(rocket1)
        
#rock class and function    
class _rock(engine.GameObject):
    def __init__(self):
        super().__init__(320,-110,-5,0,'turtle','green')
    def getx(self):
            return self.x
    def gety(self):
            return self.y
    def get_bc(self):
        return self.x,self.y,10
  
def rock():
    rock1=_rock() 
    engine.add_obj(rock1)

#hole class and function    
class _hole(engine.GameObject):
    def __init__(self):
        super().__init__(320,-125,-5,0,'circle','black')
    def getx(self):
            return self.x
    def gety(self):
            return self.y+5
    
def hole():
    hole1=_hole()
    engine.add_obj(hole1)

#Boom!/objects explode on collision
#http://pages.cpsc.ucalgary.ca/~aycock/231/as4/missile.py 
class Boom(engine.GameObject):
	def __init__(self, x, y, maxdiameter):
		self.maxdiameter = maxdiameter
		self.diameter = 0
		super().__init__(x, y, 0, 0, 'circle', 'yellow')

	def draw(self):
		oldmode = turtle.resizemode()
		turtle.shapesize(outline=self.diameter)
		id = super().draw()
		turtle.resizemode(oldmode)
		return id
	
	def step(self):
		newsize = abs(math.sin(math.radians(self.age) + 100))
		if newsize < 0.05:
			engine.del_obj(self)
			return
		self.diameter = newsize * (self.maxdiameter * 2)
		super().step()    

#Score handleing
def draw_score():
    global score
    turtle.goto(0,-185)
    turtle.dot(70,'light yellow')
    turtle.color('red')
    turtle.write(score,align='center', font=('Ariel',20,'normal'))
def points():
    global score
    score=score+10
    draw_score()
    
#calling everything, initialising background and screen          
def init():
    global score
    score=0
    engine.init_screen(W,H)
    engine.init_engine()
    turtle.bgcolor('black')
    engine.set_keyboard_handler(inputs)
    engine.add_random_event(0.01,rock)
    engine.add_random_event(0.01,hole)
    engine.add_random_event(0.1,newStar)
    engine.add_obj(buggy1)
    engine.add_obj(_ground(120,320,-320,240))
    draw_score()
    engine.add_obj(_starstuff(1,1))
    engine.register_collision(_buggy,_rock,collbr)
    engine.register_collision(_rock,_buggy,collrb)
    engine.register_collision(_buggy,_hole,collbh)
    engine.register_collision(_hole,_buggy,collhb)
    engine.register_collision(_rocket,_rock,collrtr)
    engine.register_collision(_rock,_rocket,collrrt)
      
#checking scope and starting game/engine/initial stars
if __name__ == '__main__':
    init()
    A=starList()
    starIteration(A)
    engine.engine()
   
    











        
