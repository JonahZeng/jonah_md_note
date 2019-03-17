# goal
---------------------
本节你将学习到：

*  访问像素值
*  使用0初始化一个矩阵
*  什么是 saturate_cast ，为什么它非常有用
*  学习一些很酷的关于像素转换的信息

# 图像处理
-----------

* 一般而言，图像处理接受一个或多个图像输入，输出一个最终的图像。
* 图像转换可视为如下两种：
　　　1.基于输入点本身进行转换
　　　2.基于输入点周边像素进行转换

# 像素值转换
---------

* 本节的处理方法，最终的输出值仅仅依赖于对应的输入值
* 类似的操作也适用于颜色调整以及其他转换

# 亮度，对比度调整
---------------------

* 2个常用的像素值处理方法是乘法和加（一个常数）：
$$ g(x)=αf(x)+β $$

*  α>0 和β通常被称做 gain  和bias（补偿）参数，在有些地方这两个参数又被认为分别控制对比度和亮度。
*  你可以认为`f(x)`是输入，`g(x)`是输出，用更浅显的表示方法：
$$g(i,j)=αf(i,j)+β$$
i,j分别表示了输入点在矩阵所处位置的2个坐标。


# 代码
接下来的代码执行：
$$g(i,j)=αf(i,j)+β$$
```c++
    #include <cv.h>
    #include <highgui.h>
    #include <iostream>
    
    using namespace cv;
    
    double alpha; /*对比度控制 */
    int beta;  /*亮度控制*/
    
    int main( int argc, char** argv )
    {
     
     Mat image = imread( argv[1] );  //读取指定的图像
     Mat new_image = Mat::zeros( image.size(), image.type() );   //matlab风格函数zero()，创建一个和输入图像类型，大小一致的图像，并初始化为0
    
     /// 初始化参数，接受用户输入
     std::cout<<" Basic Linear Transforms "<<std::endl;
     std::cout<<"-------------------------"<<std::endl;
     std::cout<<"* Enter the alpha value [1.0-3.0]: ";std::cin>>alpha;
     std::cout<<"* Enter the beta value [0-100]: "; std::cin>>beta;
    
     ///  new_image(i,j) = alpha*image(i,j) + beta
     //使用at()遍历所有的像素，使用的是Vec3b类型，直接使用[]操作符访问BGR
     for( int y = 0; y < image.rows; y++ )
        {
        for( int x = 0; x < image.cols; x++ )
            { 
             for( int c = 0; c < 3; c++ )
                {
                 new_image.at<Vec3b>(y,x)[c] =saturate_cast<uchar>( alpha*( image.at<Vec3b>(y,x)[c] ) + beta );
                }
            }
        }
    
     /// Create Windows
     namedWindow("Original Image", 1);
     namedWindow("New Image", 1);
    
     /// Show stuff
     imshow("Original Image", image);
     imshow("New Image", new_image);
    
     /// Wait until user press some key
     waitKey();
     return 0;
    }
```
上述代码使用了模板函数`saturate_cast<>()`来确保计算出来的值在0-255范围内。
如果你完全掌握了原理，可以直接使用`image.convertTo(new_image, -1, alpha, beta)`来替代for循环操作，这个函数更高效。
