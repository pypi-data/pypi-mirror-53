from setuptools import setup

setup(name='modern_future_hello_world',
      version='0.1.0',
      packages=['modern_future_hello_world'],
      entry_points={
          'console_scripts': [
              'modern_hello = modern_future_hello_world.hello_world:main'
          ]
      },
      )