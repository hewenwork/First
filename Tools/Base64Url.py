from urllib import parse
from base64 import b64decode


def decode_url(url: str):
    return parse.unquote(url)


def decode_base_64(url: str):
    return b64decode(url)


if __name__ == "__main__":
    a = "eyJzb2Z0d2FyZWhlYWx0aCI6eyJwbHVnaW4iOjAsInNvZnR3YXJlIjozfX0="
    aa = decode_base_64(a)
    print(aa)