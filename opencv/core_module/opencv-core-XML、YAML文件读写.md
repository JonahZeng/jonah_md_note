# **Goal**
本章回答如下问题：
1. 如何输出和读取文本？opencv怎么使用YAML和XML？
2. 怎么输出和读取Opencv数据结构？
3. 怎么输出和读取用户定义的数据结构？
4. opencv数据结构比如`FileStorage`,`FileNode`,`FileNodeTterator`的用法。

# **source code**
```c++
    #include <opencv2/core/core.hpp>
    #include <iostream>
    #include <string>

    using namespace cv;
    using namespace std;

    static void help(char** av)
    {
        cout << endl
            << av[0] << " shows the usage of the OpenCV serialization functionality."         << endl
            << "usage: "                                                                      << endl
            <<  av[0] << " outputfile.yml.gz"                                                 << endl
            << "The output file may be either XML (xml) or YAML (yml/yaml). You can even compress it by "
            << "specifying this in its extension like xml.gz yaml.gz etc... "                  << endl
            << "With FileStorage you can serialize objects in OpenCV by using the << and >> operators" << endl
            << "For example: - create a class and have it serialized"                         << endl
            << "             - use it to read and write matrices."                            << endl;
    }
    /*------------------自定义数据类型-----------------------*/
    class MyData
    {
    public:
        MyData() : A(0), X(0), id()
        {}
        explicit MyData(int) : A(97), X(CV_PI), id("mydata1234") // 显式声明构造函数，防止隐式类型转换
        {}
        void write(FileStorage& fs) const                        //串行化写入函数
        {
            fs << "{" << "A" << A << "X" << X << "id" << id << "}";
        }
        void read(const FileNode& node)                          //串行化读取函数
        {
            A = (int)node["A"];
            X = (double)node["X"];
            id = (string)node["id"];
        }
    public:                                          // 定义成公有，是为了不必定义友元函数在外部访问类成员
        int A;
        double X;
        string id;
    };
    /*--------------------------结束定义--------------------------------------*/
    //这两个函数必须在类外部定义，否则FileStorage不能正常串行化自定义数据类型
    static void write(FileStorage& fs, const std::string&, const MyData& x)
    {
        x.write(fs);
    }
    static void read(const FileNode& node, MyData& x, const MyData& default_value = MyData())
    {
        if(node.empty())
            x = default_value;
        else
            x.read(node);
    }

    // This function will print our custom class to the console
    static ostream& operator<<(ostream& out, const MyData& m)
    {
        out << "{ id = " << m.id << ", ";
        out << "X = " << m.X << ", ";
        out << "A = " << m.A << "}";
        return out;
    }
    /*--------------------------main 函数开始----------------------------------*/
    int main(int ac, char** av)
    {
        if (ac != 2)  
        {
            help(av);   //参数个数不为2，显示程序用法，然后退出
            return 1;
        }
    
        string filename = av[1];   //第二个字符串作为文本文件名称
        { 
            Mat R = Mat_<uchar>::eye(3, 3),   //创建一个3*3，对角线为1的矩阵
                T = Mat_<double>::zeros(3, 1);   //创建一个3*1，全部为0的矩阵
            MyData m(1);                         //创建自定义数据 对象
    
            FileStorage fs(filename, FileStorage::WRITE);   //写数据
    
            fs << "iterationNr" << 100;                      //写入数字100
            fs << "strings" << "[";                              //写入string 队列 用[ ]来标记开始和结束
            fs << "image1.jpg" << "Awesomeness" << "baboon.jpg";
            fs << "]";                                           //关闭队列
    
            fs << "Mapping";                              // 写入文本---图（map） 用{}标记开始和结束
            fs << "{" << "One" << 1;
            fs <<        "Two" << 2 << "}";
    
            fs << "R" << R;                                      // 写入mat对象R
            fs << "T" << T;                                     //写入mat对象T
    
            fs << "MyData" << m;                                // 写入自定义数据类型 MyData
    
            fs.release();                                     // 显示关闭文件，也可以不关闭，等fs生命周期截止自动关闭
            cout << "Write Done." << endl;
        }
    
        {
            cout << endl << "Reading: " << endl;            //读取文件
            FileStorage fs;
            fs.open(filename, FileStorage::READ);           //构造FileStorage对象
    
            int itNr;
            //fs["iterationNr"] >> itNr;                    //读取int 标记为"iterationNr"
            itNr = (int) fs["iterationNr"];                 //两种写法都可以，第一种利用iterationNr重载的>>操作符
            cout << itNr;
            if (!fs.isOpened())
            {
                cerr << "Failed to open " << filename << endl;
                help(av);
                return 1;
            }
    
            FileNode n = fs["strings"];                         // 读取string队列- Get node
            if (n.type() != FileNode::SEQ)
            {
                cerr << "strings is not a sequence! FAIL" << endl;
                return 1;
            }
    
            FileNodeIterator it = n.begin(), it_end = n.end(); // Go through the node
            for (; it != it_end; ++it)
                cout << (string)*it << endl;
    
    
            n = fs["Mapping"];                                // Read mappings from a sequence
            cout << "Two  " << (int)(n["Two"]) << "; ";
            cout << "One  " << (int)(n["One"]) << endl << endl;
    
    
            MyData m;
            Mat R, T;
    
            fs["R"] >> R;                                      // Read cv::Mat
            fs["T"] >> T;
            fs["MyData"] >> m;                                 // Read your own structure_
    
            cout << endl
                << "R = " << R << endl;
            cout << "T = " << T << endl << endl;
            cout << "MyData = " << endl << m << endl << endl;
    
            //Show default behavior for non existing nodes
            cout << "Attempt to read NonExisting (should initialize the data structure with its default).";
            fs["NonExisting"] >> m;
            cout << endl << "NonExisting = " << endl << m << endl;
        }
    
        cout << endl
            << "Tip: Open up " << filename << " with a text editor to see the serialized data." << endl;
    
        return 0;
    }
```

# **大概总结一下**
上面代码囊括了5种数据类型的串行化：C++ 基本类型，map ,vector,opencv定义的数据类型，自定义类型。
1. C++基本类型：
　　int 类型写入和读取：
```c++
    fs << "iterationNr" << 100; 
    int itNr;
    fs["iterationNr"] >> itNr;  
```
2. 队列（类似STL的vector），vector容器内的元素没有特定的名称，只能通过遍历或者特定的index来访问:
```c++
    //写入
    fs << "strings" << "[";                              //写入string 队列 用[ ]来标记开始和结束
    fs << "image1.jpg" << "Awesomeness" << "baboon.jpg";
    fs << "]";                                           //关闭队列
    //读取
    FileNode n = fs["strings"];                         // 读取string队列- Get node
    if (n.type() != FileNode::SEQ)
    {
        cerr << "strings is not a sequence! FAIL" << endl;
        return 1;
    }
    
    FileNodeIterator it = n.begin(), it_end = n.end(); // 遍历节点
    for (; it != it_end; ++it)
        cout << (string)*it << endl;
```
3. 图（类似STL的map），图的元素有特定的名称
```c++
    //写入
     fs << "Mapping";                              // 写入文本---图（map） 用{}标记开始和结束
     fs << "{" << "One" << 1;
     fs << "Two" << 2 << "}";
     //读取
     FileNode n = fs["Mapping"];                                // 读取map
     cout << "Two  " << (int)(n["Two"]) << "; ";
     cout << "One  " << (int)(n["One"]) << endl << endl;
```
4. opencv数据类型：
```c++   
    //写入
    fs << "R" << R;                                      // 写入mat对象R
    fs << "T" << T;                                     //写入mat对象T
    //读取
    fs["R"] >> R;                                      // Read cv::Mat
    fs["T"] >> T;
```
5. 自定义类型MyData，首先要让这个自定义类支持串行化，要在类内部定义成员函数：
```c++
    void write(FileStorage& fs) const                        //串行化写入函数，按照map的写入方式
    {
        fs << "{" << "A" << A << "X" << X << "id" << id << "}";
    }
    void read(const FileNode& node)                          //串行化读取函数，类似map的读取
    {
        A = (int)node["A"];
        X = (double)node["X"];
        id = (string)node["id"];
    }
```
然后在类外部定义两个函数：
```c++
    static void write(FileStorage& fs, const std::string&, const MyData& x)
    {
        x.write(fs);
    }
    static void read(const FileNode& node, MyData& x, const MyData& default_value = MyData())
    {
        if(node.empty())
            x = default_value;
        else
            x.read(node);
    }
```
然后就可以像其他类型一样使用<<和>>
```c++
    //写入
    fs << "MyData" << m;                                // 写入自定义数据类型 MyData
    //读取
    MyData m;
    fs["MyData"] >> m;                                 // Read your own structure_
```