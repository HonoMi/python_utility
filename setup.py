from setuptools import setup

setup(
    name='honoka_utility',
    version='0.0',
    description='The utility modules.',
    url='https://gitlab.rdcloud.intra.hitachi.co.jp/71389710/python_utility',
    author='HonoHono',
    author_email='terufumi.morishita.wp@hitachi.com',
    license='MIT',
    install_requires=[
        'chardet',
        'coloredlogs'
        # 'honoka_utility==0.0',    # private repositoryの依存．バージョンを指定しないと動かない．
    ],
    dependency_links=[
        # private repositoryの依存．バージョンを指定しないと動かない．
        # 'git+https://gitlab.rdcloud.intra.hitachi.co.jp/71389710/python_utility.git#egg=honoka_utility-0.0'
    ],
    packages=['honoka_utility'],
    zip_safe=False,
)
