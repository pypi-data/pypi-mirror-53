
## Usage:
```
from proxy_check import check
ok, error = await check(os.getenv('PROXY'))
if not ok:
    print(error)
```
