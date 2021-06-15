# file:///libroot/ITS_Share/Unix/Projects/2021/Q2/DockerExperiments/volley2.html
FROM fedora:34

USER root

# This is a python app, that needs 'uvicorn':
RUN /usr/bin/dnf install -y python3-uvicorn python3-pip

# Should I run this as root?   Or not? Probably not? 
RUN useradd ualuser -u 1000 -m -G users,wheel && \
    chown -R ualuser:ualuser /home/ualuser
USER ualuser  

# Grab the application components I need, and stuff them into the user's home dir
COPY main.py    /home/ualuser 
COPY vlans.json /home/ualuser 

# I should probably version this
RUN /usr/bin/pip3 install fastapi

CMD cd && uvicorn --host 0.0.0.0 main:app 
