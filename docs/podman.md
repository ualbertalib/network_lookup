# Using this codebase with Buildah & Podman 

* You can use Buildah in compatibility mode; I have added a withBuildah.sh script to demonstrate that
* To run the container with Podman, the syntax now accomodates SELinux, which is integrated with buildah

```
# podman run  -d -p 80:8000 --volume /root/dev/network_lookup/network_data:/home/ualuser/network_data:Z nmacgreg/network_lookup 
```
 
* And, you can query the running service exactly as demonstrated in [sister doc for docker](docker.md)
