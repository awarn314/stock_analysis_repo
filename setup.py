from distutils.core import setup

setup(
    name='stock_analysis_repo',
    version='1.0.0',
    packages=['yfinance',
              'pandas',
              'sklearn'],
    install_requires=['pandas',
                      'shapely',
                      'fiona',
                      'descartes',
                      'pyproj',
                      'rtree'],
    url='',
    license='MIT',
    author='Alex',
    author_email='alex.d.warning@gmail.com',
    description=''
)
