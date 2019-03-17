## 目标
回答如下问题：

* 如何遍历图像所有的像素？
* opencv 的矩阵数据如何存储？
* 如何测量算法的效率？
* 什么是lookup table ？为什么要使用它？


## 色域缩减问题
　　试着设想一种算法，它用来缩减色域范围。使用unsigned char来存储，每个通道有多达256个数值，对于3通道图像，则总共可以表现大约1600色。处理如此多的色彩给算法带来很重的压力，然而，有时候，可以用小很多的运算量来达到相同的效果。

　　很当然的，我们要进行色域缩减。我们可以把当前的像素值用一个值来划分，比如0-9的像素都归为0，10-19的像素都归为10，依此类推。
当你把unsigned char除以一个int值，得到的值仍然是char，同时小数部分被丢弃，用数学表达式表示：
$$ I_{new}=\frac{I_{old}}{10}*10$$
　　now,这个简单的色域算法需要遍历所有的像素然后做一次除法和乘法，这种做法太血腥并且是不值得的，应当尽可能的使用更轻巧的操作，比如加法，减法，赋值操作。
　　因此，预先列出所有的可能值是很明智的，这样的话，只需要赋值操作即可，使用lookup table可以做到。lookup table是一个数组，接受给定的输入值，即可查找到输出值。这样就不需要任何计算，只要读取结果就好了。
　　测试代码做如下动作：接受一组参数（包括图像文件名，除数），把给定的除数做计算得到lookup table。目前opencv有三种主要的遍历像素方法，我们将把每个方法都用一遍并分别计算它们消耗的时间。
```c++
    int divideWith = 0; 
    stringstream s;
    s << argv[2];      //接收参数，指定除数
    s >> divideWith;
    if (!s || !divideWith) //除数不能小于0
    {
        cout << "Invalid number entered for dividing. " << endl;
        return -1;
    }

    uchar table[256];
    for (int i = 0; i < 256; ++i)
       table[i] = (uchar)(divideWith * (i/divideWith));
```
这里使用了C++ stringstream 类进行字符串与int转换。然后应用前面的公式计算table。
　　另一个问题是如何计算消耗的时间。opencv提供2个函数：getTickCount()和getTickFrequency()，第一个函数返回调用此函数时的系统CPU计数，第二个函数返回每秒钟的CPU计数频率。所以计算消耗的时间就很简单了：
```c++
    double t = (double)getTickCount();
    // do something ...
    t = ((double)getTickCount() - t)/getTickFrequency();
    cout << "Times passed in seconds: " << t << endl;
```
## 图像矩阵数据在内存中的存储方式
如Mat类教程中所述，图像的大小取决于色彩系统，精确一点讲，取决于图像的通道数量。如下是灰阶单通道图像示意图：

![](http://docs.opencv.org/2.4.11/_images/math/146857cf7bb2f26ce5ef0b4ddff686cf6f945204.png)

这是RGB示意图：

![](http://docs.opencv.org/2.4.11/_images/math/b6df115410caafea291ceb011f19cc4a19ae6c2c.png)

注意排序方式BGR，不是RGB。在现代大多数情况下，内存都足够大，以致矩阵存储的方式是连续的，即一行接着一行，形成一个很大的连续存储区，这种存储方式有利于提高访问速度，你可以使用`isContinuous()`来判断是否连续存储，在下节中你可以找到这样的例子。

## 高效的遍历方式
执行层面，没有比C语言的[]操作符更高效的方式：
```c++
    Mat& ScanImageAndReduceC(Mat& I, const uchar* const table)
    {
         // accept only char type matrices
         CV_Assert(I.depth() != sizeof(uchar));
    
        int channels = I.channels();
    
        int nRows = I.rows;
        int nCols = I.cols * channels;
    
        if (I.isContinuous())
        {
            nCols *= nRows;
            nRows = 1;
        }
    
        int i,j;
        uchar* p;
        for( i = 0; i < nRows; ++i)
        {
            p = I.ptr<uchar>(i);
            for ( j = 0; j < nCols; ++j)
            {
                p[j] = table[p[j]];
            }
        }
        return I;
    }
```

　　这里我们只是简单的获取每一行起始位置的指针，然后遍历每一行。如果数据是连续存储的，我们仅仅需要获取一次指针，然后遍历全部。要格外小心，处理彩色图片，它有3个通道，所以遍历一行需要的运算量是3倍cols。
　　还有另外一种处理方式，Ｍat类的data成员指示了第一行第一列的地址，如果是NULL，则说明图片没有正确加载，检查这个指针是否为NULL是最简单的检查图片是否加载成功的方法。在连续存储的情况下，我们可以这样写遍历(灰阶图片单通道)：
```c++
    uchar* p = I.data;
    for( unsigned int i =0; i < ncol*nrows; ++i)
      *p++ = table[*p];
```      
## 安全（迭代器）遍历方式
在前面介绍的高效遍历方式中，传递正确的除数，处理行与行之间的地址间隙都是你的任务，然而，接下来介绍的安全方式将从你手中接管这些任务，你只需要获取矩阵的开始位置与结束位置，然后递增开始位置迭代器逐个访问。
```c++
    Mat& ScanImageAndReduceIterator(Mat& I, const uchar* const table)
    {
    // accept only char type matrices
    CV_Assert(I.depth() != sizeof(uchar));

    const int channels = I.channels();
    switch(channels)
    {
    case 1:
        {
            MatIterator_<uchar> it, end;
            for( it = I.begin<uchar>(), end = I.end<uchar>(); it != end; ++it)
                *it = table[*it];
            break;
        }
    case 3:
        {
            MatIterator_<Vec3b> it, end;
            for( it = I.begin<Vec3b>(), end = I.end<Vec3b>(); it != end; ++it)
            {
                (*it)[0] = table[(*it)[0]];
                (*it)[1] = table[(*it)[1]];
                (*it)[2] = table[(*it)[2]];
            }
        }
    }

    return I;
    }
```
彩色图片每列具有3个uchar分量，可以把它看做一个uchar矢量，opencv用Vec3b来代替，可以直接使用[]访问每一个分量。千万要记得，opencv的迭代器遍历每一行的所有列，并且自动跳转到下一行。所以如果你对彩色图片使用一个简单的uchar迭代器，那么你将只能访问B通道。
## 即时地址访问
　　不推荐使用如下这种方法，`at()`这个函数是设计用来获取或者修改图像中的某些像素，它的基本用法是传递你要访问的像素的坐标：第几列，第几行。通过前面的遍历方式，你可能注意到了了解遍历的元素类型是非常重要的。在如下的灰度图例子中你可以看到`at()`的用法：
　　
```c++
    Mat& ScanImageAndReduceRandomAccess(Mat& I, const uchar* const table)
    {
     // accept only char type matrices
     CV_Assert(I.depth() != sizeof(uchar));

      const int channels = I.channels();
      switch(channels)
      {
      case 1:
          {
              for( int i = 0; i < I.rows; ++i)
                  for( int j = 0; j < I.cols; ++j )
                      I.at<uchar>(i,j) = table[I.at<uchar>(i,j)];
                 break;
          }
      case 3:
          {
           Mat_<Vec3b>  _I = I;

           for( int i = 0; i < I.rows; ++i)
              for( int j = 0; j < I.cols; ++j )
                 {
                     _I(i,j)[0] = table[_I(i,j)[0]];
                     _I(i,j)[1] = table[_I(i,j)[1]];
                     _I(i,j)[2] = table[_I(i,j)[2]];
              }
           I = _I;
           break;
          }
      }

      return I;
    }
```
这个函数接收指定的的元素类型和坐标值，然后返回这个元素的值，这个值可以设定为常量或者非常量（当你需要改变这个值）。在debug模式下，程序会执行一项检查，检查输入的坐标是存在的并且是在图像坐标范围内。这种方法和第一种高效的方法相比唯一的区别在于，你必须不断的获取每一行的首地址然后用[]操作符去获取你要访问的那一列。
　　如果你需要倍乘lookup table，使用`at()`将会十分的繁琐，需要不断输入数据类型和关键字。opencv引入了`Mat_`类型来解决这个问题，使用之前，同样的，首先需要声明元素数据类型，在返回值方面，可以使用`()`快速的访问元素。更好的是：Mat_  和Mat可以方便的互相转换，上面关于彩色图像的这段代码已经演示了它的用法。值得说明的是，使用`at()`同样可以完成相同的操作，它仅仅是懒人的福音----可以少输入代码。

## 福利----core function
有一种更简便，输入量更少的方法来实现同样的目的。`LUT()`函数：
```c++
     Mat lookUpTable(1, 256, CV_8U);//创建
     uchar* p = lookUpTable.data;
     for( int i = 0; i < 256; ++i)
         p[i] = table[i];
```
然后调用函数(I是输入Mat  J是输出Mat)：
```c++
       LUT(I, lookUpTable, J);
```
## 执行效率
编译然后在自己的电脑上运行，如下是使用2560*1600彩色图片的执行结果，取的是上百次运行的平均值：

|方式           | 耗时              |
|---------------| :-------------------: |
| Efficient Way | 79.4717 milliseconds |
| Iterator      | 83.7201 milliseconds |
| On-The-Fly RA | 93.7878 milliseconds |
| LUT function  | 32.5759 milliseconds |


结论：尽可能使用opencv已经设计存在的函数，不要去重新设计相同的算法，执行最高效的是`LUT()`函数，因为这个函数通过Intel Threaded Building Blocks激活了多线程。如果你真的需要通过指针的方式去遍历图像，迭代器方式是最安全的，虽然它很慢。on-the-fly方式用于debug mode是很值得的（可以提示错误）。在release mode它可能会接近迭代器遍历方式，但是会牺牲安全性。迭代器又比on-the-fly安全性要好。