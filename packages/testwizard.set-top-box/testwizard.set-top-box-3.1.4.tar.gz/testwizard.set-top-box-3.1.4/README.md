# Testwizard - set-top-box

> Python language support for testing set-top box devices using testwizard

## Usage

* import the [testwizard.core](https://pypi.org/project/testwizard.core/) and the testwizard.set_top_box packages
* get a sesion and use it to create an set-top box testobject.
* Use this object to execute commands
* You can use the session to add results that will be reported to the robot when the script finishes or set results that will be posted immediately.

## Sample script

### Python (set-top-box.py)

```python
import sys
import time

from testwizard.core import TestWizard
from testwizard.core import ResultCodes
from testwizard.set_top_box import SetTopBox

with TestWizard() as TW:
    session = TW.session

    setTopBox = SetTopBox(session, "SetTopBox")

    print("sendRCKey")
    result = setTopBox.sendRCKey("menu")
    print(result.message)
    if (not result.success):
        session.addFail(result.message)

    if (not (session.hasFails() or session.hasErrors())):
        session.setResult(ResultCodes.PASS, "Test was successful")
```

### sidecar file (set-top-box.json)

```json
{
    "tester": "Some tester",
    "parameters": [
        { "name": "param1", "value": "value1"},
        { "name": "param2", "value": "value2"}
    ],
    "resources": [{ "category": "STB", "name": "SetTopBox", "id": "SetTopBox 1"}
    ],
    "outputFolder": "c:\\temp"
}
```

## License

[Testwizard licensing](https://www.eurofins-digitaltesting.com/testwizard/)