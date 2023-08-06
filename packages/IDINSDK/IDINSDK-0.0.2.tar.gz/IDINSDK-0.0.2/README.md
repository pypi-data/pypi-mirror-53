# Example Signer Usage

```python
from IDINSDK import IDINSigner, IDINVerifier

signer = IDINSigner("""-----BEGIN EC PRIVATE KEY-----
MHcCAQEEIO+qNUJs2qNN2seIUsXuIYJtg1cw4kY7F2SGl+ovvItQoAoGCCqGSM49
AwEHoUQDQgAE4PU/X1iUmtSlV0tBIA7rwz3wYkhXEGhraj69x0oG0l7GCgH+orX6
NYoaA5oG9Dme+qMl0xsXYOgyrRdatEQQzw==
-----END EC PRIVATE KEY-----""", key_format='pem')

signer = IDINSigner()
print('Private Key - PEM')
print(signer.to_pem())
print()

print('Private Key - HEX')
print(signer.to_hex())
print()

print('Sign data - hello')
signature = signer.sign(b'hello')
print(signature)
print()

verifier = signer.get_verifier()
print('Public Key - PEM')
print(verifier.to_pem())
print()

print('Public Key - HEX')
print(verifier.to_hex())
print()

print('Verify data - hello')
print(verifier.verify(signature, 'hello'))
print()

print('Verify data - hello2')
print(verifier.verify(signature, 'hello2'))
print()

verifier = IDINVerifier(verifier.to_hex(), key_format='hex')
print('Public Key - PEM')
print(verifier.to_pem())
print()

print('Public Key - HEX')
print(verifier.to_hex())
print()

print('Verify data - hello')
print(verifier.verify(signature, 'hello'))
print()

print('Verify data - hello2')
print(verifier.verify(signature, 'hello2'))
print()
```

# Example API usage

```python
from IDINSDK import IDINAPI, IDINSigner
import pprint, time

# API
api = IDINAPI(debug=True)

print('### Generate keypair')
signer = IDINSigner()
print('[+] Private Key - HEX')
print(signer.to_hex())
verifier = signer.get_verifier()
print('[+] Public Key - HEX')
print(verifier.to_hex())
print()


print('### Create DID')
did_address = api.did_create(signer)
print('[+] api.did_create() => DID address')
print(did_address)
print()


print('### Generate new keypair')
signer2 = IDINSigner()
print('[+] Private Key - HEX')
print(signer2.to_hex())
verifier2 = signer2.get_verifier()
print('[+] Public Key 2 - HEX')
print(verifier2.to_hex())
print()


print('### Add new keypair to DID')
public_key_to_add = verifier2.to_hex()
print('[+] api.did_add_public_key_sign() => tx body hex')
signature_of_public_key_to_add = api.did_add_public_key_sign(did_address, signer2)
tx_hash = api.did_add_public_key(did_address, signer, public_key_to_add, signature_of_public_key_to_add, async_tx=False)
print('[+] api.did_add_public_key() => transaction hash')
print(tx_hash)

print('[+] Waiting for block to be commited')
time.sleep(5)

print('### List active public key of DID')
print('[+] api.did_list_public_keys() => json')
pprint.pprint(api.did_list_public_keys(did_address))


print('### Get public key detail of DID')
print('[+] api.did_get_public_key_detail() => json')
pprint.pprint(api.did_get_public_key_detail(did_address, public_key_to_add))


print('### Remove public key from DID')
print('[+] api.did_remove_public_key() => transaction hash')
pprint.pprint(api.did_remove_public_key(did_address, signer, public_key_to_add))


print('### Register DID recovery')
print('[#] Generate keypair for recovery DID test')
signer2 = IDINSigner()
print('[+] Private Key - HEX')
print(signer2.to_hex())
verifier2 = signer2.get_verifier()
print('[+] Public Key - HEX')
print(verifier2.to_hex())

print('[#] Create DID for recovery DID test')
did_address2 = api.did_create(signer2)
print('[+] api.did_create() => DID address')
print(did_address2)

print('[#] Sign and do recovery registration')
print('[+] api.did_recovery_register_sign() => tx body json')
array_of_payload = []
array_of_payload.append(api.did_recovery_register_sign(did_address2, signer2, did_address))
pprint.pprint(array_of_payload)
print('[+] api.did_recovery_register() => transaction hash')
tx_hash = api.did_recovery_register(did_address, signer, array_of_payload, async_tx=False)
print(tx_hash)


print('### DID recovery')
print('[#] Generate new keypair for recovery DID')
signer3 = IDINSigner()
print('[+] Private Key - HEX')
print(signer3.to_hex())
verifier3 = signer3.get_verifier()
print('[+] Public Key - HEX')
print(verifier3.to_hex())

print('[#] Sign and do recovery')
print('[+] api.did_recovery_sign() => tx body json')
array_of_payload = []
array_of_payload.append(api.did_recovery_sign(verifier3.to_hex(), signer2, did_address2, did_address))
pprint.pprint(array_of_payload)
print('[+] api.did_recovery() => transaction hash')
tx_hash = api.did_recovery(did_address, signer3, array_of_payload)
print(tx_hash)


print('### VC Register')
print('[+] api.vc_register() => transaction hash')
tx_hash = api.vc_register(did_address, signer, '9ac2281f433f7354af0d873a696e1b1c11756f5c05d251e44117525dbb09aa65')
print(tx_hash)


print('### VC Revoke')
print('[+] api.vc_revoke() => transaction hash')
tx_hash = api.vc_revoke(did_address, signer, '9ac2281f433f7354af0d873a696e1b1c11756f5c05d251e44117525dbb09aa65')
print(tx_hash)

# Warning - this is a mock data
print('### VC Verify')
print('[+] api.vc_verify() => True/False')
vc = """{
  "data": "eyJAY29udGV4dCI6IFsiaHR0cHM6Ly93d3cudzMub3JnLzIwMTgvY3JlZGVudGlhbHMvdjEiXSwgImNyZWRlbnRpYWxTdWJqZWN0IjogeyJjYW1wdXNfbmFtZSI6ICJcdTBlMDJcdTBlMmRcdTBlMTlcdTBlNDFcdTBlMDFcdTBlNDhcdTBlMTkiLCAiZmFjdWx0eV9uYW1lIjogIlx1MGUwNFx1MGUxM1x1MGUzMFx1MGUyYVx1MGUxNlx1MGUzMlx1MGUxYlx1MGUzMVx1MGUxNVx1MGUyMlx1MGUwMVx1MGUyM1x1MGUyM1x1MGUyMVx1MGUyOFx1MGUzMlx1MGUyYVx1MGUxNVx1MGUyM1x1MGU0YyIsICJmaXJzdF9uYW1lX2VuIjogIkRlbW8iLCAiZmlyc3RfbmFtZV90aCI6ICJcdTBlMTdcdTBlMTRcdTBlMmFcdTBlMmRcdTBlMWEiLCAiaWQiOiAiZGlkOmlkaW46aW9VZ3NFVVUyQzJvNkoyMnhpemppeFRXZEZNQXhjZnZzMyIsICJsYXN0X25hbWVfZW4iOiAiU3lzdGVtIiwgImxhc3RfbmFtZV90aCI6ICJcdTBlMjNcdTBlMzBcdTBlMWFcdTBlMWEiLCAibWFqb3JfbmFtZSI6ICJcdTBlMmFcdTBlMTZcdTBlMzJcdTBlMWJcdTBlMzFcdTBlMTVcdTBlMjJcdTBlMDFcdTBlMjNcdTBlMjNcdTBlMjFcdTBlMjhcdTBlMzJcdTBlMmFcdTBlMTVcdTBlMjNcdTBlMWFcdTBlMzFcdTBlMTNcdTBlMTFcdTBlMzRcdTBlMTUiLCAic3R1ZGVudF9pZCI6ICI5OTk5OTk5OTk5IiwgInRpdGxlX2VuIjogIk1yLiIsICJ0aXRsZV90aCI6ICJcdTBlMTlcdTBlMzJcdTBlMjIifSwgImV4cGlyYXRpb25EYXRlIjogIjIwMjMtMDktMThUMDk6NTE6MDErMDc6MDAiLCAiaWQiOiAiMjA4OTUxODQwM2U3OWYzOTBmMDJlN2VjNTM0ZGRlNDA3MThlNWI0ZmMwYzBiMDM0Mjg5NjE2Mjk5NGM1MzNiNyIsICJpc3N1YW5jZURhdGUiOiAiMjAxOS0wOS0xOVQwOTo1MTowMSswNzowMCIsICJpc3N1ZXIiOiAiZGlkOmlkaW46aWJ2OGVUcUhyR1ZtNkY1aXY0dFhoUjRRZkJKUHg5aWFoWCIsICJ0eXBlIjogWyJLS1UgSUQgQ2FyZCJdfQ==",
  "proof": {
    "created": "2019-09-19T09:51:01+07:00",
    "type": "Secp256r1Signature2018",
    "proofPurpose": "assertionMethod",
    "verificationMethod": "did:idin:ibv8eTqHrGVm6F5iv4tXhR4QfBJPx9iahX",
    "signature": "82c879fbc60f8c0b3e7de7858a551bbbe2b9e8e95ba9491a6140fcca2d070d1989003b6b6d3e80b2e526e529f6858c7a68d08219ec11c9a08ee6506abfe134de"
  }
}"""
result = api.vc_verify(vc)
print(result)

```
