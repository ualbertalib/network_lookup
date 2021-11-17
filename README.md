# The "network lookup" API

## Goals, Background

This is a microservice, which allows users to supply either an IP address or an FQDN, to retrieve the details of the VLAN containing that host.

## Cloning this repo

* This repo uses submodules to keep the code public, but our data private, so: ```git clone --recurse-submodules git@github.com:ualbertalib/network_lookup.git```
* Or see [git submodules](https://git-scm.com/book/en/v2/Git-Tools-Submodules)

```
git clone git@github.com:ualbertalib/network_lookup.git
git submodule init
git submodule update
```

* If you're an external user, copy the file "vlans.json" is a template for the input data for this microservice. Copy it to the network_data/ directory & enter your own data.

## Query this microservice from the commandline

* To query using a valid IP address: 

```
curl http://localhost:8000/addr/10.0.0.2
{"id:":101,"netmask":"255.255.255.0","hostname":"this.that.net","gateway":"10.0.0.1","addr":"10.0.0.2","VMWareVLAN":"SAM1"}
```

* To query using a valid Fully Qualified Domain Name (FQDN), supply the full name (it must resolve in local DNS, obviously):

```
curl http://localhost:8000/fqdn/this.that.net
{"id:":101,"netmask":"255.255.255.0","hostname":"this.that.net","gateway":"10.0.0.1","addr":"10.0.0.2","VMWareVLAN":"SAM1"}
```

* If the supplied IP address or FQDN does not resolve in your local DNS, this will only give you an error (replying 404)

## Security Posture

* This web service is READ ONLY, and it's only used to lookup information we already know
* FIRM ADVICE: 
    * use a local firewall to both rate-limit and restrict the IP addresses able to reach this service
    * it needs strong authentication
    * it needs encryption
    * it needs fail2ban watching the log file & protecting the port from evildoers
    * it needs logging for fail2ban 
* The Github repository is marked PUBLIC, because it contains no actual data

## Running this locally on your desktop, sans Docker

* Just: 

```
[nmacgreg@redacted network_lookup]$ uvicorn main:app --reload
INFO:     Uvicorn running on http://127.0.0.1:8000 (Press CTRL+C to quit)
INFO:     Started reloader process [2950773] using statreload
```

## Prerequisites

* python, obviously, and I think you need python 3. I'm running v3.9.2 at inception
* "uvicorn", at least for development, and you can install that on RHEL derivatives with: ```dnf install python3-uvicorn```
* "fastapi" is a library this depends upon, but there's no RPM for it, so: ```pip install fastapi```

## Containers

* [This works with Docker](docs/docker.md)
* [This works with Podman and Buildah](docs/podman.md)

## Running within Docker

* Like this: 

```
docker run --restart=always -d -p 80:8000 --volume /root/network_lookup/network_data:/home/ualuser/network_data nmacgreg/network_lookup 
```

* Notes: 
    * I used that on node-srv-tst-1 
    * it ensures that the container will always be restarted, whenever docker starts up
    * It assumes that the copy of network_data is up to date - you will need to manually pull updates into /root/network_lookup/network_data, ok? 

## Setting up VSCode

* [This Article](https://stackoverflow.com/questions/60205056/debug-fastapi-application-in-vscode), I didn't try this
