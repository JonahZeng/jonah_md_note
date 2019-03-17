# map函数
请看如下例子：
```python
>>> def f(x):
...     return x**2
...
>>> list(map(f, [ x for x in range(10)]))
[0, 1, 4, 9, 16, 25, 36, 49, 64, 81]


>>> list(map(str, [1,2,3,4,5,6]))
['1', '2', '3', '4', '5', '6']
>>>
```
map的作用是把一个iterable对象的每一个元素传入一个函数中，返回一个iterator;
# reduce函数
reduce函数中指定的函数必须接收2个参数，并把返回结果和下一个参数继续运算，依次到最后一个参数：
```python
>>> def add(a,b):
...     return a+b
...
>>> from functools import reduce
>>> reduce(add, [1,2,3,4,5,6])
21
```

# 练习
1. 利用map()函数，把用户输入的不规范的英文名字，变为首字母大写，其他小写的规范名字。输入：['adam', 'LISA', 'barT']，输出：['Adam', 'Lisa', 'Bart']：
```
def capitalize_cus(name):
    return name.capitalize()
names = ['adam', 'LISA', 'barT']

names_out = list(map(capitalize_cus, names))
print(names_out)
```
2. Python提供的sum()函数可以接受一个list并求和，请编写一个prod()函数，可以接受一个list并利用reduce()求积：
```python
# _*_ coding = utf-8 _*_
from functools import reduce
def prod(L):
    return reduce(lambda x,y:x*y , L)

L1 = [1,2,3,4,5,-4]
print(prod(L1))
```
