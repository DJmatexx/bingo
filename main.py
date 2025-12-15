import math
import random




uint = int # TODO: add uint from commons3
TODO = NotImplementedError




class BingoBoard():
    def __init__(self, width: int = 5, height: int = 5):
        """
        Takes width and height as arguments, can be filled with labels later using its .fill() method.
        Width & height each need to be at least 2.
        """
        
        if (width < 2):
            raise ValueError("width needs to be at least 2")
        if (height < 2):
            raise ValueError("height needs to be at least 2")
        
        self.width = width
        self.height = height
        self.totalBoardSize = self.width * self.height
        self.initAndClearFields()
        
        self.rowBingos = [
            BingoBean(
                parentBoard=self,
                indices=list(range(rowIndex * self.width, (rowIndex + 1) * self.width)), # example with width=height=5: [0,1,2,3,4] for rowIndex=0, [5,6,7,8,9] for rowIndex=1 etc.
                nickname=f"row {rowIndex}"
            ) for rowIndex in range(self.height)
        ]
        self.columnBingos = [
            BingoBean(
                parentBoard=self,
                indices=list(range(columnIndex, self.totalBoardSize, self.width)), # example with width=height=5: [0,5,10,15,20] for columnIndex=0, [1,6,11,16,21] for columnIndex=1 etc.
                nickname=f"column {columnIndex}"
            ) for columnIndex in range(self.width)
        ]
        minDimension = width if width <= height else height
        diagonalXOffset = diagonalYOffset = minDimension - 1
        downwardDiagonalDeltaStep = self.width + 1
        downwardDiagonalDeltaTotal = diagonalYOffset * downwardDiagonalDeltaStep # difference between the last and the first index of a diagonal - example with width=height=5: 24 (the only diagonal down spans from 0 to 0+24)
        self.downwardDiagonalBingos = [
            BingoBean(
                parentBoard=self,
                indices=list(range(topIndex, bottomIndex + 1, downwardDiagonalDeltaStep)),
                nickname=f"downward diagonal from {topIndex} to {bottomIndex}"
            ) for topIndex in range(self.totalBoardSize - downwardDiagonalDeltaTotal)
            if (self.yDistance(topIndex, (bottomIndex := topIndex + downwardDiagonalDeltaTotal)) == diagonalYOffset) # NOTE: could be optimized
        ]
        upwardDiagonalDeltaStep = self.width - 1
        upwardDiagonalDeltaTotal = diagonalYOffset * upwardDiagonalDeltaStep
        self.upwardDiagonalBingos = [
            BingoBean(
                parentBoard=self,
                indices=list(range(topIndex, bottomIndex + 1, upwardDiagonalDeltaStep)),
                nickname=f"upward diagonal from {bottomIndex} to {topIndex}" # NOTE: starting from bottom here for easier visual differentiation (example with width=height=5: "upward diagonal from 20 to 4")
            ) for topIndex in range(diagonalXOffset, self.totalBoardSize - diagonalXOffset - upwardDiagonalDeltaTotal)
            if (self.yDistance(topIndex, (bottomIndex := topIndex + upwardDiagonalDeltaTotal)) == diagonalYOffset) # NOTE: could be optimized
        ]
        
        xCenter: float = (self.width - 1) / 2
        yCenter: float = (self.height - 1) / 2
        # NOTE: the following creates a list of the (1 to 4) central field indices on the board by intersecting the central (1 to 2) columns with the central (1 to 2) rows
        self.freeSpaceCandidates = list(
            (
                set(self.rowBingos[math.floor(yCenter)].indices) |
                set(self.rowBingos[math.ceil(yCenter)].indices)
            ) &
            (
                set(self.columnBingos[math.floor(xCenter)].indices) |
                set(self.columnBingos[math.ceil(xCenter)].indices)
            )
        )
    
    
    # CHECK: needed?
    def columnIndexOfField(self, index: uint) -> uint:
        if (index >= self.totalBoardSize):
            raise IndexError(f"index {index} is out of bounds of the board")
        return index % self.width
    
    def rowIndexOfField(self, index: uint) -> uint:
        if (index >= self.totalBoardSize):
            raise IndexError(f"index {index} is out of bounds of the board")
        return math.floor(index / self.width)
    
    # CHECK: needed?
    def xDistance(self, index1: uint, index2: uint) -> int:
        return self.columnIndexOfField(index2) - self.columnIndexOfField(index1)
    
    def yDistance(self, index1: uint, index2: uint) -> int:
        return self.rowIndexOfField(index2) - self.rowIndexOfField(index1)
    
    
    def initAndClearFields(self):
        self.fields: list = [False] * self.totalBoardSize
        self.labels: (list | None) = None
        self.labelPrintSize: uint = 0
    
    
    def fill(self, labels: list[str], isRandomizeEnabled: bool = True, freeSpaceText: str = 'BINGO'):
        """
        If less labels are provided than the total amount of fields on the board, the remaining fields will be filled with FREE-BINGO-SPACEs.
        This cannot be more than 1 for an ODDxODD board, 2 for an ODDxEVEN / EVENxODD board, and 4 for an EVENxEVEN board.
        """
        
        self.initAndClearFields()
        
        labelsAmt = len(labels)
        freeSpacesAmt = self.totalBoardSize - labelsAmt
        maxFreeSpacesAmt = len(self.freeSpaceCandidates)
        if (freeSpacesAmt < 0):
            raise ValueError(f"The label list provided has length {labelsAmt}, but the board only has {self.totalBoardSize} fields.")
        if (freeSpacesAmt > maxFreeSpacesAmt):
            raise ValueError(f"The label list provided has length {labelsAmt}, leaving {freeSpacesAmt} free spaces, but a board with dimensions {self.width}x{self.height} should have at most {maxFreeSpacesAmt}.")
        freeSpaceIndices: list = sorted(random.sample(self.freeSpaceCandidates, freeSpacesAmt)) # NOTE: indices need to be in ascending order, s.t. free spaces remain at the position they were inserted.
        
        if isRandomizeEnabled:
            random.shuffle(labels)
        
        for index in freeSpaceIndices:
            labels.insert(index, freeSpaceText)
            self.fields[index] = True
        
        maxLabelLength = max(len(repr(label)) for label in labels)
        self.labelPrintSize = math.ceil(math.sqrt(maxLabelLength))**2 # round up to nearest square
        
        self.labels = labels
    
    
    def __repr__(self):
        if (self.labels is None):
            return f"<empty BingoBoard with dimensions {self.width}x{self.height}>"
        return f"<BingoBoard with dimensions {self.width}x{self.height}>"
    
    def show(self):
        raise TODO




class BingoBean():
    def __init__(self, parentBoard: BingoBoard, indices: list[int], nickname: str):
        self.parentBoard = parentBoard
        self.indices = indices
        self.nickname = nickname
    
    def __getitem__(self, index: int) -> bool:
        return self.parentBoard.fields[self.indices[index]]
    
    def __setitem__(self, index: int, value: bool):
        self.parentBoard.fields[self.indices[index]] = value
    
    def __iter__(self):
        return (self.parentBoard.fields[index] for index in self.indices)
    
    def __repr__(self):
        return f"<BingoBean \"{self.nickname}\" | {list(self)}>"