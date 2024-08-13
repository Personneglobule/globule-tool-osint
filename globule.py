import os

try:
    import requests
    import platform
    import sys
    import webbrowser
    import time
    import random, base64, datetime
    from colorama import Fore, Style
    from googlesearch import search

except:
    os.system('pip install googlesearch-python requests platform webbrowser random pybase64 datetime colorama')

date = datetime.datetime.now()

def clear():
    os.system('cls' if os.name == 'nt' else 'clear')

def ret():
    input(color.WHITE + f'\n  {input_prompt}Press ENTER to return to the menu: ')
    main()

def error(text):
    print(color.WHITE + f'\n  {message}Unexpected error in Globule: ' + color.GREEN + str(text))
    input(color.WHITE + f'  {input_prompt}Press ENTER to return to the menu: ')
    main()

class color:
    BLUE = Fore.BLUE + Style.BRIGHT
    WHITE = Fore.WHITE + Style.BRIGHT
    RESET = Fore.RESET + Style.RESET_ALL
    GREEN = Fore.GREEN + Style.BRIGHT

input_prompt = f'{color.GREEN}[{color.WHITE}INPUT{color.GREEN}]{color.WHITE} - '
message = f'{color.GREEN}[{color.WHITE}MESSAGE{color.GREEN}]{color.WHITE} - '

def snus():
    title = r"""
  ███████╗███╗   ██╗██╗   ██╗███████╗██████╗  █████╗ ███████╗███████╗
  ██╔════╝████╗  ██║██║   ██║██╔════╝██╔══██╗██╔══██╗██╔════╝██╔════╝
  ███████╗██╔██╗ ██║██║   ██║███████╗██████╔╝███████║███████╗█████╗  
  ╚════██║██║╚██╗██║██║   ██║╚════██║██╔══██╗██╔══██║╚════██║██╔══╝  
  ███████║██║ ╚████║╚██████╔╝███████║██████╔╝██║  ██║███████║███████╗
  ╚══════╝╚═╝  ╚═══╝ ╚═════╝ ╚══════╝╚═════╝ ╚═╝  ╚═╝╚══════╝╚══════╝
    """
    options = '''
  [ 0 ] - [ Exit the program ]       [ 4 ] - [ Search with full name ]
  [ 1 ] - [ Back to the menu ]       [ 5 ] - [ Search with password ]
  [ 2 ] - [ Search with email ]      [ 6 ] - [ Search with password hash ]
  [ 3 ] - [ Search with NickName ]   [ 7 ] - [ Search with an IP address ]
'''

    SEARCH_TYPES = ["email", "username", "name", "password", "hash", "lastip"]

    def search(search_input, search_type):
        if not search_input:
            print(color.WHITE + f"\n {message}Please enter a search term")
            return

        key = 'c2J5anRoa29mdDR5YWltYndjanFwbXhzOGh1b3Zk'
        apiKey = base64.b64decode(key.encode('utf-8')).decode('utf-8')

        url = 'https://api-experimental.snusbase.com/data/search'
        headers = {
            'Auth': apiKey,
            'Content-Type': 'application/json'
        }
        payload = {
            'terms': [search_input],
            'types': [search_type],
            'wildcard': False
        }

        response = requests.post(url, json=payload, headers=headers)
        if response.status_code == 200:
            display_results(response.json().get('results', {}))
        else:
            error(response.text)

    def display_results(results):
        if not results:
            error('No results found in the database')
        else:
            for database, entries in results.items():
                for entry in entries:
                    for key, value in entry.items():
                        if key == 'lastip':
                            print(f"  {color.WHITE}{message}{key}: {value} (Get Location)")
                        else:
                            print(color.WHITE + f"  {message}{key} : {value}")
                    print('  ' + '-' * 50)

    def get_location(ip):
        url = f'http://ip-api.com/json/{ip}'
        response = requests.get(url)
        if response.status_code == 200:
            data = response.json()
            print(color.WHITE + f"  {message}Location for IP {color.GREEN}{ip}{color.WHITE}: {color.GREEN}{data['city']} : {data['region']} : {data['country']}{color.WHITE}")
        else:
            error(response.text)

    clear()
    print(color.GREEN + title)
    print(color.WHITE + options)
    
    print(color.GREEN + f'\n  ┌── <{system}@Globule> ─ [input]')
    try:
        search_type_choice = int(input(color.GREEN + '  └──╼ $ '))
    except ValueError:
        error('Invalid input')

    if search_type_choice == 0: 
        exit()
    elif search_type_choice == 1: 
        ret()
    else:
        try:
            search_type = SEARCH_TYPES[search_type_choice - 1]
        except IndexError:
            error('Invalid choice')

        search_input = input(color.WHITE + f"\n  {input_prompt}Enter the search term: ")

        search(search_input, search_type)

        while True:
            ip = input(color.WHITE + f"  {input_prompt}Enter IP to get location (or 'exit' to quit): ")
            if ip.lower() == 'exit':
                ret()
            else:
                get_location(ip)

def exit():
    clear()
    print(color.RESET)
    sys.exit()

def searcher():
    try:
        def fetch_top_search_results(query, num_results=10):
            search_results = []
            try:
                for result in search(query, num=num_results, pause=2.0):
                    search_results.append(result)
            except Exception as e:
                print(f"{color.GREEN}Error: {e}{color.RESET}")
            return search_results

        search_query = input(color.WHITE + f"\n  {input_prompt}Enter your search query: ")
        print('\n')
        top_results = fetch_top_search_results(search_query, num_results=10)

        if not top_results:
            error('No results found or an error occurred')
        else:
            print(color.WHITE + f"  {message}Search results: " + '\n')
            for idx, result in enumerate(top_results, 1):
                print(f"  {message}[{color.GREEN}{idx}{color.WHITE}] - {result}")

    except KeyboardInterrupt:
        error('Operation interrupted')

    except Exception as ex:
        error(ex)

    ret()

def db():
    try:
        path = input(f'\n  {input_prompt}Enter the path to the TXT DB file: ')
        string = input(f'  {input_prompt}Enter the string to search: ')

        print('\n')

        with open(path, 'r') as file:
            lines = file.readlines()
            found = False
            for i, line in enumerate(lines):
                if string in line:
                    print(f'  {message}String found in line {i + 1}: {line.strip()}')
                    found = True

            if not found:
                error('String not found in the database')

    except KeyboardInterrupt:
        error('Operation interrupted')

    except Exception as ex:
        error(ex)

    ret()

def darkgpt():
    try:
        print(color.WHITE + f'\n  {message}Paste the content of this page in your GPT')
        webbrowser.open('https://fr.anotepad.com/notes/phb33nb4')

    except KeyboardInterrupt:
        error('Operation interrupted')

    except Exception as ex:
        error(ex)

    ret()

def whois_lookup():
    try:
        domain = input(color.WHITE + f"\n  {input_prompt}Enter the domain for WHOIS lookup: ")
        url = f"https://www.whois.com/whois/{domain}"
        response = requests.get(url)
        if response.status_code == 200:
            print(color.WHITE + f"  {message}WHOIS Data for domain {color.GREEN}{domain}{color.WHITE}:")
            print(response.text)  # This might not be parsed; it outputs raw HTML
        else:
            error(response.text)

    except KeyboardInterrupt:
        error('Operation interrupted')

    except Exception as ex:
        error(ex)

    ret()

def reverse_dns_lookup():
    try:
        ip = input(color.WHITE + f"\n  {input_prompt}Enter the IP address for Reverse DNS lookup: ")
        url = f"https://dns.google/resolve?name={ip}&type=PTR"
        response = requests.get(url)
        if response.status_code == 200:
            data = response.json()
            if 'Answer' in data:
                for answer in data['Answer']:
                    print(color.WHITE + f"  {message}Reverse DNS for IP {color.GREEN}{ip}{color.WHITE}: {answer['data']}")
            else:
                print(color.WHITE + f"  {message}No Reverse DNS record found for IP {color.GREEN}{ip}{color.WHITE}")
        else:
            error(response.text)

    except KeyboardInterrupt:
        error('Operation interrupted')

    except Exception as ex:
        error(ex)

    ret()

def social_media_search():
    try:
        username = input(color.WHITE + f"\n  {input_prompt}Enter the username to search on social media: ")
        query = f"{username} site:facebook.com OR site:twitter.com OR site:instagram.com"
        print(color.WHITE + f"  {message}Searching for {color.GREEN}{username}{color.WHITE} on social media...")
        results = fetch_top_search_results(query, num_results=10)
        if not results:
            error('No social media profiles found or an error occurred')
        else:
            print(color.WHITE + f"  {message}Social Media Results: " + '\n')
            for idx, result in enumerate(results, 1):
                print(f"  {message}[{color.GREEN}{idx}{color.WHITE}] - {result}")

    except KeyboardInterrupt:
        error('Operation interrupted')

    except Exception as ex:
        error(ex)

    ret()

def domain_availability_check():
    try:
        domain = input(color.WHITE + f"\n  {input_prompt}Enter the domain to check availability: ")
        url = f"https://www.whois.com/whois/{domain}"
        response = requests.get(url)
        if response.status_code == 200:
            if 'No match for' in response.text:
                print(color.WHITE + f"  {message}Domain {color.GREEN}{domain}{color.WHITE} is available")
            else:
                print(color.WHITE + f"  {message}Domain {color.GREEN}{domain}{color.WHITE} is not available")
        else:
            error(response.text)

    except KeyboardInterrupt:
        error('Operation interrupted')

    except Exception as ex:
        error(ex)

    ret()

def main():
    clear()
    title = f'''
   ██████╗ ██╗      ██████╗ ██████╗ ██╗   ██╗██╗     ███████╗  [ Globule OSINT 
  ██╔════╝ ██║     ██╔═══██╗██╔══██╗██║   ██║██║     ██╔════╝  MultTool ]
  ██║  ███╗██║     ██║   ██║██████╔╝██║   ██║██║     █████╗    --------------------
  ██║   ██║██║     ██║   ██║██╔══██╗██║   ██║██║     ██╔══╝    System: {color.WHITE}{system}{color.GREEN}
  ╚██████╔╝███████╗╚██████╔╝██████╔╝╚██████╔╝███████╗███████╗  Architecture: {color.WHITE}{arch}{color.GREEN}
   ╚═════╝ ╚══════╝ ╚═════╝ ╚═════╝  ╚═════╝ ╚══════╝╚══════╝
'''
    print(color.GREEN + title)
    options = '''
  [ 00 ] - [ Exit the program ]               [ 05 ] - [ WHOIS lookup ]         
  [ 01 ] - [ Full research in SnusBase ]      [ 06 ] - [ Reverse DNS lookup ] 
  [ 02 ] - [ Search a string on the web ]     [ 07 ] - [ Social Media search ]
  [ 03 ] - [ Search in .txt DB ]              [ 08 ] - [ Domain availability check ]
  [ 04 ] - [ Get the DarkGPT payload ]          
'''
    print(color.WHITE + options)

    print(color.GREEN + f'\n  ┌── <{system}@Globule> ─ [input]')
    choice = input(color.GREEN + '  └──╼ $ ')

    if choice == '00': 
        exit()
    elif choice == '01': 
        snus()
    elif choice == '02':
        searcher()
    elif choice == '03':
        db()
    elif choice == '04':
        darkgpt()
    elif choice == '05':
        whois_lookup()
    elif choice == '06':
        reverse_dns_lookup()
    elif choice == '07':
        social_media_search()
    elif choice == '08':
        domain_availability_check()
    else: 
        error(f'Invalid choice: {choice}')

if __name__ == "__main__":
    system = platform.system()
    arch = platform.architecture()[0]
    main()
