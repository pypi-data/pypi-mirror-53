from distutils.core import setup

setup(
    name='CanvasScraper',
    version='0.2dev',
    description='D/L Lectures/Data from Canvas',
    author='Stu Campbell',
    author_email='stucampbell.git@gmail.com',
    packages=[
        'canvasscraper',
        'canvasscraper.fileops',
        'canvasscraper.objects',
    ],
    license='MIT License',
    long_description=open('README.txt').read(),
    install_requires=[
              'youtube-dl',
              'chromedriver',
              'chromedriver-binary',
              'selenium'
          ],

    classifiers=[
            'Topic :: Education',
            'Topic :: Education :: Computer Aided Instruction (CAI)',
            'Topic :: Multimedia :: Video',
            'Development Status :: 2 - Pre-Alpha',
            'Environment :: Console',
            'Environment :: Web Environment',
            'License :: Public Domain',
            'Programming Language :: Python :: 3',
            'Programming Language :: Python :: 3.7',
            'Programming Language :: Python :: 3.8',
        ],
)