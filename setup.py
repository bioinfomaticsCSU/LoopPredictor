import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name='looppredictor',
    version='0.4.10',
    packages=setuptools.find_packages(),
    url='https://github.com/bioinfomaticsCSU/LoopPredictor/',
    author='Li Tang',
    author_email='tangli_csu@csu.edu.cn',
    install_requires=[
        'pandas>=0.24.2',
        'numpy>=1.16.2',
        'scikit-learn>=0.20.3,<0.20.4',
        'pathos>=0.2.3',
    ],
    license='LICENSE',
    description='Predicting unknown enhancer-mediated genome topology by an ensemble machine learning model',
    long_description=long_description,
    long_description_content_type="text/markdown",
    include_package_data = True,

    entry_points={
        'console_scripts': [
            'looppredictor=looppredictor.looppredictor:main',
            'customized_gbrt_trainer=looppredictor.customized_gbrt_trainer:main',
            'classifyloops=looppredictor.classifyloops:main',
            ],
        },
)
