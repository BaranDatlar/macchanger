import subprocess, random, optparse, re


def arguments():
    parse_obj = optparse.OptionParser()
    parse_obj.add_option("-i", "--interface", dest="interface", help="input interface")
    parse_obj.add_option("-o", "--option", dest="tool_option")
    return parse_obj.parse_args()


(user_inputs, arguments) = arguments()


def macchanger(user_interface, user_mac):
    subprocess.call(["ifconfig", user_interface, "down"])
    subprocess.call(["ifconfig", user_interface, "hw", "ether", user_mac])
    subprocess.call(["ifconfig", user_interface, "up"])


def find_mac(interface):
    ifconfig = subprocess.check_output(["ifconfig", interface])
    new_mac = re.search(r"\w\w:\w\w:\w\w:\w\w:\w\w:\w\w", str(ifconfig))

    if new_mac:
        return new_mac.group(0)


def random_mac_creator():
    numlist = ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9"]
    doubleNumList = ["00", "11", "22", "44", "88", "99"]
    letterlist = ["a", "b", "c", "d", "e", "f"]
    randomMac = []
    for i in range(6):
        k = random.randint(0, 1)
        if k == 0:
            randomMac.append(random.choice(numlist) + random.choice(letterlist))
        else:
            randomMac.append(random.choice(doubleNumList))
        if i < 5:
            randomMac.append(":")

    finalmac = ""
    for elements in randomMac:
        finalmac += elements
    return finalmac


randommac = random_mac_creator()


def help_menu():
    print("""
                                HELP MENU
    --------------------------------------------------------------------------
    Usage: python3 mac_changer.py -i <iface> -o <option(1,2,3)>
    Ex: python3 mac_changer.py -i wlan0 -o 2

    -i    --interface       Enter a interface
    -o    --tool_option     Enter a option, options = 1,2,3 

    -o 1  --> restore mac manually
    -o 2  --> random mac
    -o 3  --> help menu

    ---------------------------------------------------------------------------
    """)


if (user_inputs.tool_option == "3"):
    help_menu()

if (user_inputs.tool_option == "2"):
    old_mac = find_mac(user_inputs.interface)
    macchanger(user_inputs.interface, randommac)
    new_mac = find_mac(user_inputs.interface)
    if (new_mac != old_mac):
        print(f"\nYour mac address successfully changed \n{old_mac} to {new_mac}")

if (user_inputs.tool_option == "1"):
    print("Please enter own mac adress, it should be match mac address rules")
    old_mac = find_mac(user_inputs.interface)
    macchanger(user_inputs.interface, str(input()))
    new_mac = find_mac(user_inputs.interface)
    if (new_mac != old_mac):
        print(f"\nYour mac address successfully changed \n{old_mac} to {new_mac}")

if (user_inputs.tool_option and user_inputs.interface) == None:
    help_menu()


