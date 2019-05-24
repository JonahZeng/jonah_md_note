最小二乘法计算多项式拟合
--------------------
# 公式
假设我们有6个点，根据这6个点拟合一条二阶曲线:

![](http://latex.codecogs.com/gif.latex?ax%5E%7B2%7D&plus;bx&plus;c%3Dy)

`a,b,c`是我们需要求的未知量，`x,y`各有6个数值，则我们计算过程如下：

![](http://latex.codecogs.com/gif.latex?A%20%3D%20%5Cleft%5B%20%5Cbegin%7Bmatrix%7D%20x%5B0%5D%5E%7B2%7D%20%26%20x%5B0%5D%20%26%201%20%5C%5C%20x%5B1%5D%5E%7B2%7D%20%26%20x%5B1%5D%20%26%201%20%5C%5C%20x%5B2%5D%5E%7B2%7D%20%26%20x%5B2%5D%20%26%201%20%5C%5C%20x%5B3%5D%5E%7B2%7D%20%26%20x%5B3%5D%20%26%201%20%5C%5C%20x%5B4%5D%5E%7B2%7D%20%26%20x%5B4%5D%20%26%201%20%5C%5C%20x%5B5%5D%5E%7B2%7D%20%26%20x%5B5%5D%20%26%201%20%5Cend%7Bmatrix%7D%20%5Cright%5D)

![](http://latex.codecogs.com/gif.latex?B%20%3D%20%5Cleft%5B%20%5Cbegin%7Bmatrix%7D%20y%5B0%5D%20%5C%5C%20y%5B1%5D%20%5C%5C%20y%5B2%5D%20%5C%5C%20y%5B3%5D%20%5C%5C%20y%5B4%5D%20%5C%5C%20y%5B5%5D%20%5Cend%7Bmatrix%7D%20%5Cright%5D)

根据最小二乘法公式可知：

![](http://latex.codecogs.com/gif.latex?%5Cleft%5B%5Cbegin%7Bmatrix%7Da%20%5C%5Cb%20%5C%5Cc%20%5Cend%7Bmatrix%7D%5Cright%5D%20%3D%20%28A%5E%7BT%7D*A%29%5E%7B-1%7D*A%5E%7BT%7D*B)

如果误差是服从正态分布的，则采用最小二乘法的结果是最准确的。这个公式稍稍变换一下：

![](http://latex.codecogs.com/gif.latex?%28A%5E%7BT%7D*A%29*%5Cleft%5B%5Cbegin%7Bmatrix%7Da%20%5C%5Cb%20%5C%5Cc%20%5Cend%7Bmatrix%7D%5Cright%5D%20%3D%20A%5E%7BT%7D*B)

对![](http://latex.codecogs.com/gif.latex?%28A%5E%7BT%7D*A%29)进行LU分解，然后解方程组即可得到`a,b,c`

不幸的是：在LU分解过程中可能会碰到主元为0，为了解决这个问题，需要进行换行挑选主元，换行实际上可以用乘一个置换矩阵的形式表达：

![](http://latex.codecogs.com/gif.latex?P*%28A%5E%7BT%7D*A%29*%5Cleft%5B%5Cbegin%7Bmatrix%7Da%20%5C%5Cb%20%5C%5Cc%20%5Cend%7Bmatrix%7D%5Cright%5D%20%3D%20P*A%5E%7BT%7D*B)
# python代码示例
如下代码演示了分别使用numpy自带的polyfit函数计算$a,b,c$以及使用最小二乘法公式手动计算`a,b,c`，它们的运算结果完全一致：

```python
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
	rows, cols = A.shape
	s = (rows if rows<cols else cols)
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

def plu_comp(A):
	'''
	PLU分解
	'''
	rows, cols = A.shape
	s = (rows if rows<cols else cols)
	P = np.zeros((rows, ), np.int)
	for i in range(rows):
		P[i] = i
	for k in range(s):
		p_update(A, k, rows, P)
		x = 1.0/p_ref(A, k, k, P)
		for i in range(k+1, rows):
			y = p_ref(A, i, k, P)*x
			p_set(A, i, k, P, y)
		for i in range(k+1, rows):
			for j in range(k+1, cols):
				y = p_ref(A, i, j, P) - p_ref(A, i, k, P)*p_ref(A, k, j, P)
				p_set(A, i, j, P, y)
	print(A)
	B = np.zeros_like(A)
	for i in range(A.shape[0]):
		B[i] = A[P[i]]
	A = B
	print(A)
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
	return P, L, U


def p_update(A, k, rows, P):
	'''
	P作为一个col vector，在每次挑选主元的时候需要更新，确保挑选这一列的最大值作为主元
	'''
	max_val = 0.0
	max_index = 0
	for i in range(k, rows):
		x = abs(p_ref(A, i, k, P))
		if x>max_val:
			max_val = x
			max_index = i

	P[k], P[max_index] = P[max_index], P[k]

def p_ref(A, i, j, P):
	'''
	P记录行交换，A实际上并没有发生行交换，因此需要借助P来取值
	'''
	return A[P[i], j]

def p_set(A, i, j, P, val):
	'''
	P记录行交换，A实际上并没有发生行交换，因此需要借助P来赋值
	'''
	A[P[i], j] = val


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

	# L, U = lu_comp(mat_l)
	# L*U*x = A^T * B = vec_r
	# vec_r = np.zeros((mat_l.shape[0], ), dtype=np.float)
	# for i in range(vec_r.shape[0]):
		# vec_r[i] = np.sum(A_tp[i, :] * B)

	P, L, U = plu_comp(mat_l)
	vec_r = np.zeros((mat_l.shape[0], ), dtype=np.float)
	for i in range(vec_r.shape[0]):
		vec_r[P[i]] = np.sum(A_tp[i, :] * B)
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
```

# 运行结果
![run](https://github.com/JonahZeng/jonah_md_note/blob/master/python/%E6%9C%80%E5%B0%8F%E4%BA%8C%E4%B9%98%E6%B3%95/run.png)
![plot](https://github.com/JonahZeng/jonah_md_note/blob/master/python/%E6%9C%80%E5%B0%8F%E4%BA%8C%E4%B9%98%E6%B3%95/figure_0.png)
