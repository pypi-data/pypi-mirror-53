from __future__ import print_function
import sys
import os
import socket


def sendToMgv(msg, address='127.0.0.1', port=None):
    """Send a command to a Mangrove instance.

    Parameters:
        msg (str): Mangrove command
        address (str): IP address of the mangrove instance
        port (str): port used by the mangrove instance
    Return (str):
        Mangrove instance response
    """
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    text = None
    try:
        port = int(os.getenv("MGVPORT")) if port is None else int(port)
        s.connect((address, port))
        s.send(msg.encode())
        text = s.recv(4096)
    except Exception as msg:
        print(msg, file=sys.__stderr__)
    finally:
        s.close()
    return text


def setParam(param, value):
    """Modify a parameter value of the current node.

    Parameters:
        param (str): parameter name
        value (str): parameter value
    Return (str):
        "ok"
    """
    msg = "*MGVSEPARATOR*".join(["SETNODEPARAM", os.getenv("MGVGRAPHKEYS"), os.getenv("MGVNODENAME"), param, value])
    return sendToMgv(msg)


def setNode(node, param, value):
    """Modify a parameter value of a specific node.

    Paramaters:
        node (str): node name
        param (str): parameter name
        value (str): parameter value
    Return (str):
        "ok"
    """
    msg = "*MGVSEPARATOR*".join(["SETNODEPARAM", os.getenv("MGVGRAPHKEYS"), node, param, value])
    return sendToMgv(msg)


def newVersion():
    """Create a new version based on the current one on
    the current node.

    Return (str):
        new version id
    """
    msg = "*MGVSEPARATOR*".join(["NEWVERSION", os.getenv("MGVGRAPHKEYS"), os.getenv("MGVNODENAME")])
    return sendToMgv(msg)


def setVersion(value):
    """Change the current version of the current node.

    Parameters:
        value (str): version id
    Return:
        "ok"
    """
    msg = "*MGVSEPARATOR*".join(["SETVERSION", os.getenv("MGVGRAPHKEYS"), os.getenv("MGVNODENAME"), value])
    return sendToMgv(msg)


def setComment(value):
    """Modify the comment of the current node's active version.

    Paramaters:
        value (str): new comment
    Return (str):
        "ok"
    """
    msg = "*MGVSEPARATOR*".join(["SETCOMMENT", os.getenv("MGVGRAPHKEYS"), os.getenv("MGVNODENAME"), value])
    return sendToMgv(msg)


def exe(*args):
    """Execute an action of the current node.

    Paramaters:
        args: action name or (node name, action name)
    Return (str):
        "ok"
    """
    if len(args) == 2:
        node, actions = args[0], args[1]
    else:
        node, actions = os.getenv("MGVNODENAME"), args[0]
    #if not node:
    #    node = os.getenv("MGVNODENAME")
    msg = "*MGVSEPARATOR*".join(["EXE", os.getenv("MGVGRAPHKEYS"), os.getenv("MGVNODENAME"), node, actions])
    return sendToMgv(msg)


def update():
    """Ask Mangrove to update the graph view

    Return (str):
        "ok"
    """
    msg = "*MGVSEPARATOR*".join(["UPDATE", os.getenv("MGVGRAPHKEYS"), os.getenv("MGVNODENAME")])
    return sendToMgv(msg)


def lock():
    """Lock the current node's active version

    Return (str):
        "ok"
    """
    msg = "*MGVSEPARATOR*".join(["LOCKVERSION", os.getenv("MGVGRAPHKEYS"), os.getenv("MGVNODENAME")])
    return sendToMgv(msg)


def setData(name, value):
    """Set or add a data to the current node data dictionnary

    Parameters:
        name (str): data name
        value (str): data value
    Return (str):
        "ok"
    """
    msg = "*MGVSEPARATOR*".join(["SETNODEDATA", os.getenv("MGVGRAPHKEYS"), os.getenv("MGVNODENAME"), name, value])
    return sendToMgv(msg)


def removeData(name):
    """Remove a data from the current node data dictionnary

    Parameters:
        name (str): data name
    Return (str):
        "ok"
    """
    msg = "*MGVSEPARATOR*".join(["DELNODEDATA", os.getenv("MGVGRAPHKEYS"), os.getenv("MGVNODENAME"), name])
    return sendToMgv(msg)


def getData(name):
    """Get a data value from the current node

    Parameters:
        name (str): data name
    Return (str):
        data value
    """
    msg = "*MGVSEPARATOR*".join(["GETNODEDATA", os.getenv("MGVGRAPHKEYS"), os.getenv("MGVNODENAME"), name])
    return sendToMgv(msg)


def setVersionData(name, value):
    """Set or add a data to the current node version data dictionnary

    Parameters:
        name (str): data name
        value (str): data value
    Return (str):
        "ok"
    """
    msg = "*MGVSEPARATOR*".join(["SETVERSIONDATA", os.getenv("MGVGRAPHKEYS"), os.getenv("MGVNODENAME"), name, value])
    return sendToMgv(msg)


def removeVersionData(name):
    """Remove a data from the current node version data dictionnary

    Parameters:
        name (str): data name
    Return (str):
        "ok"
    """
    msg = "*MGVSEPARATOR*".join(["DELVERSIONDATA", os.getenv("MGVGRAPHKEYS"), os.getenv("MGVNODENAME"), name])
    return sendToMgv(msg)


def getVersionData(name):
    """Get a data value from the current node version

    Parameters:
        name (str): data name
    Return (str):
        data value
    """
    msg = "*MGVSEPARATOR*".join(["GETVERSIONDATA", os.getenv("MGVGRAPHKEYS"), os.getenv("MGVNODENAME"), name])
    return sendToMgv(msg)