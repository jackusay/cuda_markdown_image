#md img preview
import os
import re
from cudatext import *
from .img_size import get_image_size
#from cudax_lib import get_translation

from urllib.parse import urlparse #check if Online URL

from cudax_lib import get_translation
_ = get_translation(__file__)  # I18N

#PIC_TAG = 0x1000 #minimal tag for api (CRC adds to tag)
BIG_SIZE = 500 #if width bigger, ask to resize
#DIALOG_FILTER = 'Pictures|*.png;*.jpg;*.jpeg;*.jpe;*.gif;*.bmp;*.ico'
PRE = '[Markdown Image] '
MIN_H = 10 #limitations of api to gap height
MAX_H = 500-5

data_all = {}
id_img = image_proc(0, IMAGE_CREATE)

def log(s):
    #print(s)
    pass
    
def get_url(txt):
    """input line_text, return url"""
    #url can't mix with ), otherwise it become unsure ) is url or part of image syntax.
    x = re.findall("!\[[^\]]+\]\([^\)]+\)", txt) 
        #get image syntax ex: ![Stormtroopocat](https://octodex.github.com/images/stormtroopocat.jpg "The Stormtroopocat")
    log(f"image syntax: {x}")
    if not x:
        log("Can't find image syntax.")
        return
    #q = re.search("!\[[^\]]+\]", x[0]) #get title ex: ![sdff]
    #log(q.group()[2:-1])
    p = re.search("\([^\)]+", x[0]) #get (... part ex: (https://octodex.github.com/images/stormtroopocat.jpg "The Stormtroopocat"
    pp = p.group()[1:] #strip prefix (
    url = pp.split("\"")[0].strip() #get url
    log(f"url: {url}")  
    return url

class Command:
    
    def __init__(self):

        pass

    def config(self):

        pass
        
    def on_change_slow(self, ed_self):
        carets = ed_self.get_carets()
        x1, nline, x2, y2 = carets[0]
        txt = ed_self.get_text_line(nline)
        self.insert_file(ed_self, txt, nline)

    def on_open(self, ed_self):
        #fn_ed = ed_self.get_filename()
        #if not fn_ed: return #unsaved file???
        
        for index in range(ed_self.get_line_count()):
            line = ed_self.get_text_line(index)
            self.insert_file(ed_self, line, index)


    def on_lexer(self, ed_self):
        for index in range(ed_self.get_line_count()):
            line = ed_self.get_text_line(index)
            self.insert_file(ed_self, line, index)


    def insert_file(self, ed_self, txt, nline):
        url = get_url(txt)
        if not url:
            return
        
        #if online URL, return
        if urlparse(url).scheme in ('http', 'https'):
            return
        
        #strip file:/// leading
        file_scheme_leading = re.findall("file:///", url)
        if file_scheme_leading:
            url = url[8:]
            log(f"url: {url}")
          
        log(f"absolute path?: {os.path.isabs(url)}")
        #                                           os.path.isabs()    urlparse(url).scheme in ('file')
        # file://C:\Windows\System32\Security.png   False              True
        # file:///C:\Windows\System32\Security.png  False              True
        #                                    0.jpg  False              True
        if os.path.isabs(url):
            fn = url            
        else:
            filepath = ed_self.get_filename()
            fn = os.path.join(os.path.dirname(filepath), url)

            
        if not os.path.isfile(fn):
            ed_self.gap(GAP_DELETE, nline, nline)
            msg_status(PRE + _('Cannot find picture'))
            return
        
        ntag = 2 #for delete
        
        res = get_image_size(fn)
        if not res:
            msg_status(PRE + _('Cannot detect picture sizes'))
            return
        size_x, size_y = res
        
        #reduce size and keep aspect ratio
        if size_x > BIG_SIZE or size_y > BIG_SIZE:
            if size_x >= size_y:
                # y / x = ? / max
                # ? = y / x * max
                size_y = round(size_y / size_x * BIG_SIZE)
                size_x = BIG_SIZE
            else:
                size_x = round(size_x / size_y * BIG_SIZE)
                size_y = BIG_SIZE       
        if size_y < MIN_H:
            size_y = MIN_H

        self.add_pic(ed_self, nline, fn, size_x, size_y, ntag)

        ## better don't set PROP_MODIFIED
        #ed_self.set_prop(PROP_MODIFIED, True)

        msg_status(PRE + _('Added "%s", %dx%d, line %d') % (os.path.basename(fn), size_x, size_y, nline))

    def add_pic(self, ed_self, nline, fn, size_x, size_y, ntag):

        global id_img
        log(id_img)
        log(fn)
        if not image_proc(id_img, IMAGE_LOAD, fn):
           print(PRE + _('Cannot load "%s"') % os.path.basename(fn))
           return

        new_y = None
        if size_y < MIN_H: new_y = MIN_H
        if size_y > MAX_H: new_y = MAX_H
        if new_y is not None:
            size_x = round(size_x/size_y*new_y)
            size_y = new_y

        id_bitmap, id_canvas = ed_self.gap(GAP_MAKE_BITMAP, size_x, size_y)
        canvas_proc(id_canvas, CANVAS_SET_BRUSH, color=0xffffff)
        canvas_proc(id_canvas, CANVAS_RECT_FILL, x=0, y=0, x2=size_x, y2=size_y)

        image_proc(id_img, IMAGE_PAINT_SIZED, (id_canvas, 0, 0, size_x, size_y))

        ed_self.gap(GAP_DELETE, nline, nline)
        ed_self.gap(GAP_ADD, nline, id_bitmap, tag=ntag)

        print(PRE + _('"%s", %dx%d, line %d') % (os.path.basename(fn), size_x, size_y, nline+1))

