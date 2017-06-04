class Matrix:
    def __init__(self, m, n):
        if m <= 0 or n <= 0:
            raise ValueError("m and n must be > 0")
        self.matrix = []
        for i in range(m):
            self.matrix.append([])
            for j in range(n):
                self.matrix[i].append(0)
            
        self.m = m
        self.n = n
    
    def copy(self):
        matrix = Matrix(self.m, self.n)

        for i in range(self.m):
            for j in range(self.n):
                matrix[i,j] = self.matrix[i][j]
        return matrix

    def __str__(self):
        return str(self.matrix)
    
    def __getitem__(self, index):
        i, j = index
        return self.matrix[i][j]

    def __neg__(self):
        matrix = self.copy()
        for i in range(self.m):
            for j in range(self.n):
                matrix[i,j] = -matrix[i,j]
        return matrix
    
    def __setitem__(self, index, value):
        i, j = index
        self.matrix[i][j] = value

    def __add__(A, B):
        if A.m != B.m or A.n != B.n:
            raise Exception("Matricies must be same size")

        matrix = A.copy()
        for i in range(A.m):
            for j in range(A.n):
                matrix[i,j] += B[i,j]
        return matrix

    def __sub__(A, B):
        return A + -B
    
    def __mul__(A, B):
        matrix = None
        if type(B) is int or type(B) is long:
            matrix = A.copy()
            for i in range(A.m):
                for j in range(A.n):
                    matrix.matrix[i][j] *= B
        else:
            if A.n != B.m:
                raise Exception("Not compatible for Matrix Multiplication")
            matrix = Matrix(A.m, B.n)
            for i in range(matrix.m):
                for j in range(matrix.n):
                    for k in range(A.n):
                        matrix[i,j] = matrix[i,j] + A[i,k]*B[k,j]
        return matrix

    def __mod__(A, mod):
        matrix = A.copy()
        for i in range(A.m):
            for j in range(A.n):
                matrix[i,j] = matrix[i,j] % mod
        return matrix

    def identity(self, n):
        identity = Matrix(n,n)
        for i in range(n):
            identity[i,i] = 1
        return identity
    
    def determinate(self):
        return self[0,0]*self[1,1]-self[0,1]*self[1,0]

    def inverse(self):
        matrix = Matrix(2,2)
        matrix[0,0] = float(self[1,1])/float(self.determinate())
        matrix[1,1] = float(self[0,0])/float(self.determinate())
        matrix[0,1] = -float(self[0,1])/float(self.determinate())
        matrix[1,0] = -float(self[1,0])/float(self.determinate())
        return matrix

if __name__ == "__main__":
    A = Matrix(3,3)
    B = Matrix(3,3)
    C = Matrix(3,3)
    for i in range(3):
        for j in range(3):
            A[i,j] = float(input())
    print(A)
    for i in range(3):
        for j in range(3):
            B[i,j] = float(input())
    for i in range(3):
        for j in range(3):
            C[i,j] = float(input())
    print(A*B*C)
