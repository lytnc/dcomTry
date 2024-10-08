import subprocess
import argparse

def read_file(file_path):
    """Reads a file and returns a list of lines."""
    with open(file_path, 'r') as f:
        return [line.strip() for line in f if line.strip()]

def run_dcomexec(ip, user_pass, object_name):
    """Executes dcomexec.py with the given parameters."""
    command = f"dcomexec.py -object {object_name} '{user_pass}@{ip}'" # You might need to change this according to your dcomexec bin.
    try:
        process = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)

        # Timeout is a dirty way to see for success
        stdout, stderr = process.communicate(timeout=2)  # Use a timeout to avoid hanging, since you catch a reverse shell. might need to increase for no false-positive!

        # Analyze the output for known error messages
        if 'denied' in stdout.lower() or \
           'failure' in stdout.lower() or \
           'sessionerror' in stdout.lower():
            #print(f"No rights with: {command}")
            return False
        
        # You shouldnt get this
        else:
            print(f"Unknown Result: {command} - {stdout.strip()}")
        
        return False
            
    except subprocess.TimeoutExpired:
        #Timeout indicates it could have been succesfull
        print(f"Process timed out: {command}. It might be SUCCESS.")
        return True
    except Exception as e:
        print(f"Error executing command {command}: {e}")
        return False

def main(ip_file, user_pass_file):
    """Main function to coordinate the execution of DCOM commands."""
    ips = read_file(ip_file)
    user_passes = read_file(user_pass_file)
    objects = ['MMC20', 'ShellBrowserWindow', 'ShellWindows']

    # Loop through all combinations of IPs, user:pass, and objects
    print("Starting...")
    for ip in ips:
        for user_pass in user_passes:
            for obj in objects:
                run_dcomexec(ip, user_pass, obj)
    print("finished")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="DCOM Check Tool")
    parser.add_argument('-i', '--ipfile', type=str, required=True,
                        help='Path to the file containing IP addresses (one per line).')
    parser.add_argument('-u', '--userpassfile', type=str, required=True,
                        help='Path to the file containing USER:PASS combinations (one per line).')
    
    args = parser.parse_args()

    main(args.ipfile, args.userpassfile)
