# bwb

bot with bot.

## Usage

Install with `pip install --upgrade bwb`.

```text
# Import one of:
from bwb.tanner import bwb
from bwb.jason import bwb
from bwb.tdev import bwb
from bwb.molly import bwb
```

### Handshaking

Boot up:

```text
client.send_message(CHAT_ID, '000000init ' + bwb.init())
```

On `000000init [data]`:

```text
event.respond('000000handshake ' + bwb.handshake(data))
```

On `000000handshake [data]`:

```text
event.respond(bwb.wrap('secret ' + bwb.secret(data), handshake=True))
```

On _Handshake OTP authed_ `123456secret [data]`:

```text
bwb.set_secret(data)
event.respond(bwb.wrap('🤝'))
```

On _OTP authed_ `123456🤝`:

```text
event.respond('🤝')
```

### Interaction

Run every incoming message through `bwb.parse()` since it's inexpensive. This will decrypt and remove base58 encoding.

Once decoded, send it through `bwb.check_auth()` which will return `True` or `False` if the code is valid.

Example:

```text
text = bwb.parse(text)
if text.startswith('!'):
    ...
elif text.startswith('000000'):
    text = text[6:]
elif bwb.check_auth(text, handshake=True):
    handshake_authed = True
    text = text[6:]
elif bwb.check_auth(text):
    authed = True
    text = text[6:]
else:
    return
```

Use `bwb.wrap()` to auth and encode outgoing commands.

Params:

```text
wrap(text, handshake=False, target=None, b58=False, enc=False)
```

Examples:
```text
out = bwb.wrap('ping')  # broadcast all bots
out = bwb.wrap('ping', target=TANNER)  # auth for Tannerbot
out = bwb.wrap('ping', target=JASON, enc=True)  # base58 encrypt
out = bwb.wrap('ping', target=MOLLY, b58=True)  # base58
```

## Development

### Setup

Clone the repo.

To test your changes:

```text
pip install --upgrade ~/path/to/bwb
```

### Deployment

Install setuptools:

```text
python3 -m pip install --user --upgrade setuptools wheel
```

* Increment version number in `setup.py`

Build and upload:

```text
bash build-upload.sh
```
