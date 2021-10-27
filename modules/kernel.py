from modules.process import Process
from modules.process import ProcessManager
#from modules.memory import MemoryManager
from modules.file import FileManager
import sys

class Kernel:
    def __init__(self):
        self.processes = []
        self.operations = []

    def run(self):
        processFiles = sys.argv[1]
        systemFiles = sys.argv[2]
    
        with open(processFiles, 'r') as p:
            processesDesc = p.read().splitlines()
        #print(processesDesc)

        numProcesses = len(processesDesc)
        globalProcessMemoryOffset = 0

        for i in range(numProcesses):
            processesDesc[i] = processesDesc[i].replace(',', '')
            processDescription = []
            for value in processesDesc[i].split():
                processDescription.append(value)

            if globalProcessMemoryOffset == 0:
                newOffset = 0
            else:
                newOffset = globalProcessMemoryOffset + 1

            self.processes.append(Process(i, newOffset ,processDescription))
            globalProcessMemoryOffset += int(processDescription[3])

        processManager = ProcessManager(self.processes)
        processManager.Run()

        
        with open(systemFiles, 'r') as s:
            systemDesc = s.read().splitlines()

        i = 0
        while i < len(systemDesc):
            if i == 0:
                fileManager = FileManager(int(systemDesc[i]))
                i += 1
            elif i == 1:
                numPreFiles = int(systemDesc[i])
                for j in range(2, numPreFiles+2):
                    systemDesc[j] = systemDesc[j].replace(',', '')
                    preFileDescription = []
                    for value in systemDesc[j].split():
                        preFileDescription.append(value)
                    fileManager.SetFileInMemory(preFileDescription, -1)
                i += numPreFiles +1
            else:
                self.operations.append(systemDesc[i].replace(',', ''))
                i += 1

        fileManager.Run(self.operations, self.processes)
        





        