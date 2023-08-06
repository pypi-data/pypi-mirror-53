# chat-app

Allows people to chat through terminal

## Installation

### Install Using Git:

```bash
git clone https://github.com/lol-cubes/chat-app.git
pip install cryptography
python3 chat-app/chat-app  # setup
```
### Install Using Pip:

```bash
pip install chat-app
python3 -m chat-app  # setup
```

## Usage

### Create a Server

```bash
chat-app server
```

Port is any 4-digit number that isn't already in use
(you'll know when it's in use)

### Join a Server

```bash
chat-app client
```

The server is the IP address of the server machine.
Find your IP address (on unix) using the command:
```bash
ipconfig getifaddr en0
```

## System Requirements and Dependencies
- Python 3.x installed
- Unix-based OS
