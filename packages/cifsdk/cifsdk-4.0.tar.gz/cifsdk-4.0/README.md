# Getting Started
## CommandLine
```bash
$ pip install 'cifsdk>=4.0,<5.0'
$ export CIF_REMOTE=http://localhost:5000
$ export CIF_TOKEN=1234..

$ cif -d -p
$ cif --itype url --tags phishing
..
```

## Python SDK
```python

from pprint import pprint
from cifsdk import search, submit, ping

if not ping():
    print("Server Unavailable...")

for i in search({'indicator': 'example.com'}):
    pprint(i)


rv = submit({'indicator': 'example.com', 'tags': 'phishing', 'group': 'everyone'})


```


see the [CIFv4](https://github.com/csirtgadgets/verbose-robot-sdk-py/wiki) wiki for more.

# Need More Advanced Help?

https://csirtg.io/support

 * Augment your developer cycles, spend less time on customization.
 * Influence over future features at a fraction of the cost of custom building.
 * Lessons learned from 10+ years of industry wide experience.
 * Solve problems faster.

# Getting Help
 * [the Wiki](https://github.com/csirtgadgets/verbose-robot/wiki)
 * [Known Issues](https://github.com/csirtgadgets/verbose-robot/issues?labels=bug&state=open)
 * [FAQ](https://github.com/csirtgadgets/verbose-robot/wiki/FAQ)

# Getting Involved
There are many ways to get involved with the project. If you have a new and exciting feature, or even a simple bugfix, simply [fork the repo](https://help.github.com/articles/fork-a-repo), create some simple test cases, [generate a pull-request](https://help.github.com/articles/using-pull-requests) and give yourself credit!

If you've never worked on a GitHub project, [this is a good piece](https://guides.github.com/activities/contributing-to-open-source) for getting started.

* [How To Contribute](contributing.md)  
* [Project Page](http://csirtgadgets.com/collective-intelligence-framework/)

# COPYRIGHT AND LICENSE

Copyright (C) 2018 [the CSIRT Gadgets](http://csirtgadgets.com)

Free use of this software is granted under the terms of the [Mozilla Public License (MPLv2)](https://www.mozilla.org/en-US/MPL/2.0/).
