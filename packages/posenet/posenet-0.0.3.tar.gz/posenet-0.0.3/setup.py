from setuptools import setup

setup (
  name='posenet',
  version='0.0.3',
  packages=['posenet'],
  keywords = ['machine-vision', 'computer-vision', 'image-processing', 'data-collection'],
  description='Extract pose vertex data from images',
  url='https://github.com/yaledhlab/posenet',
  author='Douglas Duhaime',
  author_email='douglas.duhaime@gmail.com',
  license='MIT',
  install_requires=[
    'numpy>=1.12.0',
    'opencv-python>=3.4.5.20',
    'Pillow>=6.1.0',
    'PyYAML>=5.1',
    'scipy>=1.1.0',
    'tensorflow>=1.14.0',
  ],
  package_data={
    'posenet': ['converter/*'],
  },
)

