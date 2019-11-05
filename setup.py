from setuptools import setup
from setuptools import find_packages

setup(
    name='honoka_utility',
    version='0.0',
    description='The utility modules.',
    url='https://gitlab.rdcloud.intra.hitachi.co.jp/71389710/honoka_utility',
    author='Honoka',
    author_email='terufumi.morishita.wp@hitachi.com',
    license='Hitachi R&D',
    install_requires=[
        'chardet',
        # 'git+https://gitlab.rdcloud.intra.hitachi.co.jp/hitachi-nlp/python-log-handler.git@master',
        # 'planispai@git+https://gitlab.rdcloud.intra.hitachi.co.jp/hitachi-nlp/planispai.git@master',
        # 'tre2@git+https://gitlab.rdcloud.intra.hitachi.co.jp/hitachi-nlp/tre2.git@honoka_dev'
    ],
    packages=find_packages(),   # __init__.pyのあるディレクトリを探してきて，パッケージに追加．
    package_data={'honoka_utility': ['data/*']},     # その他，パッケージに含めたいデータを記述．
    zip_safe=False,
)
