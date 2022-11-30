class MinMaxNuts:
    def __init__(self, lauta, liikkeet=[]) -> None:
        self.lauta = lauta
        self.liikkeet = liikkeet
        self.MAX, self.MIN = 1_000, -1_000
        self.index = None

    def update(self, lauta, liikkeet):
        self.lauta = lauta
        self.liikkeet = liikkeet

    def minimax(self, depth, nodeIndex, maximizingPlayer,
                values, alpha, beta):
        if depth == 0:
            self.index = nodeIndex
            print(nodeIndex)
            return values[nodeIndex]
        if maximizingPlayer:
            best = self.MIN
            for i in range(0, 2):
                val = self.minimax(depth - 1, nodeIndex * 2 + i,
                                   False, values, alpha, beta)
                best = max(best, val)
                alpha = max(alpha, best)
                # Alpha Beta Pruning
                if beta <= alpha:
                    break
            return best
        else:
            best = self.MAX
            for i in range(0, 2):
                val = self.minimax(depth - 1, nodeIndex * 2 + i,
                                   True, values, alpha, beta)
                best = min(best, val)
                beta = min(beta, best)
                # Alpha Beta Pruning
                if beta <= alpha:
                    break
            return best

    def getPieceValue(self, piece):
        if (piece == " "):
            return 0
        value = 0
        if piece == "P" or piece == "p":
            value = 10
        elif piece == "N" or piece == "n":
            value = 30
        elif piece == "B" or piece == "b":
            value = 30
        elif piece == "R" or piece == "r":
            value = 50
        elif piece == "Q" or piece == "q":
            value = 90
        elif piece == 'K' or piece == 'k':
            value = 900
        return value

    def getValueList(self):
        valList = []
        for vector in self.liikkeet:
            valList.append(self.getPieceValue(
                self.lauta[vector[1]][vector[0]]))
        return valList
