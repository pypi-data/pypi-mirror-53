from __future__ import unicode_literals

from Switch import Switch
from collections import OrderedDict
import ipaddress


s = Switch(ip_address="10.20.30.24", username="cvpadmin", password="nynjlab")

import json

s.get_facts()

print(s)

#Leaf config
mlag_config = s.build_mlag("MLAG1", "primary")

ip_interface_config = s.build_ip_interface_underlay(interfaces_to_ips={"ethernet1":"172.17.200.1", "ethernet2":"172.17.200.3", "ethernet3":"172.17.200.5"})

bgp_underlay_config = s.build_bgp_underlay(65001, "leaf", "172.16.0.4/32", OrderedDict({65000:["172.16.200.0", "172.16.200.2", "172.16.200.4"]}))

vxlan_data_plane_config = s.build_vxlan_data_plane({10:10010, 20:10020, 100:10100}, "1.1.1.1/32")


vtep_peers = ["172.16.0.5", "172.16.0.6"]
cvx_address = "192.168.0.1"
evpn_peers = {65000: ["172.16.0.1", "172.16.0.2", "172.16.0.3"]}
asn = 65001
svi_to_address = {12:"172.16.112.1/24", 13:"172.16.113.1/24", 14:"172.16.114.1/24"}
mac_vrf_rd = "1.1.1.1"
vrf_rd = "1.1.1.1"

vxlan_control_plane_config = s.build_vxlan_control_plane("evpn", vtep_peers=vtep_peers, cvx_address=cvx_address,
                                                        evpn_peers=evpn_peers, asn=asn, role="leaf", evpn_model="symmetric", svi_to_address=svi_to_address,
                                                        mac_vrf_route_distinguisher=mac_vrf_rd, vrf_route_distinguisher=vrf_rd,
                                                        )


print(mlag_config)
print(ip_interface_config)
print(vxlan_data_plane_config)
print(bgp_underlay_config)
print(vxlan_control_plane_config)

#Spine config
# ip_interface_config = s.build_ip_interface_underlay(interfaces_to_ips={"ethernet1":"172.17.200.0", "ethernet2":"172.17.200.2"})
# bgp_underlay_config = s.build_bgp_underlay(65000, "spine", "172.16.0.1", {65001:["172.16.200.3"], 65002:["172.16.200.4"]})

# evpn_peers = {65001: ["172.16.0.3"], 65002:["172.16.0.4"], 65003:["172.16.0.5"]}
# asn = 65000

# vxlan_control_plane_config = s.build_vxlan_control_plane("evpn", evpn_peers=evpn_peers, asn=asn)


# print(json.dumps(ordered_interface_speeds, indent=2))