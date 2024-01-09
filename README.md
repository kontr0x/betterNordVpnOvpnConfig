# Better NordVPN OVPN Configs

> __Disclaimer__: Since June 14th, 2023, NordVPN OpenVPN connections only work with VPN specific credentials.
> 
> Instructions can be found here: [NordVPN support](https://support.nordvpn.com/General-info/1653315162/Changes-to-the-login-process-on-third-party-apps-and-routers.htm).

## Why does this project exist?
I had too much time... , just kidding. I wanted a solution to automate the process of VPN server hopping, which works perfectly fine with OpenVPN.
This was also very handy on my router running OpenWRT, where this config also allows me to hop between Nodes without supplying a new config.

## Can I do this manually?
Yes, of course! Do you want to? I don't think so. :)

You can download the OpenVPN files from NordVPN from [here](https://nordvpn.com/servers/tools/) with the limitation that you can only choose one server at a time.
There is an [archive](https://downloads.nordcdn.com/configs/archives/servers/ovpn.zip) with all available servers from NordVPN including their OpenVPN config that can be downloaded from NordVPN as well. 

## What does the script different?
The script creates an OpenVPN config with 64 servers / remotes (due to OpenVPN's remote limit of 64 servers, there can't be more) from a country you can choose through the script.
Now, every time you connect to NordVPN with the OpenVPN config, a random server out of the 64 remotes will be chosen.
