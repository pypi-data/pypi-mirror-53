# Falcontool: a simple utility to create and work with Falcon-based projects

Falcontool is an attempt to provide tooling for quickly and easily starting a Falcon-based project.
 
It is inspired by Django's `django-admin` and Flask's ` flask`.

# Falcontool does the following:
- Creates a project repository given a `project_name`
- Sets up the basic project scaffolding, including:
  - Creates a `tests` subdirectory
  - Creates a `src` subdirectory
  - Creates an empty `src/api.py`
  - Creates an empty `requirements.txt` file in the root directory
  - Creates an empty `README.md` file in the root directory
  - Creates an empty `CODEOWNERS` file in the root directory
- Allow for the creation of additional resources if specified by flags:
  - `--dockerfile` creates an empty `Dockerfile` in the root directory
  - `--modelsfile` creates an empty `models.py` in `src/api` directory
  - `--dbfile` creates an empty `db.py` in `src/api` directory
  - `--resourcesfile` creates an empty `resources.py` in `src/api` directory
  - '--tox' creates an empty `tox.ini` in the root directory
  
# Installation
```sh
$> pip install falcontool
```

# Usage
```sh
$> falcon create foo
created directory foo
created directory tests
created directory src
created file requirements.txt
created file README.md
created file src/api.py
created file CODEOWNERS

$> cd foo
$> ll -a ./*
-rw-r--r-- 1 tjb tjb   40 Sep 29 20:23 ./CODEOWNERS
-rw-r--r-- 1 tjb tjb   40 Sep 29 20:23 ./README.md
-rw-r--r-- 1 tjb tjb   40 Sep 29 20:23 ./requirements.txt

./src:
total 12
drwxr-xr-x 2 tjb tjb 4096 Sep 29 20:23 ./
drwxr-xr-x 4 tjb tjb 4096 Sep 29 20:23 ../
-rw-r--r-- 1 tjb tjb   40 Sep 29 20:23 api.py

./tests:
total 8
drwxr-xr-x 2 tjb tjb 4096 Sep 29 20:23 ./
drwxr-xr-x 4 tjb tjb 4096 Sep 29 20:23 ../
```


