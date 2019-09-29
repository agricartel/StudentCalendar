#Imported variables from table
START_TIME = 0 #in DateTime format normally. end_time - start_time returns seconds
END_TIME = 43200 #in DateTime format normally
#start time - end time = answer in seconds
CHUNK_SIZE = 15 #in minutes. default: 1 chunk = 15 mins
MAX_WORK_TIME = 120 #in minutes. default: 120 mins = 2 hours
MAX_BREAK_TIME = 30 #in minutes. default: 30 mins

#converted constants
MAX_BLOCK_SIZE = (int)(MAX_WORK_TIME / CHUNK_SIZE) #max block for TaskBlocks. default is 8 chunks = 2 hours
TOTAL_CHUNKS = (int)((END_TIME - START_TIME) / (60 * CHUNK_SIZE)) #amount of chunks from now till deadline. each number from 0 to total blocks respresents a specific 15 min period
BREAK_MODIFIER = (int)(MAX_WORK_TIME / MAX_BREAK_TIME) #fraction of max block size that can be dedicated to breaks

def timeConvert(time, start): #converts DateTime to chunk number
    return (int)((time - start) / (60 * CHUNK_SIZE)) - 1

def chunkConvert(chunk, start): #converts chunk number to DateTime
    return ((chunk + 1) * 60 * CHUNK_SIZE) + start

class Block:
    def __init__(self, start, end):
        self.start = start
        self.end = end
        self.name = "block"

class Task: #a complete task, allocates TaskBlocks
    def __init__(self, name, duration):
        self.name = name
        self.duration = duration

    def assignTime(self, schedule): #assign time for entire Task
        sIndex = 0; #index in schedule of next upcoming task in events[]
        newStart = -1; #index of starting time for next TaskBlock
        newEnd = -1; #index of ending time for next endingBlock
        remain = self.duration # remaining duration to be allocated
        endBlock = Block(TOTAL_CHUNKS, 0)
        schedule.append(endBlock) #end block, which allows taskblocks after the last event to be created
        for i in range(0, TOTAL_CHUNKS):
            if(i > schedule[sIndex].end): #if the next upcoming event end chunk is less than i, move to next event where the end chuck is greater than i
                while(i > schedule[sIndex].end and sIndex < len(schedule) - 1):
                    sIndex += 1
            if(newStart == -1 and i < schedule[sIndex].start and remain > 0): #start making new TaskBlock.
                #(i < schedule[sIndex].start) prevents creating blocks while iterating through event chunks
                #(remain > 0) prevents creating blocks if task has been fully allocated
                newStart = i
                newEnd = i
            #flag saying no more remaining
            if(newStart != -1):
                remain -= 1
                #check if the current Taskblock does not exceed max block size, no event starts at current chunk, and remaining chunks to allocate . 0
                if(newEnd - newStart + 1 < MAX_BLOCK_SIZE and (i < schedule[sIndex].start - 1) and remain > 0):
                    newEnd += 1
                else: #if any criteria is met, make a new TaskBlock and necessary BreakBlocks
                    schedule = self.createTaskBlock(newStart, newEnd, schedule, sIndex)
                    newStart = -1;
                    newEnd = 0;
        schedule.remove(endBlock)
        if(remain > 0):
            print("You don't have enough time to finish all your tasks with your settings!")
        return schedule

    def createTaskBlock(self, start, end, schedule, sIndex): #create one taskblock and, if necessary, breakblocks
        newTask = TaskBlock(start, end)
        schedule.insert(sIndex, newTask) #add the taskBlock at sIndex, the index of latest event, and move all events in lsit to the right
        breaktime = (int)((end - start + 1) / BREAK_MODIFIER) #breaks are 1/BREAK_MODIFIER the length of TaskBlocks
        breakChunks = [] #list of chunks during which a break is to occur
        for i in range(0, breaktime):
            if(end+i+1 < TOTAL_CHUNKS): #prevent breaks from exceeding the deadline, maybe not an issue
                breakChunks.append(end+i+1)
        #search for any events that overlap with breaktime
        eventStart = 9999 #chunk when an event starts during designated breaktime, if any
        eventEnd = 0 #chunk when an event ends during designated breaktime, if any
        for i in range(0, len(schedule)):
            #if event starts within breakchunk (we don't care if event ends within breakchunk because a event should not be able to start before the breakchunk starts)    
            if(schedule[i].start in breakChunks):
                curr = schedule[i].start
                while(curr <= schedule[i].end and len(breakChunks) > 0): #remove all chunks from event start to event end or until all breakChunks are gone)
                   breakChunks.remove(curr)
                   curr += 1
        if(len(breakChunks) > 0): #if there are breakchunks left, make a BreakBlock containing them
            newBreak = BreakBlock(newTask, breakChunks[0], breakChunks[len(breakChunks) - 1])
            tempIndex = sIndex
            while(schedule[tempIndex].start < newBreak.start and tempIndex < len(schedule) - 1): #if an event starts before the designated break, increment index of schedule to insert break into
                tempIndex += 1
            schedule.insert(tempIndex, newBreak)
        return schedule
    
class TaskBlock(Block): #a single block of time allocated to doing an associated Task
    def __init__(self, start, end):
        self.start = start
        self.end = end
        self.name = "taskblock"

class BreakBlock(Block): # a block designed for breaks, assosiated with a specific TaskBlock
    def __init__(self, taskblock, start, end):
        self.taskblock = taskblock #this is a TaskBlock
        self.start = start
        self.end = end
        self.name = "breakblock"

def main():
    schedule = [] #list of all Blocks within current assignment duration. ordered by start time - put events into schedule, insert new TaskBlocks.
    #predefined events are generic Blocks, TaskBlocks are blocks for the Task, BreakBlocks are assigned after TaskBlocks if no event exists there
    task1 = Task("dab", 24)
    schedule.append(Block(12,15))
    schedule.append(Block(30,33))
    schedule = task1.assignTime(schedule) #potential feature: allows two tasks of same priority to alternate by returning
    #task with same name and remaining chunks, and then running assignTime on the next task, returning, etc.
    for i in range(0, len(schedule)):
        print(schedule[i].name, schedule[i].start, schedule[i].end)

main()
