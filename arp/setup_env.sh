sudo apt-get install ettercap-common -y
sudo pip2 install flask
sudo pip2 install scapy
sudo cp CustomServer/arp.py /bin
sudo chmod 777 /etc/ettercap/etter.dns
sudo ln -s /etc/ettercap/etter.dns .
echo '' > etter.dns
