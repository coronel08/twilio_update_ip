#!/path/to/your/venv/bin/python
import os
import requests
from twilio.rest import Client

# Followed instructions below
# https://www.twilio.com/blog/build-voip-system-twilio-3cx-python


# Might change to dotenv
ACCOUNT_SID = os.getenv('TWILIO_ACCOUNT_SID')
ACCOUNT_TOKEN = os.getenv('TWILIO_ACCOUNT_TOKEN')
ACL_NAME = os.getenv('TWILIO_ACL_NAME')


def get_current_ip():
    return requests.get('http://ifconfig.io/ip').text.strip()


def store_ip(ip):
    with open('/tmp/ip.txt', 'w+') as f:
        f.write(ip)


def get_stored_ip():
    try:
        return open('/tmp/ip.txt', 'r').read()
    except OSError:
        return None


def ip_needs_update():
    current_ip = get_current_ip()
    old_ip = get_stored_ip()

    if old_ip != current_ip:
        store_ip(current_ip)
        return True

def find_acl(client, name=ACL_NAME):
    for auth in client.sip.ip_access_control_lists.stream():
        if auth.friendly_name == name:
            return auth


def update_ip(auth):
    new_ip = get_stored_ip()
    ip = auth.ip_addresses.list()[0]
    ip.update(ip_address=new_ip)


def main():
    # Has the IP changed? If not, we do not need to do anything.
    if not ip_needs_update():
        return

    client = Client(ACCOUNT_SID, ACCOUNT_TOKEN)
    auth_acl = find_acl(client)
    update_ip(auth_acl)


if __name__ == '__main__':
    main()