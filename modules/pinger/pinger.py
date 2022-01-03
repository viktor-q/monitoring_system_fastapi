import os


def pinger(hostname):
    #    hostname = "192.168.1.4"
    response = os.system("ping -c 1 " + hostname)
    if response == 0:
        pingstatus = "Network Active"
    else:
        pingstatus = "Network NOT ACTIVE or Error"

    #    print(pingstatus)
    return pingstatus


# print(pinger("192.168.1.4"))
