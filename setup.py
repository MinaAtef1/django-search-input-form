from setuptools import setup, find_packages
# Remove the unused import statement for glob
# Add the templates folder to the build configuration
from setuptools import setup, find_packages


setup(
    name='django-search-input-field',
    version='0.1.2',
    license='MIT',
    author="Treyd Services AB",
    author_email='support@treyd.io',
    packages=find_packages(include=['django_search_input_field', 'django_search_input_field.*',
                                    'django_search_input_field.templates', 'django_search_input_field.templates.*']),
    include_package_data=True,
    package_data={'django_search_input_field': ['django_search_input_field/templates/*']},
    url='https://github.com/minaaaatef/django-search-input-form',
    install_requires=[

    ],
)
