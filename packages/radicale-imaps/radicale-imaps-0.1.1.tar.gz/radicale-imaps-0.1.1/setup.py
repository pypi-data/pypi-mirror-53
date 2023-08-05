from setuptools import find_packages, setup


setup(
    name='radicale-imaps',
    version='0.1.1',
    author='Louis Guidez',
    author_email='louis@hostux.fr',
    url='https://github.com/reind33r/radicale-imaps',
    description='Radicale IMAPs authentication plugin',
    include_package_data=True,
    zip_safe=False,
    packages=find_packages(),
    install_requires=['radicale'],
    license='LICENSE',
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Environment :: Console',
        'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 3 :: Only',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
    ]
)
