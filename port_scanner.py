import socket
import re
import common_ports as port_collection
ports_ref = port_collection.ports_and_services


def get_open_ports(target, port_range, Verbose=False):
    open_ports = []
    # check if target is url or ip(contains no alphabet)
    is_ip = True if target.find('c') == -1 else False

    if is_ip:
        # validate ip address
        valid_ip = re.match(
            '''^((25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\\.){3}(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)$''', target)
        if not valid_ip:
            return "Error: Invalid IP address"

    print('scanning.....', target)

    try:
        target_ip = socket.gethostbyname(target)
        hostname = ''
        try:
            # from ip to hostname
            hostname = socket.gethostbyaddr(target)[0]
        except:
            hostname = target

        for port in range(port_range[0], port_range[1]+1):
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

            sock.settimeout(0.4)
            result = sock.connect_ex((target_ip, port))
            if result == 0:
                open_ports.append(port)
            sock.close()

    except socket.error:
        return "Error: Invalid hostname"

    if Verbose:
        ip_to_print = ' ('+target_ip + \
            ')' if not is_ip or hostname != target else ''

        output = 'Open ports for {}{}\nPORT     SERVICE'.format(
            hostname, ip_to_print)
        for p in open_ports:
            port_string = str(p)
            output += '\n'+port_string+' '*(9-len(port_string))+ports_ref[p]
        return output
    else:
        return open_ports
