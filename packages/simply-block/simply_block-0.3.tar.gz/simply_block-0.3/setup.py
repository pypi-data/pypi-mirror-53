from distutils.core import setup
setup(
  name='simply_block',
  packages=['simply_block'],
  version='0.3',
  license='MIT',
  description='Signing and Request package for Simply Block API Gateway',
  author='Jitender Bhutani',
  author_email = 'Jitender.Bhutani21@gmail.com',
  url='https://github.com/JitenderBhutani/simply_block',
  download_url='https://github.com/JitenderBhutani/simply_block/archive/0.3.tar.gz',
  keywords=['Simply', 'Block', 'Simply Block', "Blockchain"],   # Keywords that define your package best
  install_requires=[            # TODO
      'requests_toolbelt',
      'requests',
      ],
  classifiers=[
    'Development Status :: 3 - Alpha',      # Chose either "3 - Alpha", "4 - Beta" or "5 - Production/Stable" as the current state of your package
    'Intended Audience :: Developers',
    'Topic :: Software Development :: Build Tools',
    'License :: OSI Approved :: MIT License',
    'Programming Language :: Python :: 2.7',
    'Programming Language :: Python :: 3.6',
  ],
)