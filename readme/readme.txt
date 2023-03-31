Markdown Image
This plugin finds all links to *local* pictures in the Markdown document, 
which may look like this:
![Stormtroopocat](image/example.jpg "The Stormtroopocat")
And it loads the linked picture and shows it inside inter-line gap,
below the text line.

#online image, no work
![alt text](https://example.com/img)
![alt text](http://example.com/img.jpg)

#local image, ok
![alt text](a.jpg "title a1") #relative path
![alt text](abc/a.jpg "title a2") #relative path
![alt text](C:\aa bb\2023-12-30.png "title a3") #absolute path

Author: jackusay
some functions are from: Alexey Torgashin

License: MIT
