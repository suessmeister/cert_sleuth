import socket
from termcolor import colored, cprint
import time
import subprocess

alive_sites = {}
start_time = None
end_time = None

def get_ports():
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

    return ports

def scan_alive(sites, speed):
    global start_time, end_time, alive_sites
    start_time = time.time()
    try:
        ports = get_ports()
        cprint(f"[*] Iterating through {len(sites)} sites on {ports} ports.", color='green')
        for port in ports:
            site_counter = 0
            cprint(f"[@] Testing port {port}...", color="magenta")
            for site in sites:
                site_counter += 1
                client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                client_socket.settimeout(int(speed))
                try:
                    str = colored(f"{site_counter}/{len(sites)} checked...", color="red")
                    print('\r' + str, end='', flush=True)
                    client_socket.connect((site, port))
                    alive_sites.update({site: port})
                    cprint(f"[!] {site} is alive on port {port}!!", color="cyan")
                except socket.error as e:
                    # cprint(f"[-] {site} is dead on port {port}! :(", color="red")
                    client_socket.close()


        cprint(f"[*] {len(alive_sites)} alive sites found! ", color="green")
        cprint(f"[*] The sites are: ", color="green")
        for alive_site in alive_sites:
            cprint(alive_site, color="yellow")

        end_time = time.time()
        return alive_sites

    except Exception as e:
        cprint(f"[-] An unknown error occurred. Error: {e} "
               f"Contact jsuess@utsystem.edu for more", color='red')


# Placeholder for now.
def aggregate_results():
    try:
        subprocess.run(['python', 'app.py'])
        print('successful')
    except Exception as e:
        cprint(f"[-] An unknown error occurred. Error: {e} "
               f"Contact jsuess@utsystem.edu for more", color='red')


