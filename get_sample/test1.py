import os
from subprocess import check_output


def switch_vpn(turn):
    check_output("chcp 437", shell=True)
    connect_status = "netstat -an"
    connect_command = "rasdial  US usa vpn2014"
    disconnect_command = "rasdial US /DISCONNECT"
    result = check_output(connect_status)
    status = bytes.decode(result)
    if turn == "on" and "1723" not in status:
        check_output(connect_command)
    elif turn == "off" and "1723" in status:
        check_output(disconnect_command)


switch_vpn("off")