# THEDEX Messaging

This package generates Messages for the THEDEX API.<br>
API Secifications can be found [at the official Sovdwaer Page](https://sovdwaer.de/files/content/dokumente/THEDEX_Entwicklerinformation.pdf).

## Installation

```bash
$ pip install ThedexMessaging
```

## Usage

*Currently, only the Message for creating new Users is implemented.*

### Message for New Client Registration
```python
from Thedex_Messaging import *

tClient = ClientData()
tClient.CLastName = "Smith"
tClient.CFirstName = "John"
tClient.CBirthday = "user['birthday']"
tClient.CSex = tClient.CONST_SEX_M
tClient.CStreet = "Main Road 12"
tClient.CZip = "12386"
tClient.CTown = "Berlin"
tClient.CTelephone = "(089) / 636-48018"
tClient.eMail = "john@smith.com"

tSender = Sender("SENDER_IDENTIFICATION", "SENDER_VERIFICATION")

ThedexMessageBuilder.newClientMessage(
    tSender,
    tClient,
    "filename.TDX"
)
```