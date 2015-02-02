
" ALLBUFFER
function! AllBuffers(cmnd)
    let cmnd = a:cmnd
    let i = 1
    while (i <= bufnr("$"))
        if bufexists(i)
            execute "buffer" i
            execute cmnd
        endif
        let i = i+1
    endwhile
endfun

command! -nargs=+ -complete=command Allbuf call AllBuffers(<q-args>)


" Supprime tous les blancs en debut de ligne
"nmap _S :%s/^\s\+//<CR>
" Converts file format to/from unix
command! Unixformat :set ff=unix
command! Dosformat :set ff=dos
" a nice command for making html-code
command! Code2html :source $VIM/syntax/2html.vim


