# 列表，元祖，字典
1. 列表和字典是可变对象，元组是不可变对象（不可变指的是元组的元素指向对象不可更改，比如不可以指向另一个对象，但指向的对象本身可以改变，比如列表）
2. 列表增删查改----列表的方法如下：
`list1.copy(    list1.count(   list1.extend(    list1.index(
list1.insert(  list1.pop(     list1.remove(    list1.append(list1.reverse( list1.clear(   list1.sort(`

* copy()方法是一个浅复制，也就是说返回的列表和原列表引用同一片对象；
* count(value) -> integer -- return number of occurrences of value，不存在的value返回0；
* extend(iterable)方法和append()方法都是在列表末尾增加元素，但是extend()会把iterable的元素到插入原列表，而append则把iterable作为一个整体元素插入到末尾；
* index(value, [start, [stop]]) -> integer -- return first index of value.，如果不存在这个value，抛出异常；
* insert(index, object) -- 在index之前的位置插入object
* pop([index]) -> item -- remove and return item at index (default last).如果index超出范围抛出IndexError;
* remove(value) -> None -- 删除第一个value元素.如果value不存在抛出ValueError ；
* reverse()  --把当前列表排列颠倒
* clear() -> None -- remove all items
* sort(key=None, reverse=False) -> None                 ---key代表排序规则，可以是一个函数或者匿名函数
3. 元祖相比列表，不能增也不能删也不能改元素，只能访问,访问方式和列表相同。支持的方法有：
```python
    tuple.count()
    tuple.index()
```
以及下标方式访问。
4. 字典支持方法：`dic1.clear() dic1.copy() dic1.fromkeys() dic1.get() dic1.items() dic1.keys() dic1.pop() dic1.popitem() dic1.setdefault() dic1.update() dic1.values()`,items(),keys(),values()方法返回所有的key,value,itmes，组成列表的方式。
* clear()清除所有的items
* copy()返回一个浅复制的字典
* fromkeys(iterable, value=None, /) 生产一个新的字典，该字典的key从iterable获取，value等于指定的value
```python
    >>> dic1
    {'zeng': 18}
    >>> list1 = [1,2,3]
    >>> dic1.fromkeys(list1)
    {1: None, 2: None, 3: None}
    >>> dic1
    {'zeng': 18}
```
* D.get(k[,d]) -> D[k] if k in D, else d.  d defaults to None.
* D.pop(k[,d]) -> v, 删除key=k的键，并且返回对应的value，如果key不存在，则返回d，如果没有指定d,抛出keyError异常
* D.popitem() -> (k, v), remove and return some (key, value) pair as a 2-tuple; but raise KeyError if D is empty.
* D.setdefault(k[,d]) -> D.get(k,d), also set D[k]=d if k not in D
* D.update([E, ]**F) -> None.  Update D from dict/iterable E and F.
    If E is present and has a .keys() method, then does:  for k in E: D[k] = E[k]
    If E is present and lacks a .keys() method, then does:  for k, v in E: D[k] = v
    In either case, this is followed by: for k in F:  D[k] = F[k]
如果需要增加一个key-value，则直接dic[newkey] = value即可，要删除一对key-value，del dic[key]即可

4. 一个使用字典的实例，统计一个字符串当中各字符出现的个数：
```python
#! /usr/bin/python3
# coding = UTF-8
#请用户输入
strUsrInput = input("请输入任意字符串:")
print("您输入的是：%s"%strUsrInput)

#请求一个字典，key = 出现的字符，如果key出现一次，则value++
strDic = {}
for ch in strUsrInput:
         if ch in strDic.keys():
                 strDic[ch] += 1
         else:
                 strDic[ch] = 1
for key,value in strDic.items():
         print("%s:%d "%(key,value),end='')
print("")

```







