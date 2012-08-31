import vim

# global variables
langdict = {
            'python':  { 'prefix':  '#', 'filler':   '#', 'suffix':   '#', 'defs':   r'^def' },
            'perl':    { 'prefix':  '#', 'filler':   '#', 'suffix':   '#', 'defs':   r'^sub' },
            'vim':     { 'prefix':  '"', 'filler':   '"', 'suffix':   '"', 'defs':   r'^function' },
            'c':       { 'prefix':  '/*', 'filler':  '*', 'suffix':   '*/', 'defs':  r''},
            'cpp':     { 'prefix':  '//', 'filler':  '//', 'suffix':  '//', 'defs':  r''},
           }

class Init():
    def __init__(self):
        self.option  = {
                'line_len' : int(vim.eval('g:creader_lines_per_block')),
                'line_num' : int(vim.eval('g:creader_chars_per_line')),
                }
        self.content = None
        self.view    = View(self.option)
        self.pageNum = 0
        self.sectNum = 0


    # opens

    def openBook(self, path):
        self.content = Content('book', Book(path, self.option), self.option)
        self.view.refreshAnchor()
        self.show()

    def openWeibo(self):
        pass

    def openTwitter(self):
        pass


    # closes

    def close(self):
        pass


    # views

    def show(self):
        # clear first
        self.view.clear()

        # get content and render 
        raw_content_list = self.content.readContent(self.pageNum, self.view.getAnchorNum())
        content_list = self.view.commentize_list(raw_content_list)
        self.view.render(content_list)

        # point to first block
        self.first()

    def hide(self):
        self.view.clear()


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
        self.relPosi   = rel_posi
        self.absPosi   = -1
        self.size      = 0
        self.preAnchor = pre_anchor

    def evalAbsPosition(self):
        if self.preAnchor is None:
            self.absPosi = self.relPosi
            return self.absPosi
        else:
            self.absPosi = self.preAnchor.evalAbsPosition() + self.preAnchor.size + self.relPosi
            return self.absPosi

    def getAbsPosition(self):
        if self.absPosi != -1:
            return self.absPosi
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
            vim.command("echo 'Sorry, this language is not supported.'")

        # define declaration reserved word
        self.defs = langdict[filetype]['defs']

        # define anchors
        self.anchors = []

        self.refreshAnchor()
        if self.getAnchorNum() == 0:
            vim.command("echo 'Sorry, there is no place for comment.'")


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

    def readContent(self, index, amount):
        items = self.stream.getItem(index, amount)
        return [i.content for i in items]

# Content: Book

class Book():
    def __init__(self, path, option):
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

        self.content = "\n".join(content)

# Content: Weibo

# Content: Douban

# Content: Twitter

# Content: Facebook
