import sys
import itertools

class Sudoku:

    def __init__(self, str_in=None, variation=False):
        if str_in is not None:
            if isinstance(str_in, list):
                self.puzzle = str_in
            else:
                self.read(str_in)
        else:
            self.puzzle = []
        self.variation = variation
    
    def __str__(self):
        out = ""
        for i in range(0, 9):
            for j in range(0, 9):
                out += str(self.get_entry(i,j))
                if j % 3 == 2:
                    out += " "
            out += "\n"
            if i % 3 == 2:
                out += "\n"
        return out
    
    def solved(self):
        return not 0 in self.puzzle
    
    def read(self, str_in):
        s = "".join(str_in.split())
        self.puzzle = []
        
        for i in range(0, len(s)):
            try:
                self.puzzle.append(int(s[i]))
            except ValueError:
                self.puzzle.append(0)
        if len(self.puzzle) > 81:
            self.puzzle = self.puzzle[:81]
        elif len(self.puzzle) < 81:
            self.puzzle += [0] * (81 - len(self.puzzle))
            
            
                    
    def row(self, r):
        return self.puzzle[9 * r: 9 * (r + 1)]
        
    def column(self, c):
        return self.puzzle[c::9]
    
    def block_at(self, i, j, as_list=True):
        out = []
        for k in range(0,3):
            out.append([])
            for l in range(0, 3):
                out[k].append(self.get_entry(i + k, j + l))
        
        if as_list:
            return out[0] + out[1] + out[2]
        
        return out
    
    def block(self, i, j, as_list=True):    
        return self.block_at(3 * i, 3 * j , as_list)    
    
    def var_block(self, i, j, as_list=True):
        if self.variation == False:
            return [0]

        if 0 < i < 4 and 0 < j < 4:
            return self.block_at(1,1,as_list)
        elif 0 < i < 4 and 4 < j < 8:
            return self.block_at(1,5,as_list)
        elif 4 < i < 8 and 0 < j < 4:
            return self.block_at(5,1,as_list)
        elif 4 < i < 8 and 4 < j < 8:
            return self.block_at(5,5,as_list)

        return [0]
    
    def get_entry(self, i, j):
        #return self.puzzle[i][j]
        return self.puzzle[9 * i + j]
        
    def set_entry(self, i, j, value):
        self.puzzle[9 * i + j] = value
        return value
    
    def pairs(self, collection, avoid):
        out = []
        for i in range(0, 8):
            for j in range(i+1, 9):
                if collection[i] == 0 and collection[j] == 0 and i != avoid and j != avoid:
                    out.append((i, j))
        return out
    
    def get_tuples(self, collection, length):
        """
        This gets all collecitons of tuples of squares that need to be
        filled in. It does not get rid of repetitions.
        """
        idxs = []
    
        for k in range(0, 9):
            if collection[k] == 0:
                idxs.append(k)

        if length > k:
            return None
        
        out = []
        
        ITP = itertools.product(idxs, repeat=length)
        for item in ITP:
            if len(item) == len(set(item)):
                # This just checks that we don't have something like (1,1), which would
                # be problematic.
                out.append(item)
        return out


    def choices_test(self, i, j):
        row = self.row(i)
                        
        for k in range(2, 4):
            tuples =  self.get_tuples(row, k)
            if tuples is None:
                break
                
            for item in tuples:
                idxs = []
                for num in item:
                    idxs += self.choices(i, num)
                print item, list(set(idxs))
            
    def choices_ind(self, i, j, depth=0):
        if depth == 1:
            return self.choices(i, j)
        
        pairs_r = self.pairs(self.row(i),j)
        
        print pairs_r
        
        for pair in pairs_r:
            choices_a = self.choices(i, pair[0])
            choices_b = self.choices(i, pair[1])
            
            print choices_a, choices_b
                        
            
            opts = list(set(choices_a + choices_b))
            
            if len(opts) == 2:
                return (pair, opts)
    
    def choices(self, i, j):
        """
        This will return a list of all of the possible numbers that
        could go in the (i,j)-th square.
        """
        opts = [1,2,3,4,5,6,7,8,9]
        
        if self.variation:
            R = list(set(self.row(i) + self.column(j) + self.block(i/3, j/3, True) + self.var_block(i, j, True)))
        else:
            R = list(set(self.row(i) + self.column(j) + self.block(i/3, j/3, True)))
        
        for k in R:
            if k in opts:
                opts.remove(k)
        
        if len(opts) == 1:
            # only one choice!
            pass
        
        return opts
    
    def rSolve(self):
        """
        This will recursively solve any solvable puzzle, I think.
        
        The only issue currently is that if you give it a puzzle that can
        not be solved, it should hang.
        """
        while 0 in self.puzzle:
            idx = self.puzzle.index(0)
            row = idx/9
            col = idx % 9
            
            choices = self.choices(row, col)
            
            if len(choices) == 0:
                return False
            
            for n in range(0, len(choices)):
                S = Sudoku(self.puzzle[:idx] + [choices[n]] + self.puzzle[idx + 1:])
            
                solved = S.rSolve()
            
                if solved != False:
                    break
            
            if solved == False:
                return False
                
            self.puzzle = solved
            
        return self.puzzle

    
    def solve(self):
        count = 0
        for i in range(0, 9):
            for j in range(0, 9):
                if self.get_entry(i,j) == 0:
                    choices = self.choices(i, j)
                    if len(choices) == 1:
                        self.set_entry(i,j,choices[0])
                        count += 1
        return count
           


def prompt(bad_file=False):
    pass

try:
    fname = sys.argv[1]
    if len(sys.argv) > 2:
        var = int(sys.argv[2])
    else:
        var = 0
    f = open(fname,"r")
    S = Sudoku(f.read())
    f.close()
except IndexError:
    sudoku = prompt()
except IOError:
    sudoku = prompt(True)

print str(S)

S.rSolve()

print str(S)

