import subprocess

# call upon a powershell command
def create_scheduled_task(executable_path, arguments, task_name, username, time):
    ps_command = f'trypy -Path "{executable_path}" -Args "{arguments}" -Name "{task_name}" -User "{username}" -Time "{time}"'
    
    subprocess.run(["powershell", "-Command", ps_command], capture_output=True)

# Example usage
if __name__ == "__main__":
    create_scheduled_task(
        executable_path="path to the python interpreter",
        arguments="'The path of the notificationscript' 'this is the message to show'",
        task_name="task name",
        username="username",
        time="target time"
    )

# import subprocess
#
# ps_script = """
# $global:myVar = 'Hello from Python'
# Write-Output $global:myVar
# """
#
# process = subprocess.Popen(["powershell", "-Command", ps_script], stdout=subprocess.PIPE, text=True)
# output, _ = process.communicate()
#
# print(f"PowerShell Global Variable: {output.strip()}")
