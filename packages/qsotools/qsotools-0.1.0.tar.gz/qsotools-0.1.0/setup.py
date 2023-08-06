from distutils.core import setup
import os,qsotools.__init__
from glob import glob

def get_data_names(root):
    '''
    Return list of all filenames (not directories) under root.
    '''
    temp = [root+'/*']
    for dirpath, dirnames, filenames in os.walk(root):
        temp.extend((os.path.join(dirpath, d, '*') for d in dirnames))
    names = []
    for path in temp:
        if any(os.path.isfile(f) for f in glob(path)):
            names.append(path.replace('qsotools/',''))
    return names

package_data = {'qsotools' : get_data_names('qsotools/data')}

setup(
    name="qsotools",
    version=qsotools.__version__,
    author="Vincent Dumont",
    author_email="vincentdumont@gmail.com",
    packages=["qsotools"],
    requires=["numpy","matplotlib","scipy","astropy"],
    package_data = package_data,
    include_package_data=True,
    scripts = glob('bin/*'),
    url="https://astroquasar.gitlab.io/programs/qsotools",
    description="Data analysis tools for quasar spectroscopy research",
    install_requires=[]
)
