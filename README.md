# Better NordVPN OVPN Configs
 
You can download the OpenVPN files from NordVPN from [here](https://nordvpn.com/servers/tools/) with the limitation that you can only use one server.

There is an [archive](https://downloads.nordcdn.com/configs/archives/servers/ovpn.zip) with all available servers from NordVPN including their OpenVPN config that can be downloaded from NordVPN as well. 

The script takes advantage of this and creates an OpenVPN config with a maximum of 64 servers (due to OpenVPN config limit of 64 servers) from a country you can define by yourself.

Now, every time you connect to NordVPN with the OpenVPN config, a random server will be chosen.