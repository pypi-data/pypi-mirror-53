import webbrowser

files = []
class NewPage:
    def __init__(self, name):
        self.name = name
        self.file = name+'.html'
        open(self.file, 'w+').close()

    def createindex(bc='white'):
        f = open('index.html', 'w+')
        files.append('index')
        f.write("<body style='background-color: %s;'>" % bc)
        f.close()

    def pic(self, path):
        f = open(self.file, 'a+')
        f.write("<img src='%s'>" %path)
        f.close()


    def title(self, text):
        f=open(file+'.html', 'a+')
        if file=='all':
            for item in files:
                f=open(self.file, 'a+')
                f.write('<title>%s</title>'% text)
                f.close()
        else:
            f = open(file+'.html', 'a')
            f.write('<title>%s</title>'% text)
            f.close()

    def customSearch(self, websiteToSearch, text='Search'):
        f = open(self.file, 'a+')
        f.write("""\n <iframe src=https://duckduckgo.com/search.html?site='"""+websiteToSearch+"""'&prefill="""+text+""" style="overflow:hidden;margin:0;padding:0;width:408px;height:40px;" frameborder="0"></iframe> \n""")
        f=open(file+'.html', 'a+')
        f.close()
    def createpage(file, bc='white'):
        f = open(file+'.html', 'w+')
        files.append(file)
        f.write("<body style='background-color: %s;'>" % bc)
        f.close()

    def header(self, text, centered=False):
            f=open(self.file, 'a+')
            if centered==True:
                f.write('<h1 style="text-align: center;">'+text+'</h1>')
            elif centered==False:
                f.write('<h1>'+text+'</h1>')
            f.close()

    def text(self, text, centered=False):
            f=open(self.file, 'a+')
            if centered==False:
                f.write('<p>'+text+'</p>')
            elif centered==True:
                f.write('<p  style="text-align: center;">'+text+'</p>')
            f.close()

    def link(self, page, text, style='text', centered=False):
        f=open(self.file, 'a+')
        if style=='text':
            if centered==True:
                f.write('<a href='+page+'.html>'+text+'</h1>')
            else:
                f.write('<a href='+page+'.html>'+text+'</h1>')
        elif style=='button':
            if centered==True:
                f.write("""
            <form>
            <input style='text-align: center;' type="button" value="""+text+""" onclick="window.location.href='"""+page+"""'" />
            </form>
                    """)
            else:
                f.write("""
        <form>
        <input type="button" value="""+text+""" onclick="window.location.href='"""+page+"""'" />
        </form>
                """)
            f.close()

    def search(self, centered=False):
        f=open(self.file, 'a+')
        if centered==True:
            f.write("""
            <div id='a' style='text-align:center;'>
            <input type='text' id='link_id'>
            <input type='button' id='link' value='Search' onClick='javascript:goTo()'>
            </div>
            <script>
            function goTo()
            {
                input = document.getElementById('link_id').value;
                location.href = 'https://www.google.com/search?safe=active&source=hp&ei=qBgiXYDCFtDVtAay2ovIAg&q='+input+'&oq='+input+'p&gs_l=psy-ab.3..0l10.4800.5462..5922...0.0..1.236.818.5j2j1......0....1..gws-wiz.....0..0i131j0i3.wh3C02wdyCM&safe=active'
            }
            </script>
                """)
        else:
            f.write("""
        <input type='text' id='link_id'>
        <input type='button' id='link' value='Search' onClick='javascript:goTo()'>
        <script>
        function goTo()
        {
            input = document.getElementById('link_id').value;
            location.href = 'https://www.google.com/search?safe=active&source=hp&ei=qBgiXYDCFtDVtAay2ovIAg&q='+input+'&oq='+input+'p&gs_l=psy-ab.3..0l10.4800.5462..5922...0.0..1.236.818.5j2j1......0....1..gws-wiz.....0..0i131j0i3.wh3C02wdyCM&safe=active'
        }
        </script>
            """)
        f.close()

    def piclink(self, page, path):
        f = open(file+'.html', 'a+')
        f.write("""
        <a href='"""+self.name+""".html'>
        <img src='"""+path+"""'>
        </a>
            """)
        f.close()

    def start(self):
        webbrowser.open_new(self.file)
