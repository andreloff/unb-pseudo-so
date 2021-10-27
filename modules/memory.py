class MemoryManager:
    def __init__(self, size):
        self.memSize = size

        self.memory = []
        for i in range(size):
            self.memory.append('0')

        self.fileTable = {}

    def AllocateMemory(self, size):
        alocSize = 0
        for idx in range(self.memSize):
            if self.memory[idx] == '0':
                alocSize += 1
                if alocSize == size:
                    return idx + 1 - alocSize
            else:
                alocSize = 0
        return -1

    def SetFileInMemory(self, fileName, memIdx, fileSize):
        if self.fileTable.get(fileName, -1) == -1:
            self.fileTable[fileName] = memIdx
        else:
            print("FALHA NA CRIACAO. ARQUIVO ", fileName, " JA EXISTE")
            return
  
        for offset in range(fileSize):
            self.memory[memIdx + offset] = fileName
            
    def SetFileInMemory(self, fileDescription):
        if self.fileTable.get(fileDescription[0], -1) == -1:
            self.fileTable[fileDescription[0]] = int(fileDescription[1])
        else:
            print("FALHA NA CRIACAO. ARQUIVO ", fileDescription[0], " JA EXISTE")
            return
  
        for offset in range(int(fileDescription[2])):
            self.memory[int(fileDescription[1]) + offset] = fileDescription[0]
        
    def DeleteFileInMemory(self, fileName, processId):
        if self.fileTable.get(fileName, -1) == -1:
            print("FALHA NA REMOCAO. ARQUIVO ", fileName, " NAO EXISTE")
            return
        else:
            auxIdx = self.fileTable[fileName]
            self.fileTable[fileName] = -1

        while auxIdx < self.memSize :
            if self.memory[auxIdx] != fileName:
                return
            self.memory[auxIdx] == '0'
            auxIdx += 1

    def PrintMemory(self):
        for i in range(self.memSize):
            print(self.memory[i], " ", end='')
        print("")
        for i in range(self.memSize):
            print((i+1), " ", end='')
        print("")
        