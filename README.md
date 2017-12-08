# CarpeCrypto
Crypto The Day
## Development Enviornment
We are using python3.6.

In order to keep our packages up to date, we have carpecrypto_env.txt at the root of this repo.

Please create a new virtual environment for this project because this will make it easier to update the text file.
If you don't know how to do this: https://tinyurl.com/y7lu2d9l


Once you have a new environment, activate it and run
```
pip install -r carpecrypto_env.txt
```
in your command line, which will install everything you need.

If you install a new package, you can replace the file using
```
pip freeze > carpecrypto_env.txt
```
which will allow others to install everything you've added easily.

Please don't freeze a nonvirtual environment since you will be adding a lot of unnecessary packages.

## Kraken API
We are using: https://github.com/dominiktraxl/pykrakenapi to make API calls. This uses https://github.com/veox/python3-krakenex

Both are helpful to look at, the code is short and well commented.
API documentation at:
https://www.kraken.com/help/api

To use, you must generate a kraken api key on their website.
Then, create the file kraken.key in the root directory (this is in the .gitignore so it will not be pushed to github)
the file should have two lines

line1: key

line2: secret