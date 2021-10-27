from modules.memory import MemoryManager


class Process:
    def __init__(self, pid, offset,processDescription):
        self.pid = int(pid)
        self.iniTime = int(processDescription[0])
        self.priority = int(processDescription[1])
        self.timeToComplete = int(processDescription[2])
        self.qtdblocks = int(processDescription[3])
        self.printer = int(processDescription[4])
        self.scanner = int(processDescription[5])
        self.modem = int(processDescription[6])
        self.driver = int(processDescription[7])
        self.offset = int(offset)
        self.timeExecuted = 0
        
    def HasStarted(self):
        if(self.timeExecuted > 0):
            return 1
        else:
            return 0

    def IsFinished(self):
        if self.timeExecuted == self.timeToComplete:
            return 1
        else:
            return 0

class ProcessManager:
    def __init__(self, processes):
        self.processes = []
        #self.readyProcesses = []
        self.rtProcesses = []
        self.userProcesses = []
        self.readyRtProcesses = []
        self.readyUserProcesses = []
        self.rtProcessesAuxIdx = 0
        self.userProcessesAuxIdx = 0
        self.currentTime = 0
        self.processTable = {}

        for process in processes:
            self.processes.append(process)

        self.processes.sort(key=lambda x: x.iniTime)

        for process in self.processes:
            self.processTable[process.pid] = process
            if int(process.priority) == 0:
                self.rtProcesses.append(process)
            else:
                self.userProcesses.append(process)
        
    
    def Run(self):
        #self.userProcesses.sort(key=lambda x: x.priority)

        lastProcessExecuted = -1
        currentProcessExecuting = -1
        finishedProcesses = 0

        while finishedProcesses < len(self.processes):
            self.CheckForNewEntryProcesses()
            if currentProcessExecuting == -1:
                if len(self.readyRtProcesses) > 0:
                    # dar posse da CPU para o primeiro processo da lista de processos real time prontos
                    currentProcessExecuting = self.readyRtProcesses[0].pid
                    self.readyRtProcesses.pop(0)
                    if self.processTable[currentProcessExecuting].HasStarted() == 0:
                        self.PrintDispatcherProcess(self.processTable[currentProcessExecuting])
                    print("process ", currentProcessExecuting, " =>")
                    print("P", currentProcessExecuting, " STARTED")
                    self.processTable[currentProcessExecuting].timeExecuted += 1
                    print("P", currentProcessExecuting, " instruction ", self.processTable[currentProcessExecuting].timeExecuted)
                    if self.processTable[currentProcessExecuting].IsFinished() == 1:
                        print("P", currentProcessExecuting, " return SIGINT")
                        print("")
                        finishedProcesses += 1
                        currentProcessExecuting = -1
                    else:
                        lastProcessExecuted = currentProcessExecuting
                else:
                    if len(self.readyUserProcesses) > 0:
                        #lista de processos de usuario tem que estar devidamente ordenada para saber quem devera ser o proximo processo
                        currentProcessExecuting = self.readyUserProcesses[0].pid
                        self.readyUserProcesses.pop(0)
                        if self.processTable[currentProcessExecuting].HasStarted() == 0:
                            self.PrintDispatcherProcess(self.processTable[currentProcessExecuting])
                        print("process ", currentProcessExecuting, " =>")
                        print("P", currentProcessExecuting, " STARTED")
                        self.processTable[currentProcessExecuting].timeExecuted += 1
                        print("P", currentProcessExecuting, " instruction ", self.processTable[currentProcessExecuting].timeExecuted)
                        if self.processTable[currentProcessExecuting].IsFinished() == 1:
                            print("P", currentProcessExecuting, " return SIGINT")
                            print("")
                            finishedProcesses += 1
                            currentProcessExecuting = -1
                        else:
                            lastProcessExecuted = currentProcessExecuting

            else:
                # existe um processo executando
                if self.processTable[currentProcessExecuting].priority == 0:
                    #print("capivara")
                    # continua processo real time que tava antes
                    self.processTable[currentProcessExecuting].timeExecuted += 1
                    print("P", currentProcessExecuting, " instruction ", self.processTable[currentProcessExecuting].timeExecuted)
                    if self.processTable[currentProcessExecuting].IsFinished() == 1:
                        print("P", currentProcessExecuting, " return SIGINT")
                        print("")
                        finishedProcesses += 1
                        currentProcessExecuting = -1
                    else:
                        lastProcessExecuted = currentProcessExecuting
                else:
                    #print("wada wada")
                    # checar se eh preciso trocar qual processo tem posse da CPU
                    if(len(self.readyRtProcesses) > 0):
                        # existe processo rt pronto; parar processo atual para colocar o rt
                        print("P", currentProcessExecuting, " STOPPED")
                        print("")
                        self.readyUserProcesses.append(self.processTable[currentProcessExecuting])
                        self.readyUserProcesses.sort(key=lambda x: x.priority)
                        # colocar o rt
                        currentProcessExecuting = self.readyRtProcesses[0].pid
                        self.readyRtProcesses.pop(0)
                        if self.processTable[currentProcessExecuting].HasStarted() == 0:
                            self.PrintDispatcherProcess(self.processTable[currentProcessExecuting])
                        print("process ", currentProcessExecuting, " =>")
                        print("P", currentProcessExecuting, " STARTED")
                        self.processTable[currentProcessExecuting].timeExecuted += 1
                        print("P", currentProcessExecuting, " instruction ", self.processTable[currentProcessExecuting].timeExecuted)
                        if self.processTable[currentProcessExecuting].IsFinished() == 1:
                            print("P", currentProcessExecuting, " return SIGINT")
                            print("")
                            finishedProcesses += 1
                            currentProcessExecuting = -1
                        else:
                            lastProcessExecuted = currentProcessExecuting
                    else:
                        # checar se tem processo de usuario pronto
                        if(len(self.readyUserProcesses) > 0):
                            #trocar para o processo de usuario com maior prioridade
                            print("P", currentProcessExecuting, " STOPPED")
                            print("")
                            self.readyUserProcesses.append(self.processTable[currentProcessExecuting])
                            self.readyUserProcesses.sort(key=lambda x: x.priority)
                            #colocar o novo processo
                            #checar se o primeiro da lista de prioridade eh o mesmo processo anterior
                            if self.readyUserProcesses[0].pid == lastProcessExecuted and len(self.readyUserProcesses) > 1:
                                currentProcessExecuting = self.readyUserProcesses[1].pid
                                self.readyUserProcesses.pop(1)
                            else:
                                currentProcessExecuting = self.readyUserProcesses[0].pid
                                self.readyUserProcesses.pop(0)

                            
                            if self.processTable[currentProcessExecuting].HasStarted() == 0:
                                self.PrintDispatcherProcess(self.processTable[currentProcessExecuting])
                            print("process ", currentProcessExecuting, " =>")
                            print("P", currentProcessExecuting, " STARTED")
                            self.processTable[currentProcessExecuting].timeExecuted += 1
                            print("P", currentProcessExecuting, " instruction ", self.processTable[currentProcessExecuting].timeExecuted)
                            if self.processTable[currentProcessExecuting].IsFinished() == 1:
                                print("P", currentProcessExecuting, " return SIGINT")
                                print("")
                                finishedProcesses += 1
                                currentProcessExecuting = -1
                            else:
                                lastProcessExecuted = currentProcessExecuting
                        else:
                            #continuar processo de usuario atual
                            self.processTable[currentProcessExecuting].timeExecuted += 1
                            print("P", currentProcessExecuting, " instruction ", self.processTable[currentProcessExecuting].timeExecuted)
                            if self.processTable[currentProcessExecuting].IsFinished() == 1:
                                print("P", currentProcessExecuting, " return SIGINT")
                                print("")
                                finishedProcesses += 1
                                currentProcessExecuting = -1
                            else:
                                lastProcessExecuted = currentProcessExecuting

            self.currentTime += 1





    def CheckForNewEntryProcesses(self):
        while self.rtProcessesAuxIdx < len(self.rtProcesses) and self.rtProcesses[self.rtProcessesAuxIdx].iniTime == self.currentTime:
            self.readyRtProcesses.append(self.rtProcesses[self.rtProcessesAuxIdx])
            self.readyRtProcesses.sort(key=lambda x: x.priority)
            self.rtProcessesAuxIdx += 1
            
        while self.userProcessesAuxIdx < len(self.userProcesses) and self.userProcesses[self.userProcessesAuxIdx].iniTime == self.currentTime:
            self.readyUserProcesses.append(self.userProcesses[self.userProcessesAuxIdx])
            self.readyUserProcesses.sort(key=lambda x: x.priority)
            self.userProcessesAuxIdx += 1
        
        

    def PrintDispatcherProcess(self, processToPrint):
        print("dispatcher =>")
        print("\tPID: ", processToPrint.pid)
        print("\toffset: ", processToPrint.offset)
        print("\tblocks: ", processToPrint.qtdblocks)
        print("\tpriority: ", processToPrint.priority)
        print("\ttime: ", (processToPrint.timeToComplete - processToPrint.timeExecuted))
        print("\tprinters: ", processToPrint.printer)
        print("\tscanners: ", processToPrint.scanner)
        print("\tmodems: ", processToPrint.modem)
        print("\tdrivers: ", processToPrint.driver)
        print("")

        
        
    
