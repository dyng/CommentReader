CommentReader
=============

Read your favorite content (twitter, weibo, digital novel, etc.) at work by pretending you are reading source code. :P

Requirements
============

- Vim 7.3+
- Python support for Vim

Installation
=============

It can be easily installed by just dropping all files to your `$HOME/.vim/` directory.

However I recommend using [vundle](https://github.com/gmarik/vundle/) or [pathogen](https://github.com/tpope/vim-pathogen/) instead as managing your vim plugins.

Usage and Configuration
=============

Twitter
-------------
1. Open a source file and run

        :CRopentwitter

2. If it is the first time you run the command, it will guide you to authorize it. Open the url stored in `+` register in your browser. If you are using gVim, you can paste it by `Ctrl + V`(Windows) or `Commands + V`(Mac) as usual.

3. It should be the twitter authorization page containing a PIN code. Copy it and run

        :CRopentwitter <your PIN code>

4. If everything goes right, the tweets should appear as comments now!

Weibo
-------------
1. Open a source file and run

        :CRopenweibo

2. It will require your authorization at the first time you run it. Open the url in `+` register the same as above.

3. Copy the last part of redirected url. For example, `17e80a3d4fe458da96f8561ab21d32fe` for redirected url as `https://api.weibo.com/oauth2/default.html?code=17e80a3d4fe458da96f8561ab21d32fe`.

4. run

        :CRopenweibo <your code>
    
and enjoy!

Novel
-------------
1. Open a source file and run

        :CRopenbook

2. If you haven't opened a book ever, it will require you to give the path to the command as argument. Like

        :CRopenbook <path to your file>

3. Up to now, CommentReader can read plain text file in *UTF-8* encoding *only*.

Commands
-------------

Maps
-------------
- l: next page
- h: previous page
- j: next item
- k: previous item
- r: refresh (for twitter and weibo)
- q: quit

There is also a useful command `CRtoggle` you can map to the key as you like, `<F5>` for example.

        :nnoremap <F5> :CRtoggle<CR>

Session
-------------

Configs
-------------

Snapshots
=============
[![snapshot1](http://dygvirus.info/images/thumbnail/2013-01-30T1.png)](http://dygvirus.info/images/full/2013-01-30T1.png)

[![snapshot1](http://dygvirus.info/images/thumbnail/2013-01-30T2.png)](http://dygvirus.info/images/full/2013-01-30T2.png)
