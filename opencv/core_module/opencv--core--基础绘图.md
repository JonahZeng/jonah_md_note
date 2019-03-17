# goal
---------
本节知识点：

*  使用Point 在图像中定义一个2D点
*  使用Scalar 容器类
*  使用opencv函数line()绘制一条线
*  使用ellipse()绘制椭圆
*  使用rectangle()绘制矩形
*  使用circle()绘制圆
*  使用fillPoly()绘制实心多边形

# Point &  Scalar
------------
**Point**描述了图像中像素坐标x、y，可以这样定义一个点：
```c++
    Point pt;
    pt.x=10;
    pt.y=8;
```
或者：
```c++
    Point pt=Point(10,8);
```
**Scalar**

* 是一个4元素的矢量（vector），被opencv大量运用在传递像素值上。
* 本节将用Scalar来代表RGB值，如果用不到4个值，则没有必要去定义第四个值。
* 举个例子，如果我们要求一个颜色值，我们给出如下：
　　　　　`Scalar(a,b,c)`
那么相对应的，颜色值被定义成：R=c,G=b,B=a  ;

# code解析
```c++
    #include <opencv2/core/core.hpp>
    #include <opencv2/highgui/highgui.hpp>
    
    #define w 400
    
    using namespace cv;
    
    /// --------------------------绘图函数预声明
    void MyEllipse( Mat img, double angle );
    void MyFilledCircle( Mat img, Point center );
    void MyPolygon( Mat img );
    void MyLine( Mat img, Point start, Point end );
    //----------------------------------------
  
    int main( void )
    {
    
      //----------------------------------------两个窗口用来显示绘制的2个图像，一个原子型，一个石头
      char atom_window[] = "Drawing 1: Atom";
      char rook_window[] = "Drawing 2: Rook";
     //--------------------------------------------
      // ------------------------------------------
      Mat atom_image = Mat::zeros( w, w, CV_8UC3 );
      Mat rook_image = Mat::zeros( w, w, CV_8UC3 );
      //--------------------------------------------新建两个Mat对象，用0初始化，就是全黑的图像
      
      /// 1. Draw a simple atom:
      
      
      /// 1.a. 画4个不同角度的椭圆
      MyEllipse( atom_image, 90 );
      MyEllipse( atom_image, 0 );
      MyEllipse( atom_image, 45 );
      MyEllipse( atom_image, -45 );
    
      /// 1.b. 画一个圆
      MyFilledCircle( atom_image, Point( w/2, w/2) );
    
      /// 2. Draw a rook
      /// ------------------
    
      /// 2.a.画一个自定义多边形，内部填充自定义颜色
      MyPolygon( rook_image );
    
      /// 2.b. 画矩形
      rectangle( rook_image,
             Point( 0, 7*w/8 ),
             Point( w, w),
             Scalar( 0, 255, 255 ),
             -1,
             8 );
    
      /// 2.c. 在矩形内部画线
      MyLine( rook_image, Point( 0, 15*w/16 ), Point( w, 15*w/16 ) );
      MyLine( rook_image, Point( w/4, 7*w/8 ), Point( w/4, w ) );
      MyLine( rook_image, Point( w/2, 7*w/8 ), Point( w/2, w ) );
      MyLine( rook_image, Point( 3*w/4, 7*w/8 ), Point( 3*w/4, w ) );
    
      /// 3. 显示
      imshow( atom_window, atom_image );
      moveWindow( atom_window, 0, 200 );
      imshow( rook_window, rook_image );
      moveWindow( rook_window, w, 200 );
    
      waitKey( 0 );
      return(0);
    }
```    
  
  
 
# 自定义函数解析
```c++
    void MyEllipse( Mat img, double angle )
    {
      int thickness = 2;
      int lineType = 8;
    
      ellipse( img,
               Point( w/2.0, w/2.0 ),   //椭圆中心位置
               Size( w/4.0, w/16.0 ),  //椭圆的宽度和高度
               angle,                 //倾斜角度
               0,                  
               360,                  //在0-360度之间画，即一个完整的椭圆
               Scalar( 255, 0, 0 ),//使用Blue划线
               thickness,          //划线宽度
               lineType );         //线型
    }
    /*-----------------------------直线-------------------------------*/
    void MyLine( Mat img, Point start, Point end )
    {
      int thickness = 2;
      int lineType = 8;
      line( img,
            start,             //起点
            end,               //终点
            Scalar( 0, 0, 0 ), //黑色  BGR
            thickness,    //线宽
            lineType );  //线型
    }   
    
    /*------------------------------圆形----------------------------*/
    void MyFilledCircle( Mat img, Point center )
    {
     int thickness = -1;
     int lineType = 8;
    
     circle( img,
             center,        //圆的中心点                
             w/32.0,        //半径
             Scalar( 0, 0, 255 ),  //颜色   红色
             thickness,    //线宽     -1表示填充
             lineType );   //线型
    }
    /*--------------------------多边形-------------------------------------*/
    void MyPolygon( Mat img )
    {
      int lineType = 8;
    
      /** Create some points */
      Point rook_points[1][20];
      rook_points[0][0] = Point( w/4.0, 7*w/8.0 );
      rook_points[0][1] = Point( 3*w/4.0, 7*w/8.0 );
      rook_points[0][2] = Point( 3*w/4.0, 13*w/16.0 );
      rook_points[0][3] = Point( 11*w/16.0, 13*w/16.0 );
      rook_points[0][4] = Point( 19*w/32.0, 3*w/8.0 );
      rook_points[0][5] = Point( 3*w/4.0, 3*w/8.0 );
      rook_points[0][6] = Point( 3*w/4.0, w/8.0 );
      rook_points[0][7] = Point( 26*w/40.0, w/8.0 );
      rook_points[0][8] = Point( 26*w/40.0, w/4.0 );
      rook_points[0][9] = Point( 22*w/40.0, w/4.0 );
      rook_points[0][10] = Point( 22*w/40.0, w/8.0 );
      rook_points[0][11] = Point( 18*w/40.0, w/8.0 );
      rook_points[0][12] = Point( 18*w/40.0, w/4.0 );
      rook_points[0][13] = Point( 14*w/40.0, w/4.0 );
      rook_points[0][14] = Point( 14*w/40.0, w/8.0 );
      rook_points[0][15] = Point( w/4.0, w/8.0 );
      rook_points[0][16] = Point( w/4.0, 3*w/8.0 );
      rook_points[0][17] = Point( 13*w/32.0, 3*w/8.0 );
      rook_points[0][18] = Point( 5*w/16.0, 13*w/16.0 );
      rook_points[0][19] = Point( w/4.0, 13*w/16.0) ;
    
      const Point* ppt[1] = { rook_points[0] };
      int npt[] = { 20 };
    
      fillPoly( img,
                ppt,     //多边形顶点
                npt,     //顶点数量
                1,       //多边形数量
                Scalar( 255, 255, 255 ),    //颜色
                lineType );
     }
     /*-------------矩形------------------*/
     rectangle( rook_image,
           Point( 0, 7*w/8.0 ),//起点
           Point( w, w),       //终点
           Scalar( 0, 255, 255 ),  //颜色
           -1,                   //填充
           8 );
```           
# 结果


![](http://docs.opencv.org/2.4.11/_images/Drawing_1_Tutorial_Result_0.png)