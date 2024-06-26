import socket
from termcolor import colored, cprint
from cert_sleuth import config


def scan_alive(sites):
    alive_sites = {}
    try:
        cprint(f"[*] Which ports do you want to test? (Use 80 and 443 for webservers).", color='green')
        ports = []
        answer = ''
        while answer != 'd':
            answer = input(colored(f"[*] Enter one at a time OR type 'd' for done: ", color="green"))
            if answer != 'd':
                if 65535 > int(answer) > 0:
                    ports.append(int(answer))
                else:
                    cprint(f"[!] Please type a valid port. ", color="red")


        cprint(f"[*] Iterating through {len(sites)} sites on {ports} ports.", color='green')
        for port in ports:
            cprint(f"[@] Testing port {port}...", color="magenta")
            for site in sites:
                client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                client_socket.settimeout(int(config.get_args().speed))
                try:
                    client_socket.connect((site, port))
                    alive_sites.update({site: port})
                    cprint(f"[!] {site} is alive on port {port}!!", color="cyan")
                except socket.error as e:
                    cprint(f"[-] {site} is dead on port {port}! :(", color="red")
                    client_socket.close()

        cprint(f"[*] {len(alive_sites)} alive sites found! ", color="green")
        cprint(f"[*] The sites are: ", color="green")
        for alive_site in alive_sites:
            cprint(alive_site, color="yellow")


    except Exception as e:
        cprint(f"[-] An unknown error occurred. Error: {e} "
               f"Contact jsuess@utsystem.edu for more", color='red')

# Placeholder for now.
def aggregate_results():
    return 0

