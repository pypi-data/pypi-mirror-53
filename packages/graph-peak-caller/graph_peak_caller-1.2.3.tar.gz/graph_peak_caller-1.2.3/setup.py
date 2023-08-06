from setuptools import setup

setup(name='graph_peak_caller',
      version='1.2.3',
      description='Graph peak caller',
      url='http://github.com/uio-bmi/graph_peak_caller',
      author='Ivar Grytten and Knut Rand',
      author_email='',
      license='MIT',
      packages=['graph_peak_caller', 'graph_peak_caller.legacy', 'graph_peak_caller.control',
                'graph_peak_caller.sample', 'graph_peak_caller.postprocess',
                'graph_peak_caller.analysis', "graph_peak_caller.shiftestimation"],
      zip_safe=False,
      install_requires=['pymysql', 'numpy', 'filecache', 'scipy',
                        'memory_profiler', 'python-coveralls', 'matplotlib==3.0.0',
                        'biopython', 'pyfaidx', 'pyvg', 'offsetbasedgraph'
                        ],
      classifiers=[
            'Programming Language :: Python :: 3'
      ],
      entry_points = {
        'console_scripts': ['graph_peak_caller=graph_peak_caller.command_line_interface:main'],
      }

      )

"""
To update package:
#Update version number manually in this file

sudo python3 setup.py sdist
sudo python3 setup.py bdist_wheel
twine upload dist/graph_peak_caller-1.2.3.tar.gz 
"""
