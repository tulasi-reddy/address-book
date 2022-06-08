# address-book
Pre requisites: Python (used Python 3.7.8 version), SQLite (used SQLite 3.36.0 version)


<!-- Install required dependencies -->
1. cd to the directory where requirements.txt is located
2. activate your virtualenv
    a. pip install virtualenv
    b. virtualenv <<virtual-env-name>>
    c. source my-env/Scripts/activate or my-env/Scripts/activate (here i gave 'myenv' for <<virtual-env-name>>)
3. run: pip install -r requirements.txt in your shell

<!-- Start server -->
uvicorn address_book.main:app

<!-- Run in browser -->
Please use the below url in the browser:
http://127.0.0.1:8000/docs

