from setuptools import setup, find_packages
from d2lbook import __version__

requirements = [
    'jupyter',
    'sphinx==1.8.5',  # sphinx 2.0 has a bug in search
    'recommonmark',
    'sphinxcontrib-bibtex',
    'mu-notedown',
    'mxtheme>=0.3.9',
    'sphinxcontrib-svg2pdfconverter',
    'numpydoc',
    'awscli',
]

setup(
    name='d2lbook',
    version=__version__,
    install_requires=requirements,
    python_requires='>=3.5',
    author='D2L Developers',
    author_email='d2l.devs@google.com',
    url='https://book.d2l.ai',
    description="Create an online book with Jupyter Notebooks and Sphinx",
    license='Apache-2.0',
    packages=find_packages(),
    include_package_data=True,
    package_data={'d2lbook':['config_default.ini', 'upload_doc_s3.sh']},
    entry_points={
        'console_scripts': [
            'd2lbook = d2lbook.main:main',
        ]
    },
)
