# Few handy python modules

Hey, I wanna share with You my python modules,

I have for now:
* logger
* tictoc
* hashing passwords
* files_info
* downloading files
* password validation

I hope You enjoy it!

PS. You can find source codes on [my github](https://github.com/admw15/modules)

## Docs:
* logger:  
##### Info

Package contains "CreateLogger" class that quickly create logger for us, 
instead of importing logging module and adding handlers etc...

log file has default name same as file name, with .log.
Also it is in new folder called 'logs'  
Example: python_file.py -> logs/python_file.log

##### Arguments:
* logger_name  
Type: str  
Default: your file name  
Description: logger name should be unique!  
Default is your filename (without .py) so it will look like: 
mailer/flask_receiver/my_first_file etc.

WARNING: If you have file (parent) 
with logger, and you are importing in it another local file (child), 
then remember to give a new logger name to child!  

```python
# parent.py:
import handymodules
import child  # local file

log = handymodules.CreateLogger()  # its ok, don't need any arguments
log.info('Starting...')
child.function()
log.info('Done')
```

```python
# child.py:
import handymodules
log = handymodules.CreateLogger()  # BAD!!!
log = handymodules.CreateLogger('child')  # Good

def function():
    # do something
    log.warning('Something is wrong')
```

In this case, there are two loggers and two files, if you want to have 
these two loggers in one file, then you should edit line in child  
```python
log = handymodules.CreateLogger('child', log_filename='parent')
```  
Remember to use file basename (without .py) 

* stream_handler  
Type: bool  
Default: True  
Description: add a stream handler to your logger (logs in console)

* file_handler  
Type: bool  
Default: True  
Description: add a file handler to your logger. It creates "logs" 
folder inside directory where your file is.  

* log_filename  
Type: str  
Default: filename  
Description: Just what it says, default logfile has same name as your 
python file, but with .log  
Eg. flask_app.py -> logs/flask_app.log 

##### Kwargs
* timed_rotating_file  
Type: bool  
Default: False  
Description: if file handler should be timed rotating. If True, it
will change every midnight  

* days_to_keep  
Type: int  
Default: 7  
Description: only if timed rotated file, select how long should logger
keep old daily files

* log_inside_folder  
Type: bool  
Default: False  
Description: if True, logs are saving inside logs and inside one 
more folder, eg.   
False - logs/flask_app.log  
True - logs/flask_app/flask_app.log  

Useful when using timed rotating for like month or three months

##### Usage:

```python
import handymodules
log = handymodules.CreateLogger(stream_handler=True, file_handler=False)

log.info('some info')
log.debug('some info')
log.warning('some info')
log.error('some info')
log.critical('some info')

try:
    x += 2
except:
    log.add_file_handler()
    log.exception('Only when exception!')

log.change_level('warning')
log.change_format('%(message)s')
```

Sample log file line:

`2019-03-27 20:52:27,471 - flask_app - INFO - some info`

* tictoc:

```python
import tictoc as t

t.tic()
t.toc()
# more code
t.toc()

t.tic()
t.toc()
```
You can use toc multiple times, it will count since last `tic()` function

toc() output:
`Elapsed time: 2.562 seconds.`

Also there is a class with this functionality,  
You can have now multiple timers.
```python
import handymodules
t = handymodules.TicToc()
t.tic()
t.toc()
```

* hashing passwords

Two functions:
```python
import handymodules as h
hashed = h.hash_password('Pa$$w0rd')
# store it somewhere!
h.validate_hashed_password('Pa$$w0rd', hashed)
```
It's simple and secure, returns `True` or `False`
I am using SHA3-512.

* files_info
```python
import handymodules
filename = handymodules.get_filename()
filepath = handymodules.get_file_abspath(file)
```

it will always return filename that uses it, 
and absolute file path to the specific file

* password validation

```python
import handymodules.password_validation as p
password = p.validate_password()
```
in `password` variable You have user password from keyboard.   
It was taken by getpass so it wasn't visible for others (just like in linux)  

I recommend to use it with hashing_password, 
do not store passwords in plain text!

* download_file

```python
import handymodules.downloading_file as d

url1 = 'http://example.com/text.txt'
url2 = 'http://example.com/zipfile.zip'

d.download(url1)
d.download_zip(url2)
```

You can simply download any file from web giving url only.  
Zip default will be unpacked to folder (with same name as package) and deleted, 
of course You can change it



### changelog:
* 2.1.0 - Added support to Python versions lower than 3.6 (removed f-strings)
* 2.0.1 - updated docs
* 2.0.0 - Changed name to handymodules, added kwargs to CreateLogger, 
you can now change logfile name, updated docs

