import requests
import json
import sys
import dns.resolver


def request(url):
    try:
        resp = requests.get(url)
        if resp.status_code == 200:
            return resp
    except Exception as e:
        print(e)


def parsing(resp_text):
    try:
        return json.loads(resp_text.text)
    except Exception as e:
        print(e)


if __name__ == "__main__":
    if len(sys.argv) == 1:
        print("Usage: python subcertsearch.py [domain]")

    try:
        s = "estr3llas"
        domain = sys.argv[1]
        print("[+]Searching for subdomains in {}...".format(str(domain)))
        print("[+]Resolving DNS Records...")

        URL = "https://crt.sh/?q=" + str(domain) + "&output=json"
        req = request(URL)
        parsed_req = parsing(req)
        resolver = dns.resolver.Resolver()

        if parsed_req:
            for i in range(len(parsed_req)):
                common = parsed_req[i]['common_name']
                common_ip = resolver.resolve(common, "A")
                match = parsed_req[i]['name_value']
                match_ip = resolver.resolve(match, "A")
                print("Common Name:")
                print("{}\n".format(common_ip.rrset))
                print("Matching Identities:")
                print("{}".format(match_ip.rrset))
                print("-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-")
        else:
            print("It was not possible to search for certificates.")
    except:
        print("An unexpected error has occurred. Please restart the program.")


