# Mat类特征
opencv2.x版本引入Mat类来替代传统的CMat lpimage等C语言结构。

使用Mat对象可以不需要去手动分配和释放内存空间。
兼容C，除非从事嵌入式系统，否则没必要再去用lpimage等C语言结构。

如果传递一个已经分配内存的的Mat对象，则会被拒绝（传递对象而不是指针将给形参分配内存）。使用Mat类将使得尽可能少的使用内存空间来达到目标。

Mat类分为两部分：

* 1）矩阵头：包含矩阵大小，图像存储方式（维度），存储的位置信息（如单通道还是多通道）等信息；

* 2）指向矩阵的指针（* data）；

opencv是一个图像处理库，包含很多处理函数，通常会调用很多函数去实现目标，那么，传递**图像数据**给函数将是一种常态动作。

在opencv当中，每个mat对象都有自己的矩阵头，而data指针指向的数据是可以共享的。比如如下：

    Mat A, C;                                 // creates just the header parts
    A = imread(argv[1], CV_LOAD_IMAGE_COLOR); // here we'll know the method used (allocate matrix)
	Mat B(A);                                 // Use the copy constructor
	C = A;                                    // Assignment operator
	//通过A构造的B C对象和A对象共享一个矩阵数据区

以上的A B C对象拥有各自的矩阵头，但是共享一个矩阵数据，修改任何一个对象都会导致另2个同步变化。


有趣的是，你可以仅仅使用矩阵数据的一部分来手动创建一个Mat对象：

	Mat D (A, Rect(10, 10, 100, 100) ); // using a rectangle
	Mat E = A(Range::all(), Range(1,3)); // using row and column boundaries

对象D E仅仅创建了矩阵头，数据区仍然共用A的数据区。

## 多个对象如何释放公用的数据区
答案是最后一个被释放的对象释放矩阵数据。opencv使用一种计数机制，当用户复制一次矩阵头信息，计数器加1，当对象矩阵头被释放，计数器减1。当计数器等于0，矩阵数据区将被释放。

如果想完全复制数据区，opencv提供了两个函数`clone()`和`copyTo()`


	Mat F = A.clone();
	Mat G;
	A.copyTo(G);

如上代码，对象G F的数据区与A的数据区是独立的。


## 你应该牢记的
* opencv函数返回的数据区 内存分配是自动的
* 使用opencv C++ 接口的时候不需要去理会内存管理
* 使用赋值和拷贝构造函数，只会创建矩阵头，不会重新创建矩阵数据区
* 使用Mat的成员函数`clone()`，`copyTo()`可以复制一份矩阵数据。

## 数据存储方式

这里的数据存储方式，指的是如何存储pixel value。 比如选择色域，矩阵元素的数据类型。色域标示了用户如何拆分一个给定的颜色。最简单的是灰度图，只需要处理0-255。


对于彩色，我们有很多种色域来选择，每种色域都会把彩色信息分解成3或者4个分量，我们可以利用这些分量来新建其他颜色。最流行的当然是RGB色彩空间，主要是因为人眼对色彩的感知机制就是RGB混合方式。3个分量是R,G,B。有时候为了用代码描述透明图片，会引入第4个分量：alpha.


各种色彩空间优势如下：

* RGB最接近肉眼的对光谱的感知方式，主动发光设备比如显示器也使用RGB描述颜色。
* HSV HLS把颜色分解成色相，饱和度，明度，这种描述方式更接近大脑对颜色的辨识机制。
* YCrCb被应用于JPEG格式。
* Lab很奇特，如果你需要测量两个给定的颜色有多大差异，使用Lab方式很方便。


每个颜色分量都有各自的取值范围。这样就决定了我们该采用何种数据类型来存储。最小的数据类型是char，8bit。存储的时候可以设定为unsigned char，这样就可以存储0-255（RGB）或者设定为signed char，存储-128--127（LAB中的ab通道）。尽管在3维的色彩空间，已经可以描述1600万色，有时候我们可能会需要更大更精确的控制，这个时候我们需要使用float类型或者double类型来存储各个分量。然而，请记得，增加每个分量的大小，同时就会导致图片占用的空间变大。

## 显式创建Mat对象
为方便演示，我们使用Mat重载的操作符<<来演示（**<<只对二维数组有效**）。

尽管mat类作为图像容器表现很好，但其本质上仍然是一个数组类。所以我们可以创建一个对象并且操作多维数组。有多种方式去创建mat对象：

1. **Mat构造函数Mat()：**

	    Mat M(2,2, CV_8UC3, Scalar(0,0,255));
	    cout << "M = " << endl << " " << M << endl << endl;
![](http://docs.opencv.org/2.4.11/_images/MatBasicContainerOut1.png)
    
对于2维多通道的图像，首先指定行数(rows)，列数（cols），然后指定颜色分量的位深，每个像素有几个通道，opencv预定义了一些宏，规则如下：

      CV_[The number of bits per item][Signed or Unsigned][Type Prefix][The channel number]
      //CV_[分量位深][无符号or有符号][数据类型前缀][通道数量]

opencv预定义的宏最大支持4通道，Scalar是4成员的short类型vector,使用scalar可以初始化所有的矩阵元素为同一个值；如果需要更多类型，使用如上的宏并在末尾的括号内注明通道数量；
2. **使用带数组参数的构造函数：**

          int sz[3] = {2,2,2};
          Mat L(3,sz, CV_8UC(1), Scalar::all(0));
          //    矩阵维度，每个维度的容量，数据类型，元素值
这个例子的Mat()构造函数，首先传递矩阵维度，然后是每个维度的容量，接着是数据类型，最后是元素值。
3. **利用已经存在的lpimage指针**

        IplImage* img = cvLoadImage("greatwave.png", 1);
        Mat mtx(img); // convert IplImage* -> Mat
4. **create()函数**

        M.create(4,4, CV_8UC(2));
        cout << "M = "<< endl << " "  << M << endl << endl;
        
输出：![](http://docs.opencv.org/2.4.11/_images/MatBasicContainerOut2.png)

create()函数不能初始化元素值，只会在矩阵大小和之前不同时重新分配内存。
5. **MATLAB风格函数指定元素值以及数据类型**
如下：

        Mat E = Mat::eye(4, 4, CV_64F);
        cout << "E = " << endl << " " << E << endl << endl;

        Mat O = Mat::ones(2, 2, CV_32F);
        cout << "O = " << endl << " " << O << endl << endl;

        Mat Z = Mat::zeros(3,3, CV_8UC1);
        cout << "Z = " << endl << " " << Z << endl << endl;
        
![](http://docs.opencv.org/2.4.11/_images/MatBasicContainerOut3.png)
6. **对于小规模的矩阵，使用逗号分割，直接复制：**

        Mat C = (Mat_<double>(3,3) << 0, -1, 0, -1, 5, -1, 0, -1, 0);
        cout << "C = " << endl << " " << C << endl << endl;
![](http://docs.opencv.org/2.4.11/_images/MatBasicContainerOut6.png)
7. **创建一个矩阵头然后用clone()和copyTo()复制数据**

        Mat RowClone = C.row(1).clone();
        cout << "RowClone = " << endl << " " << RowClone << endl << endl;
        
![](http://docs.opencv.org/2.4.11/_images/MatBasicContainerOut7.png)

## 随机赋值

    Mat R = Mat(3, 2, CV_8UC3);
    randu(R, Scalar::all(0), Scalar::all(255));
    
需要传递给randu()最大值和最小值；
## 格式化输出
前面的例子使用的都是默认的输出格式，opencv允许你使用不同的风格输出。
1. 默认格式：

            cout << "R (default) = " << endl <<        R           << endl << endl;
     
![](http://docs.opencv.org/2.4.11/_images/MatBasicContainerOut8.png)
2. python风格：
             
            cout << "R (python)  = " << endl << format(R,"python") << endl << endl;
         
![](http://docs.opencv.org/2.4.11/_images/MatBasicContainerOut16.png)
3. CSV风格：

          cout << "R (csv)     = " << endl << format(R,"csv"   ) << endl << endl;
          
![](http://docs.opencv.org/2.4.11/_images/MatBasicContainerOut10.png)
4. numpy风格：

      cout << "R (numpy)   = " << endl << format(R,"numpy" ) << endl << endl;
      
![](http://docs.opencv.org/2.4.11/_images/MatBasicContainerOut9.png)
5.  C

    cout << "R (c)       = " << endl << format(R,"C"     ) << endl << endl;
    
![](http://docs.opencv.org/2.4.11/_images/MatBasicContainerOut11.png)

## 其他通用结构的输出
* 2D point

        Point2f P(5, 1);
        cout << "Point (2D) = " << P << endl << endl;

![](http://docs.opencv.org/2.4.11/_images/MatBasicContainerOut12.png)

* 3D point

        Point3f P3f(2, 6, 7);
        cout << "Point (3D) = " << P3f << endl << endl;
        
![](http://docs.opencv.org/2.4.11/_images/MatBasicContainerOut13.png)

* std::vector via cv::Mat

        vector<float> v;
        v.push_back( (float)CV_PI);   v.push_back(2);    v.push_back(3.01f);

        cout << "Vector of floats via Mat = " << Mat(v) << endl << endl;
        
![](http://docs.opencv.org/2.4.11/_images/MatBasicContainerOut14.png)

* std::vector of points

        vector<Point2f> vPoints(20);
        for (size_t i = 0; i < vPoints.size(); ++i)
          vPoints[i] = Point2f((float)(i * 5), (float)(i % 7));

        cout << "A vector of 2D Points = " << vPoints << endl << endl;
        
![](http://docs.opencv.org/2.4.11/_images/MatBasicContainerOut15.png)
     
