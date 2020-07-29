import tkinter as tk
from tkinter import messagebox

board= [[0 for i in range(9)] for j in range(9)]

class SimpleTableInput(tk.Frame):
    def __init__(self, parent):
        tk.Frame.__init__(self, parent)

        self._entry = {}
        self.rows = 9
        self.columns = 9

        # register a command to use for validation
        vcmd = (self.register(self._validate), "%P")

        # create the table of widgets
        for row in range(9):
            for column in range(self.columns):
                index = (row, column)
                e = tk.Entry(self, validate="key", validatecommand=vcmd,width="5",highlightcolor="red",selectbackground="cyan",justify="center")
                e.grid(row=row, column=column, stick="nsew")
                self._entry[index] = e
        # adjust column weights so they all expand equally
        for column in range(9):
            self.grid_columnconfigure(column)
        # designate a final, empty row to fill up any extra space
        self.grid_rowconfigure(9)
        #self.reset = tk.Button(self, text="Reset", command=self.reset, activebackground="cyan")


    def set(self):
        for row in range(9):
            for column in range(9):
                index = (row, column)
                self._entry[index].delete(0,"end")
                self._entry[index].insert(0, board[row][column])

    def reset(self):
        for row in range(9):
            for column in range(9):
                index = (row, column)
                self._entry[index].delete(0,"end")
                board[row][column]=0


    def get(self):
        '''Return a list of lists, containing the data in the table'''
        result = []
        for row in range(9):
            current_row = []
            for column in range(9):
                index = (row, column)
                current_row.append(self._entry[index].get())
                self._entry[index].delete(0, "end")
                self._entry[index].insert(0, board[row][column])
            result.append(current_row)

        return result


    def _validate(self, P): #Ensure range of entered values is between 1-9
        if P.strip() == "":
            return True

        try:
            f = int(P)
        except ValueError:
            self.bell()
            return False
        return True


class Solver:


    def backTrack(self,sudo):
        # print(board) uncomment this for checking how backtracking works
        find = self.empty(sudo)
        if not find:
            return True
        else:
            row, col = find

        for i in range(1, 10):
            if self.validity(sudo, i, (row, col)):
                sudo[row][col] = i  # check if valid and add
                if self.backTrack(sudo):
                    return True
                sudo[row][col] = 0
        return False

    def empty(self,sudo):
        for x in range(len(sudo)):
            for y in range(len(sudo[0])):
                if sudo[x][y] == 0:
                    return x, y
        return None


    def validity(self,sudo, number, pos):
        # Check Row
        for y in range(len(sudo[0])):  # column
            if sudo[pos[0]][y] == number and pos[1] != y:
                return False

        for y in range(len(sudo)):  # row
            if sudo[y][pos[1]] == number and pos[0] != y:
                return False

        box_x = pos[0] // 3
        box_y = pos[1] // 3
        for x in range(box_x * 3, box_x * 3 + 3):
            for y in range(box_y * 3, box_y * 3 + 3):
                if sudo[x][y] == number and (x, y) != pos:
                    return False
        return True

    def showSudo(self,sudo):
        for x in range(len(sudo)):
            if x % 3 == 0 and x != 0:
                print("- - - - - - - - - - - - - ")  # to separate every 3 rows

            for y in range(len(sudo[0])):
                if y % 3 == 0 and y != 0:
                    print(" | ", end="")  # doesnt print /n so that it doesnt do to second line
                if y == 8:
                    print(sudo[x][y])
                else:
                    print(str(sudo[x][y]) + " ", end="")

    def Overallvalidity(self, sudo, number, pos):
        # Check Row
        for y in range(len(sudo[0])):  # column
            if sudo[pos[0]][y] == number and pos[1] != y and number != 0:
                return False

        for y in range(len(sudo)):  # row
            if sudo[y][pos[1]] == number and pos[0] != y and number != 0:
                return False

        box_x = pos[0] // 3
        box_y = pos[1] // 3
        for x in range(box_x * 3, box_x * 3 + 3):
            for y in range(box_y * 3, box_y * 3 + 3):
                if sudo[x][y] == number and (x, y) != pos and number != 0:
                    return False
        return True


class Example(Solver,tk.Frame):
    def __init__(self, parent):
        tk.Frame.__init__(self, parent)
        self.table = SimpleTableInput(self)
        self.submit = tk.Button(self, text="Submit", command=self.on_submit, activebackground="cyan")
        self.reset1 = tk.Button(self, text="Reset", command=self.table.reset, activebackground="pink")
        self.table.pack(side="top", fill="both")
        self.submit.pack(side="bottom",fill="both")
        self.reset1.pack(side= "bottom",fill="both")

    def on_submit(self):
        # print(self.table.get())
        a = self.table.get()

        #print(a)
        for x in range(9):
            for y in range(9):
                if a[x][y] != '':
                    board[x][y] = int(a[x][y])
        #Solver.showSudo(self,board)


        flag = True
        for x in range(9):
            b = 1
            for y in range(9):
                if board[x][y]!=0:
                    if board[x][y]<1 or board[x][y]>9:
                        b = 0
                        flag = False
                        break
            if b != 1:
                break


        for x in range(9):
            a = 1
            for y in range(9):
                check = Solver.Overallvalidity(self,board,board[x][y], (x, y))
                #print(check)
                if check == False:
                    flag = False
                    #print("Not valid")
                    a = 0
                    break
            if a != 1:
                break



        #Solver.showSudo(self,board)
        if flag == True:
            Solver.backTrack(self,board)
            #print("Solved:")
            #Solver.showSudo(self,board)
            self.table.set()
        else:
            print("NOT VALID SUDOKU")
            messagebox.showerror("Error", "Not a Valid Sudoku")
            self.table.reset()



if __name__ == "__main__":
    print("Running Sudoku Solver")
    root = tk.Tk(className="Sudoku solver")
    root.geometry("415x270")
    Example(root).pack(side="top", fill="both")
    root.mainloop()
    print("Program Closed")



