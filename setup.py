from setuptools import setup, find_packages

setup(
    name='honoka_utility',
    version='0.0',
    description='The utility modules.',
    url='https://gitlab.rdcloud.intra.hitachi.co.jp/71389710/python_utility',
    author='Honoka',
    author_email='terufumi.morishita.wp@hitachi.com',
    license='Hitashi R&D',
    install_requires=[
        'chardet',
        'coloredlogs'
        # 'honoka_utility==0.0',    # private repositoryへの依存は，バージョンを指定しないと動かない．
    ],
    dependency_links=[
        # private repositoryの依存がある場合に，探すリンクを書く．バージョンを指定しないと動かない．
        # 'git+https://gitlab.rdcloud.intra.hitachi.co.jp/71389710/python_utility.git#egg=honoka_utility-0.0'
    ],
    packages=find_packages(),   # __init__.pyのあるディレクトリを探してきて，パッケージに追加．
    package_data={'honoka_utility': ['data/*']},     # その他，パッケージに含めたいデータを記述．
    zip_safe=False,
)
