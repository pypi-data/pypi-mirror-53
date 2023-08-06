import setuptools
  
with open("README.md", "r") as f:
    long_description = f.read()

setuptools.setup(
   name="trank",
   version="0.1.0",
   author="Grupo Investigativo de Sistemas",
   #author_email="",
   description="A web based application to rank tennis players",
   long_description=long_description,
   long_description_content_type="text/markdown",
   url="https://bitbucket.org/grupoinvestigativodesistemas/trank",
   packages=setuptools.find_packages(),
   include_package_data=True,
   classifiers=[
      'Programming Language :: Python :: 3',
      'License :: OSI Approved :: BSD License',
      'Operating System :: OS Independent',
   ],
   python_requires = '>= 3.7.4',
   install_requires=[
      'psycopg2 == 2.8.*',
      'pycrypto == 2.6.*',
      'flask == 1.0.*',
      'pyjade == 4.0.*',
      'queuepool == 1.3.*',
      'pyaconf == 0.7.*',
      'pyyaml == 5.1.*',
   ],
   scripts = [
      'trank_start',
   ],
   project_urls={
        'Bug Reports': 'https://bitbucket.org/grupoinvestigativodesistemas/trank/issues',
   },
)

