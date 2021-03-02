#!/usr/bin/env python
# coding: utf-8

# In[2]:


import copy


# In[3]:


'''Stack class'''
'''
_type: type of stack >> narrow:0, wide:1
cost: thin stack has cost of 1, and wide stack has cost of 2
disks: lists of disks are currently in the stack
'''
class stack:
    def __init__(self, _type=0, numOfDisks=3):
        if _type > 1:
            raise Exception ('type of stack must be 0 for narrow or 1 for wide')
        self._type = _type
        if self._type:
            self.cost = 2
        else:
            self.cost = 1
        self.numOfDisks = numOfDisks
        
        self.disks = []    
        self.disks = [i for i in range(numOfDisks, 0, -1)] # if number of disks was 4 : [4, 3, 2, 1] 4 larger than 3 and so on
    
    
    def __eq__(self,otherStack):
        '''
        to compare between two stacks, so this function will check: 
        * if the number of disks the same in both stacks
        * if the disks positions the same in both stacks
        * we ignore type and cost of each stack
        '''
        if isinstance(otherStack, stack):
            if len(self.disks) == len(otherStack.disks):
                for i in range(0,len(self.disks)):
                    if self.disks[i] != otherStack.disks[i]:
                        return False
            else:
                return False
            return True
        else:
            return False
 
    def getType(self):
        '''get the type of stack : narrow or wide'''
        if self._type:
            print('wide stack')
        else:
            print('narrow stack')

    def getCost(self):
        '''get the cost of the stack: 2 for wide and 1 for narrow'''
        print(self.cost)
        
    def isEmptyStack(self):
        '''check if the stack is empty or not'''
        return len(self.disks) == 0
    
    def getTopDisk(self):
        '''get the top disk value in the stack without pop it from the stack'''
        if self.isEmptyStack():
            return 12
        return self.disks[-1]
    
    def popTopDisk(self):
        '''pop the top disk in the stack'''
        self.disks.pop(-1)
    
    def moveTopDisk(self,xStack):
        '''move top disk from non empty stack to a legal stack, which is empty or its top disk is larger than new disk'''
        if self.isEmptyStack():
            print("can't move disks from empty stack")
            return False
        else:
            if self.getTopDisk() < xStack.getTopDisk():
                xStack.disks.append(self.getTopDisk())
                self.popTopDisk()
                return True
            else:
                print("the top disk is the same in the bothe staks or the moved disk is larger")
        return False


# In[ ]:





# In[4]:


'''state class'''
'''
representation for any state in the tower of hanoi, so it contains
numOfStacks: number of stacks in the tower
stacks: a list of stacks objects
parentState: parent state for the current state
movement: string hold information of how disk has been moved
'''
class state(object):
    def __init__(self,numOfStacks=3, stacks=[], parentState=None, goal_state=False):
        if numOfStacks < 3 or numOfStacks >10:
            raise Exception('number of stacks must be between 3 and 10')
        self.stacks = stacks
        self.numOfStacks = len(self.stacks)#numOfStacks
        self.parentState = parentState
        self.cost = 0
        self.movement = ''

    def __iter__(self):
        return iter(self.stacks)

    def __eq__(self, otherState):
        '''
        to compare between two states, so this function will check: 
        * if the number of stacks the same in both states
        * if the stacks positions the same in both state
        '''
        if isinstance(otherState, state):
            try:
                if self.numOfStacks == otherState.numOfStacks:
                    for i in range(0,self.numOfStacks):
                        if self.stacks[i] != otherState.stacks[i]:
                            return False
                else:
                    return False
            except IndexError:
                return False
            return True
        else:
            return False
    
    def calG(self,srcStackIndex,dstStackIndex):
        '''calculate function g to find cost of moving from state to another according to the stack cost'''
        return self.stacks[srcStackIndex].cost + self.stacks[dstStackIndex].cost
    
    def calH(self,goalState):
        '''calculate function h to find heuristic cost to the final state'''
        '''if the number of the disks in the stack is not the same in the goal stack then there is a value for H, it will
        equal the difference between number of disks, this indicate the number of possible movement to reach the goal state'''
        H = 0
        
        i=0
        # get the index of the full stack in the goal state
        for i in range(0,self.numOfStacks):
            if not goalState.stacks[i].isEmptyStack():
                break
        H=len(goalState.stacks[i].disks) - len(self.stacks[i].disks)
        ############################################################
 
        return H
    
    def calF(self,goalState,srcStackIndex,dstStackIndex):
        '''F function to calculate total cost (H,G) to reach the goal state'''
        self.cost = self.calG(srcStackIndex,dstStackIndex) + self.calH(goalState)
        return self.cost
    
    def printState(self):
        '''print state representation'''
        print(self.representState(), self.cost)
    
    def representState(self):
        '''represent state as string'''
        stateStr = self.movement +'\n'
        for i in range(0,self.numOfStacks):
            stateStr += str(self.stacks[i].disks)
            stateStr += ' '
        stateStr += str(self.cost)
        return stateStr
       
                    
                        
                        
  


# In[ ]:





# In[5]:


'''strategy class'''
'''
start: initial state
goal: goal state
openQue: frieng
closedQue: the closed path to reach the goal state
numOfExStates: number of expanded states to reach the goal
'''
class strategy:
    def __init__(self, startState, goalState):
        if not isinstance(startState, state): 
            raise Exception('initial state is not type of state')
        if not isinstance(goalState, state):
            raise Exception('goal state is not type of state')
        self.start = startState
        self.goal = goalState
        self.openQue = []
        self.closedQue = []
        self.numOfExStates = 0
        
             
    def expand(self, aState):
        '''do expand the current state to its possible children states'''
        
        if not isinstance(aState,state):
            raise Exception('this is not an object of state to be expand')
        actions = []
        if aState == self.goal:
            print('it is the goal state')
            return actions
        
# nested loops on all stacks of the tower, to try moving disks from each stack to other stacks 
        for i in range(0,aState.numOfStacks):
            try: 
                # take deep copy of the state object to gurantee it will not be affected
                st = copy.deepcopy(aState)
                for j in range(0,st.numOfStacks):
                    try:
# start to move from stack i to j, so i and j must be different and i is not empty
                        if i != j and len(st.stacks[i].disks) > 0:                        
                            isMoved = st.stacks[i].moveTopDisk(st.stacks[j])
                            if st != aState:
                                st.parentState = aState
                            if isMoved:
                                st.movement = 'move top disk of stack {0} to stack {1}'.format(i,j)
                                st.cost = st.calF(self.goal,i,j)#calculate cost of movement
                                if st.parentState == aState and st != self.start:
                                    actions.append(st)
                                st = state()
                                # delete state st and start another one
                                del st
                                st = copy.deepcopy(aState)
                                print('---------------------------------------')
                                    
                    except IndexError:
                        continue        
            except IndexError:
                continue
        print(len(actions))
        return actions

    
    def getNextState(self):
        '''choose one state from the frieng with lowest cost'''
        minCost = 100000000
        i=0
        # compare states cost to get the state with the lowest cost
        for i in range(0,len(self.openQue)):
            if self.openQue[i].cost > minCost:
                minCost = self.openQue[i].cost
        minCostState=self.openQue[i]
        # remove selected state from openQue
        del self.openQue[i]
        return minCostState

    
    
    def AstarSearch(self):
        '''perform A* search algorithm to reach the goal state'''
        
        # open a txt file to record movements and progress
        file = open('movements_A_star.txt','+a')
        file.write('Initial state: {0}\n'.format(self.start.representState()))
        file.write('Goal State: {0}\n'.format(self.goal.representState()))
        if self.start == self.goal:
            print("here is the goal!!!")
            return
   
        self.openQue.append(self.start)
    
        # start searching while openQue has states
        while len(self.openQue):
            
            # get the next state from the openQue
            nextState = self.getNextState()
            self.closedQue.append(nextState)
            
            file.write('\nnew state: {0}\n'.format(nextState.representState()))
            print('selected State')
            nextState.printState()
    
            if nextState == self.goal:
                file.write('here is the goal!!!\n')
                file.write('number of expanded states: {0}\n'.format(str(self.numOfExStates)))
                file.write('-------------------------------------------------\n\n')
                print("here is the goal!!!")
                break
            
            else:
                # expand nextState for its possible children state
                childrenStates = self.expand(nextState)
                # increase number of expanded states
                self.numOfExStates += 1
#check if the state is already visited or not, to remove from openQue and append the new state
                for childState in childrenStates:
                    visitedState = False
                    for cState in self.closedQue:
                        if cState == childState:
                            visitedState = True
                    if not visitedState:
                        for oState in self.openQue:
                            if oState == childState:
                                visitedState = True
                                if oState.cost > childState.cost:
                                    self.openQue.remove(oState)
                                    self.openQue.append(childState)
                                    break
                        if not visitedState:
                            self.openQue.append(childState)
                                      


# In[ ]:





# In[7]:


# sub class that will use another version of Heuristic
class strategyH2(strategy):
    def calH(self,goalState):
        '''calculate function h to find heuristic cost to the final state'''

        # using number of disks in the middle stack as heuristic
        H = len(self.stacks[int(self.numOfStacks/2)].disks)
        return H
        


# In[8]:


# sub class that will use another version of Heuristic
class strategyH3(strategy):
    def calH(self,goalState):
        '''calculate function h to find heuristic cost to the final state'''
        i=0
        # get the index of the full stack in the goal state
        for i in range(0,self.numOfStacks):
            if not goalState.stacks[i].isEmptyStack():
                break
        h = 0
        # check if there is a difference between disks order in the goal state stack
        if len(self.stacks[i].disks) != 0:
            
            for k in range(0,len(goalState.stacks[i].disks)):
                try:
                    if self.stacks[i].disks[k] != goalState.stacks[i].disks[k]:
                        h += 1
                except IndexError:
                    continue
                
        else:
            h = len(goalState.stacks[i].disks)
 
        return h

        


# In[ ]:





# In[15]:


#start state
s1=stack(1,5)
s2=stack(1,0)
s3=stack(0,0)
s4=stack(1,0)
#goal state
s11=stack(1,5)
s22=stack(1,0)
s33=stack(0,0)
s44=stack(1,0)

SS = state(4,[s1,s2,s3,s4])
GS = state(4,[s44,s33,s22,s11])


# In[ ]:


#first version of hurestic 
slover1 = strategy(SS,GS)
slover1.AstarSearch()


# In[17]:


#second version of hurestic 
slover2 = strategyH2(SS,GS)
slover2.AstarSearch()


# In[12]:


#third version of hurestic 
slover3 = strategyH3(SS,GS)
slover3.AstarSearch()


# In[ ]:




