# Using this codebase with Buildah & Podman 

* You can use Buildah in compatibility mode; I have added a withBuildah.sh script to demonstrate that
* To run the container with Podman, the syntax is the same as with Docker: ```# podman run -d -p 80:8000 --volume /root/dev/network_lookup/network_data:/home/ualuser/network_data nmacgreg/network_lookup```