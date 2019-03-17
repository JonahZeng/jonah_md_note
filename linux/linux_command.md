# pwd
print current work directory
打印当前目录路径
# cd
change directory
进入目标路径
```
jonah@Inspiron-3420:~$ pwd
/home/jonah
jonah@Inspiron-3420:~$ ls
Desktop    Downloads         Music     Public        Templates
Documents  examples.desktop  Pictures  python_space  Videos
jonah@Inspiron-3420:~$ cd Downloads/
jonah@Inspiron-3420:~/Downloads$ cd ~
jonah@Inspiron-3420:~$ pwd
/home/jonah
jonah@Inspiron-3420:~$ cd ..
jonah@Inspiron-3420:/home$ pwd
/home
jonah@Inspiron-3420:/home$ 
```
cd ~进入/home/当前用户/
cd .进入当前目录，不改变
cd ..进入父目录
# clear
清屏
# ls
打印目录内容
ls -a 显示所有包括隐藏文件
ls -l 以较长列表显示详细信息
ls -h 以可阅读方式显示包括size信息,把具体的字节信息缩略成KB，MB等
ls *JPG 显示以JPG结尾的文件
# touch
touch [option] [file]
update文件更改时间为当前系统时间，如果文件不存在，则创建一个空文件，如果应用了-c -h，则不创建
# mkdir
创建目录
# rm
rm -r [目录]递归删除目录下所有文件和文件夹
rm -f [文件]强制删除文件
# more
如果某个文本很大，一页显示不完，可以使用more [file]来显示，按下空格才会显示下一页，按q退出
# 管道
举例来说，我要显示/usr/bin下的文件，但是这里面的文件太多了，一页显示不完，想借助more来显示，可以
```
jonah@Inspiron-3420:/usr/bin$ ls |more

```
中间`|`就是管道符号，作用是把上一个命令的输出作为下一个命令的输入
```
jonah@Inspiron-3420:/usr/bin$ ls |grep "x86*"
cpan5.22-x86_64-linux-gnu
perl5.22-x86_64-linux-gnu
x86_64
x86_64-linux-gnu-addr2line
x86_64-linux-gnu-ar
x86_64-linux-gnu-as
x86_64-linux-gnu-c++filt
x86_64-linux-gnu-cpp
x86_64-linux-gnu-cpp-5
x86_64-linux-gnu-dwp
x86_64-linux-gnu-elfedit
x86_64-linux-gnu-g++
x86_64-linux-gnu-g++-5
x86_64-linux-gnu-gcc
x86_64-linux-gnu-gcc-5
x86_64-linux-gnu-gcc-ar
x86_64-linux-gnu-gcc-ar-5
x86_64-linux-gnu-gcc-nm
x86_64-linux-gnu-gcc-nm-5
x86_64-linux-gnu-gcc-ranlib
x86_64-linux-gnu-gcc-ranlib-5
x86_64-linux-gnu-gcov
x86_64-linux-gnu-gcov-5
x86_64-linux-gnu-gcov-tool
x86_64-linux-gnu-gcov-tool-5
x86_64-linux-gnu-gprof
x86_64-linux-gnu-ld
x86_64-linux-gnu-ld.bfd
x86_64-linux-gnu-ld.gold
x86_64-linux-gnu-nm
x86_64-linux-gnu-objcopy
x86_64-linux-gnu-objdump
x86_64-linux-gnu-pkg-config
x86_64-linux-gnu-ranlib
x86_64-linux-gnu-readelf
x86_64-linux-gnu-size
x86_64-linux-gnu-strings
x86_64-linux-gnu-strip
x86_64-pc-linux-gnu-pkg-config
```
# cat和重定向
看一段例子
```
onah@Inspiron-3420:~/linux_operation$ ls
1.txt  2.txt  3.txt  4.txt  5.tat  6.tbt
jonah@Inspiron-3420:~/linux_operation$ cat 1.txt
hello world!
jonah@Inspiron-3420:~/linux_operation$ cat 2.txt
hello python!
jonah@Inspiron-3420:~/linux_operation$ cat 1.txt 2.txt
hello world!
hello python!
jonah@Inspiron-3420:~/linux_operation$ cat 1.txt 2.txt > new1.txt
jonah@Inspiron-3420:~/linux_operation$ cat new1.txt 
hello world!
hello python!
```
cat和more一样也可以显示文本内容，但是不会像more那样分页显示，而是直接完全显示，但是cat可以同时显示多个文本，这样就可以利用cat和重定向来生成一个合并多个文本的新文本
# find
查找文件，还是看一个例子
```
jonah@Inspiron-3420:~/linux_operation$ ls
1.txt  2.txt  3.txt  4.txt  5.tat  6.tbt  new1.txt
jonah@Inspiron-3420:~/linux_operation$ find ./ -name "*.t?t"
./2.txt
./4.txt
./3.txt
./1.txt
./6.tbt
./5.tat
./new1.txt
jonah@Inspiron-3420:~/linux_operation$ find ./ -name "*.txt"
./2.txt
./4.txt
./3.txt
./1.txt
./new1.txt
jonah@Inspiron-3420:~/linux_operation$ find ./ -size -1K
find: 无效的 -size 类型“K”
jonah@Inspiron-3420:~/linux_operation$ find ./ -size -1024
./
./2.txt
./4.txt
./3.txt
./1.txt
./6.tbt
./5.tat
./new1.txt
```
find可以根据文件名来查找，也可以根据文件大小来查找

# cp和mv
拷贝文件和移动文件
```
jonah@Inspiron-3420:~/linux_operation$ ls
1.txt  2.txt  3.txt  4.txt  5.tat  6.tbt  new1.txt  newdir
jonah@Inspiron-3420:~/linux_operation$ cp 5.tat ./newdir/
jonah@Inspiron-3420:~/linux_operation$ ls newdir/
5.tat
jonah@Inspiron-3420:~/linux_operation$ mv 6.tbt ./newdir/
jonah@Inspiron-3420:~/linux_operation$ ls
1.txt  2.txt  3.txt  4.txt  5.tat  new1.txt  newdir
jonah@Inspiron-3420:~/linux_operation$ ls newdir/
5.tat  6.tbt
```
基本用法 cp [源文件] [目标路径]

# tar归档和压缩
事实上，tar可以只归档不压缩也可以指定参数来压缩，比如：
```
jonah@Inspiron-3420:~/linux_operation$ ls
1.txt  2.txt  3.txt  4.txt  5.tat  new1.txt  newdir
jonah@Inspiron-3420:~/linux_operation$ tar -cvf Test.tar ./*
./1.txt
./2.txt
./3.txt
./4.txt
./5.tat
./new1.txt
./newdir/
./newdir/6.tbt
./newdir/5.tat
jonah@Inspiron-3420:~/linux_operation$ ls
1.txt  2.txt  3.txt  4.txt  5.tat  new1.txt  newdir  Test.tar
jonah@Inspiron-3420:~/linux_operation$ gzip Test.tar 
jonah@Inspiron-3420:~/linux_operation$ ls
1.txt  2.txt  3.txt  4.txt  5.tat  new1.txt  newdir  Test.tar.gz
```
tar先进行归档，然后使用gzip来进行压缩，最后得到tar.gz文件，如果要解压，先使用gzip -d Test.tar.gz，再tar -xvf Test.tar恢复成原来的样子。
也可以一步到位，tar -zxvf .....
```
jonah@Inspiron-3420:~/linux_operation$ tar -zcvf Test.tar.gz ./*
./1.txt
./2.txt
./3.txt
./4.txt
./5.tat
./new1.txt
./newdir/
./newdir/6.tbt
./newdir/5.tat
jonah@Inspiron-3420:~/linux_operation$ ls
1.txt  2.txt  3.txt  4.txt  5.tat  new1.txt  newdir  Test.tar.gz
```
除了gz还有bz压缩方式:
```
jonah@Inspiron-3420:~/linux_operation$ tar -jcvf Test.tar.bz ./*
./1.txt
./2.txt
./3.txt
./4.txt
./5.tat
./new1.txt
./newdir/
./newdir/6.tbt
./newdir/5.tat
jonah@Inspiron-3420:~/linux_operation$ ls
1.txt  2.txt  3.txt  4.txt  5.tat  new1.txt  newdir  Test.tar.bz
```
如果需要制定解压的目录，则tar -zxvf test.tar.gz -C xxxx/

# zip和unzip
zip压缩用法：
zip [目标文件名] [压缩源目录]
比如zip test ./* 把当前目录下的所有文件目录压缩到test.zip中去
unzip解压用法：
unzip -d [解压目标路径] [压缩文件]

# ssh
ssh 用户名@ip，远程登录
假设目标主机存在用户jonah,IP地址为192.168.1.101，那么就是ssh jonah@192.168.1.101

# which
查看链接的最终目标路径，比如：
```
jonah@Inspiron-3420:~/linux_operation$ which python
/usr/bin/python
jonah@Inspiron-3420:~/linux_operation$ which python3
/usr/bin/python3
```
# useradd,userdel和passwd
创建账户useradd和设置密码passwd,都需要root权限：
```
jonah@Inspiron-3420:~$ sudo useradd yqzeng -m -d /home/yqzeng
[sudo] jonah 的密码： 
jonah@Inspiron-3420:~$ sudo passwd yqzeng
输入新的 UNIX 密码： 
重新输入新的 UNIX 密码： 
passwd：已成功更新密码
```
切换到创建的账户：
```
jonah@Inspiron-3420:/home$ su yqzeng
密码： 
yqzeng@Inspiron-3420:/home$ 
```
也可以su - yqzeng,这样登陆后直接进入这个账户的用户根目录.
删除账户，sudo userdel -r yqzeng即可，如果不加-r，则不会删除/home/yqzeng，反之则删除

# groupadd,groupmod, usermod组管理
创建一个账户后，需要加入某些组获取权限；
创建一个组，groupadd [组名]，在/etc/group这个文件里就可以看到新添加的组，如果要删掉，使用groupdel [组名]，如果需要修改group的名称或者GID等信息，使用groupmod;
重要的是，如何管理用户，需要使用usermod命令，比如：
usermode -g [组名] username，username这个账户就被加入到这个组当中，并且这个组是这个账户的默认组，如果要把这个组添加到别的组，使用usermode -a -G [组名] username，如果需要使这个账户可以获取root权限，则需要加入adm组或者sudo组，usermode -a -G sudo username

# chmod
改变文件的读写可执行权限，主要记两种写法
第一种，chmod u=rwx, g=r-w, o=r-x [filename]，这样导致这个文件的权限为rwxr-xr-x。u=user, g=group,o=other;
第二种，chmod 755 [filename],导致的权限为rwxr-xr-x，这是二进制表示法，效果一样

# 升级新内核后旧的内核会保留，查看当前安装了哪些内核，以及正在使用哪个内核：
```
jonah@Inspiron-3420:~$ sudo dpkg --get-selections|grep linux-image
linux-image-4.10.0-38-generic			install
linux-image-4.10.0-40-generic			install
linux-image-extra-4.10.0-38-generic		install
linux-image-extra-4.10.0-40-generic		install
jonah@Inspiron-3420:~$ uname -a
Linux Inspiron-3420 4.10.0-38-generic #42~16.04.1-Ubuntu SMP Tue Oct 10 16:32:20 UTC 2017 x86_64 x86_64 x86_64 GNU/Linux

```
然后删除不用的内核：
```
sudo apt-get purge +内核
```
最后清除配置
```
sudo dpke -P +内核
```
