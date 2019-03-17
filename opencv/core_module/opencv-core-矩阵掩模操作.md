# 矩阵掩模
----------
　　在opencv中，掩模操作是相对简单的。大致的意思是，通过一个掩模矩阵，重新计算图像中的每一个像素值。掩模矩阵控制了旧图像当前位置以及周围位置像素对新图像当前位置像素值的影响力度。用数学术语讲，即我们自定义一个权重表。
　　
## 测试程序
　　请先设想一个对比度增强算法(严格来说不属于传统的增强对比度，更像是锐化)，基本上我们会给图像中的每一个像素应用一个数学公式：
　　
![](./掩模.png)
　　　　　　
第一行使用了数学表达方式，第二行使用的是更紧凑的掩模矩阵表达方式，两者是一样的。这个掩模矩阵的作用：中心位置，即i=0并且j=0的位置，是你要重新计算的像素点，然后把图像的像素值与掩模矩阵对应位置的值相乘，结果即重新计算后的像素值。在大型图像处理中，第二种表示方法显然是更直观的。

## 基本方法
```c++
    void Sharpen(const Mat& myImage, Mat& Result)
    {
       CV_Assert(myImage.depth() == CV_8U);  //只接受8bit 图像
   
       Result.create(myImage.size(), myImage.type());  //构造输出Mat对象
       const int nChannels = myImage.channels();
   
       for(int j = 1; j < myImage.rows - 1; ++j)
       {
           const uchar* previous = myImage.ptr<uchar>(j - 1);
           const uchar* current  = myImage.ptr<uchar>(j    );
           const uchar* next     = myImage.ptr<uchar>(j + 1);
   
           uchar* output = Result.ptr<uchar>(j);
   
           for(int i = nChannels; i < nChannels * (myImage.cols - 1); ++i)
           {
               *output++ = saturate_cast<uchar>(5 * current[i]
                            -current[i - nChannels] - current[i + nChannels] - previous[i] - next[i]);
           }
       }

       Result.row(0).setTo(Scalar(0));//边界情况
       Result.row(Result.rows - 1).setTo(Scalar(0));
       Result.col(0).setTo(Scalar(0));
       Result.col(Result.cols - 1).setTo(Scalar(0));
     }
```
首先使用`CV_Assert`检查图像位深，如果条件为假则抛出异常。接着为输出Mat对象创建矩阵数据，获取输入图像的通道数量，是为了获取每一行究竟有多少子列。
　　然后首先获取输入图像前3行每一行的指针，previous current next  从current行开始遍历BGR-BGR-BGR，各通道是独立操作的，然后写入输出Mat  矩阵数据。最下面是边界4行都设置成0；
　　
## filter2D()
　　opencv已经设计了一个函数用于掩模操作，首先你需要自定义一个Mat_<>  ：
　　
```c++
    Mat kern = (Mat_<char>(3,3) <<  0, -1,  0,
                                   -1,  5, -1,
                                    0, -1,  0);
```                                    
调用方法，依次是输入Mat  输出Mat  位深，mask矩阵：
```c++
filter2D(I, K, I.depth(), kern);
```    
第五个参数可以设置mask矩阵的中心位置，第六个参数决定在操作不到的地方（边界）如何进行操作。使用这个函数最大的好处就是快。