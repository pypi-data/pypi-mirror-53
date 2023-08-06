import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name = 'recmetrics_sweep',
    packages=setuptools.find_packages(),
    version = '0.0.0',  # Ideally should be same as your GitHub release tag varsion
    description = 'Execute all desired rec metrics at once, quickly, including with different values of k.',
    long_description=long_description,
    long_description_content_type="text/markdown",
    author = 'Joshua Mathias',
    author_email = 'joshuaamathias@gmail.com',
    url = 'https://github.com/JoshuaMathias/recmetrics_sweep',
    # download_url = 'download link you saved',
    keywords = ['recommendation', 'recommender systems', 'evaluation', 'metrics'],
    classifiers = [
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",],
)