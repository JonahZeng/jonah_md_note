# **goal**
------------------
* 使用随机数生成类（random number generator class）以及how to get a random number from a uniform distribution
* 使用putText()函数在opencv窗口上显示文本

# **code**
----------------------
* 上一节（基本绘图）中我们绘制了不同类型的几何图案，你可能注意到了我们显示传递了函数参数比如：坐标，颜色，线宽等。
* 本节中，我们将使用随机数来给这些函数参数赋值。同时，将绘制多种几何图案在同一个图片上，我们将把这些绘制初始化为随机类型，这个过程我们将使用循环来自动完成。

# 代码解析
------------------
```c++
    const int NUMBER = 100;
    const int DELAY = 5;
    
    const int window_width = 900;
    const int window_height = 600;
    int x_1 = -window_width/2;
    int x_2 = window_width*3/2;
    int y_1 = -window_width/2;
    int y_2 = window_width*3/2;
    
    int main( void )
    {
      int c;
    
      /// 创建一个窗口
      char window_name[] = "Drawing_2 Tutorial";
    
      /// 新建一个RNG对象，用0XFFFFFFFF初始化
      RNG rng( 0xFFFFFFFF );
    
      ///新建一个Mat对象，并初始化为0
      Mat image = Mat::zeros( window_height, window_width, CV_8UC3 );
      /// 显示Mat  ,延迟DELAY  ms后关闭。
      imshow( window_name, image );
      waitKey( DELAY );
    
      ///划线
      c = Drawing_Random_Lines(image, window_name, rng);
      if( c != 0 ) return 0;
    
      ///画矩形
      c = Drawing_Random_Rectangles(image, window_name, rng);
      if( c != 0 ) return 0;
    
      /// 画椭圆
      c = Drawing_Random_Ellipses( image, window_name, rng );
      if( c != 0 ) return 0;
    
      /// 多边形
      c = Drawing_Random_Polylines( image, window_name, rng );
      if( c != 0 ) return 0;
    
      /// 填充多边形
      c = Drawing_Random_Filled_Polygons( image, window_name, rng );
      if( c != 0 ) return 0;
    
      /// 画圆
      c = Drawing_Random_Circles( image, window_name, rng );
      if( c != 0 ) return 0;
    
      ///显示文本
      c = Displaying_Random_Text( image, window_name, rng );
      if( c != 0 ) return 0;
    
      /// Displaying the big end!
      c = Displaying_Big_End( image, window_name, rng );
      if( c != 0 ) return 0;
    
      waitKey(0);
      return 0;
    }
``
自定义函数解析：
```c++
    /**--------------生成随机颜色-------------------**/
    static Scalar randomColor( RNG& rng )
    {
      int icolor = (unsigned) rng;
      return Scalar( icolor&255, (icolor>>8)&255, (icolor>>16)&255 );
    }

    /*--------------划线，起点终点，颜色，线宽随机--------------------*/
    int Drawing_Random_Lines( Mat image, char* window_name, RNG rng )
    {
      Point pt1, pt2;
    
      for( int i = 0; i < NUMBER; i++ )//循环画线
      {
        pt1.x = rng.uniform( x_1, x_2 );  //pt1.x将会在x_1,x_2之间随机生成
        pt1.y = rng.uniform( y_1, y_2 );
        pt2.x = rng.uniform( x_1, x_2 );
        pt2.y = rng.uniform( y_1, y_2 );
    
        line( image, pt1, pt2, randomColor(rng), rng.uniform(1, 10), 8 );//起点，终点，颜色，线宽，线型
        imshow( window_name, image );
        if( waitKey( DELAY ) >= 0 )
          { return -1; }
      }
    
      return 0;
    }
    
    /*---------------------------输出文本-------------------------------*/
    int Displaying_Random_Text( Mat image, char* window_name, RNG rng )
    {
      int lineType = 8;
    
      for ( int i = 1; i < NUMBER; i++ )//循环输出文本，每次都随机
      {
        Point org;
        org.x = rng.uniform(x_1, x_2);
        org.y = rng.uniform(y_1, y_2);
    
        putText( image, "Testing text rendering", org, rng.uniform(0,8),
                 rng.uniform(0,100)*0.05+0.1, randomColor(rng), rng.uniform(1, 10), lineType);
        //org是文本框输出起点（坐下角），rng.uniform(0,8)限定了字体类型，rng.uniform(0,100)*0.05+0.1限定了字体大小，
        //randomColor(rng)限定了字体颜色，rng.uniform(1, 10)限定了字体宽度
        imshow( window_name, image );
        if( waitKey(DELAY) >= 0 )
          { return -1; }
      }
    
      return 0;
    }
    
    /*----------------------输出结尾，背景压暗-------------*/
    int Displaying_Big_End( Mat image, char* window_name, RNG rng )
    {
      Size textsize = getTextSize("OpenCV forever!", CV_FONT_HERSHEY_COMPLEX, 3, 5, 0);//获取要输出的文本size
      Point org((window_width - textsize.width)/2, (window_height - textsize.height)/2);//设定输出起点
      int lineType = 8;                                                                  //线型
    
      Mat image2;
    
      for( int i = 0; i < 255; i += 2 )
      {
        image2 = image - Scalar::all(i);        //Mat  image减掉i（变暗），此处应该是重载了-操作符
                                                //内建了saturate限制保证值在0-255之间
        putText( image2, "OpenCV forever!", org, CV_FONT_HERSHEY_COMPLEX, 3,            
               Scalar(i, i, 255), 5, lineType );
    
        imshow( window_name, image2 );
        if( waitKey(DELAY) >= 0 )
          { return -1; }
      }
    
      return 0;
    }
```    
# 输出
　　　　　![](http://docs.opencv.org/2.4.11/_images/Drawing_2_Tutorial_Result_0.jpg)
　　　　　
　　　　　![](http://docs.opencv.org/2.4.11/_images/Drawing_2_Tutorial_Result_2.jpg)
　　　　　
　　　　　![](http://docs.opencv.org/2.4.11/_images/Drawing_2_Tutorial_Result_3.jpg)
　　　　　
　　　　　![](http://docs.opencv.org/2.4.11/_images/Drawing_2_Tutorial_Result_5.jpg)
　　　　　
　　　　　![](http://docs.opencv.org/2.4.11/_images/Drawing_2_Tutorial_Result_7.jpg)
　　　　　