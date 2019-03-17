这是从Mat头文件里找到的：
```
    /** @overload */
    template<typename _Tp> _Tp* ptr(int i0=0);
    /** @overload */
    template<typename _Tp> const _Tp* ptr(int i0=0) const;
    /** @overload */
    template<typename _Tp> _Tp* ptr(int i0, int i1);
    /** @overload */
    template<typename _Tp> const _Tp* ptr(int i0, int i1) const;
    /** @overload */
    template<typename _Tp> _Tp* ptr(int i0, int i1, int i2);
    /** @overload */
    template<typename _Tp> const _Tp* ptr(int i0, int i1, int i2) const;
    /** @overload */
    template<typename _Tp> _Tp* ptr(const int* idx);
    /** @overload */
    template<typename _Tp> const _Tp* ptr(const int* idx) const;
    /** @overload */
    template<typename _Tp, int n> _Tp* ptr(const Vec<int, n>& idx);
    /** @overload */
    template<typename _Tp, int n> const _Tp* ptr(const Vec<int, n>& idx) const;
```
我经常这样用：
```
uchar* ptr1=Mat1.ptr<uchar>(1000,1000);//获取x=1000,y=1000的像素值
```
因为传递了2个int参数，理所当然的，使用的是如下模板：
```
    template<typename _Tp> _Tp* ptr(int i0, int i1);
```
`ptr<uchar>()`当中的uchar用于通知函数实例化的typename，这样就实现了相同的参数实现不同的返回值。