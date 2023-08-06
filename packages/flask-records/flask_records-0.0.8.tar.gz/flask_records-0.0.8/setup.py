import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="flask_records",
    version="0.0.8",
    author="leo",
    author_email="leo.anonymous@qq.com",
    description="Flask wrapper for the SQL Records",
    # 包的详细介绍(一般通过加载README.md)
    long_description=long_description,
    # 和上条命令配合使用，声明加载的是markdown文件
    long_description_content_type="text/markdown",
    # 项目开源地址，我这里写的是同性交友官网，大家可以写自己真实的开源网址
    url="https://github.com/",
    # 如果项目由多个文件组成，我们可以使用find_packages()自动发现所有包和子包，而不是手动列出每个包，在这种情况下，包列表将是example_pkg
    packages=setuptools.find_packages(),
    classifiers=[                                           # 关于包的其他元数据(metadata)
        "Programming Language :: Python :: 3",              # 该软件包仅与Python3兼容
        "License :: OSI Approved :: MIT License",           # 根据MIT许可证开源
        "Operating System :: OS Independent",               # 与操作系统无关
    ],
    install_requires=['Flask>=0.9',
                      'Flask-SQLAlchemy>=1.0',
                      'records>=0.5.3'],
    test_suite="tests"
)
