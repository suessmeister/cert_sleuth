# Cert Sleuth: Instant Reconnaissance with SSL/TLS Certificates

Cert Sleuth is a powerful tool designed to leverage SSL/TLS certificates for comprehensive reconnaissance of domains and ports within minutes. It utilizes publicly available certificate information from crt.sh, providing users and organizations with valuable insights into their digital footprint.

## Key Features

- **Certificate Parsing**: Cert Sleuth fetches and parses JSON results from crt.sh to compile a comprehensive list of all names associated with the specified domain.
  
- **Port Selection**: Users can select specific ports (e.g., 80, 443) for reconnaissance. This helps identify active HTTP and HTTPS servers, among others.

- **Socket Connections**: Establishes socket connections to determine which servers are running on the selected ports, facilitating quick identification of potential entry points for further exploitation.

- **Interactive GUI**: Displays results on a static HTTP server developed with Flask, featuring clickable links for each live site discovered during the scan.

## Flags

To use Cert Sleuth effectively, use the following command line flags:

- **-d**: Specify the domain name to analyze _(REQUIRED)._
- **-s**: Set the speed of the scan (1-4, higher values for deeper scans) _(REQUIRED)._
- **-v**: Enable verbose output for detailed scan information _(OPTIONAL)._

## Disclaimer

Cert Sleuth is intended for ethical purposes only, aimed at improving both offensive and defensive security efforts. Misuse of this tool is not condoned, and the developer assumes no responsibility for any unauthorized or malicious use.

## Installation and Dependencies

Cert Sleuth runs with cert_sleuth.py. Once the tool is installed, attach necessary flags here. 
Requirements:

Python version 3.7+  
Flask


