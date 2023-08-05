from setuptools import setup, find_packages

version = '1.0.33'

setup(
	name='primalytics',
	packages=find_packages(),
	version=version,
	license='MIT',											# Chose a license from here: https://help.github.com/articles/licensing-a-repository
	description='Analytic library for Prima',				# Give a short description about your library
	author='Stefano Rossotti',
	author_email='stefano.rossotti@hotmail.it',
	url='https://github.com/user/reponame',					# Provide either the link to your github or to your website
	download_url='https://github.com/primait/prima-analytics/archive/{}.tar.gz'.format(version),
	keywords=['prima', 'analytics'], 						# Keywords that define your package best
	install_requires=[
		'numpy>=1.16.2',
		'pandas>=0.24.2',
		'matplotlib>=3.0.3',
		'scikit-learn>=0.20.3',
		'seaborn',
		'pydotplus',
		'IPython'
	],
	classifiers=[
		'Development Status :: 3 - Alpha',      			# Chose either "3 - Alpha", "4 - Beta" or "5 - Production/Stable" as the current state of your package
		'Intended Audience :: Developers',      			# Define that your audience are developers
		'Topic :: Software Development :: Build Tools',
		'License :: OSI Approved :: MIT License',   		# Again, pick a license
		'Programming Language :: Python :: 3',      		# Specify which pyhton versions that you want to support
		'Programming Language :: Python :: 3.4',
		'Programming Language :: Python :: 3.5',
		'Programming Language :: Python :: 3.6',
		'Programming Language :: Python :: 3.7',
	],
)