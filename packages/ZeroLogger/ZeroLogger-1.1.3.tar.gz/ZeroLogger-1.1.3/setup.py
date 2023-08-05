from setuptools import setup, Extension

setup(
    name="ZeroLogger",
    version="1.1.3",
    description="My Own Logger Package to throw done/warn/error/critical(error + exit) messages",    
    long_description="""# ZeroLogger

ZeroLogger is a simple logger i made for my projects its simple and helps me alot keeping the output clean and smooth.

u can use:
  - done_task("Lorem") 
        - to show something worked fine 

  - warn("Ipsum") 
        - to show a warning 

  - error("Dorem") 
        - to show a non critical error 

  - critical("FCK") 
        - Shows a Critical error and quit the "programm" 

# How to use:

  - import using:
  ```python
            from ZeroLogger.ZeroLogger import *
  ```
  
  - now u can just use:
  ```python
  done_task("Finished")
  warn("oh oh something is wrong")
  error("Okay i cant handle this, but i can go on...")
  critical("Icant handle it EXIT! NOW!")
  ```
""",

    long_description_content_type='text/markdown',
    url="https://github.com/oOHiyoriOo/ZeroLogger",
    author="ZéroTwó#5019",
    author_email="wolf.sf75@googlemail.com",
    license="MIT",
    install_requires=["colorama"],
    packages=['ZeroLogger'],
    package_dir={'ZeroLogger':'ZeroLogger/'}
)
