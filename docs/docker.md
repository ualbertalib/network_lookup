# Running this in Docker

## Docker 

* I have added a Dockerfile, and you can call build.sh to build the image locally
* I have added network_data as a [git submodule](https://git-scm.com/book/en/v2/Git-Tools-Submodules)... ```git submodules init; git submodules update```
* (note: network_data is a Private repo, containing data that should not be released publicly) 
* You can run it: ```# docker run -d -p 80:8000 --volume /home/autobuild/network_lookup/network_data:/home/ualuser/network_data nmacgreg/network_lookup```

## Querying the application running under Docker

```
curl http://localhost:80/addr/10.0.0.2
{"id:":101,"netmask":"255.255.255.0","hostname":"this.that.net","gateway":"10.0.0.1","addr":"10.0.0.2","VMWareVLAN":"SAM1"}
```

* To query using a valid Fully Qualified Domain Name (FQDN), supply the full name (it must resolve in local DNS, obviously):

```
curl http://localhost:80/fqdn/this.that.net
{"id:":101,"netmask":"255.255.255.0","hostname":"this.that.net","gateway":"10.0.0.1","addr":"10.0.0.2","VMWareVLAN":"SAM1"}
```

