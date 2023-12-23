"""
这个程序是康康写的，将任意矩阵转换成简化的行阶梯形矩阵（RREF）
2023年3月9日编写
2023年10月26日更改

（吐槽一下：这以前写的什么玩意儿。。。看不懂了。虽然能正常工作，但是看着很不舒服，逻辑很复杂。）
（重写一份简洁的吧）

（必须再吐槽一下，重新编写了一遍，发现新代码思路和之前的一模一样。。。好吧我承认以前的思路挺好的😂）
"""

import numpy as np

'''
def choose_best_line(matrix: np.ndarray, index, start_row):
    for i, row in enumerate(matrix[start_row:], start_row):
        if row[:index].sum() > 0:
            continue
        if row[index] != 0:
            return i
    return None


def solve_problem(matrix: np.ndarray):
    current_row = 0
    for index in range(len(matrix[0]) - 1):
        best_line = choose_best_line(m, index, current_row)
        if best_line is None:
            # print("no best line", index, current_row)
            # print(matrix)
            continue
        # make the best line to be the first line
        interchange(matrix, best_line, current_row)
        # make the leading number to be one
        # print("\n\n", current_row, best_line)
        # print(matrix)
        matrix[current_row] /= matrix[current_row][index]
        # print("first to be one")
        # print(matrix)
        # make the rest of lines on the index to be zero
        for row in matrix[current_row + 1:]:
            factor = -row[index]
            row[:] += matrix[current_row] * factor
        # print("rest to be zero")
        # print(matrix)
        current_row += 1

    for current_row in range(len(matrix)-1, 0, -1):
        # find the index of leading one
        for i, item in enumerate(matrix[current_row]):
            if item == 1:
                index = i
                break
        else:
            continue
        # make the numbers above the leading one to be zero
        # print("\n\n", current_row, index)
        # print(matrix)
        # print("make numbers above to be zero")
        for row in matrix[current_row-1::-1]:
            factor = -row[index]
            row[:] += matrix[current_row] * factor
        # print(matrix)


def interchange(matrix: np.ndarray, line1, line2):
    temp = matrix[line1].copy()
    matrix[line1] = matrix[line2]
    matrix[line2] = temp


if __name__ == '__main__':
    m = np.array([
        [-0.9834,  0.    ,  0.33  , 0],
        [ 0.18  , -0.9834,  0.    , 0],
        [ 0.    ,  0.71  , -0.0434, 0]], dtype=np.float64)
    print("input")
    print(m)
    solve_problem(m)
    print("answer")
    print(m)
'''

"""
思路：先做REF，再做RREF

做REF：
从row=0到row=-1（-1指代最后一行）：
    在第row行到第-1行之间找到最适合当pivot row的那一行，将其挪到第row行
    将这一行的pivot化成1
    将第row+1行到-1行的所有行的这一列化成0

做RREF：
从row=-1到row=0：
    如果这一行有pivot，那就将上面的所有行的此列归零
    如果没有pivot就跳过
"""


def do_ref(matrix: np.ndarray):
    def find_best_row(matrix: np.ndarray, start_row) -> (int, int):
        """
        return the best row number and the pivot column number
        只在start_row到-1之间寻找best row
        best row指的是有非零元素最靠前的那一行
        """
        best_row = start_row
        best_pivot = matrix.shape[1]
        for row in range(start_row, matrix.shape[0]):
            for col in range(matrix.shape[1]):
                if abs(matrix[row, col]) > 1e-8:
                    pivot = col
                    break
            else:
                pivot = matrix.shape[1]
            if pivot < best_pivot:
                best_row = row
                best_pivot = pivot
        return best_row, best_pivot

    for row in range(matrix.shape[0]):
        # 找到最适合当pivot row的那一行，将其挪到上面
        best_row, pivot = find_best_row(matrix, row)
        if pivot == matrix.shape[1]:
            # 这种情况说明没有pivot row了
            break
        row_swap(matrix, row, best_row)
        # 将这一行的pivot变成1
        row_mul(matrix, row, 1/matrix[row, pivot])
        # 将这之后的所有行的这一列都变成0
        for row1 in range(row + 1, matrix.shape[0]):
            row_add(matrix, row1, row, -matrix[row1, pivot])
        #print(matrix)

    return matrix


def do_rref(matrix: np.ndarray):
    """
    注意这个默认matrix已经做过ref了
    """
    for row in range(matrix.shape[0]-1, 0, -1):
        # 找pivot
        for col in range(matrix.shape[1]):
            if abs(matrix[row, col]) > 1e-8:
                pivot = col
                break
        else:
            # 这里对应本行没有pivot的情况
            continue
        # 将上方的此列归零
        for row1 in range(row-1, -1, -1):
            row_add(matrix, row1, row, -matrix[row1, col])

    return matrix


def row_swap(matrix: np.ndarray, r1, r2):
    """
    交换两行。r1和r2是要交换的两行的indices。注意是从0开始计数的
    """
    temp = matrix[r1].copy()
    matrix[r1] = matrix[r2]
    matrix[r2] = temp
    return matrix


def row_mul(matrix: np.ndarray, row, k):
    """
    将其中的一行乘系数k
    """
    matrix[row] *= k
    return matrix


def row_add(matrix: np.ndarray, r1, r2, k):
    """
    将r2乘k加到r1上（注意改变的是r1的值而不是r2）
    """
    matrix[r1] += matrix[r2] * k
    return matrix


if __name__ == '__main__':
    # 修改下面这个矩阵，然后运行程序就能看到打印出来的结果了~
    A = [[0, 1, 2, 3],
         [-1, 1, 0, 3],
         [2, 0, -3, -7]]

    A = np.array(A, dtype=np.float64)
    do_ref(A)
    do_rref(A)
    np.set_printoptions(precision=6, suppress=True)
    print(A)
