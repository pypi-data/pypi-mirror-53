# PyNonameDomain

## Unofficial NonameDomain.hu API module and CLI tool

### Installation
```bash
pip install pynonamedomain  // Use pip3 if Python2 is the default on your system
```

---
---

## nnd-cli

```
$ nnd-cli 
Usage: nnd-cli [OPTIONS] COMMAND [ARGS]...

  Unofficial CLI tool for NonameDomain.hu

Options:
  --help  Show this message and exit.

Commands:
  create   Create new entry in the zone.
  login    Aquire API token.
  read     Read/find DNS entries in the zone.
  remove   Remove DNS entry from the zone.
  update   Update DNS entry in the zone.
  version  Version info.
```

### Autocomplete
```bash
eval "$(_NND_CLI_COMPLETE=source nnd-cli)"      # for BASH
eval "$(_NND_CLI_COMPLETE=source_zsh nnd-cli)"  # for ZSH
```

### Basic usage

```bash
export NND_DOMAIN="example.com"      # optional
export NND_USERNAME="api_user"       # optional
export NND_PASSWORD="api_pw"         # optional
export NND_TOKEN=$(nnd-cli login -q) # optional
nnd-cli read | jq
nnd-cli create -r '{"type":"A","host":"test","ip":"192.168.0.1","ttl":"60"}'
nnd-cli read -r '{"type":"A"}' -o csv
nnd-cli update --hash d67053c0cc0a544e074696a63723b296feeec564d -r '{"host":"test2"}'
nnd-cli remove --hash d67053c0cc0a544e074696a63723b296feeec564d
```

See per command `--help` for more info.

### Using with [`certbot`](https://certbot.eff.org)

```bash
export NND_DOMAIN="example.com"      # recommended
export NND_USERNAME="api_user"       # mandatory
export NND_PASSWORD="api_pw"         # mandatory
export NND_TOKEN=$(nnd-cli login -q) # mandatory
certbot certonly --manual --preferred-challenges=dns --manual-auth-hook "nnd-cli create -c" --manual-cleanup-hook "nnd-cli remove -q" -d example.com --manual-public-ip-logging-ok --agree-tos -m "your@email.address"
```

### Using with [`lego`](https://go-acme.github.io/lego)

```bash
cp /usr/lib/python3.7/site-packages/pynonamedomain/lego-helper.sh .
# edit ./lego-helper.sh with your credentials
export EXEC_PATH=$(pwd)/lego-helper.sh
lego --dns exec --domains example.com --email "your@email.address" --accept-tos run
```

### Using with [Traefik](https://traefik.io)

Since Traefik uses `lego` for ACME certs, the same helper script can be used.  

```bash
cp /usr/lib/python3.7/site-packages/pynonamedomain/lego-helper.sh .
# edit ./lego-helper.sh with your credentials
export EXEC_PATH=$(pwd)/lego-helper.sh
# Traefik will handle the rest
```

---
---

## pynonamedomain


### Usage

> `class NonameDomain(domain, api_user=None, api_pw=None, token=None)`

Class to implement CRUD operations to the Noname Domain API 

Log into the API.


#### Args

**`domain`**: the domain to manage

**`api_user`**: API user

**`api_pw`**: password of API user

**`token`**: API token


#### Raises

**`ValueError`**: if neither user+password or token provided


#### Examples

`nnd = pynonamedomain.NonameDomain("example.com", "username", "password")`

`nnd = pynonamedomain.NonameDomain("example.org", token = "3e4n23y87tresnt32erstn48")`

---

> `def create(self, **data)`

Create new DNS entry.


###### Args

**`**data`**: a dictionary with all the necessary data to create a new entry


###### Raises

**`SubdomainAlreadyExists`**: if entry already exists

**`requests.HTTPError`**: if HTTP error occurs

**`requests.SSLError`**: if SSL error occurs


###### Returns

'ok' if entry created successfully


###### Examples

`nnd.create(type = "A", host = "test", "ip" = "192.168.0.1", ttl = "600")`

`nnd.create(type = "TXT", text = "something", host = "sample", ttl = "60")`

---

> `def read(self, cached=True, **search)`

Read the current entries in the zone.


###### Args

**`cached`**: returns cached list if True, otherwise query the API


**`**search`**: filter the entries based on their attributes


###### Raises

**`SubdomainNotFound`**: if entry not found


###### Returns

all subdomains if **search** is omitted, otherwise the matching subdomains


###### Examples

`nnd.read()`

`nnd.read(cached = False)`

`nnd.read(type = "A")`

---

> `def remove(self, record_hash)`

Remove entry from the zone.


###### Args

**`record_hash`**: hash of the entry to be deleted


###### Raises

`requests.HTTPError`: if HTTP error occurs

`requests.SSLError`: if SSL error occurs


###### Returns

'ok' if entry removed successfully


###### Examples

`nnd.remove("ab83e38eaquf86ye28e35E8c6")`

---

> `def update(self, record_hash, new_values)`

Update entry in the zone.


###### Args

**`record hash`**: hash of the entry to be updated

**`new_values`**: dictionary of the new attributes


###### Raises

**`ValueError`**: if `new_values` is not a dictionary


###### Returns

'ok' if entry updated successfully


###### Examples

`nnd.update("ab83e38eaquf86ye28e35E8c6", text = "newtext", ttl = "300")`

`nnd.update("ab83e38eaquf86ye28e35E8c6", type = "A", ip = "192.168.1.38")`

