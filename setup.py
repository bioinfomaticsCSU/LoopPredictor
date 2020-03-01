from distutils.core import setup

setup(
    name='LoopPredictor',
    version='0.1.0',
    author='Li Tang',
    author_email='tangli_csu@csu.edu.cn',
    packages=['looppredictor'],
    scripts=['bin/Customized_GBRT_trainer.py','bin/LoopPredictor.py','bin/ClassifyLoops.py'],
    url='http://pypi.python.org/pypi/looppredictor/',
    license='LICENSE.txt',
    description='Predicting unknown enhancer-mediated genome topology by an ensemble machine learning model',
    long_description=open('README.txt').read(),
    install_requires=[
        "pandas >= 0.24.2",
        "numpy >= 1.16.2",
        "scikit-learn = 0.20.3",
        "pathos >= 0.2.3"
    ]
)