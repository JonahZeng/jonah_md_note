# Goal

* 什么是线性混合，用于何处？
* 怎么使用addWeighted()？

# Theory

　　前面已经学到了一点基本的像素级操作，一个比较有趣的二元操作是线性混合操作：

$$g(x)=(1-α)f_{0}(x)+αf_{1}$$

α在0-1之间变化，这种操作用于两幅图像或者录像交叉融合。

# 示例代码
```c++
    #include <cv.h>
    #include <highgui.h>
    #include <iostream>

    using namespace cv;
    
    int main( int argc, char** argv )
    {
     double alpha = 0.5; double beta; double input;
    
     Mat src1, src2, dst;
    
     /// Ask the user enter alpha
     std::cout<<" Simple Linear Blender "<<std::endl;
     std::cout<<"-----------------------"<<std::endl;
     std::cout<<"* Enter alpha [0-1]: ";
     std::cin>>input;
    
     //alpha必须在0-1之间
     if( input >= 0.0 && input <= 1.0 )
       { alpha = input; }
    
     src1 = imread("../../images/LinuxLogo.jpg");    //**两张图片的大小类型需要一致**
     src2 = imread("../../images/WindowsLogo.jpg");
    
     if( !src1.data ) { printf("Error loading src1 \n"); return -1; }
     if( !src2.data ) { printf("Error loading src2 \n"); return -1; }
    
     /// Create Windows
     namedWindow("Linear Blend", 1);
    
     beta = ( 1.0 - alpha );
     addWeighted( src1, alpha, src2, beta, 0.0, dst);
    
     imshow( "Linear Blend", dst );
    
     waitKey(0);
     return 0;
    }
```    
`addWeighted( src1, alpha, src2, beta, 0.0, dst);`
addWeighted执行：
   $$ dst=src1*α+src2*β+γ $$
   
在上面例子里γ=0  。