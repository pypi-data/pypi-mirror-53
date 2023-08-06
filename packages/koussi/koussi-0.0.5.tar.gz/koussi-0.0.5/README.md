This package helps import secrets to project from different sources.
Supported:
- Environment variables
- YAML file in Keybase folder

YAML example:

```yaml
facebook:
  app:
    id: '446546543413'
    secret: top_secret
  user:
    id: '1398jlkj9s'
    token: kkkkkkkkkkkkkk
  page:
    id: '345634563'
    post: '54634563456yerty'
```

```python
params = {'keybase': {'user': 'pavelch', 'project': 'facebook'},
                  'envs': {'CYCOBOT_MESSAGE_API_KEY': 'ghghjg', 'FOO': 'bar', 'DD_API_KEY': 'key'}}
my_secrets = Secrets(**params)()
pprint.pprint(my_secrets)
```
```text
{'CYCOBOT_MESSAGE_API_KEY': 'kkkkkkkkkk',
 'DD_API_KEY': 'djdjdjdjdjdjdjdjdjdjd',
 'FOO': 'bar',
 'app': ordereddict([('id', '446546543413'), ('secret', 'top_secret')]),
 'page': ordereddict([('id', '345634563'), ('post', '54634563456yerty')]),
 'user': ordereddict([('id', '1398jlkj9s'), ('token', 'kkkkkkkkkkkkkk')])}
```