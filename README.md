# cuda_markdown_image


* work only local image
* can't use right parenthesis in url
* `![aaa](bbb)` - In `bbb` part, if you put some behind url, it needs to be *behind* double quate. ex: `![alt text](a.jpg "title a1")`

```
#local image, ok
![alt text](a.jpg "title a1") #relative path
![alt text](abc/a.jpg "title a1") #relative path
![alt text](C:\aa bb\2023-12-30.png "title a1") #absolute path
![alt text](中/a c 文.jpg "title a1") #non ascii 
![alt text](file:///C:\Current Work\Service\12-30-34.png)

#online image, no work
![alt text](https://example.com/img)
![alt text](http://example.com/img.jpg)

#fail, duo to markdown image syntax limit, you can't use right parenthesis in url:
![alt text](a (2).jpg "title a1") #wrong!

#???
![alt text](//aa/bb/12-30-34.png)
![alt text](abc/a b.jpg =205x251)
  wrong: =205x251
  https://gitlab.com/gitlab-org/gitlab-foss/-/issues/58426
![smiley](smiley.png){:height="36px" width="36px"}.
  https://linuxpip.org/markdown-change-image-size/
```