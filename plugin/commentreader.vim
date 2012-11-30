if exists('g:commentreader_loaded') || !has('python')
    finish
endif
let g:commentreader_loaded = 1

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
    let g:creader_debug_file = '/var/tmp/creader.log'
endif

" initialization
python cr_instance = CommentReader()

" define functions
function! s:CRopenbook(path)
    python cr_instance.openBook(vim.eval('a:path'))
endfunction

function! s:CRopenweibo(auth_code)
    python cr_instance.openWeibo(vim.eval('a:auth_code'))
endfunction

function! s:CRopendouban()
    python cr_instance.openDouban()
endfunction

function! s:CRopentwitter()
    python cr_instance.openTwitter()
endfunction

function! s:CRhide()
    python cr_instance.hide()
endfunction

function! s:CRforward()
    python cr_instance.forward()
endfunction

function! s:CRbackward()
    python cr_instance.backward()
endfunction

function! s:CRnext()
    python cr_instance.next()
endfunction

function! s:CRprevious()
    python cr_instance.previous()
endfunction

" define commands
command! -nargs=1 -complete=file CRopenbook  call s:CRopenbook('<args>')
command! -nargs=1                CRopenweibo call s:CRopenweibo('<args>')
command! -nargs=0                CRforward   call s:CRforward()
command! -nargs=0                CRbackward  call s:CRbackward()
command! -nargs=0                CRhide      call s:CRhide()
command! -nargs=0                CRnext      call s:CRnext()
command! -nargs=0                CRprevious  call s:CRprevious()

" define maps
nnoremap <silent> <leader>d :CRforward<CR>
nnoremap <silent> <leader>a :CRbackward<CR>
nnoremap <silent> <leader>w :CRprevious<CR>
nnoremap <silent> <leader>s :CRnext<CR>
