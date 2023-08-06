# Testwizard - Web

> Python language support for testing websites, web-apps or webservices using testwizard

## Usage

* import the [testwizard.core](https://pypi.org/project/testwizard.core/) and the testwizard.web packages
* get a sesion and use it to create a web testobject.
* Use this object to execute commands
You can use the session to add results that will be reported to the robot when the script finishes or set results that will be posted immediately.

## Sample script

### Python (website.js)

```Python
import sys
import time

from testwizard.core import TestWizard
from testwizard.core import ResultCodes
from testwizard.web import Web

with TestWizard() as TW:
    session = TW.session

    website = Web(session, "TestwizardWebsite")

    print("startWebDriver")
    result = website.startWebDriver()
    print(result.message)
    if (not result.success):
        session.addFail(result.message)

    # Add your commands here

    print("quitDriver")
    result = website.quitDriver()
    print(result.message)
    if (not result.success):
        session.addFail(result.message)

    if (not (session.hasFails() or session.hasErrors())):
        session.setResult(ResultCodes.PASS, "Test was successful")
```

### sidecar file (website.json)

```json
{
    "tester": "Some tester",
    "parameters": [
        { "name": "param1", "value": "value1"},
        { "name": "param2", "value": "value2"}
    ],
    "resources": [{ "category": "WEB", "name": "TestwizardWebsite", "id": "Testwizard web site"}
    ],
    "outputFolder": "c:\\temp"
}
```

## License

[Testwizard licensing](https://www.eurofins-digitaltesting.com/testwizard/)
