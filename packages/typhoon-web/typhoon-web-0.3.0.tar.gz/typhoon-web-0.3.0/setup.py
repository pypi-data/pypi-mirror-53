from setuptools import setup, find_packages

with open('README.md', 'r', encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='typhoon-web',
    version=__import__('typhoon').__version__,
    description='A wrapper around the Tornado web framework that supports logs with traceId.',
    long_description=long_description,
    long_description_content_type="text/markdown",
    author='WeiJi Hsiao',
    author_email='weiji.hsiao@gmail.com',
    license='MIT License',
    url='https://github.com/WeiJiHsiao/typhoon',
    packages=find_packages(),
    install_requires=['tornado>=5.1'],
    classifiers=[
        "Intended Audience :: Developers",
        "Operating System :: OS Independent",
        "Topic :: Software Development :: Libraries :: Python Modules"
    ]
)
