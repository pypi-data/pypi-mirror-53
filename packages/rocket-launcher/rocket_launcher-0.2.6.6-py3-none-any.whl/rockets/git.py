def git():
    os.system('sudo -H -u who configure-version-controller >/dev/null 2>&1')
    os.system('configure-version-controller >/dev/null 2>&1')
