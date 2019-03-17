# 函数指针
```c++
void swap(int);//函数原型声明

void (*p)(int );//函数指针声明

p=swap;
//使用函数指针的函数如何声明？

void doSwap(void(*p)(int));
```
# 函数模板
## sample code
以下代码介绍如何定义函数模板以及函数模板的重载
```c++
#include <stdio.h>
//交换两个值
template <class T>//可以使用关键字typename代替class
void swap(T& a,T& b)
{
	T temp=b;
	b=a;
	a=temp;
	
}
//交换2个数组之间的值
template <class T>                //模板重载swap，应用不同的算法
void swap(T* ptr1,T* ptr2,int count)
{
	for(int i=0;i<count;i++)
	{
		T temp;
		temp=ptr2[i];
		ptr2[i]=ptr1[i];
		ptr1[i]=temp;
	}
}

int main()
{
	int a=3,b=5;
	double i=2.34,j=9.34;
	printf("origin intger value a=%d,b=%d\n",a,b);
	swap(a,b);  //两个参数，使用第一个模板
	printf("after swap ,a=%d,b=%d\n",a,b);
	
	printf("origin double value i=%.4lf,j=%.4lf\n",i,j);
	swap(i,j);  //两个参数，使用第一个模板
	printf("after swap ,i=%.4lf,j=%.4lf\n",i,j);
	
	int array1[5]={1,2,3,4,5};
	int array2[5]={5,4,3,4,1};
	printf("before swap,array1[5]=%d,%d,%d,%d,%d,array2[5]=%d,%d,%d,%d,%d\n",array1[0],array1[1],array1[2],array1[3],array1[4],array2[0],array2[1],array2[2],array2[3],array2[4]);
	swap(array1,array2,5);  //使用第二个模板
	printf("after swap,array1[5]=%d,%d,%d,%d,%d,array2[5]=%d,%d,%d,%d,%d\n",array1[0],array1[1],array1[2],array1[3],array1[4],array2[0],array2[1],array2[2],array2[3],array2[4]);
	return 0;
}
```
最新的C++标准支持显式具体化，当编译器发现函数名有多个版本并且参数个数，类型无法区分时（比如常规版本，显式具体化版本，常规模板版本都存在），优先级：常规版本>显式具体化>模板；显式具体化示例：
```c++
struct p{
char name[40];
float salary;
};
//我们只想交换salary成员，不想交换name，这样的话，之前定义的swap模板无法做到这个功能；
//这个时候仍然保留之前的swap模板，针对这个需求，可以使用显式具体化函数模板
template<> swap<p>(p& p1,p& p2)
{
   float temp;
   temp=p2.salary;
   p2.salary=p1.salary;
   p1.salary=temp;
}
```
>然而，其实我感觉这是很傻逼的做法，使用编程语言应当尽量关注问题本身，而不应该耗费开发者相当多的精力在高深复杂的语法中，尤其是用其他简单的方式也可以实现相同的功能的时候

# 类模板
最简单也是最常用的一种类型，容器类,下面代码介绍了类模板声明的基本规则
```c++
#ifndef STACKTP_H
#define STACKTP_H

template <class T>
class Stack
{
private:
	enum{MAX=10};
	T items[MAX];
	int top;
public:
    Stack();
	bool isempty();
	bool isfull();
	bool push(const T& item);
	bool pop(T& item);
	
};

template <class T>
Stack<T>::Stack()
{
	top=0;
}

template <class T>
bool Stack<T>::isempty()
{
	return top==0;
}

template <class T>
bool Stack<T>::isfull()
{
	return top==MAX;
}

template <class T>
bool Stack<T>::push(const T& item)
{
	if(top<MAX)
	{
		items[top]=item;
		top++;
		return true;
	}
	else
		return false;
}

template <class T>
bool Stack<T>::pop(T& item)
{
	if(top>0)
	{
		item=items[--top];
		return true;
	}
	else
		return false;
}
#endif
```
使用类模板构造对象：
```c++
#include "head.h"
#include <iostream>
using namespace std;
int main()
{
	int squence[5]={0,1,2,3,4};
	Stack<int> nStack;    //这里使用了int来构造对象
	for(int i=0;i<5;i++)
	{
		bool pushsuccess=nStack.push(squence[i]);
		if(pushsuccess==false)
			break;
		else
		{
		    cout<<"push #"<<i<<" success !"<<endl;
		}
	}
	
	
	return 0;
}


```
## 多个参数类型的模板
```c++
template <class T1,class T2>
class Stack
{
....
};
```
