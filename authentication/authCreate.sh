rm -r /etc/mosquitto/certs
rm authentication/ca.key
rm authentication/ca.srl
rm authentication/server.csr

openssl genrsa -des3 -out ca.key 2048
openssl req -new -x509 -days 1826 -key ca.key -out ca.crt
openssl genrsa -out server.key 2048
openssl req -new -out server.csr -key server.key
openssl x509 -req -in server.csr -CA ca.crt -CAkey ca.key -CAcreateserial -out server.crt -days 360 

#create directory for certificates
mkdir /etc/mosquitto/certs
mv ca.crt /etc/mosquitto/certs
mv server.crt /etc/mosquitto/certs
mv server.key /etc/mosquitto/certs
mv ca.key authentication
mv ca.srl authentication
mv server.csr authentication

rm /etc/mosquitto/passwd.conf
rm /etc/mosquitto/aclfile.conf

mosquitto_passwd -c /etc/mosquitto/passwd.conf server
mosquitto_passwd -b /etc/mosquitto/passwd.conf client password

sudo echo '# This only affects clients with username "server".
user server
topic server/card
topic terminal/card
topic server/ID
topic terminal/ID
# This only affects clients with username "client".
user client
topic read server/card
topic read server/ID
topic terminal/card
topic terminal/ID' > /etc/mosquitto/aclfile.conf
