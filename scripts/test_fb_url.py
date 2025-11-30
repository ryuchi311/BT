import requests

url = 'https://scontent-lhr8-2.xx.fbcdn.net/v/t39.30808-6/469572050_472871262500521_1691824578606866080_n.jpg?_nc_cat=101&ccb=1-7&_nc_sid=a5f93a&_nc_ohc=hmO6WqejAZMQ7kNvwGUKTvG&_nc_oc=AdlqT2dcYqhrwj8IrY045JXFM_yfpZg2fdp5C7lu6yzIjL4j_7hIeSdvj6XtjxuUKYsR8jsCQ1K8MfRmfShT2VAP&_nc_zt=23&_nc_ht=scontent-lhr8-2.xx&_nc_gid=a1PhYCuFUTehG9VO-Bf9rA&oh=00_AfjqzVqSaPWrEUfGVfoEWzlN9-1mL0w2qhOGiAsY27PZmg&oe=6931FF51'

print("Testing HEAD request...")
try:
    resp = requests.head(url, timeout=10, allow_redirects=True)
    print(f'HEAD Status: {resp.status_code}')
    print(f'Content-Type: {resp.headers.get("content-type")}')
    print(f'All headers: {dict(resp.headers)}')
except Exception as e:
    print(f'HEAD failed: {e}')

print("\nTesting GET request...")
try:
    resp = requests.get(url, timeout=10, allow_redirects=True, stream=True)
    print(f'GET Status: {resp.status_code}')
    print(f'Content-Type: {resp.headers.get("content-type")}')
except Exception as e:
    print(f'GET failed: {e}')
