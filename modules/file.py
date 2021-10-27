class FileManager:
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
            
    def SetFileInMemory(self, fileDescription, creatorPID):
        fileInfo = self.fileTable.get(fileDescription[0], [-1, -1])

        if fileInfo[0] == -1:
            self.fileTable[fileDescription[0]] = [int(fileDescription[1]), creatorPID]
        else:
            #arquivo ja existe
            return -1
  
        for offset in range(int(fileDescription[2])):
            self.memory[int(fileDescription[1]) + offset] = fileDescription[0]

        return 0


        
    def DeleteFileInMemory(self, fileName, processId):
        fileInfo = self.fileTable.get(fileName, [-1, -1])
        if fileInfo[0] == -1:
            #arquivo nao existe
            return -1
        elif processId != -1:
            
            if fileInfo[1] != processId:
                #processo nao tem permissao para deletar esse arquivo
                return -2
            else:
                auxIdx = self.fileTable[fileName][0]
                self.fileTable[fileName] = [-1, -1]
        else:
            auxIdx = self.fileTable[fileName][0]
            self.fileTable[fileName] = [-1, -1]

        while auxIdx < self.memSize :
            if self.memory[auxIdx] != fileName:
                return 0
            self.memory[auxIdx] = '0'
            auxIdx += 1
        return 0

    def PrintMemory(self):
        for i in range(self.memSize):
            print(self.memory[i], " ", end='')
        print("")
        for i in range(self.memSize):
            print(i, " ", end='')
        print("")

    def Run(self, operations, processes):
        print("Sistema de arquivos =>")

        opIdx = 1

        self.PrintMemory()

        for op in operations:
            opDescription = []
            #opDescription[0] = id processo
            #opDescription[1] = tipo operacao
            #opDescription[2] = nome do arquivo
            #opDescription[3] = se for criar, tamanho do arquivo a ser criado
            for value in op.split():
                opDescription.append(value)
            
            if int(opDescription[0]) >= len(processes):
                print("Operacao ", opIdx, " => Falha")
                print("O processo ", opDescription[0], " nao existe.")
            else:
                #processo existe
                if int(opDescription[1]) == 0:
                    #criar arquivo
                    memoryOffset = self.AllocateMemory(int(opDescription[3]))
                    if memoryOffset == -1:
                        print("Operacao ", opIdx, " => Falha")
                        print("O processo ", opDescription[0], " nao pode criar o arquivo ", opDescription[2], " (falta de espaco).")
                    else:
                        #fileDesc[0] = nome arquivo
                        #fileDesc[1] = idx do primeiro bloco de memoria
                        #fileDesc[2] = tamanho do arquivo
                        fileDesc = [opDescription[2], memoryOffset, int(opDescription[3])]

                        creationResult = self.SetFileInMemory(fileDesc, int(opDescription[0]))
                        if creationResult == 0:
                            print("Operacao ", opIdx, " => Sucesso")
                            print("O processo ", opDescription[0], "criou o arquivo ", opDescription[2], " (blocos ", end='')
                            for i in range(int(opDescription[3])):
                                if i == int(opDescription[3]) -2:
                                    #penultimo
                                    print(i + memoryOffset, " e ",end='')
                                elif i == int(opDescription[3]) -1:
                                    #ultimo
                                    print(i + memoryOffset, ").")
                                else:
                                    print(i + memoryOffset, ", ",end='')
                            self.PrintMemory()
                        else:
                            print("Operacao ", opIdx, " => Falha")
                            print("O processo ", opDescription[0], " nao pode criar o arquivo", opDescription[2], " (arquivo ja existe).")
                else:
                    #deletar arquivo
                    deleteResult = 0
                    priori = int(processes[int(opDescription[0])].priority)

                    if priori == 0:
                        #se for processo de tempo real, nao importa quem criou o arquivo, ele pode ser deletado
                        deleteResult = self.DeleteFileInMemory(opDescription[2], -1)
                    else:
                        deleteResult = self.DeleteFileInMemory(opDescription[2], int(opDescription[0]))
                    
                    if deleteResult == 0:
                        print("Operacao ", opIdx, " => Sucesso")
                        print("O processo ", opDescription[0], " deletou o arquivo ", opDescription[2], ".")
                        self.PrintMemory()
                    elif deleteResult == -1:
                        print("Operacao ", opIdx, " => Falha")
                        print("O processo ", opDescription[0], " nao pode deletar o arquivo ", opDescription[2], " porque ele nao existe.")
                    else:
                        print("Operacao ", opIdx, " => Falha")
                        print("O processo ", opDescription[0], " nao pode deletar o arquivo ", opDescription[2], " porque ele nao possui permissao.")
            opIdx += 1
            print("")
        