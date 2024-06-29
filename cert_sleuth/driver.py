import requests
from termcolor import colored, cprint
import methods
import argparse


banner = r"""                         __      _________ .__                       __    .__      
  ____     ____   _______  _/  |_   /   _____/ |  |     ____    __ __  _/  |_  |  |__   
_/ ___\  _/ __ \  \_  __ \ \   __\  \_____  \  |  |   _/ __ \  |  |  \ \   __\ |  |  \  
\  \___  \  ___/   |  | \/  |  |    /        \ |  |__ \  ___/  |  |  /  |  |   |   Y  \ 
 \___  >  \___  >  |__|     |__|   /_______  / |____/  \___  > |____/   |__|   |___|  / 
     \/       \/                           \/              \/                       \/  

    ＣᗴＲ丅Ｓ⎳ＵᗴＴᕼ v. 1.0.3

    Created by Joseph Suess, 6/20/2024. Last modified: 6/26/2024.
    
    Company Use: University of Texas System - Office of Information Security.
    
    For Legal and Ethical Use Only, Author assumes no responsibility for misuse.
"""


global args

def get_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('-d', '--domain', required=True, help='Website to enumerate')
    parser.add_argument('-s', '--speed', required=True, help='Speed of scans(quick=1, '
                                                  'slow=4. not recommend to go past 4.)')
    parser.add_argument('-v', '--verbose', action='store_true', required=False, help='Verbose output on dead/alive websites')
    arguments = parser.parse_args()
    return arguments

args = get_args()


# Credit to Dru Banks for the majority of this method.  It used to get the subdomains of the iterated domain.
# I have changed it to pull the name values of each domain instead. This gives way more scope!
def get_names(domain):
    cprint("[+] Getting the common names...", "green")
    url = f"https://crt.sh/?q={domain}&output=json"
    try:
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()
        sites = set()
        for item in data:
            name_value = item["name_value"]
            if name_value.find('\n'):
                subname_value = name_value.split('\n')
                for subname in subname_value:
                    if subname.find('*') == -1:
                        sites.add(subname)

        # Now sort, based on increasing order to give a full list.
        return sorted(sites)
    except requests.RequestException:
        cprint("[-] Error retrieving data from crt.sh", "red")
        return set()


def main():
    print(banner)
    sites = get_names(args.domain)
    size = (len(sites))
    if sites:
        cprint(f"[*] Dead and Alive websites of {args.domain}:", "green")
        for site in sites:
            cprint(site, "yellow")
        cprint(f"[*] {size} unique names found.", color="green")
        answer = input(colored(f"[*] Would you like to only find running websites (y/n)? ", color="green"))
        if answer == 'y' or answer == 'yes':
            alive_sites = methods.scan_alive(sites, args.speed)
        else:
            cprint(f"[*] Would you like an output of this list in txt form? (y/n).", color="green")

    try:
        methods.aggregate_results()
    except Exception as e:
        cprint(f"[-] error generating the site...", color="red")

    else:
        cprint(f"[-] No websites (dead or alive) found for {args.domain}", "red")
        cprint(f"[-] Please try again! Usually this signals the site crt.sh is down OR a typo in the -d flag"
               f".. contact jsuess@utsystem.edu :(", color="red")


if __name__ == "__main__":
    main()
