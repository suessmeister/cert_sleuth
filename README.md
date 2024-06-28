cert_sleuth offers an alternative to traditional reconnassiance. 

it relies on the the crt.sh website, parses the json results, then returns a comprehensive list of all names associated with the entered domain. 

the user is then prompted to select ports of which to perform reconnassiance on. these will typically 80 or 443 (http/https servers) though the option to include others is there. 

socket connections are established to find which servers are running said services.

final GUI is displayed on a static HTTP server developed with flask, with clickable links for each of the alive sites.

hope this tools helps your efforts, both offensive and defensive. i do not assume any responsibility from misuse of the program. god bless! 

flags -->  

**-d** : specifiy the domain name to look at. (REQUIRED)  
**-s**: specifiy the speed of the scan. more common than not, you should set this value to 1, but the option to increase the depth is there. try not to exceed 4. (REQUIRED)  
**-v**: verbose output on the scans. (OPTIONAL)  
