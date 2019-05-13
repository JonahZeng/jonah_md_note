import numpy as np
import matplotlib.pyplot as plt
import seaborn
seaborn.set(style='darkgrid')

def polyfit2_np(x_in:np.ndarray, y_in:np.ndarray):
	if len(x_in.shape) != 1 or len(y_in.shape) != 1:
		raise ValueError('x and y must be one dim')
	if x_in.shape[0] != y_in.shape[0]:
		raise ValueError('x length != y length')
	return np.polyfit(x_in, y_in, 2)

# LU分解方阵
def lu_comp(A):
	row, col = A.shape
	s = (row if row<col else col)
	for k in range(s):
		for i in range(k+1, row):
			A[i, k] = A[i, k]/A[k, k]
		for i in range(k+1, row):
			for j in range(k+1, col):
				A[i, j] = A[i, j] - A[i, k]*A[k, j]
	L = np.zeros_like(A)
	U = np.zeros_like(A)
	s = (L.shape[0] if L.shape[0]<L.shape[1] else L.shape[1])
	for row in range(A.shape[0]):
		for col in range(A.shape[1]):
			if row>col:
				L[row, col] = A[row, col]
			else:
				U[row, col] = A[row, col]
	for i in range(s):
		L[i, i] = 1
	return L, U

def polyfit2_lsq(x_in:np.ndarray, y_in:np.ndarray):
	if len(x_in.shape) != 1 or len(y_in.shape) != 1:
		raise ValueError('x and y must be one dim')
	if x_in.shape[0] != y_in.shape[0]:
		raise ValueError('x length != y length')
	# A^T * A * x = A^T * B
	A = np.zeros((x_in.shape[0], 3), dtype=np.float)
	B = np.zeros((y_in.shape[0], ), dtype=np.float)
	for i in range(A.shape[0]):
		A[i, 0], A[i, 1], A[i, 2] = x_in[i]**2, x_in[i], 1
		B[i] = y_in[i]

	A_tp = np.zeros((A.shape[1], A.shape[0]), dtype=np.float)
	for i in range(A_tp.shape[0]):
		for j in range(A_tp.shape[1]):
			A_tp[i, j] = A[j, i]

	mat_l = np.zeros((A.shape[1], A.shape[1]), dtype=np.float)
	for i in range(mat_l.shape[0]):
		for j in range(mat_l.shape[1]):
			mat_l[i, j] = np.sum(A_tp[i, :]*A[:, j])

	L, U = lu_comp(mat_l)
	# L*U*x = A^T * B = vec_r
	vec_r = np.zeros((mat_l.shape[0], ), dtype=np.float)
	for i in range(vec_r.shape[0]):
		vec_r[i] = np.sum(A_tp[i, :] * B)

	# L*y = vec_r，解出y
	y = np.zeros((L.shape[0], ), dtype=np.float)
	for i in range(0, L.shape[0]):
		y[i] = vec_r[i]
		for j in range(0, i):
			y[i] = y[i] - L[i, j]*y[j]

	# U*x = y，解出x
	x = np.zeros_like(y)
	for i in range(x.shape[0]-1, -1, -1):
		x[i] = y[i]
		for j in range(x.shape[0]-1, i, -1):
			x[i] = x[i] - U[i, j]*x[j]
		x[i] = x[i]/U[i, i]
	# x就是最终的系数
	return x

x = np.arange(6)
y = 4*x**2 + 5*x + 7
# 人为加上一点误差
y1 = y + np.array([3.4, -2.02, 3.94, 2.09, -4.8, 3.6])

coff_lsq = polyfit2_lsq(x, y1)
print('最小二乘法手动计算结果：', coff_lsq)
# A^T * A * coff = A^T * B
coff_np = polyfit2_np(x, y1)
print('numpy自带的polyfit函数计算结果', coff_np)

x_i = np.linspace(0, 5, 50)
y_i = 4*x_i**2 + 5*x_i + 7
y2_i = coff_np[0]*x_i**2 + coff_np[1]*x_i + coff_np[2]

f = plt.figure(0)
ax = f.add_subplot(111)
ax.set_title('xxxx')
ax.plot(x_i, y_i, 'b-', label='$4x^2+5x+7$')
ax.scatter(x, y1, c='g', marker='o')
ax.plot(x_i, y2_i, 'r--', label='$%fx^2+%fx+%f$'%(coff_np[0], coff_np[1], coff_np[2]))
ax.legend()
plt.show()