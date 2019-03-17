相机固有畸变问题，但是幸运的是畸变在相机上是固化的，可以通过calibration或者remapping来修正。进一步讲，calibration决定了camera的成像位置（pixel）与真实世界（比如mm）的映射关系。
# theory
opencv把畸变分成两种：半径方向的畸变和正切方向的畸变；
半径方向的畸变公式：
$$x_{corrected}=x(1+k_{1}r^{2}+k_{2}r^{4}+k_{3}r^{6})$$
$$y_{corrected}=y(1+k_{1}r^{2}+k_{2}r^{4}+k_{3}r^{6})$$
也就是说input image的坐标点$(x,y)$经过矫正后，坐标变为$(x_{corrected},y_{corrected})$,半径方向的畸变，存在形式就是日常常见的桶形畸变和鱼眼效果。

正切方向的畸变是因为镜头没有完全平行成像面，校正公式：
$$x_{corrected}=x+[2p_{1}xy+p_{2}(r^{2}+2x^{2})]$$
$$y_{corrected}=y+[p_{1}(r^{2}+2y^{2})+2p_{2}xy]$$
这样，目前就得到了5个必须的参数：
$$Distortion_{coefficients}=(k_{1}　k_{2}　p_{1}　p_{2}　k_{3})$$
那么对于真实世界的单位，和成像坐标点（像素）的单位转换，使用如下公式：
$$
\begin{bmatrix}x \\y \\w\end{bmatrix}=
\begin{bmatrix}f_{x}&0&c_{x}\\0&f_{y}&c_{y}\\0& 0& 1\end{bmatrix}
\begin{bmatrix}X\\Y\\Z\end{bmatrix}
$$
这里的w出现是因为使用了单应性坐标系$(w=Z)$,$f_{x}$和$f_{y}$是未知的，它们代表了镜头的焦距，大部分时候$f_{x}$和$f_{y}$有一个比例关系($f_{x}=\alpha*f_{y}$)，$c_{x},c_{y}$则代表了成像场的中心位置（单位是pixel）。这个包含4个未知参数的矩阵就是**camera matirx**。需要注意的是不管图像的分辨率怎么变，$Distortion_{coefficients}$是不会变的，但是camera matirx需要从calibration分辨率scale到当前分辨率。
校正过程就是得到这两个矩阵的值。具体过程就是解几何方程，为了获得方程，需要在图像中放置特定的参考物体。opencv支持3种deceted object:

* Classical black-white chessboard
* Symmetrical circle pattern
* Asymmetrical circle pattern

所以，你要做的就是用你的相机对你的参考物进行拍照，每一个opencv识别出来的图像都会生成一个方程，为了解这些方程，你需要事先计划好拍多少照片，对于chessboard pattern来说要多拍一些，而circle pattern则相对要少一些。理论上来说，最少只要2张照片即可以得到所有的未知参数，但是因为拍的照片有时候有缺陷，通常我们都需要拍10张来获取这2个矩阵。

# goal
示例程序将有如下动作:

* Determine the distortion matrix
* Determine the camera matrix
* Take input from Camera, Video and Image file list
* Read configuration from XML/YAML file
* Save the results into XML/YAML file
* Calculate re-projection error
# source code
这个程序只接受一个参数：设置xml文件，在这个xml文件里你可以设置输入源是camera,video或者image list。如果你选择image list,则需要创建另一个xml文件来指定image list.
```c++
int main(int argc, char* argv[])
{
    help();

    //读取 setting.xml
    Settings s;
    const string inputSettingsFile = argc > 1 ? argv[1] : "default.xml";
    FileStorage fs(inputSettingsFile, FileStorage::READ); 
    if (!fs.isOpened())
    {
        cout << "Could not open the configuration file: \"" << inputSettingsFile << "\"" << endl;
        return -1;
    }
    fs["Settings"] >> s;
    fs.release();                                       
  

    if (!s.goodInput)//校验设置参数
    {
        cout << "Invalid input detected. Application stopping. " << endl;
        return -1;
    }
    //声明imagePoints用于存储检测到的角点坐标
    vector<vector<Point2f> > imagePoints;
    Mat cameraMatrix, distCoeffs;
    Size imageSize;
    int mode = s.inputType == Settings::IMAGE_LIST ? CAPTURING : DETECTION;
    clock_t prevTimestamp = 0;
    const Scalar RED(0,0,255), GREEN(0,255,0);
    const char ESC_KEY = 27;

    
    for(;;)
    {
        Mat view;
        bool blinkOutput = false;

        view = s.nextImage();

        //-----  If no more image, or got enough, then stop calibration and show result -------------
		//if 使用imageList  并且图片数达到了设定值
        if( mode == CAPTURING && imagePoints.size() >= (size_t)s.nrFrames )
        {
          if( runCalibrationAndSave(s, imageSize,  cameraMatrix, distCoeffs, imagePoints)) 
          //当读取和检测所有image的chess board角点完成后开始运行calibration
              mode = CALIBRATED;
          else
              mode = DETECTION;
        }
        if(view.empty())          //一旦发生中断或者全部读取完成
        {
            
            if( mode != CALIBRATED && !imagePoints.empty() )//如果是imageList类型，则此处不执行，直接break
                runCalibrationAndSave(s, imageSize,  cameraMatrix, distCoeffs, imagePoints);
            break;
        }
      

        imageSize = view.size();  
        if( s.flipVertical )    //如果设定了翻转，则实行翻转
			flip( view, view, 0 );

        //声明单个vector<point2f>用于暂存单个image的角点坐标
        vector<Point2f> pointBuf;

        bool found;
        switch( s.calibrationPattern ) // 根据detected obj的类型选择
        {
        case Settings::CHESSBOARD:
            found = findChessboardCorners( view, s.boardSize, pointBuf,
                CALIB_CB_ADAPTIVE_THRESH | CALIB_CB_FAST_CHECK | CALIB_CB_NORMALIZE_IMAGE);
            break;
        case Settings::CIRCLES_GRID:
            found = findCirclesGrid( view, s.boardSize, pointBuf );
            break;
        case Settings::ASYMMETRIC_CIRCLES_GRID:
            found = findCirclesGrid( view, s.boardSize, pointBuf, CALIB_CB_ASYMMETRIC_GRID );
            break;
        default:
            found = false;
            break;
        }
        
        
        if ( found)                // 如果在当前image找到了corner,提升corner坐标准确度
        {
              // improve the found corners' coordinate accuracy for chessboard
                if( s.calibrationPattern == Settings::CHESSBOARD)
                {
                    Mat viewGray;
                    cvtColor(view, viewGray, COLOR_BGR2GRAY);
                    //根据梯度以及正交矢量来寻找交点
                    cornerSubPix( viewGray, pointBuf, Size(11,11),
                        Size(-1,-1), TermCriteria( TermCriteria::EPS+TermCriteria::COUNT, 30, 0.1 ));
                        //误差在0.1以内则立即停止
                }

                if( mode == CAPTURING &&  // For camera only take new samples after delay time
                    (!s.inputCapture.isOpened() || clock() - prevTimestamp > s.delay*1e-3*CLOCKS_PER_SEC) )
                {
                    imagePoints.push_back(pointBuf);//把单个vector<point2f>压入
                    prevTimestamp = clock();
                    blinkOutput = s.inputCapture.isOpened();
                }

                // Draw the corners.
                drawChessboardCorners( view, s.boardSize, Mat(pointBuf), found );
        }
       
        //----------------------------- Output Text ------------------------------------------------
        
        string msg = (mode == CAPTURING) ? "100/100" :
                      mode == CALIBRATED ? "Calibrated" : "Press 'g' to start";
        int baseLine = 0;
        Size textSize = getTextSize(msg, 1, 1, 1, &baseLine);
        Point textOrigin(view.cols - 2*textSize.width - 10, view.rows - 2*baseLine - 10);

        if( mode == CAPTURING )
        {
            if(s.showUndistorsed)
                msg = format( "%d/%d Undist", (int)imagePoints.size(), s.nrFrames );
            else
                msg = format( "%d/%d", (int)imagePoints.size(), s.nrFrames );
        }

        putText( view, msg, textOrigin, 1, 1, mode == CALIBRATED ?  GREEN : RED);

        if( blinkOutput )
            bitwise_not(view, view);
        
        //------------------------- Video capture  output  undistorted ------------------------------
        
        if( mode == CALIBRATED && s.showUndistorsed )
        //对于imageList来说，这一步不会执行，因为以前mode！=CALIBRATED，一旦相等则break这个循环
        {
            Mat temp = view.clone();
            undistort(temp, view, cameraMatrix, distCoeffs);
        }
       
        //------------------------------ Show image and check for input commands -------------------
        
        imshow("Image View", view);
        char key = (char)waitKey(s.inputCapture.isOpened() ? 50 : s.delay);

        if( key  == ESC_KEY )
            break;

        if( key == 'u' && mode == CALIBRATED )
           s.showUndistorsed = !s.showUndistorsed;

        if( s.inputCapture.isOpened() && key == 'g' )
        {
            mode = CAPTURING;
            imagePoints.clear();
        }
        
    }//end for()

    // -----------------------Show the undistorted image for the image list ------------------------
    //! [show_results]
    if( s.inputType == Settings::IMAGE_LIST && s.showUndistorsed )
    {
        Mat view, rview, map1, map2;
        initUndistortRectifyMap(cameraMatrix, distCoeffs, Mat(),
            getOptimalNewCameraMatrix(cameraMatrix, distCoeffs, imageSize, 1, imageSize, 0),
            imageSize, CV_16SC2, map1, map2);

        for(size_t i = 0; i < s.imageList.size(); i++ )
        {
            view = imread(s.imageList[i], 1);
            if(view.empty())
                continue;
            remap(view, rview, map1, map2, INTER_LINEAR);
            imshow("Image View", rview);
            char c = (char)waitKey();
            if( c  == ESC_KEY || c == 'q' || c == 'Q' )
                break;
        }
    }
    //! [show_results]

    return 0;
}
```
# explanation
1. 读取xml设置

```c++
    Settings s;
    const string inputSettingsFile = argc > 1 ? argv[1] : "default.xml";
    FileStorage fs(inputSettingsFile, FileStorage::READ); // Read the settings
    if (!fs.isOpened())
    {
        cout << "Could not open the configuration file: \"" << inputSettingsFile << "\"" << endl;
        return -1;
    }
    fs["Settings"] >> s;
    fs.release();                                         // close Settings file
```
在类settings中的读取最后面还有一个校验函数检查输入是否合规。
2. 不断读取imageList中的图片，直到读取失败或者读取足够数量后，开始运行calibration

```c++
    for(;;)
    {
        Mat view;
        bool blinkOutput = false;
        view = s.nextImage();
        //-----  If no more image, or got enough, then stop calibration and show result -------------
        if( mode == CAPTURING && imagePoints.size() >= (size_t)s.nrFrames )
        {
          if( runCalibrationAndSave(s, imageSize,  cameraMatrix, distCoeffs, imagePoints))
              mode = CALIBRATED;
          else
              mode = DETECTION;
        }
        if(view.empty())          // If there are no more images stop the loop
        {
            // if calibration threshold was not reached yet, calibrate now
            if( mode != CALIBRATED && !imagePoints.empty() )
                runCalibrationAndSave(s, imageSize,  cameraMatrix, distCoeffs, imagePoints);
            break;
        }
```
3. 在当前帧或者image中识别角点（chess board）圆（ Symmetrical circle pattern）
所有识别到的坐标将放在vector<point2f> pointBuf里，最后组合成`vector<vector<point2f>> imagePoint`

```c++
        vector<Point2f> pointBuf;
        bool found;
        switch( s.calibrationPattern ) // Find feature points on the input format
        {
        case Settings::CHESSBOARD:
            found = findChessboardCorners( view, s.boardSize, pointBuf,
                CALIB_CB_ADAPTIVE_THRESH | CALIB_CB_FAST_CHECK | CALIB_CB_NORMALIZE_IMAGE);
            break;
        case Settings::CIRCLES_GRID:
            found = findCirclesGrid( view, s.boardSize, pointBuf );
            break;
        case Settings::ASYMMETRIC_CIRCLES_GRID:
            found = findCirclesGrid( view, s.boardSize, pointBuf, CALIB_CB_ASYMMETRIC_GRID );
            break;
        default:
            found = false;
            break;
        }
```
根据你选择的pattern类型使用函数` cv::findChessboardCorners` 或者`cv::findCirclesGrid`. 参数需要格子数量和image size,然后，调用这个函数返回一个bool值指示是否成功识别pattern。尽量不要使用相似的图片，相似的图片会导致相似的坐标从而导致相似的方程。
```c++
        if ( found)                // If done with success,
        {
              // improve the found corners' coordinate accuracy for chessboard
                if( s.calibrationPattern == Settings::CHESSBOARD)
                {
                    Mat viewGray;
                    cvtColor(view, viewGray, COLOR_BGR2GRAY);
                    cornerSubPix( viewGray, pointBuf, Size(11,11),
                        Size(-1,-1), TermCriteria( TermCriteria::EPS+TermCriteria::COUNT, 30, 0.1 ));
                }
                if( mode == CAPTURING &&  // For camera only take new samples after delay time
                    (!s.inputCapture.isOpened() || clock() - prevTimestamp > s.delay*1e-3*CLOCKS_PER_SEC) )
                {
                    imagePoints.push_back(pointBuf);
                    prevTimestamp = clock();
                    blinkOutput = s.inputCapture.isOpened();
                }
                // Draw the corners.
                drawChessboardCorners( view, s.boardSize, Mat(pointBuf), found );
        }
```
4. 向用户显示识别结果, 并且接受键盘输入控制后续状态
```c++
        string msg = (mode == CAPTURING) ? "100/100" :
                      mode == CALIBRATED ? "Calibrated" : "Press 'g' to start";
        int baseLine = 0;
        Size textSize = getTextSize(msg, 1, 1, 1, &baseLine);
        Point textOrigin(view.cols - 2*textSize.width - 10, view.rows - 2*baseLine - 10);
        if( mode == CAPTURING )
        {
            if(s.showUndistorsed)
                msg = format( "%d/%d Undist", (int)imagePoints.size(), s.nrFrames );
            else
                msg = format( "%d/%d", (int)imagePoints.size(), s.nrFrames );
        }
        putText( view, msg, textOrigin, 1, 1, mode == CALIBRATED ?  GREEN : RED);
        if( blinkOutput )
            bitwise_not(view, view);
```
如果运行calibration成功获取camera matrix和distortion coefficients,就可以进行校正：
```c++
        if( mode == CALIBRATED && s.showUndistorsed )
        {
            Mat temp = view.clone();
            undistort(temp, view, cameraMatrix, distCoeffs);
        }
```
接下来显示图像，等待用户输入，u表示进行undistort,g
Then we show the image and wait for an input key and if this is u we toggle the distortion removal, if it is g we start again the detection process, and finally for the ESC key we quit the application:
```c++
        imshow("Image View", view);
        char key = (char)waitKey(s.inputCapture.isOpened() ? 50 : s.delay);
        if( key  == ESC_KEY )
            break;
        if( key == 'u' && mode == CALIBRATED )
           s.showUndistorsed = !s.showUndistorsed;
        if( s.inputCapture.isOpened() && key == 'g' )
        {
            mode = CAPTURING;
            imagePoints.clear();
        }
```

5. 给imageList做矫正然后显示
因为在上面的循环里不会对imageList多矫正，所以在循环结束后才可以做这一步.这其实是有优势的，因为上面的函数`cv::undistort()`本质上是函数` cv::initUndistortRectifyMap`与`cv::remap`的组合，` cv::initUndistortRectifyMap`的作用是把计算变形矩阵，而`cv::remap`的作用是执行这个变形矩阵。这样的话，其实只需要计算一次变形矩阵就可以了，可以节省开销.
```c++
        if( s.inputType == Settings::IMAGE_LIST && s.showUndistorsed )
        {
            Mat view, rview, map1, map2;
            initUndistortRectifyMap(cameraMatrix, distCoeffs, Mat(),
                getOptimalNewCameraMatrix(cameraMatrix, distCoeffs, imageSize, 1, imageSize, 0),
                imageSize, CV_16SC2, map1, map2);
            for(size_t i = 0; i < s.imageList.size(); i++ )
            {
                view = imread(s.imageList[i], 1);
                if(view.empty())
                    continue;
                remap(view, rview, map1, map2, INTER_LINEAR);
                imshow("Image View", rview);
                char c = (char)waitKey();
                if( c  == ESC_KEY || c == 'q' || c == 'Q' )
                     break;
            }
        }
```