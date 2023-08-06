from setuptools import setup


with open('README.md', 'r') as f:
    readme = f.read()


if __name__ == '__main__':
    setup(
        name='marshmallow_pageinfo',
        version='1.0.0',
        author='Dmitriy Pleshevskiy',
        author_email='dmitriy@ideascup.me',
        description='Page info marshmallow schema for api',
        long_description=readme,
        long_description_content_type='text/markdown',
        package_data={'': ['LICENSE', 'README.md']},
        include_package_data=True,
        license='MIT',
        packages=['marshmallow_pageinfo']
    )
