import subprocess;
import os;


def get_os_mem():
    (status1, used) = subprocess.getstatusoutput(
        "free | sed -n '2p' |awk '{print $3}' ")
    (status2, total) = subprocess.getstatusoutput(
        "free | sed -n '2p' |awk '{print $2}' ")
    if status1 == 0 and status2 == 0:
        return {"used": int(used), "total": int(total)}
    else:
        raise RuntimeError("can't get os mem")
