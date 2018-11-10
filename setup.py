from setuptools import setup
try:
    import pypandoc
    description = pypandoc.convert('README.md','rst')
    
except:
    description=''
setup(name='lyrics_download',
      version="0.0.1",
      description='Download song lyrics',
      author="analyticsbot",
      author_email='email@email.com',
      license='MIT',
      packages=['lyrics_download'],
      url="http://github.com/analyticsbot/lyrics_download",
      install_requires=[
            'beautifulsoup4','requests', 'wikipedia'],
      classifiers=[
          "Development Status :: Development",
          "License :: OSI Approved :: MIT License",
          "Programming Language :: Python"
      ],
      zip_safe=False)
