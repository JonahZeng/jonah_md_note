
为什么要写这个笔记
---------------------------
因为真的容易忘记各个常用的绘图函数的参数和用法。

因此，我想写一个note，把常用的直线图，轮廓图，直方图，3d图绘制方式和参数做一个记录，参数力求全面。

这个笔记要求你懂一点Python3和numpy库，对matplotlib的结构要有一定了解，如果这方面的基础缺失的话，建议花一两天时间熟悉一下，这个笔记用到的知识点并不多。

# 划分axes
首先是一个简单的示例：


```python
import numpy as np
import matplotlib.pyplot as plt
import seaborn
seaborn.set(style='darkgrid')#美化，有white,whitegrid,dark,darkgrid 4种选项

fig, ax_list = plt.subplots(2,2)# 划分2x2 axes，并返回ax_list保存4个axes
type(ax_list[0, 0])
```




    matplotlib.axes._subplots.AxesSubplot




![png](https://github.com/JonahZeng/jonah_md_note/blob/master/matplotlib/20190408_plot_contourf/output_1_1.png?raw=true)


换种方式来添加axes:


```python
fig = plt.figure(0)
ax0 = fig.add_subplot(221)
ax1 = fig.add_subplot(222)
ax2 = fig.add_subplot(223)
ax3 = fig.add_subplot(224)
```


![png](https://github.com/JonahZeng/jonah_md_note/blob/master/matplotlib/20190408_plot_contourf/output_3_0.png)


# 折线图
仍然是一个简单的示例：


```python
x = np.linspace(0, 10, 20)
y1 = np.sin(x)
y2 = np.cos(x)

fig = plt.figure(0)
ax0 = fig.add_subplot(111)
ax0.set_xlabel('x axis')
ax0.set_ylabel('y axis')
ax0.set_title('sin & cos')
ax0.plot(x, y1, 'ro-', linewidth=1, markersize=2, label='sin')#和下面的写法一致
#ax0.plot(x, y1, color='red', linestyle='solid', marker='o', linewidth=1, markersize=2, label='sin')
ax0.plot(x, y2, 'b^--', linewidth=1, markersize=4, label='cos')
ax0.legend()
fig.tight_layout()
```


![png](https://github.com/JonahZeng/jonah_md_note/blob/master/matplotlib/20190408_plot_contourf/output_5_0.png)


关于折线图的颜色，线型，标记形状，有以下缩写供参考：

|代号|颜色|
|:-----:|:--:|
|'b'	|blue|
|'g'	|green|
|'r'    |red|
|'c'	|cyan|
|'m'	|magenta|
|'y'	|yellow|
|'k'	|black|
|'w'    |white|

|代号|marker形状|
|:--:|:--:|
|'.'	|point marker|
|','	|pixel marker|
|'o'	|circle marker|
|'v'	|triangle_down marker|
|'^'	|triangle_up marker|
|'<'	|triangle_left marker|
|'>'	|triangle_right marker|
|'1'	|tri_down marker|
|'2'	|tri_up marker|
|'3'	|tri_left marker|
|'4'	|tri_right marker|
|'s'	|square marker|
|'p'	|pentagon marker|
|'\*'	|star marker|
|'h'	|hexagon1 marker|
|'H'	|hexagon2 marker|
|'+'	|plus marker|
|'x'	|x marker|
|'D'	|diamond marker|
|'d'	|thin_diamond marker|
|'\|'	|vline marker|
|'_'|	|hline marker|

|代号	|description|
|:--:|:--:|
|'-'	|solid line style|
|'--'	|dashed line style|
|'-.'	|dash-dot line style|
|':'	|dotted line style|

## 自定义折线
plot函数的折线形状是可以自定义的：


```python
x = np.linspace(0, 10, 20)
y1 = np.sin(x)
y2 = np.cos(x)

fig = plt.figure(0)
ax0 = fig.add_subplot(111)
ax0.set_xlabel('x axis')
ax0.set_ylabel('y axis')
ax0.set_title('sin & cos')
line1, = ax0.plot(x, y1, 'r', linewidth=1, markersize=2, label='sin')
line1.set_dashes([2,2,10,2])
ax0.plot(x, y2, 'b^', dashes=[5,5], linewidth=1, markersize=4, label='cos')
ax0.legend()
fig.tight_layout()
```


![png](https://github.com/JonahZeng/jonah_md_note/blob/master/matplotlib/20190408_plot_contourf/output_10_0.png)


# 轮廓图


```python
from matplotlib import cm
x = np.linspace(-10, 10, 40)
y = np.linspace(-10, 10, 40)
X, Y = np.meshgrid(x, y)
Z = np.sin(X) + np.cos(Y)
fig = plt.figure(0)
ax = fig.add_subplot(111)
cs = ax.contourf(X, Y, Z, np.linspace(-2, 2, 11), cmap=cm.get_cmap('coolwarm'))
type(cs)
ax.set_xlabel('x')
ax.set_ylabel('y')
ax.set_axis_off()
fig.colorbar(cs)
```




    <matplotlib.colorbar.Colorbar at 0x306e5ac8>




![png](https://github.com/JonahZeng/jonah_md_note/blob/master/matplotlib/20190408_plot_contourf/output_12_1.png)


## 关于color map


```python
import numpy as np
import matplotlib.pyplot as plt


cmaps = [('Perceptually Uniform Sequential', [
            'viridis', 'plasma', 'inferno', 'magma', 'cividis']),
         ('Sequential', [
            'Greys', 'Purples', 'Blues', 'Greens', 'Oranges', 'Reds',
            'YlOrBr', 'YlOrRd', 'OrRd', 'PuRd', 'RdPu', 'BuPu',
            'GnBu', 'PuBu', 'YlGnBu', 'PuBuGn', 'BuGn', 'YlGn']),
         ('Sequential (2)', [
            'binary', 'gist_yarg', 'gist_gray', 'gray', 'bone', 'pink',
            'spring', 'summer', 'autumn', 'winter', 'cool', 'Wistia',
            'hot', 'afmhot', 'gist_heat', 'copper']),
         ('Diverging', [
            'PiYG', 'PRGn', 'BrBG', 'PuOr', 'RdGy', 'RdBu',
            'RdYlBu', 'RdYlGn', 'Spectral', 'coolwarm', 'bwr', 'seismic']),
         ('Cyclic', ['twilight', 'twilight_shifted', 'hsv']),
         ('Qualitative', [
            'Pastel1', 'Pastel2', 'Paired', 'Accent',
            'Dark2', 'Set1', 'Set2', 'Set3',
            'tab10', 'tab20', 'tab20b', 'tab20c']),
         ('Miscellaneous', [
            'flag', 'prism', 'ocean', 'gist_earth', 'terrain', 'gist_stern',
            'gnuplot', 'gnuplot2', 'CMRmap', 'cubehelix', 'brg',
            'gist_rainbow', 'rainbow', 'jet', 'nipy_spectral', 'gist_ncar'])]


gradient = np.linspace(0, 1, 256)
gradient = np.vstack((gradient, gradient))


def plot_color_gradients(cmap_category, cmap_list):
    # Create figure and adjust figure height to number of colormaps
    nrows = len(cmap_list)
    figh = 0.35 + 0.15 + (nrows + (nrows-1)*0.1)*0.22
    fig, axes = plt.subplots(nrows=nrows, figsize=(6.4, figh))
    fig.subplots_adjust(top=1-.35/figh, bottom=.15/figh, left=0.2, right=0.99)

    axes[0].set_title(cmap_category + ' colormaps', fontsize=14)

    for ax, name in zip(axes, cmap_list):
        ax.imshow(gradient, aspect='auto', cmap=plt.get_cmap(name))
        ax.text(-.01, .5, name, va='center', ha='right', fontsize=10,
                transform=ax.transAxes)

    # Turn off *all* ticks & spines, not just the ones with colormaps.
    for ax in axes:
        ax.set_axis_off()


for cmap_category, cmap_list in cmaps:
    plot_color_gradients(cmap_category, cmap_list)
```


![png](https://github.com/JonahZeng/jonah_md_note/blob/master/matplotlib/20190408_plot_contourf/output_14_0.png)



![png](https://github.com/JonahZeng/jonah_md_note/blob/master/matplotlib/20190408_plot_contourf/output_14_1.png)



![png](https://github.com/JonahZeng/jonah_md_note/blob/master/matplotlib/20190408_plot_contourf/output_14_2.png)



![png](https://github.com/JonahZeng/jonah_md_note/blob/master/matplotlib/20190408_plot_contourf/output_14_3.png)



![png](https://github.com/JonahZeng/jonah_md_note/blob/master/matplotlib/20190408_plot_contourf/output_14_4.png)



![png](https://github.com/JonahZeng/jonah_md_note/blob/master/matplotlib/20190408_plot_contourf/output_14_5.png)



![png](https://github.com/JonahZeng/jonah_md_note/blob/master/matplotlib/20190408_plot_contourf/output_14_6.png)
