# filter筛选
filter函数也接收2个参数，一个函数名，一个序列。不同于map的是，filter根据返回是true/false来决定是否抛弃这个元素。测试是否奇数：
```
def is_odd(n):
    return n % 2 == 1

list(filter(is_odd, [1, 2, 4, 5, 6, 9, 10, 15]))
# 结果: [1, 5, 9, 15]
```
# 练习，测试回数
回数就是从左到右，从右到左是相同的，比如191，282：
```
def isHS(n):
    m = str(n)
    length = len(m)
    idx = 0
    while idx < length//2:
        if m[idx] == m[length - 1 - idx]:
            idx += 1
            continue
        else:
            return False
    return True

L = filter(isHS, range(0,200))
print(list(L))
```