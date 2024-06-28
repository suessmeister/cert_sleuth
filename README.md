A practice often forgotten by penetration testers and ethical hackers alike is the use of website certificates as a tool of reconnassiance. SSL and TLS certificates are public information and organizations almost always have a plethora of these registered under their common domain name. This opens up the doors for many reconnassiance possibilities and endpoints that might have been missed!  

This is where cert sleuth comes in. With it comes a comprehensive tool that will immidiately give both users and organizations **instantaneous reconnassiance** on domains and ports of their choosing. In just 5 minutes, you will know which sites are running and which can provide an entryway to further exploitation.   

It relies on the the crt.sh website, parses the json results, then returns a comprehensive list of all names associated with the entered domain. 

The user is then prompted to select ports of which to perform reconnassiance on. These will typically be 80 or 443 (http/https servers) though the option to include whichever ports necessary are there.   

Socket connections are established to find which servers are running said services.  

Final GUI is displayed on a static HTTP server developed with flask, with clickable links for each of the alive sites.  

Hope this tools helps your efforts, both offensive and defensive. I do not assume any responsibility from misuse of the program. 
May God bless you!  

flags -->  

**-d** : specifiy the domain name to look at. (REQUIRED)  
**-s**: specifiy the speed of the scan. more common than not, you should set this value to 1, but the option to increase the depth is there. try not to exceed 4. (REQUIRED)  
**-v**: verbose output on the scans. (OPTIONAL)  
