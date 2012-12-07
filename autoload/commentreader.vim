" parser user-define options
if !exists('g:creader_chars_per_line')
    let g:creader_chars_per_line = 20
endif
if !exists('g:creader_lines_per_block')
    let g:creader_lines_per_block = 5
endif
if !exists('g:creader_debug_mode')
    let g:creader_debug_mode = 1
endif
if !exists('g:creader_debug_file')
    " TODO: default value
    let g:creader_debug_file = '/var/tmp/creader.log'
endif
if !exists('g:creader_session_file')
    " TODO: default value
    let g:creader_session_file = $HOME.'/.vim-infos/vim_creader_session'
endif

" import vim
python import vim

" import oauth2
let libpath = substitute(expand('<sfile>:p:r'), 'commentreader$', 'lib', '')
python sys.path.append(vim.eval('libpath'))
python module = __import__('oauth2')
python del sys.path[-1]

" load commentreader.py
let pyfile = expand('<sfile>:r') . '.py'
exe 'pyfile' pyfile

" define functions
function! commentreader#CRopenbook(path)
    python CRopen(vim.eval("bufnr('')"), 'Book', vim.eval('a:path'))
endfunction

function! commentreader#CRopenweibo(auth_code)
    python CRopen(vim.eval("bufnr('')"), 'Weibo', vim.eval('a:auth_code'))
endfunction

function! commentreader#CRopendouban()
    python CRopen(vim.eval("bufnr('')"), 'Douban')
endfunction

function! commentreader#CRopentwitter(PIN)
    python CRopen(vim.eval("bufnr('')"), 'Twitter', vim.eval('a:PIN'))
endfunction

function! commentreader#CRclose()
    python CRclose(vim.eval("bufnr('')"))
endfunction

function! commentreader#CRhide()
    python CRoperation(vim.eval("bufnr('')"), 'hide')
endfunction

function! commentreader#CRforward()
    python CRoperation(vim.eval("bufnr('')"), 'forward')
endfunction

function! commentreader#CRbackward()
    python CRoperation(vim.eval("bufnr('')"), 'backward')
endfunction

function! commentreader#CRnext()
    python CRoperation(vim.eval("bufnr('')"), 'next')
endfunction

function! commentreader#CRprevious()
    python CRoperation(vim.eval("bufnr('')"), 'previous')
endfunction

function! commentreader#CRsavesession()
    python CRoperation(vim.eval("bufnr('')"), 'saveSession')
endfunction
