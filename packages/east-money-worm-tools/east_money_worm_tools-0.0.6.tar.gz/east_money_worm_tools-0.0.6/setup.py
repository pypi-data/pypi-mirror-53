# coding=utf8
import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()
setuptools.setup(
    name='east_money_worm_tools',
    version='0.0.6',
    description='east_money_worm_tools',
    long_description=long_description,
    long_description_content_type="text/markdown",
    keywords='east_money_worm_tools',
    install_requires=[],
    packages=setuptools.find_packages(),
    author='Peter Wang',
    author_email='2856954422@qq.com',
    classifiers=[
        # 'Development Status :: 1 - Planning',
        # 'Development Status :: 2 - Pre-Alpha',
        # 'Development Status :: 3 - Alpha',
        # 'Development Status :: 4 - Beta',
        # 'Development Status :: 5 - Production/Stable'
        'Development Status :: 5 - Production/Stable',  
        'Intended Audience :: Developers', 
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
    ],
)
