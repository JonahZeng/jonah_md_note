# goal
本节介绍：

* 使用OpenCV函数`matchTemplate()` 在一幅图像和一个指定的小图像里寻找是否有匹配
* 使用OpenCV函数`minMaxLoc()` 在一个给定的数组里找到最大值和最小值(同时也找到相应的位置)
# theory
## What is template matching?
模板匹配是一种用于寻找图像上和指定的模板相匹配区域的技术.
## how does it works ?
* 首先需要准备两个素材:
a. Source image (I):就是我将在这幅图像上进行查找相匹配的区域
b. Template image (T): 模板
我们的目的就是找到匹配度最高的区域:
![](leanote://file/getImage?fileId=575ace4eab64413806000bdc)
* 为了找到这个区域, 我们将不断地横向遍历图像来和模板进行比较:
![](leanote://file/getImage?fileId=575ace4eab64413806000bda)
* 滑动, 就是说计算的区域大小不变，每次调整一个像素位置 (从左往右，从上往下).在每个位置上，都有一个对应的矩阵用于计算该位置覆盖的区域和模板的匹配程度 ；
* 对于T覆盖在I上的每个位置, 把计算结果放在输出：matrix (R). R上的元素指示了匹配相似程度:
![](leanote://file/getImage?fileId=575ace4eab64413806000bde)
上面这个结果就是使用TM_CCORR_NORMED方式进行滑动遍历计算的结果. 亮的地方代表了高相似度. 如你所见，红色标注的地方可能就是匹配度最高的区域, 所以黑色框起来的块就是这个区域.

* 我们使用函数`minMaxLoc`来定位R输出里最大值（或者最小值，取决你采用哪种匹配方式）.
## opencv有哪些可用的匹配方式？
在函数`matchTemplate`里，总共有6种匹配方式：
1. method=CV_TM_SQDIFF
$$R(x,y)= \sum _{x',y'} (T(x',y')-I(x+x',y+y'))^2$$
2. method=CV_TM_SQDIFF_NORMED

$$R(x,y)= \frac{\sum_{x',y'} (T(x',y')-I(x+x',y+y'))^2}{\sqrt{\sum_{x',y'}T(x',y')^2 \cdot \sum_{x',y'} I(x+x',y+y')^2}}$$
3. method=CV_TM_CCORR

$$R(x,y)= \sum _{x',y'} (T(x',y')  \cdot I(x+x',y+y'))$$
4. method=CV_TM_CCORR_NORMED

$$R(x,y)= \frac{\sum_{x',y'} (T(x',y') \cdot I(x+x',y+y'))}{\sqrt{\sum_{x',y'}T(x',y')^2 \cdot \sum_{x',y'} I(x+x',y+y')^2}}$$
5. method=CV_TM_CCOEFF

$$R(x,y)= \sum _{x',y'} (T'(x',y')  \cdot I(x+x',y+y'))$$

where

$$\begin{array}{l} T'(x',y')=T(x',y') - 1/(w  \cdot h)  \cdot \sum _{x'',y''} T(x'',y'') \\ I'(x+x',y+y')=I(x+x',y+y') - 1/(w  \cdot h)  \cdot \sum _{x'',y''} I(x+x'',y+y'') \end{array}$$
6. method=CV_TM_CCOEFF_NORMED

$$R(x,y)= \frac{ \sum_{x',y'} (T'(x',y') \cdot I'(x+x',y+y')) }{ \sqrt{\sum_{x',y'}T'(x',y')^2 \cdot \sum_{x',y'} I'(x+x',y+y')^2} }$$

# Code
* 这个程序做什么?
a. 加载源图像和模板图像
b. 使用函数`matchTemplate`和上面列出的6种匹配方式进行计算 . 用户可以通过滚动条选择使用哪种匹配方式.
c. 归一化R输出值
d. 定位匹配程度最高的位置
e. 在匹配程度最大的区域画矩形
* 代码：
```c++
        #include "opencv2/highgui/highgui.hpp"
        #include "opencv2/imgproc/imgproc.hpp"
        #include <iostream>
        #include <stdio.h>
        
        using namespace std;
        using namespace cv;
        
        
        Mat img; Mat templ; Mat result;
        char* image_window = "Source Image";
        char* result_window = "Result window";
        
        int match_method;
        int max_Trackbar = 5;
        
        
        void MatchingMethod( int, void* );
        
        
        int main( int argc, char** argv )
        {
        
          img = imread( argv[1], 1 );
          templ = imread( argv[2], 1 );
        
        
          namedWindow( image_window, CV_WINDOW_AUTOSIZE );
          namedWindow( result_window, CV_WINDOW_AUTOSIZE );
        
        
          char* trackbar_label = "Method: \n 0: SQDIFF \n 1: SQDIFF NORMED \n 2: TM CCORR \n 3: TM CCORR NORMED \n 4: TM COEFF \n      5: TM COEFF NORMED";
          createTrackbar( trackbar_label, image_window, &match_method, max_Trackbar, MatchingMethod );
        
          MatchingMethod( 0, 0 );//第一次显示的默认方式
        
          waitKey(0);
          return 0;
        }
        
        
        void MatchingMethod( int, void* )
        {
          /// Source image to display
          Mat img_display;
          img.copyTo( img_display );
        
          /// Create the result matrix
          int result_cols =  img.cols - templ.cols + 1;
          int result_rows = img.rows - templ.rows + 1;
        
          result.create( result_rows, result_cols, CV_32FC1 );
        
          /// Do the Matching and Normalize
          matchTemplate( img, templ, result, match_method );
          normalize( result, result, 0, 1, NORM_MINMAX, -1, Mat() );
        
          /// Localizing the best match with minMaxLoc
          double minVal; double maxVal; Point minLoc; Point maxLoc;
          Point matchLoc;
        
          minMaxLoc( result, &minVal, &maxVal, &minLoc, &maxLoc, Mat() );
        
          /// For SQDIFF and SQDIFF_NORMED, the best matches are lower values. For all the other methods, the higher the better
          if( match_method  == CV_TM_SQDIFF || match_method == CV_TM_SQDIFF_NORMED )
            { matchLoc = minLoc; }
          else
            { matchLoc = maxLoc; }
        
          /// Show me what you got
          rectangle( img_display, matchLoc, Point( matchLoc.x + templ.cols , matchLoc.y + templ.rows ), Scalar::all(0), 2, 8, 0     );
          rectangle( result, matchLoc, Point( matchLoc.x + templ.cols , matchLoc.y + templ.rows ), Scalar::all(0), 2, 8, 0 );
        
          imshow( image_window, img_display );
          imshow( result_window, result );
        
          return;
        }
```
# explanation
1. 声明全局变量,比如源图像，模板图像，计算输出图像和匹配方式，窗口名称：
```c++
        Mat img; Mat templ; Mat result;
        char* image_window = "Source Image";
        char* result_window = "Result window";

        int match_method;
        int max_Trackbar = 5;
```
2. 加载源图像和模板:
```c++
        img = imread( argv[1], 1 );
        templ = imread( argv[2], 1 );
```
3. 创建窗口显示结果:
```c++
        namedWindow( image_window, CV_WINDOW_AUTOSIZE );
        namedWindow( result_window, CV_WINDOW_AUTOSIZE );
```
4. 在显示窗口创建滚动条用于选择哪种匹配方式. `MatchingMethod` 在滚动条改变时调用.
```c++
        char* trackbar_label = "Method: \n 0: SQDIFF \n 1: SQDIFF NORMED \n 2: TM CCORR \n 3: TM CCORR NORMED \n 4: TM COEFF \n 5: TM COEFF NORMED";
        createTrackbar( trackbar_label, image_window, &match_method, max_Trackbar, MatchingMethod );
```
5. 等待退出.
```c++
        waitKey(0);
        return 0;
```
6. 回调函数`MatchingMethod`. 首先，复制一个源图像:
```c++
        Mat img_display;
        img.copyTo( img_display );
```
7. 接下来，创建一个用于存储计算结果的Mat. 注意长度和宽度
```c++
        int result_cols =  img.cols - templ.cols + 1;
        int result_rows = img.rows - templ.rows + 1;

        result.create( result_rows, result_cols, CV_32FC1 );
```
8. 进行匹配计算:
```c++
        matchTemplate( img, templ, result, match_method );
```
参数很明显的分别是源输入image I, 模板 T, 存储结果的 R 和匹配计算方式

9. 归一化计算结果:
```c++
        normalize( result, result, 0, 1, NORM_MINMAX, -1, Mat() );
```
10. 使用函数`minMaxLoc`找到R输出里的最大值或者最小值及其位置.
```c++
        double minVal; double maxVal; Point minLoc; Point maxLoc;
        Point matchLoc;

        minMaxLoc( result, &minVal, &maxVal, &minLoc, &maxLoc, Mat() );
```
参数列表:
* result: 计算结果Mat
* &minVal and &maxVal: 在R中的最大值和最小值
* &minLoc and &maxLoc: 最大值最小值的位置
* Mat(): 可选的掩模（屏蔽）
11. ( CV_SQDIFF and CV_SQDIFF_NORMED )最小值代表了最匹配. 其他方式则最大值代表了最匹配. 
```c++
        if( match_method  == CV_TM_SQDIFF || match_method == CV_TM_SQDIFF_NORMED )
         { matchLoc = minLoc; }
        else
         { matchLoc = maxLoc; }
```
12. 显示源图像以及计算匹配结果的图像. 在匹配度最高的地方画一个矩形:
```c++
        rectangle( img_display, matchLoc, Point( matchLoc.x + templ.cols , matchLoc.y + templ.rows ), Scalar::all(0), 2, 8, 0 );
        rectangle( result, matchLoc, Point( matchLoc.x + templ.cols , matchLoc.y + templ.rows ), Scalar::all(0), 2, 8, 0 );

        imshow( image_window, img_display );
        imshow( result_window, result );
```
# result
1. 源图像和模板分别是：
![](leanote://file/getImage?fileId=575ace4eab64413806000bee) ![](leanote://file/getImage?fileId=575ace4eab64413806000bea)
2. 一下第一列分别是SQDIFF, CCORR ， CCOEFF的结果，第二列是他们的normalize版本结果：
![](leanote://file/getImage?fileId=575ace4eab64413806000be4) ![](leanote://file/getImage?fileId=575ace4eab64413806000be6)
![](leanote://file/getImage?fileId=575ace4eab64413806000be0) ![](leanote://file/getImage?fileId=575ace4eab64413806000be8)
![](leanote://file/getImage?fileId=575ace4eab64413806000be2) ![](leanote://file/getImage?fileId=575ace4eab64413806000bec)
3.CCORR 和 CCDEFF 给出的结果有些不对,但是他们的normalize版本的结果正确，因为我们仅仅只考虑了最大值，并没有考虑其他高可能型的点 。