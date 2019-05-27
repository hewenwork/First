import os
import subprocess
from subprocess import check_output, call


def switch_vpn(turn):
    # connect_status = "netstat -an"
    connect_command = "rasdial  US usa vpn2014"
    disconnect_command = "rasdial US /DISCONNECT"
    command_dict = {
        "on": connect_command,
        "off": disconnect_command
    }
    try:
        subprocess.check_output("chcp 437", shell=True)
        subprocess.check_output(command_dict[turn], shell=True)
        return True
    except subprocess.CalledProcessError:
        return False


aa = switch_vpn("on")
print(aa)