import subprocess

def get_maven_version():
    version = subprocess.check_output([
        "mvn", "-q", "-Dexec.executable=echo", "-Dexec.args='${project.version}'", "-f", "../../..", "exec:exec"
    ]).strip()
    return version.decode().replace("-", "+").lower()
