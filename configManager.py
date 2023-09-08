import os
import re
import random
from platform import system as getOS
from shutil import rmtree
from zipfile import ZipFile

import requests
from colorama import init, Fore, Style

# enable colors for cmd and powershell
if getOS() == 'Windows': init(convert=True)

def downloadConfigs(filename):
    try:
        _log("Started download of ovpn files")
        download_link = "https://downloads.nordcdn.com/configs/archives/servers/ovpn.zip"
        req = requests.get(download_link)
        _log("Download finished")
        open(filename, 'wb').write(req.content)
    except Exception as e:
        _log(f"Download failed: {e.args[0]}", True)
        exit()

def unzip(filename):
    try:
        _log("Extracting files")
        with ZipFile(filename, 'r') as zipObj:
            zipObj.extractall(os.curdir)
        _log("Extracted files")
    except Exception as e:
        _log(f"Extraction failed: {e.args[0]}", True)
        exit()

def getCountry(path):
    countries_dict = {}
    coutry_regex = r'([a-z]{2}|[a-z]{2}-[a-z]{2,5})[0-9]{1,}\.nordvpn\.com\.(tcp|udp)\.ovpn'
    for file in os.listdir(path):
        country_match = re.match(coutry_regex, file)
        country = country_match.groups()[0]
        if country not in countries_dict.keys():
            countries_dict[country] = 0
        countries_dict[country] += 1

    user_input = _user_input("List availible countries? [y/n]", ['y', 'yes', 'n', 'no'])

    if user_input in ['y', 'yes']:
        print("Availible countries")
        for keys, values in countries_dict.items():
            print(f"{keys:9}: {values}")

    selected_country_by_user = _user_input("Please select one country", countries_dict.keys())

    return selected_country_by_user

def grepServersFromFiles(path, region):
    connection_type_regex = r'proto (?:tcp|udp){1}'
    server_regex = r'remote [\d.]{7,15} [\d]{1,5}'
    servers = []

    ovpn_template = None

    for file in os.listdir(path):

        # using f-string and r-string in combination is a horrible experience in python
        dot = r'\.'
        ovpn_nordvpn_filename_regex = rf"({region}[0-9]{{1,4}}){dot}nordvpn{dot}com{dot}(tcp|udp){{1}}{dot}ovpn"

        filename_match = re.match(ovpn_nordvpn_filename_regex, file)
        if filename_match != None:
            with open(path+"/"+file, 'r') as file:
                ovpn_content = file.read()
                file.close()
                server_match = re.findall(server_regex, ovpn_content)
                if server_match != []:
                    servers.append(server_match[0])
                    if ovpn_template == None:
                        ovpn_template = str(ovpn_content).replace(server_match[0], f"%s")
                        ovpn_template = ovpn_template.replace(re.findall(connection_type_regex, ovpn_template)[0], f"proto %s")
                    continue

    return servers, ovpn_template

def createConfigs(template, country, connection_type, servers):
    # Temporarlily outcommenting "verify-x509-name" from the ovpn config becouse there is no option to match the name suffix
    template = template.replace("verify-x509-name", "#verify-x509-name")

    # Add optionally predefined login credential config, if you want to use it uncomment the line in the ovpn config
    template = template.replace("auth-user-pass", "auth-user-pass #login.conf")

    servers_str = "#\n# Maximum number of servers in OVPN config is 64\n#\n"
    max_range = 64 if len(servers) > 64 else len(servers)
    for index in random.sample(range(0, max_range), max_range):
        servers_str += servers[index] + "\n"
    ovpn_config = template%(connection_type, servers_str)
    _log("Writing ovpn config")
    ovpn_filename = f"{country}.nordvpn.com.{connection_type}.ovpn"
    try:
        open(ovpn_filename, 'wt').write(ovpn_config)
    except Exception as e:
        _log(f"Failed to write file: {e.args[0]}", True)
        print("\n" + ovpn_config)
    _log(f"Writen ovpn config -> {ovpn_filename}")

def configure_config():
    connection_type = _user_input("What type of vpn connection do you want?", ['tcp', 'udp'], True)
    path = f"ovpn_{connection_type}"
    country = getCountry(path)
    servers, ovpn_template = grepServersFromFiles(path, country)
    createConfigs(ovpn_template, country, connection_type, servers)

def run():
    archiv_filename = "ovpn.zip"
    downloadConfigs(archiv_filename)
    unzip(archiv_filename)

    user_input = None
    while user_input in ['y', 'yes'] or user_input == None:
        configure_config()
        user_input = _user_input("Do you want to create more ovpn configs? [y/n]", ['y', 'yes', 'n', 'no'])

    _log("Cleaning up files")
    os.remove(archiv_filename)
    rmtree("ovpn_tcp", ignore_errors=True)
    rmtree("ovpn_udp", ignore_errors=True)
    _log("Finished clean up")

def _log(msg, failure=False):
    print(f"{Fore.RED+'[-]'+Style.RESET_ALL if failure else Fore.GREEN+'[+]'+Style.RESET_ALL} {msg}")

def _user_input(msg, possible_user_options, show_options = False):
    user_input = None
    while user_input not in possible_user_options:
        user_input = str.lower(input(f"{msg + ' ' + str(possible_user_options) if show_options else msg}: "))
    return user_input

if __name__ == "__main__":
    run()
    _log("Thank you for using my script ;)")