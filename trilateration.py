import math
import numpy as np
from numpy import linalg
from numpy.core.numeric import NaN
# constant
rssi_ref = -45
n = 2.75
# b1_pos = [0, 0.3]
# b2_pos = [5.84, 2.5]
# b3_pos = [5.84, 4.5]
# b4_pos = [5.84, 6.5]
# b5_pos = [5.84, 8.5]
# b6_pos = [0, 11.64]
b1_pos = [0, 6]
b2_pos = [5.84, 6]
b3_pos = [3, 10]
b4_pos = [3, 2]
# b5_pos = [5.84, 8.5]
# b6_pos = [0, 11.64]

beacon_position = {
    "B1": b1_pos,
    "B2": b2_pos,
    "B3": b3_pos,
    "B4": b4_pos,
    # "B5": b5_pos,
    # "B6": b6_pos,
}


def calculate(rssi1, rssi2, rssi3, b_first, b_second, b_third):

    a = beacon_position[b_first]
    b = beacon_position[b_second]
    c = beacon_position[b_third]

    h1, k1 = a[0], a[1]
    h2, k2 = b[0], b[1]
    h3, k3 = c[0], c[1]

    exp1 = (rssi_ref - rssi1)/(10*n)
    exp2 = (rssi_ref - rssi2)/(10*n)
    exp3 = (rssi_ref - rssi3)/(10*n)
    d1 = math.pow(10, exp1)
    d2 = math.pow(10, exp2)
    d3 = math.pow(10, exp3)
    # print("RssiRef: ", rssi_ref)
    # print("Rssi1: ", rssi1)
    # print("Rssi2: ", rssi2)
    # print("Rssi3: ", rssi3)
    # print("D1: ", d1)
    # print("D2: ", d2)
    # print("D3: ", d3)
    # print("x1: ", h1)
    # print("x2: ", h2)
    # print("x3: ", h3)
    # print("y1: ", k1)
    # print("y2: ", k2)
    # print("y3: ", k3)
    # print("coefX1: ", 2*(h2-h1))
    # print("coefX2: ", 2*(h3-h1))
    # print("coefY1: ", 2*(k2-k1))
    # print("coefY2: ", 2*(k3-k1))
    # print("answer1: ", pow(d1, 2)-pow(d2, 2) -
    #       pow(h1, 2)+pow(h2, 2)-pow(k1, 2)+pow(k2, 2))
    # print("answer2: ", pow(d1, 2)-pow(d3, 2) -
    #       pow(h1, 2)+pow(h3, 2)-pow(k1, 2)+pow(k3, 2))
    # x_coeff1 = [[1, pow(d1, 2)-pow(h1, 2)-pow(k1, 2), -2*k1]]
    # x_coeff2 = [[1, pow(d1, 2)-pow(h1, 2)-pow(k1, 2), -2*k2]]
    # x_coeff3 = [[1, pow(d1, 2)-pow(h1, 2)-pow(k1, 2), -2*k3]]

    # coeff = [[1, -2*h1, -2*k1],
    #          [1, -2*h2, -2*k2],
    #          [1, -2*h3, -2*k3]]
    # constant = [[pow(d1, 2)-pow(h1, 2)-pow(k1, 2)], [pow(d2, 2) -
    #                                                  pow(h2, 2)-pow(k2, 2)], [pow(d3, 2)-pow(h3, 2)-pow(k3, 2)]]
    # coeff2 = [[1, -2*h1, -2*k1], [1, -2*h2, -2*k2], [1, -2*h3, -2*k3]]

    # matrix = [1, -2*h1, -2*k1, pow(d1, 2)-pow(h1, 2)-pow(k1, 2),
    #           1, -2*h2, -2*k2, pow(d2, 2)-pow(h2, 2)-pow(k2, 2),
    #           1, -2*h3, -2*k3, pow(d3, 2)-pow(h3, 2)-pow(k3, 2), ]

    A_matrix = np.array([[2*(h3-h1), 2*(k3-k1)], [2*(h3-h2), 2*(k3-k2)]])
    # A_matrix1 = np.array([[pow(d1, 2)-pow(d3, 2)-pow(h1, 2)+pow(h3, 2)-pow(k1, 2)+pow(k3, 2), 2*(
    #     k3-k1)], [pow(d2, 2)-pow(d3, 2)-pow(h2, 1)+pow(h3, 2)-pow(k2, 2)+pow(k3, 2), 2*(k3-k2)]])

    # A_matrix2 = np.array([[2*(h3-h1), pow(d1, 2)-pow(d3, 2)-pow(h1, 2)+pow(h3, 2)-pow(k1, 2)+pow(
    #     k3, 2)], [2*(h3-h2), pow(d2, 2)-pow(d3, 2)-pow(h2, 1)+pow(h3, 2)-pow(k2, 2)+pow(k3, 2)]])

    # A_matrix = np.array([[2*(h2-h1), 2*(k2-k1)], [2*(h3-h1), 2*(k3-k1)]])
    A_matrix1 = np.array([[pow(d1, 2)-pow(d2, 2)-pow(h1, 2)+pow(h2, 2)-pow(k1, 2)+pow(k2, 2), 2*(
        k2-k1)], [pow(d1, 2)-pow(d3, 2)-pow(h1, 1)+pow(h3, 2)-pow(k1, 2)+pow(k3, 2), 2*(k3-k1)]])

    A_matrix2 = np.array([[2*(h2-h1), pow(d1, 2)-pow(d2, 2)-pow(h1, 2)+pow(h2, 2)-pow(k1, 2)+pow(
        k2, 2)], [2*(h3-h1), pow(d1, 2)-pow(d3, 2)-pow(h1, 1)+pow(h3, 2)-pow(k1, 2)+pow(k3, 2)]])

    A_matrix.shape = (2, 2)
    # print("A_MATRIX: ", A_matrix)
    # print("A_MATRIX1: ", A_matrix1)
    # print("A_MATRIX2: ", A_matrix2)
    det_A = np.linalg.det(A_matrix)
    det_A1 = np.linalg.det(A_matrix1)
    det_A2 = np.linalg.det(A_matrix2)
    x = det_A1/det_A
    y = det_A2/det_A
    # x = round(det_A1/det_A, 2)
    # y = round(det_A2/det_A, 2)
    # print("DetA: ", det_A)
    # print("DetA1: ", det_A1)
    # print("DetA2:", det_A2)
    # print("x: ", x)
    # print("y: ", y)
    # x = round(x, 2)
    # y = round(y, 2)
    # if isinstance(x, float) and isinstance(y, float):
    #     if x <= 11 and y <= 11:
    #         return x, y
    #     # return x, y
    # else:
    #     return NaN, NaN
    # else:
    #     return NaN, NaN
    # if x <= 11 and y <= 11:
    #     return x, y
    return x, y

# result = calculate(-48, -61, -65, "B1", "B2", "B3")
# x,y = result
# print(x)
# print(y)
