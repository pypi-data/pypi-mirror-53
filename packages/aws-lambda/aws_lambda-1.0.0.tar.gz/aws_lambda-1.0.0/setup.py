from setuptools import setup, find_packages

setup(
    name='aws_lambda',
    version='1.0.0',
    license='GNU GENERAL PUBLIC LICENSE Version 3',
    packages=find_packages(),
    description='Package which helps to do various actions associated with AWS Lambda functions.',
    include_package_data=True,
    install_requires=[
        'boto3',
        'botocore',
        'troposphere',
        'cfnresponse'
    ],
    author='Laimonas Sutkus',
    author_email='laimonas.sutkus@gmail.com',
    keywords='AWS SDK CloudFormation Lambda Infrastructure Cloud',
    url='https://github.com/laimonassutkus/AwsCfSdk',
    classifiers=[
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Operating System :: OS Independent',
    ],
)
