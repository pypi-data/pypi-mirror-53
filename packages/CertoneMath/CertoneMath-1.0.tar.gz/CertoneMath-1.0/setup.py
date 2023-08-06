from distutils.core import setup

setup(
    name='CertoneMath',  # 对外我们模块的名字
    version='1.0',  # 版本号
    description='这是第一个对外发布的模块，测试哦',  # 描述
    author='Certone',  # 作者
    author_email='Certone@163.com',
    py_modules=['CertoneMath.demo1', 'CertoneMath.demo2']  # 要发布的模块
)

# python setup.py sdist
# python setup.py install
# python setup.py sdist upload
