from setuptools import setup

with open('README.md', 'r') as fp:
    long_desc = fp.read()

setup(
    name='discord_msg_lite',
    version='2',
    author='Tom YU Choe',
    author_email='yonguk.choe@gmail.com',
    description='A simple and lightweight Python PyPI module to send messages easily using Discord Webhooks.',
    long_description=long_desc,
    url='https://github.com/YUChoe/discord_msg_lite',
    long_description_content_type="text/markdown",
    py_modules=['discord_msg_lite'],
    package_dir={'': 'src'},
    license='MIT',
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Intended Audience :: Information Technology",
        "Intended Audience :: Developers",
        "Intended Audience :: System Administrators",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.4",
        "Programming Language :: Python :: 3.6",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)