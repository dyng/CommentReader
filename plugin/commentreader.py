import vim
import urllib
import urllib2
from datetime import datetime
import json
import logging

# global variables
langdict = {
            'python':  { 'prefix':  '#', 'filler':   '#', 'suffix':   '#', 'defs':   r'^def' },
            'perl':    { 'prefix':  '#', 'filler':   '#', 'suffix':   '#', 'defs':   r'^sub' },
            'vim':     { 'prefix':  '"', 'filler':   '"', 'suffix':   '"', 'defs':   r'^function' },
            'c':       { 'prefix':  '/*', 'filler':  '*', 'suffix':   '*/', 'defs':  r''},
            'cpp':     { 'prefix':  '//', 'filler':  '//', 'suffix':  '//', 'defs':  r''},
           }

class CommentReader():
    def __init__(self):
        self.option  = {
                'line_len': int(vim.eval('g:creader_lines_per_block')),
                'line_num': int(vim.eval('g:creader_chars_per_line')),
                }
        self.meta = {
                'debug_mode': int(vim.eval('g:creader_debug_mode')),
                'debug_file': vim.eval('g:creader_debug_file'),
                'app_key':    '1861844333',
                'app_secret': '160fcb0ca75b22e35c644f8758e279c1',
                }
        self.content = None
        self.view    = View(self.option)
        self.pageNum = 0
        self.sectNum = 0

        # logging setting
        if self.meta['debug_mode'] == 1:
            logging.basicConfig(filename=self.meta['debug_file'], level=logging.DEBUG, format='%(asctime)s %(message)s')


    # opens

    def openBook(self, path):
        self.content = Content('book', Book(path, self.meta, self.option), self.option)
        self.view.refreshAnchor()
        self.show()

    def openWeibo(self, auth_code):
        self.content = Content('weibo', Weibo(auth_code, self.meta, self.option), self.option)
        self.view.refreshAnchor()
        self.show()

    def openTwitter(self):
        pass

    def refresh(self):
        self.content.refresh()
        self.pageNum = 0
        self.sectNum = 0
        self.show()

    # closes

    def close(self):
        pass



    # views

    def show(self):
        # clear first
        self.view.clear()

        # get content and render 
        raw_content_list = self.content.read(self.pageNum, self.view.getAnchorNum())
        content_list = self.view.commentize_list(raw_content_list)
        self.view.render(content_list)

        # point to first block
        self.first()

    def hide(self):
        # save and restore cursor position
        (line_bak, col_bak) = (vim.eval("line('.')"), vim.eval("col('.')"))
        self.view.clear()
        vim.command("call cursor('{0}', '{1}')".format(line_bak, col_bak))


    # cursor moves

    def forward(self):
        self.pageNum += self.view.getAnchorNum()
        self.show()
        self.first()

    def backward(self, from_prev=False):
        self.pageNum -= self.view.getAnchorNum()
        if self.pageNum < 0:
            self.pageNum = 0
        self.show()
        if from_prev:
            self.last()
        else:
            self.first()

    def first(self):
        self.sectNum = 0
        self.view.pointTo(self.sectNum)

    def last(self):
        self.sectNum = self.view.getAnchorNum() - 1
        self.view.pointTo(self.sectNum)

    def next(self):
        self.sectNum += 1
        if self.sectNum >= self.view.getAnchorNum():
            self.forward()
        else:
            self.view.pointTo(self.sectNum)

    def previous(self):
        self.sectNum -= 1
        if self.sectNum < 0:
            self.backward(from_prev=True)
        else:
            self.view.pointTo(self.sectNum)

class Anchor():
    def __init__(self, rel_posi, pre_anchor):
        self.rel_posi   = rel_posi
        self.abs_posi   = -1
        self.size       = 0
        self.pre_anchor = pre_anchor

    def evalAbsPosition(self):
        if self.pre_anchor is None:
            self.abs_posi = self.rel_posi
            return self.abs_posi
        else:
            self.abs_posi = self.pre_anchor.evalAbsPosition() + self.pre_anchor.size + self.rel_posi
            return self.abs_posi

    # Warning: if you need EXACT position, call evalAbsPosition instead of this
    def getAbsPosition(self):
        if self.abs_posi != -1:
            return self.abs_posi
        else:
            return self.evalAbsPosition()

    def bind(self, str):
        self.abs_posi = self.evalAbsPosition()
        self.size = str.count("\\n")

    def unbind(self):
        self.abs_posi = -1
        self.size = 0


class View():
    def __init__(self, option):
        # user defined options
        self.lineLen = option['line_len']
        self.lineNum = option['line_num']

        # define commenter
        filetype = vim.eval("&filetype")
        if filetype in langdict:
            self.prefix = langdict[filetype]['prefix']
            self.filler = langdict[filetype]['filler']
            self.suffix = langdict[filetype]['suffix']
        else:
            vim.command("echom 'Sorry, this language is not supported.'")

        # define declaration reserved word
        self.defs = langdict[filetype]['defs']

        # define anchors
        self.anchors = []

        self.refreshAnchor()
        if self.getAnchorNum() == 0:
            vim.command("echom 'Sorry, there is no place for comment.'")


    # anchors

    def getAnchorNum(self):
        return len(self.anchors)

    def refreshAnchor(self):
        # clear comment first
        self.clear()

        # reassign anchors
        self.anchors = []

        # save original cursor positon
        (line_bak, col_bak) = (vim.eval("line('.')"), vim.eval("col('.')"))
        vim.command("call cursor('1', '1')")
        pre_anchor = None
        pre_posi = 0
        while 1:
            posi = int(vim.eval("search('{0}', 'W')".format(self.defs)))
            if posi == 0: break
            new_anchor = Anchor(posi - pre_posi, pre_anchor)
            self.anchors.append(new_anchor)
            pre_posi = posi
            pre_anchor = new_anchor
        # restore cursor position
        vim.command("call cursor('{0}', '{1}')".format(line_bak, col_bak))



    # show or hide contents

    def render(self, string_list):
        for (anchor, content) in zip(self.anchors, string_list):
            # bind content and anchor
            anchor.bind(content)

            # escape '"' as a string
            for char in '"':
                content = content.replace(char, '\\'+char)

            # render content in vim
            abs_posi = anchor.getAbsPosition()
            command = 'silent! {0}put! ="{1}"'.format(abs_posi, content)
            # escape '|' and '"' as argument for 'put' command
            for char in '|"':
                command = command.replace(char, "\\"+char)
            # make 'modified' intact
            modified_bak = vim.eval('&modified')
            vim.command(command)
            vim.command('let &modified={0}'.format(modified_bak))

    def clear(self):
        for anchor in self.anchors:
            if anchor.size > 0:
                # clear content from buffer
                abs_posi = anchor.evalAbsPosition()
                range = "{0},{1}".format(abs_posi, abs_posi + anchor.size - 1)
                command = "silent! {0}delete _".format(range)
                # make 'modified' intact
                modified_bak = vim.eval('&modified')
                vim.command(command)
                vim.command('let &modified={0}'.format(modified_bak))
            else:
                pass

            # unbind content and anchor
            anchor.unbind()



    # cursor move

    def pointTo(self, sect_num):
        anchor = self.anchors[sect_num]
        position = anchor.getAbsPosition() + (anchor.size - 1)//2
        vim.command("normal {0}z.".format(position))


    # content formatter

    def commentize(self, str):
        output = self.prefix + self.filler * self.lineLen * 2 + "\\n"
        for l in str.split("\n"):
            output += "{0} {1}\\n".format(self.filler, l.encode('utf-8'))
        output += self.filler * self.lineLen * 2 + self.suffix + "\\n"
        return output

    def commentize_list(self, str_list):
        return [self.commentize(str) for str in str_list]


class Content():
    def __init__(self, type, stream, option):
        self.type   = type
        self.stream = stream

    def read(self, index, amount):
        items = self.stream.getItem(index, amount)
        return [i.content() for i in items]

    def refresh(self):
        if self.type == 'weibo':
            stream.refreshWeibo()


# Content: Book

class Book():
    def __init__(self, path, meta, option):
        self.fd      = open(path, 'r')
        self.items   = []
        self.lineLen = option['line_len']
        self.lineNum = option['line_num']

    def getItem(self, index, amount):
        output = []
        for i in range(index, index + amount):
            if i < len(self.items):
                output.append(self.items[i])
            else:
                option = {
                        'line_len':self.lineLen,
                        'line_num':self.lineNum,
                        }
                item = Page(self.fd, option)
                if item.content == "": break
                self.items.append(item)
                output.append(item)
        return output

class Page():
    def __init__(self, fd, option):
        self.lineLen = option['line_len']
        self.lineNum = option['line_num']

        content = []
        line_loaded = 0
        while line_loaded <= self.lineLen:
            line = fd.readline().decode('utf-8')
            if not line: break
            line = line.rstrip('\r\n')
            if len(line) == 0: line = " "
            p = 0
            while p < len(line):
                content.append(line[p:p+self.lineNum])
                line_loaded += 1
                p += self.lineNum

        self.string = "\n".join(content)

    def content(self):
        return self.string

# Content: Weibo

class Weibo():
    def __init__(self, auth_code, meta, option):
        self.auth_code = auth_code
        self.items = []
        self.next_page = 1
        self.token_info = None

    def reqAccessToken(self):
        client_id = '1861844333'
        client_secret = '160fcb0ca75b22e35c644f8758e279c1'
        redirect_uri = 'https://api.weibo.com/oauth2/default.html'

        url = 'https://api.weibo.com/oauth2/access_token'
        params = {
                'client_id': client_id,
                'client_secret': client_secret,
                'grant_type': 'authorization_code',
                'redirect_uri': redirect_uri,
                'code': self.auth_code,
                }

        try:
            logging.debug("request: " + url + ' POST: ' + urllib.urlencode(params))
            res = urllib2.urlopen(url, urllib.urlencode(params))
            self.token_info = json.load(res)
            logging.debug("response: " + str(self.token_info))
            logging.debug("access_token: " + self.token_info['access_token'])
        except:
            # TODO: error handle
            logging.exception('')

        return self.token_info['access_token']

    # you can get more tweets by calling this method repeatedly
    def pullTweets(self):
        # call reqAccessToken first if access_token not defined
        if self.token_info is None:
            self.reqAccessToken()

        url = 'https://api.weibo.com/2/statuses/home_timeline.json'
        params = {
                'access_token': self.token_info['access_token'],
                'count': 20,
                'page': self.next_page,
                }

        try:
            logging.debug("request: " + url + '?' + urllib.urlencode(params))
            res = urllib2.urlopen(url + '?' + urllib.urlencode(params))
            raw_timeline = json.load(res)
            logging.debug("response: " + str(raw_timeline))
            self.next_page += 1
        except:
            # TODO: error handle
            logging.exception('')

        for raw_tweet in raw_timeline['statuses']:
            # we need only tweets that older than the tail tweet
            if len(self.items) > 0 and int(raw_tweet['id']) >= self.items[-1].id: continue
            self.items.append(Tweet(raw_tweet))

        return self.items

    def getItem(self, index, amount):
        while index + amount > len(self.items):
            self.pullTweets()
        return self.items[index:index+amount]

    def refreshWeibo(self):
        self.items = []
        self.next_page = 1

class Tweet():
    def __init__(self, raw_tweet):
        self.id     = int(raw_tweet['id'])
        self.author = raw_tweet['user']['screen_name']
        self.text   = raw_tweet['text']

    def content(self):
        return self.author + ": " + self.text + "\n"

# Content: Douban

# Content: Twitter

# Content: Facebook
