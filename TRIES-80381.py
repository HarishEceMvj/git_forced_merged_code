import paramiko

print(" 1.Pre-requests for execution of commands required 'git cli' tool to be installed on your machine \
        2. git repository to be cloned to host, where force merge going to check")

host_ip = input("enter the host_ip\n")
host_username = input("enter the username\n")
host_password = input("enter the password\n")

git_cloned_directory = input("provide git cloned repository path Example. '/home/cyc/cyclone'")
# with open("output_file_read.txt", "w+") as f:
ssh1 = paramiko.SSHClient()
ssh1.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh1.connect(hostname=host_ip, port=22, username=host_username, password=host_password)

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

