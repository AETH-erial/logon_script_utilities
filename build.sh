ls /bin | grep nordvpn
EXIT_STATUS=$(echo $?)
if [ $EXIT_STATUS == 0 ]; then
#  adding the dnsleaktest script to a working directory, then moving it to the /bin and
##  making it executable.
mkdir /tmp/dns-leak-test
touch /tmp/dns-leak-test/dnsleaktest.py
curl https://raw.githubusercontent.com/macvk/dnsleaktest/master/dnsleaktest.py -o /tmp/dns-leak-test/dnsleaktest.py

cp /tmp/dns-leak-test/dnsleaktest.py /bin
chmod +x ~/bin/dnsleaktest.py
rm -rf /tmp/dns-leak-test
#  creating the executable shell script to establish nord connection and 
##  run the dnsleaktest we just cloned
touch /tmp/vpn_diag.sh
echo "nordvpn connect ; nordvpn status ; dnsleaktest.sh" >> /tmp/vpn_diag.sh
mv /tmp/vpn_diag.sh /bin
chmod +x /bin/vpn_diag.sh
rm -f /tmp/vpn_diag.sh
else
echo "Could not find the 'nordvpn' binary in your /bin! \n
      Please install and login to nordvpn on your system"