import setuptools
import os



base_packages = ["scikit-learn>=0.20.2",
                 "pandas>=0.25",
                 "matplotlib==3.1.1",
                 "seaborn>=0.9.0",
                 "shap>=0.29",
		        "joblib>=0.13.2"]

try:
    if os.environ.get('CI_COMMIT_TAG'):
        version = os.environ['CI_COMMIT_TAG']
    else:
        version = os.environ['CI_JOB_ID']
except:
    version = 'local'


setuptools.setup(
    name='probatus',
    version='0.1',
    description='Validate your models like a lion',
    author='RPAA ING',
    author_email='ml_risk_and_pricing_aa@ing.com',
    license='MIT License',
    packages=setuptools.find_packages(),
    package_data={'pyrisk': ['datasets/data/*.pkl']},
    install_requires=base_packages,
    url='https://gitlab.com/ing_rpaa/pyrisk',
    zip_safe=False
)
