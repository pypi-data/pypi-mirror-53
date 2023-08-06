# Ghee echoes to Google Hangouts Chat easly

# How to install

Simply:

    pip install ghee

# How to use

You should now have a command line application:

    ghee https://chat.googleapis.com/v1/... The message you want to send!

It's extremely dumb. First argument is the Google Chat room webhook URL. Everything that follows is the message (`*bold*` and `_italics_` work).

For the information about the api go to: https://developers.google.com/hangouts/chat/how-tos/webhooks

## Create PyPI package

**Important:** following assumes that you are using virtualenv.

Install build tools:

    $ pip install --upgrade pip setuptools wheel

Build package:

    $ python setup.py sdist bdist_wheel
    # [output edited out]
    $ ls -l dist 
    total 8
    -rw-rw-r-- 1 michal_chalupczak michal_chalupczak 3032 paź  7 16:22 ghee-0.0.1-py3-none-any.whl
    -rw-rw-r-- 1 michal_chalupczak michal_chalupczak 1602 paź  7 16:22 ghee-0.0.1.tar.gz
    
## Upload the package to the PyPI!

**Important:** following assumes that you are using virtualenv.

Install upload tools:

    $ pip install --upgrade twine


First register at the test repo: https://test.pypi.org/account/register/ and upload:

    $ twine upload --repository-url https://test.pypi.org/legacy/ dist/*

And check if that worked:

    $ pip install --index-url https://test.pypi.org/simple/ --no-deps ghee

If that worked repeat with the real https://pypi.org/.