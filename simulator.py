class CPU:
	def __init__(self):
		self.PCB = []       #list for processes
		self.RCB = []       #list for Resources
		self.RL  = []       #ready list, keep index of pcb for process
		self.WL  = []       #wait list, keep index of pcb for process
		self.halt = False

	#funtion to set inital state of CPU
	def init(self):
		for i in range(16):
			self.PCB.append([-1, -1, -1,[], []])    #(state, parent ,  priority,children - pid, resource - rid and quant)
		self.RCB = [[1, 1, []], [1, 1, []], [2, 2, []], [3, 3, []]]     #(total, available, processes)
		self.RL = [[], [], [], []]                  #ready list for 4 priorities
		self.WL = []                                #block list only pid
		self.cpi = 0                                #current process id = 0
		self.PCB[0] = [2, -1, -1, [], []]           #0 process with priority 0
		self.halt = False

	def create(self, p):
		"""create new process if  no space then set cpi = -1 and stop cpu"""
		for i, pcb in enumerate(self.PCB):
			if pcb[0] == -1:    #if find one empty entry
				pcb[0] = 1      #state = ready
				pcb[1] = self.cpi   #set parent as current process
				pcb[2] = p          #set priority
				self.RL[p].append(i)        #insert to the RL
				self.PCB[self.cpi][3].append(i)     #insert child to current process
				self.scheduler()            #call schedular
				return
		#when all pcbs are allocated
		self.halt = True
		self.cpi = -1

	def scheduler(self):
		p = 3
		while p > self.PCB[self.cpi][2]:
			if len(self.RL[p]) > 0:         #if there is a process with higher prioriy in a ready list
				pid = self.RL[p].pop(0)
				self.PCB[self.cpi][0] = 1                               #state = ready
				if self.PCB[self.cpi][2]!=-1:self.RL[self.PCB[self.cpi][2]].append(self.cpi)            #add current process to end of ready list
				self.cpi = pid
				self.PCB[self.cpi][0] = 2                               #state = run
				return
			p -= 1

	def timeout(self):
		"""add current process to the end of ready list and call schedule"""
		self.PCB[self.cpi][0] = 1
		self.RL[self.PCB[self.cpi][2]].append(self.cpi)
		self.cpi = 0
		self.scheduler()

	def request(self, r, q):
    		"""request resource r with q amount"""
			#error handling
			
    		pass

	def run(self, line):
		args = line.split(' ')
		if args[0] == 'in':
			self.init()
		elif args[0] == 'cr':
			self.create(int(args[1]))
		elif args[0] == 'to':
			self.timeout()


if __name__ == '__main__':
	cpu = CPU()
	lines = open('sample-input.txt')
	for line in lines:
		line = line.strip()
		if len(line) == 0: continue
		cpu.run(line)
		print(line, cpu.cpi)
