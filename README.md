## 代码自动生成工具

注意：因为Mac的sed和gnu-sed有一些不同，Mac的sed版本可能比较低，所以遇到sed会指明使用gnu-sed。gnu-sed安装命令 brew install gnu-sed



开发新项目，写了几个脚本用来生成一些格式固定的代码。

比如说依据后台的接口返回的json生成model文件的属性。

输入

```
{
	"name" : "张三"
}
```

输出

```
@property (nonatomic, copy) NSString *name;
```

其他成员觉得能用的上，但是有些麻烦，想使用图形界面操作,因此写了一个简单的Mac OS App，后续会不定期更新这个App的代码。

### Json 生成属性声明 

![屏幕快照2019-06-26下午4.47.52.png](https://i.loli.net/2019/06/26/5d133238850eb70741.png)

### 控件名字生成控件属性声明

![屏幕快照2019-06-26下午4.57.23.png](https://i.loli.net/2019/06/26/5d13337c253b733371.png)

### 控件属性声明生成getter、addSubview、约束语句

![屏幕快照2019-06-26下午4.54.17.png](https://i.loli.net/2019/06/26/5d1332d2a56f569257.png)

目前就是这么简单，只能后续逐步改进了。




