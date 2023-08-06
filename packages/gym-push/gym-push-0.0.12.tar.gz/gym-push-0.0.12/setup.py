from setuptools import setup, find_packages

setup(name='gym-push',
      packages=find_packages(),
      package_data={
        '': ['*.csv', '*.npy'],
      },      
      include_package_data=True,
      version='0.0.12',
      install_requires=['gym', 'numpy', 'pandas', 'joblib', 'eel', 'json-tricks'], 
      author='Kieran Fraser',
      author_email='kfraser@tcd.ie',
      download_url='https://github.com/kieranfraser/gym-push/raw/master/dist/gym-push-0.0.10.tar.gz'
) 