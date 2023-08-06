# satang-pro-signer

[![Build Status](https://travis-ci.org/thebevrishot/satang-pro-signer.svg?branch=master)](https://travis-ci.org/thebevrishot/satang-pro-signer)
[![PyPI version](https://badge.fury.io/py/satang-pro-signer-x.svg)](https://badge.fury.io/py/satang-pro-signer-x)

An implementation of Satang Pro request signing scheme.

https://docs.satang.pro/authentication

## installation

```
pip install satang-pro-signer-x
```

## usage

```python
import json
import satang_pro_signer # import signer

# prepare secret
secret = bytes.fromhex('8781e58f94f8b2a58b6aa30649fd6a46')

# create signer
signer = satang_pro_signer.Signer(secret)

# prepare payload to be sign
payload = json.loads('{"type":"limit","pair":"btc_thb", "side":"sell", "price":"100000", "amount":"100", "none":"1570763737"}')

# sign
signature = signer.sign(payload) # bytes
```