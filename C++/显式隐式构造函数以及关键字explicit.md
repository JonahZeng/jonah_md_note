# 什么是显式构造函数

首先要理解什么是隐式构造函数，并且弄清它的优缺点。
```c++
    #include <iostream>
    using std::cout;
    using std::endl;
    class complexNumbers 
    {
      double real, img;
    public:
      complexNumbers() : real(0), img(0) //默认构造函数，不带参数，自定义不带参数的构造函数后，编译器便不再去隐式的生成
      { }
      complexNumbers(const complexNumbers& c) //拷贝构造函数，如果类成员有指针成员，千万注意“浅复制”“深复制”
      { 
         real = c.real; img = c.img; 
      }
      complexNumbers(double r,double i)//一般构造函数，可以写多个参数个数不同，或者参数类型不同的构造函数
      {
        real=r;
        img=i;
      }
      //接受一个参数的构造函数，用于类型隐式转换------此种函数千万要注意
      complexNumbers( double r, double i = 0.0) 
      { 
        real = r; 
        img = i; 
      }
      friend void display(complexNumbers cx);
    };
    void display(complexNumbers cx)
    {
      cout<<"Real Part: "<<cx.real<<"Imag Part: "<<cx.img<<endl;
    }
    int main() 
    {
      complexNumbers one(1);                  //一个参数的构造函数
      complexNumbers five = 5;                //隐式转换，仍然使用一个参数的构造函数
      display(one);
      display(five);
      return 0;
    }
```    
# 杜绝隐式转换
　　由于存在隐式转换，上面的友元函数存在一个问题，比如`display(300);`，也许我们的本意是打印数字本身，结果编译器发现300不符合参数类型：`complexNumbers`，而正好有接受一个参数的构造函数`complexNumbers( double r, double i = 0.0)`，结果编译器构造一个临时对象传递给`dispaly()`，编译器不报错，此时容易产生歧义。由此对于接受一个参数的构造函数，应当在前面添加一个关键字**explicit**
```c++
      explicit complexNumbers( double r, double i = 0.0) 
      { 
        real = r; 
        img = i; 
      }
```
添加**explicit**后`complexNumbers five = 5`也将无法通过编译；
