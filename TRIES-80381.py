import paramiko
import argparse
import time

print(" 1.Pre-requests for execution of commands required 'git cli' tool to be installed on your machine \
        2. git repository to be cloned to host, where force merge going to check")

parser = argparse.ArgumentParser()
parser.add_argument("Host_IP", type=str, default="10.207.146.173", help="Specify Host_IP")
parser.add_argument("Host_User_Name", type=str, default="cyc", help="Provide Host Username")
parser.add_argument("Host_User_Password", type=str, default="cycpass", help="Provide Host Password")
parser.add_argument("full_Git_hub_repository_Name", type=str, default="Matrix/Matrix_Tools", help="Provide git repo "
                                                                                                  "tobe cloned to "
                                                                                                  "check forced merge")

'''execute locally un-uncomment below lines'''
# host_ip = input("enter the host_ip\n")
# host_username = input("enter the username\n")
# host_password = input("enter the password\n")
# repo_tobe_cloned = input("provide git cloned repository path Example. '/home/cyc/cyclone'")


# Parse the arguments to local variable from CLI
args = parser.parse_args()
host_ip = args.Host_IP
host_username = args.Host_User_Name
host_password = args.Host_User_Password
repo_tobe_cloned = args.full_Git_hub_repository_Name

# get the cloned repo
git_cloned_directory = "/home/cyc/" + repo_tobe_cloned.split("/")[1]
print(git_cloned_directory)
# Create a SSH object
ssh1 = paramiko.SSHClient()
ssh1.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh1.connect(hostname=host_ip, port=22, username=host_username, password=host_password)

# clone the repository
command_to_clone_repo = "gh repo clone eos2git.cec.lab.emc.com/" + repo_tobe_cloned
print(command_to_clone_repo)
# cloning the repository
stdin, stdout, stderr = ssh1.exec_command(command_to_clone_repo)
print(stdout.readlines(), stderr.readlines())

# Lists all merged PRs number
git_cmd = 'gh pr list --state merged' + ' | awk ' + """'{ printf "%6s\\n", $1}'"""
# print(git_cmd)
cmd = f"cd {git_cloned_directory} && {git_cmd}"
# print(cmd)

# Add all PRs to a list
Pr_recovered = []  # added one PR to a list, which was forced merged for testing purpose
stdin, stdout, stderr = ssh1.exec_command(cmd)

# appending all PRs to list
for line in stdout.readlines():
    Pr_recovered.append(line.strip())
print("listed PRs are: ", Pr_recovered)
for pr in Pr_recovered:
    git_pr_view_cmd = f'cd {git_cloned_directory} && gh pr view {pr} --comments | grep -i "force merge me please"'
    # print(git_pr_view_cmd)
    stdin, stdout, stderr = ssh1.exec_command(git_pr_view_cmd)
    for comment_line in stdout.readlines():
        if comment_line.strip() == "force merge me please":
            print(f"this pr {pr} is force merged!")

ssh1.close()

