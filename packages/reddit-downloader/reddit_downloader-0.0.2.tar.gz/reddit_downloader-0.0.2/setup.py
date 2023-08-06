import setuptools

with open("README.md", 'r') as f:
    long_description = f.read()


setuptools.setup(
    name='reddit_downloader',
    version='0.0.2',
    packages=setuptools.find_packages(),
    url='https://gitlab.com/jeffmc/reddit_image_downloader',
    license='',
    author='Jeffrey McAthey',
    author_email='jeffmcathey@gmail.com',
    long_description=long_description,
    long_description_content_type="text/markdown",
    description='Image downloader based on subreddit.'
)
