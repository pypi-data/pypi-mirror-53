from setuptools import setup, find_packages
from codecs import open
from os import path

name = "pyVali"
here = path.abspath(path.dirname(__file__))

with open('README.rst', encoding='utf-8') as f:
    long_description = f.read()

# setup(
#     name='pyVali',
#     version='0.0.1',
#     author='gpsbird',
#     author_email="704415698@qq.com",
#     packages=find_packages(),
#     license='MIT',
#     description='python parameter validate',
#     long_description=long_description,
#     url='https://github.com/gpsbird/pyVali'
# )
setup(
    name="pyVali",
    version="0.0.1",
    author="gpsbird",
    author_email="gpsbird@qq.com",
    description="python parameter validate",
    long_description="""
======
README
======
pyVali is a validation tool for python

    Python 2 and 3 compatible

Common usage::

    from pyVali import Int,Float,Str,Dict,List

    value = {
        "user_id": 123,
        "tenant_id": 345,
        "question_list": [{
            "question_id": "asdfsdf",
            "question": "你好？",
            "answer": "我很好，你是谁？",
            "status": 0,
        }]
    }
    schema = Dict({
        "user_id": Int(comment="用户id"),
        "tenant_id": Int(comment="tenant_id"),
        "question_list": List(
            struct=[Dict(
                {"question_id": Str(comment="问题id"),
                 "question": Str(comment="问题"),
                 "answer": Str(comment="回答"),
                 "status": Int(comment="状态")},
                comment="问题")],
            comment="问题列表")
    })

    print(schema.validate(value))

    sub_schema = Dict(struct={"question_id": Str(comment="问题id"),
                              "question": Str(comment="问题"),
                              "answer": Str(comment="回答"),
                              "status": Int(comment="状态")},
                      comment="问题")
    schema = Dict({
        "user_id": Int(comment="用户id"),
        "tenant_id": Int(comment="tenant_id"),
        "question_list": List(
            struct=[sub_schema, ],
            comment="问题列表")
    })
    err, value = schema.validate(value)    
""",
    # long_description_content_type="text/markdown",
    url="https://github.com/gpsbird/pyVali",
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
