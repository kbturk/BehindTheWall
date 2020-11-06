'''MIT License

Copyright (c) 2020 Katherine Turk

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
'''
#written by kbturk @ 11/5/2020

import requests, sys
from bs4 import BeautifulSoup

def error_log(s):
    print(s, file=sys.stderr)

def parse_bool(x: str):
    x = x.lower()
    if x == 'true':
        return True
    elif x == 'false':
        return False
    raise ValueError(f'not a bool: {x}')

def main(argv):

    if len(argv) > 4:
        try:
            URL, search, class_, id_ = argv[1], argv[2], parse_bool(argv[3]), parse_bool(argv[4])

        except ValueError:
            print( 'issues parsing command line inputs.\n' )
            
    elif len(argv) == 3:
    
        try:
            URL, search = argv[1].strip(),argv[2].strip()
        except ValueError:
            print( 'issues parsing command line inputs.\n' )

        class_, id_ = False, False
    else: 
        print(f'\n\nThe following arguments were provided:\n {argv}')
        print('''please provide one of the following combinations of arguments:
        short search: {URL} {html tag search term - usually "body"}
        deep search: {URL} {search - item inside of first search tag term} {class_: True or False} {id: True or False}
        ''')

        return

        #Troubleshooting defaults:
        '''
        URL = 'https://realpython.com/python-or-operator/'
        search = 'boolean-logic'
        class_ = False
        id_ = True
        '''

    print(f'URL: {URL}\nsearch: {search}\nclass_: {class_}\nid_:{id_}')


    #Let's do a little web scraping. returns a urllib3.response.HTTPResponse object.
    r = requests.get(URL, stream=True)
    r.encoding = 'utf-8'

    if len(r.text) == 0:
        print('had issue with requests.get scraper.')

    #Translate that shit to beautiful soup.
    soup = BeautifulSoup(r.text, 'html.parser')

    #find the content you're looking for:
    if class_ or id_ :

        if id_:
            entries = soup.find_all( id = search )

        else:
            entries = soup.find_all( class_ = search )

    else:
        entries = soup.find_all( search )

    if len(entries) == 0:
        print(f'no entries found. {entries}')
        return
        
    content = []

    for entry in entries:
            try:
                content.append(entry.get_text().strip('   \n'))
            except ValueError:
                print('issues scraping text.')
                error_log(entry)

    content = ''.join(content)

    with open('website.txt', 'w', encoding = 'utf8') as f:
        f.write(content)
    print('''site scraping is complete. To view results, please open website.txt. 
    We recommend using the following command from the command line: fold -s website.txt to view in terminal.''')

if __name__ == '__main__':
    sys.exit(main(sys.argv))