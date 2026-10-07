import ipaddress


def validate_ip(ip):
    try:
        ipaddress.ip_address(ip)
        return True
    except ValueError:
        return False


def validate_network(network):
    try:
        ipaddress.ip_network(network, strict=False)
        return True
    except ValueError:
        return False


def validate_vlan(vlan):
    try:
        vlan = int(vlan)
        return 1 <= vlan <= 4094
    except ValueError:
        return False