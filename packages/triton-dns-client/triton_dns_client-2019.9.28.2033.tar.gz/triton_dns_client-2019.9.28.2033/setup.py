from setuptools import setup, find_packages

setup(
    name='triton_dns_client',  # How you named your package folder (MyLib)
    packages=find_packages(exclude=['*.tests', '*.tests.*', 'tests.*', 'tests']),  # Chose the same as "name"
    version='2019.09.28.2033',  # Start with a small number and increase it with every change you make
    license='MIT',  # Chose a license from here: https://help.github.com/articles/licensing-a-repository
    long_description='''# Triton DNS client
Triton is a simple DNS client made for better understanding of DNS protocol

# Installation
## From PYPI

`pip3 install triton-dns-client`

## From this repo

```
git clone https://git.best-service.online/yurzs/triton`  
cd triton 
python3 setup.py install
```

## How to use

Here is an example query for A record of this gitlab instance
```
import asyncio
import triton
reply_message = asyncio.run(triton.query('8.8.8.8', 'git.best-service.online', 1))
print(reply_message.__dict__)
>>> {'header':
 {'id': 10023,
  'qr': 1,
  'opcode': 0,
  'aa': 0,
  'tc': 0,
  'rd': 1,
  'ra': 1,
  'z': 0,
  'rcode':0,
  'qdcount': 1,
  'ancount': 1,
  'nscount': 0,
  'arcount': 0},
'question':
 [
   {'qname':"git.best-service.online",
    'qtype': 1, 'qclass': 1}
 ],
'answer': 
 [
   {'name': 'git.best-service.online',
    'type': 1,
    'class': 1,
    'ttl': 999,
    'rdata': {
      'address': 1356055586} # This is int repr of IP address
    }
 ],
'authority': [],
'additional': []}
``` 

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


''',
    long_description_content_type='text/markdown',
    description='Async DNS client',  # Give a short description about your library
    author='Yury (Yurzs)',  # Type in your name
    author_email='dev@best-service.online',  # Type in your E-Mail
    url='https://git.best-service.online/yurzs/triton',  # Provide either the link to your github or to your website
    keywords=['triton', 'DNS', 'client'],  # Keywords that define your package best
    install_requires=['bitstring', 'pycryptodomex'],
    classifiers=[
        'Development Status :: 3 - Alpha',
        # Chose either "3 - Alpha", "4 - Beta" or "5 - Production/Stable" as the current state of your package
        'Intended Audience :: Developers',  # Define that your audience are developers
        'Topic :: Software Development :: Build Tools',
        'License :: OSI Approved :: MIT License',  # Again, pick a license
        'Programming Language :: Python :: 3',  # Specify which pyhton versions that you want to support
        'Programming Language :: Python :: 3.7',
    ],
)