import copy


def get_matrix_minor(matrix, size, row, column):
    minor = [[0 for x in range(size - 1)] for x in range(size - 1)]
    m_row, m_column = (0, 0)

    for i in range(size):
        if i != row:
            for j in range(size):
                if j != column:
                    minor[m_row][m_column] = matrix[i][j]
                    m_column += 1
            m_row += 1
            m_column = 0

    return minor


def get_matrix_determinant(matrix, size):
    if size == 2:
        determinant = matrix[0][0] * matrix[1][1] - matrix[0][1] * matrix[1][0]
        print(f"D({size}) = {matrix[0][0] * matrix[1][1]} - {matrix[0][1] * matrix[1][0]} = {determinant}")
    elif size == 3:
        determinant = (matrix[0][0] * matrix[1][1] * matrix[2][2]) + (matrix[0][1] * matrix[1][2] * matrix[2][0]) + (matrix[1][0] * matrix[2][1] * matrix[0][2]) - (
            matrix[0][2] * matrix[1][1] * matrix[2][0]) - (matrix[1][0] * matrix[0][1] * matrix[2][2]) - (matrix[1][2] * matrix[2][1] * matrix[0][0])
        print(f"D({size}) = {(matrix[0][0] * matrix[1][1] * matrix[2][2])} + {(matrix[0][1] * matrix[1][2] * matrix[2][0])} + {(matrix[1][0] * matrix[2][1] * matrix[0][2])} - {(matrix[0][2] * matrix[1][1] * matrix[2][0])} - {(matrix[1][0] * matrix[0][1] * matrix[2][2])} - {(matrix[1][2] * matrix[2][1] * matrix[0][0])} = {determinant}")
    elif size > 3:
        determinant = 0
        for column in range(size):
            minor_determinant = get_matrix_determinant(
                matrix=get_matrix_minor(matrix, size, 0, column), size=size-1)
            
            temp_determinant = (-1)**(1 + column + 1) * matrix[0][column] * minor_determinant
            determinant += (-1)**(1 + column + 1) * matrix[0][column] * minor_determinant
            print(f"D({column + 1}/{size}) = {(-1)**(1 + column + 1)} * {matrix[0][column]}({minor_determinant}) = {temp_determinant}")
        print(f"\nD{size} = {determinant}")
            
    return determinant


def get_matrix_addon(matrix, size, row, column):
    if size == 2:
        for i in range(size):
            if i != row:
                for j in range(size):
                    if j != column:
                        addon = (-1)**(row + column + 2) * matrix[i][j]
    else:
        addon = (-1)**(row + column + 2) * get_matrix_determinant(get_matrix_minor(matrix, size, row, column), size - 1)
        
    return addon


def get_opposite_matrix(matrix, size):
    print("Matrix determinant:")
    determinant = get_matrix_determinant(matrix, size)
    print("~" * 40)
    
    addons_matrix = [[0 for x in range(size)] for x in range(size)]
    for i in range(size):
        for j in range(size):
            addons_matrix[i][j] = get_matrix_addon(matrix, size, row=i, column=j)
            print(f"A({i + 1}{j + 1}) = {addons_matrix[i][j]}")
            print("~" * 40)
    
    trans_matrix = copy.deepcopy(addons_matrix)
    for i in range(size):
        for j in range(size):
            trans_matrix[j][i] = addons_matrix[i][j]
    
    opposite_matrix = copy.deepcopy(trans_matrix)
    for i in range(size):
        for j in range(size):
            if opposite_matrix[i][j] % determinant == 0:
                opposite_matrix[i][j] = trans_matrix[i][j] / determinant
            else:
                opposite_matrix[i][j] = f"({trans_matrix[i][j]}/{determinant})"
                
    print("A* = ", end="")
    for i in range(size):
        if i > 0:
            print(" " * 5, end="")
        for j in range(size):
            print(f"| {addons_matrix[i][j]} ", end="")
            
        print("|")
    
    print("A*T = ", end="")
    for i in range(size):
        if i > 0:
            print(" " * 6, end="")
        for j in range(size):
            print(f"| {trans_matrix[i][j]} ", end="")
        print("|")
        
    print("A(-1) = ", end="")
    for i in range(size):
        if i > 0:
            print(" " * 8, end="")
        for j in range(size):
            print(f"| {opposite_matrix[i][j]} ", end="")
        print("|")


def multiply_matrixes(f_matrix, s_matrix, f_size):
    result_list = []
    
    for i in range(f_size):
        result = 0
        for j in range(f_size):
            result += f_matrix[i][j] * s_matrix[j]
        result_list.append(result)

    return result_list


def multiply_matrix_by_num(matrix, num, size):
    result_matrix = copy.deepcopy(matrix)
    
    for i in range(size):
        for j in range(size):
            result_matrix[i][j] *= num
    
    return result_matrix


def main():
    matrix_size = 2
    matrix_size = 3
    matrix_size = 4
    
    a = [
        [10, 2],
        [1, 9]
    ]
    
    a = [
        [4, 8, 9],
        [11, 10, 2],
        [0, 1, 9]
    ]
    
    a = [
        [7, 3, 4, 12],
        [13, 4, 8, 9],
        [3, 11, 10, 2],
        [4, 0, 1, 9]
    ]

    b = [7, 14, 9, 1]
    
    print("=" * 40)
    print("Matrix determinant")
    print("-" * 40)
    get_matrix_determinant(a, matrix_size)
    print("=" * 40 + "\n")
    print("=" * 40)
    print("Opposite matrix")
    print("-" * 40)
    get_opposite_matrix(a, matrix_size)
    print("=" * 40)

    # matrix_size = int(input("Enter matrix size: "))
    # a = [[0 for x in range(matrix_size)]
    #      for x in range(matrix_size)]
    # b = []

    # for i in range(0, matrix_size):
    #     b.append(float(input(f"Enter {i + 1} b: ")))
    #     for j in range(0, matrix_size):
    #         a[i][j] = float(input(
    #             f"Enter {j + 1} element in {i + 1} row: "))


if __name__ == "__main__":
    main()