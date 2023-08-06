# keeper-cnab240

CNAB-240 file pattern for brazilian banking financial integration.

    pip install keeper-cnab240
    
### Available Banks
| Bank | Shipment | Return | Segments |
| ---- | -------- | ------ | -------- |
| Itau / Sispag | Beta | Beta | A, J/J-52 |

### Requirements
- Python 3.6+

### Dependency Installation
```bash
pip install -r requirements.txt
```

### Publish new library version
```bash
python3 -m pip install --user --upgrade setuptools wheel
python3 -m pip install --user --upgrade twine

python3 setup.py sdist bdist_wheel
python3 -m twine upload dist/*
```
