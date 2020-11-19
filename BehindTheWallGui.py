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
#written by kbturk @ 11/17/2020

import requests, sys, tkinter as tk, os
from bs4 import BeautifulSoup

back_ground = "#fae28c"
button_color = "#f6f6f6"
title_color = "#d8e3eb"

class Application(tk.Frame):
    def __init__ (self, master = None):
        super().__init__(master)
        self.master = master
        self.grid(column = 0, row = 0, sticky = (tk.N, tk.W, tk.E, tk.S ) )
        self.config( bg = back_ground, bd = 15 )
        self.create_widgets()

    def create_widgets(self):

        self.URL = tk.StringVar()
        tk.Label(self, text = "URL", bg = back_ground ).grid( column = 1, row = 1, sticky = tk.E )

        self.url_get = tk.Entry( self, textvariable = self.URL )
        self.url_get.grid(column = 2, columnspan = 3, row = 1,  sticky = ( tk.W, tk.E ) )

        self.search_obj = tk.StringVar()
        tk.Label(self, text = "html tag search:", bg = back_ground ).grid( column = 1, row = 2, sticky = tk.E )

        self.search_term = tk.Entry(self, textvariable = self.search_obj )
        self.search_term.grid(column = 2, columnspan = 3, row = 2, sticky = ( tk.W, tk.E ) )

        tk.Label(self, text = "search by:", bg = back_ground ).grid( column = 1, row = 3, sticky = tk.E )

        self.select = tk.StringVar()
        self.select.set('All')
        self.search_selector1 = tk.Radiobutton(self, text='All', variable = self.select, value = 'All', bg = back_ground )
        self.search_selector1.grid(column = 2, row = 3, sticky = ( tk.W, tk.E ) )

        self.search_selector2 = tk.Radiobutton(self, text='ID tags only', variable = self.select, value = 'ID', bg = back_ground )
        self.search_selector2.grid(column = 3, row = 3, sticky = ( tk.W, tk.E ) )

        self.search_selector3 = tk.Radiobutton(self, text='Class tags only', variable = self.select, value = 'Class', bg = back_ground )
        self.search_selector3.grid(column = 4, row = 3, sticky = ( tk.W, tk.E ) )

        self.run_button = tk.Button( self, text = "🏃‍ Run", command = self.run_program, bg = button_color )
        self.run_button.grid(column = 2, row = 4, sticky = ( tk.W, tk.E ) )
        
        self.view_results_button = tk.Button(self, text = "View Results", command = self.create_results, bg = button_color )
        self.view_results_button.grid(column = 3, row = 4, sticky = ( tk.W, tk.E ) )

        self.quit = tk.Button(self, text = "Quit", fg = "red", command = self.master.destroy, bg = button_color )
        self.quit.grid(column = 4, row = 4, sticky = ( tk.W, tk.E ) )

        self.bottom_message = tk.StringVar()
        self.bottom_message.set("Welcome")
        self.message = tk.Label(self, textvariable = self.bottom_message, bg = back_ground ).grid(column = 2, row = 5, columnspan=4, sticky = (tk.E, tk.W ) )

        for child in self.winfo_children(): 
            child.grid_configure( padx = 5, pady = 5 )
            
    def run_program(self):
        try:
            result = scraper(self.URL.get(), self.search_obj.get(), self.select.get())
            if result:
                self.bottom_message.set("site scraping is complete. To view results, please open website.txt.")
            else:
                self.bottom_message.set("No results found on website. Please try again. If this error continues, try 'body' in search for full dump.")

        except ValueError:
            self.bottom_message.set("Hmm, something went wrong. Check that URL & Search term was supplied.")
        
    def create_results(self):
        self.bottom_message.set("Opening website.txt!")
        if os.path.exists("website.txt"):
            try:
                os.startfile("website.txt")
            except ValueError:
                print(file=sys.stderr)

        else:
            self.bottom_message.set("website.txt file not created yet.")

def scraper(URL, search, select):
    print(f"hello!\nThe URL scraped is: { URL }\n The search term is: { search }\nSearch by { select }" )

    #Let's do a little web scraping. returns a urllib3.response.HTTPResponse object.
    r = requests.get( URL, stream=True )
    r.encoding = 'utf-8'

    if len(r.text) == 0:
        print( 'had issue with requests.get scraper.' )

    #Translate that shit to beautiful soup.
    soup = BeautifulSoup( r.text, 'html.parser' )

    #find the content you're looking for:

    if select == 'ID':
        entries = soup.find_all( id = search )
    elif select == 'Class':
        entries = soup.find_all( class_ = search )
    else:
        entries = soup.find_all( search )

    if len(entries) == 0:
        print(f'no entries found. {entries}')
        return False
        
    content = []

    for entry in entries:
        i = 0
        try:
            for text in entry.stripped_strings:
                if i % 15 == 0:
                    content.append("\n\n")
                content.append(f" {text}")
                #content.append(entry.get_text('|', strip=False))
                i = i + 1

        except ValueError:
            print('issues scraping text.')
            print( entry, file=sys.stderr )
            return False

    content = ''.join(content)

    with open('website.txt', 'w', encoding = 'utf8') as f:
        f.write(content)

    print('''site scraping is complete. To view results, please open website.txt
    I recommend using the following command from the command line: fold -s website.txt to view in terminal.''')

    return True

def main(argv):
    #tinkter built window:
    root = tk.Tk()
    root.title( "Behind the Wall - a website content scraper" )
    root.columnconfigure( 0, weight = 1 )
    root.rowconfigure( 0, weight =1 )
    app = Application(master=root)
    app.mainloop()

if __name__ == '__main__':
    sys.exit(main(sys.argv))