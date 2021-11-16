import copy
from math import floor


class matrix_():
    
    """
        Class that represents a square matrix with fields:
            .size
            .matrix
            
        You should use .__str__() instead of str() to
        get correct matrix representation
    """
    
    def __init__(self, size=3):
        self.size = size
        self.matrix = [[0 for x in range(size)] for x in range(size)]
    
    
    def __str__(self, margin=0):
        max_lengths_list = [0 for x in range(self.size)]
        for i in range(self.size):
            for j in range(self.size):
                if len(str(self.matrix[j][i])) > max_lengths_list[i]:
                    max_lengths_list[i] = len(str(self.matrix[j][i]))
                    
        for i in range(self.size):
            if i > 0:
                print(" " * margin, end="")
            for j in range(self.size):
                item = str(self.matrix[i][j])
                while len(item) < max_lengths_list[j]:
                    if len(item) <= max_lengths_list[j] - 2: 
                        item += " "
                    item = item.rjust(len(item) + 1)
                print(f"| {item} ", end="")
            
            print("|")


class shell_():
    
    """
        Class that represents fraction with fields:
            .top = denominator
            .bottom = divider
    """
    
    def __init__(self, top=0, bottom=0):
        self.top = top
        self.bottom = bottom
    
    
    def __str__(self):
        return f"({self.top}/{self.bottom})"
    
    
    def __len__(self):
        len(str(self))


def get_matrix_minor(matrix_orig, row, column):
    matrix = matrix_orig.matrix
    size = matrix_orig.size
    minor = matrix_(size - 1)
    m_row, m_column = (0, 0)
    
    for i in range(size):
        if i != row:
            for j in range(size):
                if j != column:
                    minor.matrix[m_row][m_column] = matrix[i][j]
                    m_column += 1
            m_row += 1
            m_column = 0

    return minor


def get_matrix_determinant(matrix_orig):
    size = matrix_orig.size
    matrix = matrix_orig.matrix
    
    if size == 2:
        determinant = matrix[0][0] * matrix[1][1] - matrix[0][1] * matrix[1][0]
        print(f"D({size}) = {matrix[0][0] * matrix[1][1]} - {matrix[0][1] * matrix[1][0]} = {determinant}")
    elif size == 3:
        determinant = (matrix[0][0] * matrix[1][1] * matrix[2][2]) + (matrix[0][1] * matrix[1][2] * matrix[2][0]) + (
            matrix[1][0] * matrix[2][1] * matrix[0][2]) - (matrix[0][2] * matrix[1][1] * matrix[2][0]) - (
            matrix[1][0] * matrix[0][1] * matrix[2][2]) - (matrix[1][2] * matrix[2][1] * matrix[0][0])
        print(f"D({size}) = {(matrix[0][0] * matrix[1][1] * matrix[2][2])} + {(matrix[0][1] * matrix[1][2] * matrix[2][0])} + {(matrix[1][0] * matrix[2][1] * matrix[0][2])} - {(matrix[0][2] * matrix[1][1] * matrix[2][0])} - {(matrix[1][0] * matrix[0][1] * matrix[2][2])} - {(matrix[1][2] * matrix[2][1] * matrix[0][0])} = {determinant}")
    elif size > 3:
        determinant = 0
        for column in range(size):
            minor_determinant = get_matrix_determinant(
                matrix_orig=get_matrix_minor(matrix_orig, 0, column))
            temp_determinant = (-1)**(column + 2) * matrix[0][column] * minor_determinant
            determinant += temp_determinant
            print(f"D({column + 1}/{size}) = {(-1)**(column + 2)} * {matrix[0][column]}({minor_determinant}) = {temp_determinant}")
        print(f"\nD({size}) = {determinant}")
            
    return determinant


def get_matrix_addon(matrix_orig, row, column):
    size = matrix_orig.size
    
    if size == 2:
        for i in range(size):
            if i != row:
                for j in range(size):
                    if j != column:
                        addon = (-1)**(row + column + 2) * matrix_orig.matrix[i][j]
    else:
        addon = (-1)**(row + column + 2) * get_matrix_determinant(get_matrix_minor(matrix_orig, row, column))
        
    return addon


def get_opposite_matrix(matrix_orig, determinant):
    size = matrix_orig.size
    addons_matrix = matrix_(size)
    
    for i in range(size):
        for j in range(size):
            addons_matrix.matrix[i][j] = get_matrix_addon(matrix_orig, row=i, column=j)
            print(f"A({i + 1}{j + 1}) = {addons_matrix.matrix[i][j]}")
            print("~" * 40)
    
    trans_matrix = copy.deepcopy(addons_matrix)
    for i in range(size):
        for j in range(size):
            trans_matrix.matrix[j][i] = addons_matrix.matrix[i][j]
    
    opposite_matrix = copy.deepcopy(trans_matrix)
    for i in range(size):
        for j in range(size):
            nums_after_dot = len(str((opposite_matrix.matrix[i][j] / determinant) - floor(opposite_matrix.matrix[i][j] / determinant))) - 2
            if nums_after_dot < 5:
                opposite_matrix.matrix[i][j] = trans_matrix.matrix[i][j] / determinant
            else:
                opposite_matrix.matrix[i][j] = shell_(trans_matrix.matrix[i][j], determinant)
                
    print("A* = ", end="")
    addons_matrix.__str__(5)
    
    print("\nA*T = ", end="")
    trans_matrix.__str__(6)
        
    print("\nA(-1) = ", end="")
    opposite_matrix.__str__(8)
        
    return opposite_matrix


def multiply_matrixes(f_matrix, s_matrix):
    
    """
        This function works only for solve eqution.
        s_matrix height must be equals f_matrix size 
    """
    
    f_size = f_matrix.size
    result_list = []
    
    for i in range(f_size):
        result = 0
        result_shell = shell_()
        result_str = ""
        result_str_f = ""
        isShell = False
        
        for j in range(f_size):
            if isinstance(f_matrix.matrix[i][j], shell_):
                s = f_matrix.matrix[i][j]
                b = s_matrix[j]
                result_shell.bottom = s.bottom
                result_shell.top += s.top * b
                result_str += f"({s.top}*{b}/{s.bottom}) "
                result_str_f += f"({s.top * b}/{s.bottom}) "
                isShell = True
            else: 
                result += (round(f_matrix.matrix[i][j] * s_matrix[j] * 100) / 100)
                result_str += f"({f_matrix.matrix[i][j]}*{s_matrix[j]}) "
                result_str_f += f"({round(f_matrix.matrix[i][j] * s_matrix[j] * 100) / 100}) "
        
        if isShell:
            if isinstance(result, int):
                result_list.append(result_str.strip().replace(" ", " + ") + f" = \n\t" + result_str_f.strip().replace(" ", " + ") + f" = {result_shell}")
            else:
                result_list.append(result_str.strip().replace(" ", " + ") + f" = \n\t" + result_str_f.strip().replace(" ", " + ") + f" = {result_shell} + {result}")        
        else:
            result_list.append(round(result * 100) / 100)

    return result_list


def multiply_matrix_by_num(matrix_orig, num):
    size = matrix_orig.size
    result_matrix = copy.deepcopy(matrix_orig)
    
    for i in range(size):
        for j in range(size):
            result_matrix.matrix[i][j] *= num
    
    return result_matrix


def solve_matrix_eqution(b_matrix, opp_matrix):
    answer_list = multiply_matrixes(opp_matrix, b_matrix)
    
    for answer in enumerate(answer_list):
        print(f"x({answer[0] + 1}) = {answer[1]}")
        print("~" * 40) 


def kramer(matrix_orig, matrix_b, determinant):
	size = matrix_orig.size
	determinants_list = [determinant]

	for i in range(size):
		temp_matrix = copy.deepcopy(matrix_orig)
		for j in range(size):
			temp_matrix.matrix[j][i] = matrix_b[j]
		
		print(f"∆({i + 1}) = ", end="")
		temp_matrix.__str__(7)
		determinants_list.append(get_matrix_determinant(temp_matrix))
		print("~" * 40)

	print("ANSWERS" + "\n" + "~" * 40)
	for i in range(1, len(determinants_list)):
         print(f"x({i}) = ({determinants_list[i]} / {determinants_list[0]}) = {round(determinants_list[i] / determinants_list[0] * 100) / 100}")
         print("~" * 40)
	

def main():
    # matrix_size = 2
    # matrix_size = 3
    # matrix_size = 4
    
    # a = matrix_(matrix_size)
    
    # a.matrix = [
    #     [10, 2],
    #     [1, 9]
    # ]
    
    # a.matrix = [
    #     [4, 8, 9],
    #     [11, 10, 2],
    #     [0, 1, 9]
    # ]
    
    # a.matrix = [
    #     [7, 3, 4, 12],
    #     [13, 4, 8, 9],
    #     [3, 11, 10, 2],
    #     [4, 0, 1, 9]
    # ]
    
    # b = [9, 1]
    # b = [14, 9, 1]
    # b = [7, 14, 9, 1]
    
    matrix_size = int(input("Enter matrix size: "))
    a = matrix_(matrix_size)
    b = []

    for i in range(matrix_size):
        b.append(int(input(f"Enter b{i + 1}: ")))
        for j in range(matrix_size):
            a.matrix[i][j] = int(input(
                f"Enter a{i + 1}{j + 1}: "))
    
    print("=" * 40)
    print("Matrix determinant".upper())
    print("-" * 40)
    d = get_matrix_determinant(a)
    print("=" * 40 + "\n")
    print("=" * 40)
    print("Opposite matrix".upper())
    print("-" * 40)
    opp = get_opposite_matrix(a, d)
    print("=" * 40 + "\n")
    print("=" * 40)
    print("Eqution".upper())
    print("-" * 40)
    solve_matrix_eqution(b, opp)
    print("=" * 40 + "\n")
    print("=" * 40)
    print("Kramer".upper())
    print("-" * 40)
    kramer(a, b, d)
    print("=" * 40)


if __name__ == "__main__":
    main()