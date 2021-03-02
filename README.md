# TowerOfHanoi
                                                          
Tower of Hanoi solver using A* and UCS


Skeleton of the solution 
Input:
The code is based on OOP and it is dynamic (number of disks and stacks are changeable ), the input will be states (goal and initial), stacks have to be constructed first, by defining number of disks and type of stack. States will be constructed from the stacks and we have to specify number of stacks. Then the strategy object will take (goal and initial) states.
Output:
The output will be recorded in a file with all movements, costs and number of expand states for each algorithm.
Implementation:
Tower of Hanoi has 3 entities: disks, stacks and state of tower.
The problem is handled using classes, which are as follow:
1.  Stack class: which has attributes for type, cost and disks currently in the stack. Type attribute will be narrow or wide, and 0 or 1 respectively as binary representation. According to the type, the cost of the stack will be set. For disks, user will enter number of disks in a certain stack, and the stack will be filled descending order, so if user enter 3, stack will have >> [3,2,1] 3>2>1.
In this class, a group of functions are defined as needed:
__eq__: to override equal operation.
getTopDisk(), moveTopDisk(), popTopDisk(), isEmptyStack(), getType(), getCost().
2. State class: representation for any state in the tower of hanoi, so it contains numOfStacks which is the number of stacks in the tower, stacks which is a list of stacks objects, parentState which is the parent state for the current state and must be a type of state, and movement which is a string hold information of how disk has been moved. 
The state class also defined the needed function as follow:
__eq__ () which is an override for equal operation, then a couples of function to calculate cost of movements (calG() for UCS algorithm and calF(), calG(), calH() for A* search algorithm). Also, representState() to represent a state in string format.
3. Strategy class: which is responsible of performing search algorithm and solve the problem to reach the goal state achieving minimum cost. It consists of :
start: initial state
goal: goal state
openQue: frieng
closedQue: the closed path to reach the goal state
numOfExStates: number of expanded states to reach the goal
Functions that are defined in this class:
expand(state):
This function take a certain state and expand it to its successors or children states. First of all, it will check if the current state is an instance of class state, then it will check if it is a goal to not expand and return, then if it has to expand, it will take a deep copy of the current state, in order to not be affected and we can reuse it again to expand rest of children. Then, it will go through nested loops to loop on all stacks and check if any movement in each stack can be done or not. For example, it will take the first stack in the first loop, in the second loop will loop on the rest of stacks to check if any movement is possible. So the first stack mustn’t be empty and the two stack must not be the same stack (as we loop on all stacks). If any movement happen, then we set the parent of the children and calculate the cost, if UCS >> calG and if A* >> calF(), and we record the movement, then the resultant states will be appended to the actions(successors).
getNextState():
This function will check which state in the openQue, has the lowest cost, once we have it, it will be taken and delete the object.
Search function: 
As the difference between A* and UCS is in cost calculation, so they seems the same algorithm. In the search method: 
It will be checked if the state is a goal state, then the initial state will be appended to the openQue, then we will go through loop while the openQue not empty, here we get the next state and append it to openQue, and we check if the next state is a goal or not, if not, then we have to expand its successor and check if this successor is in the closedQue, that mean is it visited or not. If not visited, we have to check if there is another successor equal to it in the openQue and have a lower cost, to append the new to the openQue and remove the child from the openQue. If it is not visited at all, then we have to append it to the openQue and get the next state.
Heuristic function
To use different heuristics, another two classes has been added, which inherit the supre strategy class. The used heuristic functions will give a cost less than G or equal .
