" load python module
let pyfile = expand('<sfile>:r') . '.py'
exe 'pyfile' pyfile

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

" define functions
function! commentreader#CRopenbook(path)
    python CRopenbook(vim.eval("bufnr('')"), vim.eval('a:path'))
endfunction

function! commentreader#CRopenweibo(auth_code)
    python CRopenweibo(vim.eval("bufnr('')"), vim.eval('a:auth_code'))
endfunction

function! commentreader#CRopendouban()
    python CRopendouban(vim.eval("bufnr('')"))
endfunction

function! commentreader#CRopentwitter()
    python CRopentwitter(vim.eval("bufnr('')"))
endfunction

function! commentreader#CRhide()
    python CRhide(vim.eval("bufnr('')"))
endfunction

function! commentreader#CRforward()
    python CRforward(vim.eval("bufnr('')"))
endfunction

function! commentreader#CRbackward()
    python CRbackward(vim.eval("bufnr('')"))
endfunction

function! commentreader#CRnext()
    python CRnext(vim.eval("bufnr('')"))
endfunction

function! commentreader#CRprevious()
    python CRprevious(vim.eval("bufnr('')"))
endfunction

function! commentreader#CRclose()
    python CRclose(vim.eval("bufnr('')"))
endfunction

function! commentreader#CRsavesession()
    python CRsavesession(vim.eval("bufnr('')"))
endfunction
