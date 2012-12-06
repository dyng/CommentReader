if exists('g:commentreader_loaded') || !has('python')
    finish
endif
let g:commentreader_loaded = 1

" define commands
command! -nargs=? -complete=file CRopenbook    call commentreader#CRopenbook('<args>')
command! -nargs=?                CRopenweibo   call commentreader#CRopenweibo('<args>')
command! -nargs=?                CRopentwitter call commentreader#CRopentwitter('<args>')
command! -nargs=?                CRopendouban  call commentreader#CRopendouban('<args>')
command! -nargs=0                CRforward     call commentreader#CRforward()
command! -nargs=0                CRbackward    call commentreader#CRbackward()
command! -nargs=0                CRhide        call commentreader#CRhide()
command! -nargs=0                CRnext        call commentreader#CRnext()
command! -nargs=0                CRprevious    call commentreader#CRprevious()
command! -nargs=0                CRclose       call commentreader#CRclose()
command! -nargs=0                CRsave        call commentreader#CRsavesession()

" define maps
nnoremap <silent> <leader>d :CRforward<CR>
nnoremap <silent> <leader>a :CRbackward<CR>
nnoremap <silent> <leader>w :CRprevious<CR>
nnoremap <silent> <leader>s :CRnext<CR>
