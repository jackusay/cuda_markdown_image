#md img preview
import os
from cudatext import *
#from cudax_lib import get_translation

from urllib.parse import urlparse #check if Online URL

#PIC_TAG = 0x1000 #minimal tag for api (CRC adds to tag)
BIG_SIZE = 400 #if width bigger, ask to resize
#DIALOG_FILTER = 'Pictures|*.png;*.jpg;*.jpeg;*.jpe;*.gif;*.bmp;*.ico'
PRE = '[Markdown Image] '
MIN_H = 10 #limitations of api to gap height
MAX_H = 500-5

data_all = {}
id_img = image_proc(0, IMAGE_CREATE)

def log(s):
    #print(s)
    pass

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
        import re       
        x = re.findall("!\[[^\]]+\]\([^\)]+\)", txt) #get image syntax ex: ![Stormtroopocat](https://octodex.github.com/images/stormtroopocat.jpg "The Stormtroopocat")
        log(f"image syntax: {x}")
        if not x:
            log("Can't find image syntax.")
            return
        #q = re.search("!\[[^\]]+\]", x[0]) #get title ex: ![sdff]
        #log(q.group()[2:-1])
        p = re.search("\([^\)]+", x[0]) #get () part ex: (https://octodex.github.com/images/stormtroopocat.jpg "The Stormtroopocat"
        pp = p.group()[1:]
        url = pp.split("\"")[0].strip() #get url
        log(f"url: {url}")
        
        #if online URL, return
        if urlparse(url).scheme in ('http', 'https'):
            return
        
        log(f"absolute path?: {os.path.isabs(url)}")
        if os.path.isabs(url):
            fn = url
        else:
            filepath = ed_self.get_filename()
            fn = os.path.join(os.path.dirname(filepath), url)
            
        if not os.path.isfile(fn):
            ed_self.gap(GAP_DELETE, nline, nline)
        
        ntag = 2 #for delete
        size_x = BIG_SIZE
        size_y = BIG_SIZE
        self.add_pic(ed_self, nline, fn, size_x, size_y, ntag)
        ed.set_prop(PROP_MODIFIED, '1')
        msg_status(PRE+'Added "%s", %dx%d, line %d' % (os.path.basename(fn), size_x, size_y, nline))

    def add_pic(self, ed, nline, fn, size_x, size_y, ntag):

        global id_img
        log(id_img)
        log(fn)
        if not image_proc(id_img, IMAGE_LOAD, fn):
           print(PRE+'Cannot load "%s"' % os.path.basename(fn))
           return

        new_y = None
        if size_y < MIN_H: new_y = MIN_H
        if size_y > MAX_H: new_y = MAX_H
        if new_y is not None:
            size_x = round(size_x/size_y*new_y)
            size_y = new_y

        id_bitmap, id_canvas = ed.gap(GAP_MAKE_BITMAP, size_x, size_y)
        canvas_proc(id_canvas, CANVAS_SET_BRUSH, color=0xffffff)
        canvas_proc(id_canvas, CANVAS_RECT_FILL, x=0, y=0, x2=size_x, y2=size_y)

        image_proc(id_img, IMAGE_PAINT_SIZED, (id_canvas, 0, 0, size_x, size_y))

        ed.gap(GAP_DELETE, nline, nline)
        ed.gap(GAP_ADD, nline, id_bitmap, tag=ntag)

        print(PRE+'"%s", %dx%d, line %d' % (os.path.basename(fn), size_x, size_y, nline+1))

