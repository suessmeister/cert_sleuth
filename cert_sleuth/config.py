import argparse


# This is put into config.py in order for both driver and methods can be able to access it.

# We must keep track of the arguments the user provides! This is imperative.

# Original Method from CertSPY. No modifications needed. Credit to Dru Banks.
# Forces the user to give a domain in their argument.
def get_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('-d', '--domain', required=True, help='Website to enumerate')
    parser.add_argument('-s', '--speed', required=True, help='Speed of scans(quick=1, '
                                                  'slow=4. not recommend to go past 4.)')
    parser.add_argument('-v', '--verbose', action='store_true', required=False, help='Verbose output on dead/alive websites')
    arguments = parser.parse_args()
    return arguments

args = get_args()