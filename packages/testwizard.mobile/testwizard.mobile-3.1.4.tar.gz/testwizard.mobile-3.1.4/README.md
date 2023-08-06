# Testwizard - Mobile

> Python language support for testing Mobile devices using testwizard

## Usage

* import the [testwizard.core](https://pypi.org/project/testwizard.core/) and the testwizard.mobile packages
* get a sesion and use it to create a mobile testobject.
* Use this object to execute commands
You can use the session to add results that will be reported to the robot when the script finishes or set results that will be posted immediately.

## Sample

### Python (mobile.py)

```Python
import sys
import time

from testwizard.core import TestWizard
from testwizard.core import ResultCodes
from testwizard.mobile import Mobile

with TestWizard() as TW:
    session = TW.session

    print(session.args['param1'])
    print(session.args['param2'])

    mobile = Mobile(session, "Mobile")

    print("InitDriver")
    result = mobile.initDriver()
    print(result.message)
    if (not result.success):
        session.addFail(result.message)

    # Add your commands here

    print("QuitDriver")
    result = mobile.quitDriver()
    print(result.message)
    if (not result.success):
        session.addFail(result.message)

    if (not (session.hasFails() or session.hasErrors())):
        session.setResult(ResultCodes.PASS, "Test was successful")
```

### sidecar file (mobile.json)

```json
{
    "tester": "Some tester",
    "parameters": [
        { "name": "param1", "value": "value1"},
        { "name": "param2", "value": "value2"}
    ],
    "resources": [{ "category": "MOBILE", "name": "Mobile", "id": "Mobile 1"}
    ],
    "outputFolder": "c:\\temp"
}
```

## License

[Testwizard licensing](https://www.eurofins-digitaltesting.com/testwizard/)