## Example
```
from pycloudproxy import connect as proxy_connect

proxy_connect('my-project:my-cloudsql-instance')

```

## Deploy to pip
`python3 setup.py sdist bdist_wheel`
`python3 -m twine upload dist/*`
