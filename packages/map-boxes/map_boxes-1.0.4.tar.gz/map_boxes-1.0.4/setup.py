try:
    from setuptools import setup
except:
    from distutils.core import setup

setup(
    name='map_boxes',
    version='1.0.4',
    author='Roman Sol (ZFTurbo)',
    packages=['map_boxes', ],
    url='https://github.com/ZFTurbo/Mean-Average-Precision-for-Boxes',
    license='MIT License',
    description='Function to calculate mAP for set of detected boxes and annotated boxes. ',
    long_description='Function to calculate mean average precision (mAP) for set of boxes. Useful for object detection pipelines.'
                     'More details: https://github.com/ZFTurbo/Mean-Average-Precision-for-Boxes',
    install_requires=[
        "numpy",
        "pandas",
    ],
    package_data={'': ['compute_overlap.pyx']},
    include_package_data=True,
)
