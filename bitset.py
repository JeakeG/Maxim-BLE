class BitSet:
    def __init__(self, bitArray):
        bitArray.sort()
        self.bitArray = bitArray
    
    def toLongArray(self, startIndex, stopIndex):
        bitSet = []
        for bit in self.bitArray:
            if bit in range(48, 68):
                bitSet.append(bit)

        # bitSet = self.bitArray[startIndex:stopIndex]
        subSets = []
        while bitSet:
            tempSet = []
            [tempSet.append(x) for x in bitSet if x < 64]
            if tempSet:
                subSets.append(tempSet)

            for i in range(len(bitSet)):
                bitSet[i] -= 64
            
            bitSet = [x for x in bitSet if x >= 0]

        arr = []

        for set in subSets:
            binString = ''
            for i in range(64, -1, -1):
                if i in set:
                    binString += "1"
                else:
                    binString += "0"
            arr.append(int(binString, 2))
        
        return arr