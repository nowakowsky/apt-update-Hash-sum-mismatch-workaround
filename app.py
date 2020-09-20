import subprocess
import fileinput
import sys

def swap_hashes(apt_output: str):
    try:
        #Expected file sha256
        expected_sha256_start = apt_output.index("SHA256") + 7
        expected_sha256_end = expected_sha256_start + apt_output[expected_sha256_start:].index("SHA1") - 2
        expected_sha256 = apt_output[expected_sha256_start:expected_sha256_end].replace(' ','').replace('\n','')
    except ValueError:
        #try - expect block checks if apt has been fixed in previous loop
        print ("Completed!")
        sys.exit(0)

    #Expected file sha1
    expected_sha1_start = apt_output.index("SHA1") + 5
    expected_sha1_end = expected_sha1_start + apt_output[expected_sha1_start:].index("[") - 1
    expected_sha1 = apt_output[expected_sha1_start:expected_sha1_end]

    #Expected file md5
    expected_md5_start = apt_output.index("MD5Sum") + 7
    expected_md5_end = expected_md5_start + apt_output[expected_md5_start:].index("[") - 1
    expected_md5 = apt_output[expected_md5_start:expected_md5_end]

    #Remove expected data from output
    apt_output = apt_output[expected_md5_end:]

    #Recived file sha256
    recived_sha256_start = apt_output.index("SHA256") + 7
    recived_sha256_end = recived_sha256_start + apt_output[recived_sha256_start:].index("SHA1") - 2
    recived_sha256 = apt_output[recived_sha256_start:recived_sha256_end].replace(' ','').replace('\n','')

    #Recived file sha1
    recived_sha1_start = apt_output.index("SHA1") + 5
    recived_sha1_end = recived_sha1_start + apt_output[recived_sha1_start:].index("[") - 1
    recived_sha1 = apt_output[recived_sha1_start:recived_sha1_end]

    #Recived file md5
    recived_md5_start = apt_output.index("MD5Sum") + 7
    recived_md5_end = recived_md5_start + apt_output[recived_md5_start:].index("[") - 1
    recived_md5 = apt_output[recived_md5_start:recived_md5_end]

    #Grep to look for broken file
    grep = subprocess.Popen([f'grep -i {expected_sha256} *'], stdout=subprocess.PIPE, shell=True)
    grep_output = grep.communicate()[0].decode("utf8")
    broken_file = grep_output[:grep_output.index(":")]
    
    #Inplace file editing
    with fileinput.FileInput(broken_file, inplace=True, backup='.bak') as file:
        for line in file:
            print(line.replace(expected_md5, recived_md5), end='')
            print(line.replace(expected_sha1, recived_sha1), end='')
            print(line.replace(expected_sha256, recived_sha256), end='')

def app():
    #Call apt update and get output
    apt = subprocess.Popen(["apt", "update"], stderr=subprocess.PIPE, stdout=subprocess.DEVNULL)
    print ("Running apt update...")
    apt_output = apt.communicate()[1].decode("utf8")
    print ("Swapping broken hashes..")
    swap_hashes(apt_output)

if __name__ == "__main__":
    while True:
        app()
