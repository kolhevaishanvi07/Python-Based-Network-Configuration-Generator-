import ipaddress


def calculate_subnet(network):

    net = ipaddress.ip_network(network, strict=False)

    hosts = list(net.hosts())

    if hosts:
        first_ip = hosts[0]
        last_ip = hosts[-1]
    else:
        first_ip = "N/A"
        last_ip = "N/A"

    return {
        "network": str(net.network_address),
        "broadcast": str(net.broadcast_address),
        "subnet_mask": str(net.netmask),
        "first_ip": str(first_ip),
        "last_ip": str(last_ip),
        "total_hosts": net.num_addresses - 2
    }