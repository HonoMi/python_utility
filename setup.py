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
        'chardet'
        'python_log_handler@git+https://gitlab.rdcloud.intra.hitachi.co.jp/hitachi-nlp/python-log-handler'
        # 'planispai@git+https://gitlab.rdcloud.intra.hitachi.co.jp/hitachi-nlp/planispai',
        # 'tre2@git+https://gitlab.rdcloud.intra.hitachi.co.jp/hitachi-nlp/tre2.git@honoka_dev'     # 別ブランチの指定
    ],
    packages=find_packages(),   # __init__.pyのあるディレクトリを探してきて，パッケージに追加．
    package_data={'honoka_utility': ['data/*']},     # その他，パッケージに含めたいデータを記述．
    zip_safe=False,
)
