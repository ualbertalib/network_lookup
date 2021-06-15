# The "network lookup" API

## Goals, Background

This is a microservice, which allows users to supply either an IP address or an FQDN, to retrieve the details of the VLAN containing that host.

## Calling this from the commandline: 

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
    * it need encryption
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
* "uvicorn", at least for development, and you can install that with: ```dnf install python3-uvicorn```
* "fastapi" is a library this depends upon, but there's no RPM for it, so: ```pip install fastapi```

## Docker: 

* I've added a Dockerfile; you can call build.sh to build the image locally
* *Do not push this to a repo like DockerHub, RE: Security!*
* You can run it: ```# docker run -d -p 80:8000 nmacgreg/network_lookup```
* (Some work in progress, here)

## Buildah & Podman: 

* You can use Buildah in compatibility mode; I've added a withBuildah.sh script to demonstrate that
* To run the container with Podman, the syntax is the same as with Docker: ```# podman run -d -p 80:8000 namcgreg/network_lookup```  (cool!) 

## Setting up VSCode

* [This Article](https://stackoverflow.com/questions/60205056/debug-fastapi-application-in-vscode), I didn't try this
