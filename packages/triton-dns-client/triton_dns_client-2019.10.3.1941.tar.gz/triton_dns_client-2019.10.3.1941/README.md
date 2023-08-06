# Triton DNS client
Triton is a simple DNS client made for better understanding of DNS protocol

# Installation
## From PYPI 

`pip3 install triton-dns-client`

## From this repo

```bash
git clone https://git.best-service.online/yurzs/triton.git  
cd triton 
python3 setup.py install
```

## How to use

Here is an example query for A record of this gitlab instance
```python3
>>> import triton
>>> a = triton.sync_query('8.8.8.8', 'google.com')
>>> print(a.to_json())
{
    "header": {
        "id": 37920,
        "qr": 1,
        "opcode": 0,
        "aa": 0,
        "tc": 0,
        "rd": 1,
        "ra": 1,
        "z": 0,
        "rcode": 0,
        "qdcount": 1,
        "ancount": 6,
        "nscount": 0,
        "arcount": 0
    },
    "question": [
        {
            "name": "google.com",
            "type": 1,
            "class": 1
        }
    ],
    "answer": [
        {
            "name": "google.com",
            "type": "A",
            "class": 1,
            "ttl": 257,
            "rdata": {
                "address": "64.233.165.113"
            }
        },
        {
            "name": "google.com",
            "type": "A",
            "class": 1,
            "ttl": 257,
            "rdata": {
                "address": "64.233.165.102"
            }
        },
        {
            "name": "google.com",
            "type": "A",
            "class": 1,
            "ttl": 257,
            "rdata": {
                "address": "64.233.165.101"
            }
        },
        {
            "name": "google.com",
            "type": "A",
            "class": 1,
            "ttl": 257,
            "rdata": {
                "address": "64.233.165.139"
            }
        },
        {
            "name": "google.com",
            "type": "A",
            "class": 1,
            "ttl": 257,
            "rdata": {
                "address": "64.233.165.100"
            }
        },
        {
            "name": "google.com",
            "type": "A",
            "class": 1,
            "ttl": 257,
            "rdata": {
                "address": "64.233.165.138"
            }
        }
    ],
    "authority": [],
    "additional": []
}
``` 
For demonstration purposes sync function is used.  
Call ```triton.query``` for async version

## Tree resolve
Also there is experimental full DNS tree resolve function

```python3
>>> import triton
>>> a = triton.sync_full_chain('git.best-service.online', 1)
>>> print(a.to_json())
{
    "header": {
        "id": 45902,
        "qr": 1,
        "opcode": 0,
        "aa": 1,
        "tc": 0,
        "rd": 1,
        "ra": 0,
        "z": 0,
        "rcode": 0,
        "qdcount": 1,
        "ancount": 1,
        "nscount": 1,
        "arcount": 1
    },
    "question": [
        {
            "name": "git.best-service.online",
            "type": 1,
            "class": 1
        }
    ],
    "answer": [
        {
            "name": "git.best-service.online",
            "type": "A",
            "class": 1,
            "ttl": 1000,
            "rdata": {
                "address": "80.211.196.34"
            }
        }
    ],
    "authority": [
        {
            "name": "best-service.online",
            "type": "NS",
            "class": 1,
            "ttl": 100,
            "rdata": {
                "nsdname": "dns-core.best-service.online"
            }
        }
    ],
    "additional": [
        {
            "name": "dns-core.best-service.online",
            "type": "A",
            "class": 1,
            "ttl": 1000,
            "rdata": {
                "address": "163.172.161.149"
            }
        }
    ]
}
```
For demonstration purposes sync function is used.  
Call ```triton.full_chain``` for async version
## TODO List
- [ ] Enable EDNS
- [ ] Add DNSSEC Resource Record types

## List of available resource record types
- [x] A
- [x] AAAA
- [X] NS
- [x] TXT
- [x] SOA
- [x] OPT
- [x] RRSIG
- [x] DNSKEY
- [x] DS
- [x] NSEC
- [x] NSEC3
- [x] NSEC3PARAM

## Currently supported DNSSEC algorithms
- [x] RSASHA1
- [x] RSASHA256
- [x] RSASHA512
- [ ] ECCGOST
- [ ] RSA_NSEC3_SHA1
- [ ] DSA
- [ ] DSA_NSEC3_SHA1
- [ ] ECDSAP256SHA256
- [ ] ECDSAP256SHA384
- [ ] ED448
- [ ] ED25519