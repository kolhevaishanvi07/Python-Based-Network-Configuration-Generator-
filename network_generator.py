def generate_vlan(vlan_id, vlan_name):

    return f"""vlan {vlan_id}
name {vlan_name}
exit
"""


def generate_interface(interface, vlan_id):

    return f"""interface {interface}
switchport mode access
switchport access vlan {vlan_id}
no shutdown
exit
"""


def generate_ip(interface, ip, mask):

    return f"""interface {interface}
ip address {ip} {mask}
no shutdown
exit
"""


def generate_complete_config(vlans, interface, ip, mask):

    config = "enable\nconfigure terminal\n\n"

    # VLAN configuration
    for vlan in vlans:
        config += generate_vlan(
            vlan["id"],
            vlan["name"]
        )

    config += "\n"

    # Interface configuration
    for vlan in vlans:
        config += generate_interface(
            vlan["interface"],
            vlan["id"]
        )

    config += "\n"

    # IP configuration
    config += generate_ip(
        interface,
        ip,
        mask
    )

    config += "\nend\n"
    config += "write memory\n"

    return config