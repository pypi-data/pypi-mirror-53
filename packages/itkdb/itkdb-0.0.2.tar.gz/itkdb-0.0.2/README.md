# ITk DB

To install as a user

```
pip install itkdb
```

or if you wish to develop/contribute

```
git clone ...
cd production_database_scripts/
pip install -e .[develop]
```

or

```
git clone ...
cd production_database_scripts/
pip install -e .[complete]
```

## Using

Command line available via

```
itkdb --help
```

## Develop

### Bump Version

Run `bumpversion x.y.z` to bump to the next version. We will always tag any version we bump, and this creates the relevant commits/tags for you. All you need to do is `git push --tags` and that should be it.
