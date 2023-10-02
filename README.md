# dpea-odrive

## DISCLAIMER
This library is meant to replace [RPI_ODrive](https://github.com/dpengineering/RPi_ODrive)
and be used for the 2022-2023 school year.

## About
dpea-odrive is a helper library for DPEA projects that use the ODrive motor controller. You can think
of this library as a wrapper to existing odrive functions to streamline the programming processs. For
more detailed information, consider visiting the below links and digging around.
 - [ODrive Getting Started Page](https://docs.odriverobotics.com/v/latest/getting-started.html)
 - [Official ODrive Github Repo](https://github.com/odriverobotics/ODrive)

## Usage
To get your ODrive up and running, please navigate to the following site --
* [DPEA ODrive Getting Started](https://dpengineering.github.io/dpea-odrive/)

## Build Instructions
To build the PyPI project, run the following:

Install python build package
```python3 -m pip install --upgrade build```

Install twine
```python3 -m pip install --upgrade twine```

Build package (make sure to change the version in pyproject.toml to provent version collision!):
```python3 -m build```

Push the project to PyPi:
```python3 -m twine upload dist/*```

Twine will prompt you for a password. Use
```
Username: __token__
Password: YOUR_API_TOKEN
```
