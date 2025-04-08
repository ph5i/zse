# zipslipeasy (zse)
[![License](https://img.shields.io/badge/license-MIT-_red.svg)](https://opensource.org/licenses/MIT)

zse automates the creation of zipslip exploits for testing purposes, saving you from the hassle of manually crafting them.

### requirements
---
- python 3
- 7z (must be in your system's `PATH`)

### installation
---
```sh
git clone https://github.com/ph5i/zse.git
cd zse
python3 zse.py -h
```

### example usage
---
to traverse up 5 directories and place the payload in the `/var/www/foo/bar` directory, run:

```sh
python3 zse.py -d 5 -t var/www/foo/bar payload.php 
```

this will result in a zip archive that, when extracted, places the `payload.php` file in the `/var/www/foo/bar` directory.

### license
---
this tool is licensed under the [MIT](https://opensource.org/license/MIT) license.
