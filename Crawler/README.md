# Crawler
## Install tor 
````
sudo apt install tor
````
## Install obfs4proxy
````
sudo apt install obfs4proxy
````
## Add briges
- from https://bridges.torproject.org/
- choose obsf4
- copy it
- Append the bridges to etc/tor/torrc
````
UseBridges 1
ClientTransportPlugin obfs4 exec /usr/bin/obfs4proxy
Bridge obfs4 "bridge"
````

## Hash password
- run in terminal
````
tor --hash-password "pass"
````
and copy the hashed password.

## Uncomment those line in /etc/tor/torrc
- controlport
- socks
- Hashedpassword ( and add the hashed password)

## Run tor in terminal
````
tor
````

## Run the crawler code
````
python crawler.py
````
