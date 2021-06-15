import re
import json
import socket
import ipaddress
from fastapi import FastAPI, HTTPException

# read a JSON-formatted file detailing the pantheon of VLANs at UAL
#with open('vlans.json', 'r') as myfile:
    #jsondata = myfile.read()

with open('network_data/vlans.json', 'r') as myfile:
    jsondata = myfile.read()

# transform that into a local datastructure
vlans = json.loads(jsondata)

# Loop across all the items in the network list, adding a structured object describing the VLAN
# Ref: https://docs.python.org/3/library/ipaddress.html
limit = len(vlans)
for counter in range(0, limit):
    #print(vlans[counter]['network'])
    vlans[counter]['object'] = ipaddress.IPv4Network(vlans[counter]['network'])

app = FastAPI()

#########################################################################################
@app.get("/")
async def root():
    """This function merely returns a Hello World dict"""
    return {"message": "Hello World"}

#########################################################################################
@app.get("/addr/{item}")
async def addr(item: str):
    """This function returns a dict describing the VLAN which matches the input IP address"""
    # Does that look like a valid IP address?
    flag = False
    if "." in item:
        elements_array = item.strip().split(".")
        if len(elements_array) == 4:
            for i in elements_array:
                if (i.isnumeric() and int(i) >= 0 and int(i) <= 255):
                    flag = True
                else:
                    flag = False
                    break
    if not flag:
        raise HTTPException(status_code=404, detail="Not a valid IP address")

    # Construct an object from that IP address
    sample = ipaddress.ip_address(item)

    # Does that IP address resolve?
    try:
        hostname = socket.gethostbyaddr(item)
    except socket.error as bad_hostname:
        raise HTTPException(status_code=404, detail="Unable to resolve hostname") from bad_hostname

    # Loop across the list of IP networks, looking for a match
    mylimit = len(vlans)
    for mycounter in range(0, mylimit):
        if sample in list(vlans[mycounter]['object'].hosts()):
            return {"id": vlans[mycounter]['id'], "netmask": vlans[mycounter]['object'].netmask,
            "hostname": hostname[0], "gateway": vlans[mycounter]['gateway'], "addr": item,
            'VMWareVLAN': vlans[mycounter]['vmware']}  # found a matching VLAN!

    # Didn't find a match in any record?
    raise HTTPException(status_code=404, detail="Item not found")

#########################################################################################
def is_valid_hostname(hostname):
    """This function describes whether the input is a valid hostame"""
    if len(hostname) > 255:
        return False
    if hostname[-1] == ".":
        hostname = hostname[:-1] # strip exactly one dot from the right, if present
    allowed = re.compile("(?!-)[A-Z\d-]{1,63}(?<!-)$", re.IGNORECASE)
    return all(allowed.match(x) for x in hostname.split("."))

#########################################################################################
@app.get("/fqdn/{item}")
async def fqdn(item: str):
    """This function returns a dict describing a VLAN, matching input Fully Qualified Domain Name"""
    # Does that item look something like a FQDN?
    if not is_valid_hostname(item):
        raise HTTPException(status_code=404, detail="Not an FQDN")
    # Resolve that FQDN into an IP address
    try:
        complex_struct = socket.getaddrinfo(item, 80)
    except (socket.gaierror, IndexError, ConnectionError) as bad_fqdn:
        raise HTTPException(status_code=404, detail="Cannot resolve hostname") from bad_fqdn

    # That returns a complex data structure... ?
    #print(complex_struct)
    address = complex_struct[0][4][0]
    #print(address)

    # Construct an object from that IP address
    sample = ipaddress.ip_address(address)

    # Loop across the list of IP networks, looking for a match
    mylimit = len(vlans)
    for mycounter in range(0, mylimit):
        if sample in list(vlans[mycounter]['object'].hosts()):
            return {"id": vlans[mycounter]['id'], "netmask": vlans[mycounter]['object'].netmask,
            "hostname": item, "gateway": vlans[mycounter]['gateway'], 'addr': address,
            'VMWareVLAN': vlans[mycounter]['vmware']}  # found a matching VLAN!

    # Didn't find a match in any record?
    raise HTTPException(status_code=404, detail="Your FQDN does not match a known VLAN, sorry")
