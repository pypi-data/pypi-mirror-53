from distutils.core import setup
setup(
    name='banzhanSuperMath',#对外我们模块的名字
    version='1.0',#版本号
    description='这是第一个对外发布的模块，测试哦',#用于描述模块
    author='gaoqi',#作者
    author_email='gaoqi110@163.com',
    py_modules=['banzhanSuperMath.demo1','banzhanSuperMath.demo2']#要发布的模块
)