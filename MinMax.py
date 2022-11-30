class MinMaxNuts:
    def __init__(self) -> None:
        self.MAX, self.MIN = 1_000, -1_000
        self.index = 1

    def minimax(self, depth, nodeIndex, maximizingPlayer,
                values, alpha, beta):
        if depth == 0:
            self.index += 2
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
        if piece == "S" or piece == "s":
            value = 10
        elif piece == "L" or piece == "l":
            value = 30
        elif piece == "H" or piece == "h":
            value = 60
        elif piece == "T" or piece == "t":
            value = 50
        elif piece == "Q" or piece == "q":
            value = 100
        elif piece == 'K' or piece == 'k':
            value = 200
        return value

    def getValueList(self, lauta, liikkeet):
        self.index = 1
        valList = []
        for position in range(1, len(liikkeet), 2):
            valList.append(self.getPieceValue(
                lauta[liikkeet[position][0][0]][liikkeet[position][0][0]]))
        return valList
