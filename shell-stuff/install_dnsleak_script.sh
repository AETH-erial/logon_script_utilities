mkdir ~/dns-leak-test
touch ~/dns-leak-test/dnsleaktest.py
curl https://raw.githubusercontent.com/macvk/dnsleaktest/master/dnsleaktest.py -o ~/dns-leak-test/dnsleaktest.py

cp ~/dns-leak-test/dnsleaktest.py /bin
chmod +x ~/bin/dnsleaktest.py