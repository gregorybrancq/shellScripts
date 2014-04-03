
"" -*- vim -*-

"" ===================================================================
"" Fichier de configuration de Vim
""
"" File           : vimrc.vim
"" Initial Author : Gregory Brancq
"" Last update    : 13/06/2006
"" ===================================================================
"
" 1. General setup
" 2. Graphic User Interface
" 3. Indent
" 4. Searching, Substituting
" 5. Statusline, Menu
" 6. file, backup, path
"



"" ===================================================================
"" -----------------------------------------------------------
"" 1. General setup
"" -----------------------------------------------------------
"" ===================================================================

" first, clear any existing autocommands:
autocmd!

" always have syntax highlighting in with the gui:
syntax on
" Permet de voir le tit. du doc. crt. ds les XTERM
set title
" Les caracteres dans le pattern sont pris litteralement
set magic
" don't have files trying to override this .vimrc:
set nomodeline
" Shell setting
set shell=/bin/tcsh
" Session options
set sessionoptions=winsize,winpos,resize,globals,buffers,slash,unix
" filetype et compatible ne fonctionne pas ensemble
set nocompatible

" N'ecrit pas automatiquement le fichier
set noautowrite
" What info to store from an editing session
" in the viminfo file;  can be used at next session.
set viminfo=%,'50,\"100,:100,n~/.viminfo
" remember all of these between sessions, but only 10 search terms; also
" remember info for 10 files, but never any on removable disks, don't remember
" marks in files, don't rehighlight old search patterns, and only save up to
" 100 lines of registers; including @10 in there should restrict input buffer
" but it causes an error for me:
"set viminfo=/10,'10,r/mnt/zip,r/mnt/floppy,f0,h,\"100
" utilisation des options de formats
set formatoptions-=t
" Repertoire ou on sotcke les .swp
set directory=.,~/.vim/swap/
" On ne coupe pas les lignes si elles sont grandes
"set nowrap
" Hide the mouse pointer while typing
set mousehide
" have the mouse enabled all the time:
set mouse=a
" mouse type
set mousemodel=popup_setpos
" focus follows mouse
"set mousef
"fait pas de bip lors d'une erreur
set errorbells
" set silent (no beep)
set visualbell
"permet d'ouvrir un 2eme fichier sans fermer le 1er
set hidden
" shell window size
"set lines=40
" Allow the last line to be a modeline - useful when the last line in sig gives the preferred textwidth for replies.
set modeline
set modelines=3
" Completion on th command line shows a menu
set wildmenu
set noinsertmode
"" Raffraichit automatiquement
"set autoread

"Indicates a fast terminal connection
set ttyfast
" make all windows the same size when adding/removing windows
set noequalalways
set nomore lazyredraw  ari
" When completing a word in insert mode (see |ins-completion|) from the
" tags file, show both the tag name and a tidied-up form of the search
" pattern (if there is one) as possible matches
set showfulltag
"Give a warning message when a shell command is used while the buffer
" has been changed.
set nowarn
"Change the way text is displayed
set dy=lastline
" Threshold for reporting number of lines changed
set report=0
" Minimum initial height of the help window
set helpheight=35
set cpo=Bes wim=list:full cpt=.,b,u,t
set shiftround
set notimeout
set linebreak

" Fold option
set foldmethod=indent
set foldlevel=1
set nofoldenable
let fold_enable=0

" Encoding
let &termencoding=&encoding
set fileencodings=utf-8
set encoding=utf-8

" supprimer le backup
set nobackup
" Repertoire de sauvegarde automatique
"set backupdir=~/.backup
" show always statusline of last window
set laststatus=2
" Le swap est mis a jour apres 50 caracteres saisies
set uc=50


"" ===================================================================
"" -----------------------------------------------------------
"" 2. Graphic User Interface
"" -----------------------------------------------------------
"" ===================================================================

if has("gui_running")

    " set font
    set guifont=Monospace\ 10
    " scroll bar at the right rather than the left:
    set guioptions+=r
    set guioptions-=l
    " menu
    set guioptions+=m
    " toolbar
    set guioptions+=T
    " clipboard to autoselect
    set guioptions+=a
    " initialize $top to first edited file directory
    let $top = expand("%:p:h")
    " minimal number of lines used for the current window
    set winheight=1
    " winwidth
    set winwidth=1
    " minimal number of lines used for the current window
    "set winminwidth=1
    " Minimum height of VIM's windows opened
    set winminheight=0
    " a new window is put below the current one
    set splitbelow
    " alt jumps to menu
    set winaltkeys=menu
    " Nombre d'espace utilise pour une auto indentation
    set shiftwidth=4

endif " gui_running



"" ===================================================================
"" -----------------------------------------------------------
"" 3. Indent
"" -----------------------------------------------------------
"" ===================================================================

    " quand on tape un ), vim montre furtivement le ( correspondant.
    set showmatch
    " largeur du texte
    set textwidth=0
    " autorise l'effacement en mode ajout
    " same as :set backspace=indent,eol,start
    set backspace=2
    " on garde d'une ligne a l'autre l'indentation d'un paragraphe
    set autoindent
    " smartindenting (clever autoindenting)
    set si
    " line numbers
    set number
    " remplace des shiftwidth au lieu des tab
    set expandtab
    " a <tab> in an indent inserts 'shiftwidth' spaces (not tabstop)
    set smarttab
    " number of spaces the tab stands for
    set tabstop=4




"" ===================================================================
"" -----------------------------------------------------------
"" 4. Searching, Substituting
"" -----------------------------------------------------------
"" ===================================================================

    " recommence la recherche au debut quand EOF atteint
    set wrapscan
    " highlight all matches...
    set hls
    " show the `best match so far' as search strings are typed:
    set incsearch
    " assume the /g flag on :s substitutions to replace all matches in a line:
    set gdefault
    " turn off the fucking :s///gc toggling
    "set noedcompatible
    "set scs
    " make searches case-insensitive, unless they contain upper-case letters:
    set ignorecase
    " on n'ignore pas les majuscules
    set smartcase
    " Switch on search pattern highlighting.
    set hlsearch
    set scrolloff=2

    "Characters that form pairs.  The |%| command jumps from one to the
    "other.
    set matchpairs+=<:>,(:),[:]



"" ===================================================================
"" -----------------------------------------------------------
"" 5. Statusline, Menu
"" -----------------------------------------------------------
"" ===================================================================

    " use tab for auto-expansion in menus
    set wc=<TAB>
    " show a list of all matches when tabbing a command
    set wmnu
    " remember last xx typed commands
    set history=200
    " show cursor position below each window
    set ruler
    " display the current mode and partially-typed commands in the status line:
    set showcmd
    " shows the current status (insert, visual, ...) in statusline
    set showmode
    " use shortest messages
    set shortmess+=atr

    " have command-line completion <Tab> (for filenames, help topics, option names)
    " first list the available options and complete the longest common part, then
    " have further <Tab>s cycle through the possibilities:
    set wildmode=list:longest,full
    " ignore some files for filename completion
    set wildignore=*.o,*.r,*.so,*.sl,*.tar,*.tgz,*.obj,*.bak,*.exe


"" ===================================================================
"" -----------------------------------------------------------
"" 6. Abbreviations
"" -----------------------------------------------------------
"" ===================================================================

    iabbrev gregb Gregory Brancq
    " correct my common typos without me even noticing them:
    abbreviate teh the



"" ===================================================================
"" -----------------------------------------------------------
"" 7. Mapping
"" -----------------------------------------------------------
"" ===================================================================

    :set path=.
    :set suffixesadd=.v,.vi

    "in which module u are actually residing in.
    "this map works only when u are whithin the module.placing it on module/endmodule does not make any sense.
    map module ma?module<CR>Wyiw'a:echo "module -->" @0<CR>

    :map <tab>   :bn<CR>
    :map <s-tab> :bp<CR>

    "" This is yet another feature that vi does not have.
    "" As I always want to see the buffer number I map it to CTRL-G.
    "" Please note that here we need to prevent a loop in the mapping by
    "" using the comamnd "noremap"!
    noremap <C-G> 2<C-G>
    noremap gf gf`"
    noremap <BS> dd

    "   set winaltkeys=no
    "       map <F5> ]!wakyes!
    "   noremap ]!wakyes! :map <F5> ]!wakmenu!<CR>:set winaltkeys=yes<CR>
    "   noremap ]!wakmenu! :map <F5> ]!wakno!<CR>:set winaltkeys=menu<CR>
    "   noremap ]!wakno! :map <F5> ]!wakyes!<CR>:set winaltkeys=no<CR>

    " Supprime tout les blancs en fin de ligne
    nmap d$ :%s/[ \t]*$//<CR>

    " Annuler aka Undo (windows's style)
    noremap <C-Z> u
    inoremap <C-Z> <C-O>u

    " Refaire aka Redo (windows's style)
    "noremap <C-R> <C-R>
    "inoremap <C-R> <C-O><C-R>

    " Tout selectionner (windows's style)
    noremap <C-A> gggH<C-O>G
    inoremap <C-A> <C-O>gg<C-O>gH<C-O>G
    cnoremap <C-A> <C-C>gggH<C-O>G


    " ctags mapping
    " jump to tag under cursor
    map ,z :tjump <C-R><C-W> <CR>zt
    map ,t :tab split <CR> :tjump <C-R><C-W> <CR>zt
    " open a preview window and jump to to tag under cursor
    map ,p :ptjump <C-R><C-W><CR>
    " split preview window
    map ,s :stjump <C-R><C-W><CR>
    " close preview window
    map ,c :pclose <CR>


    " have <F1> prompt for a help topic, rather than displaying the introduction
    " page, and have it do this from any mode:
    nnoremap <F1> :help<Space>
    vmap <F1> <C-C><F1>
    omap <F1> <C-C><F1>
    map! <F1> <C-C><F1>

    :map <F2> :w<CR>
    :imap <F2> <ESC>:w<CR>
    :map <C-S> :w<CR>
    :imap <C-S> <ESC>:w<CR>
    :map <F3> :wall<CR>
    :imap <F3> <ESC>:wall<CR>

    :map <S-F2> :mksession! ~/vim/last_vim_session.vim<CR>

    :map <F4> :quit<Esc>
    :map <F5> :sp<Esc>
    :map <F6> :vsp<Esc>
    :map <F7> :tabnew<Esc>
    :map <F9> :e!<Esc>
    :map <F10> :set guioptions+=b<Esc>:set nowrap<Esc>
    :map <F11> :set guioptions-=b<Esc>:set wrap<Esc>



"" ===================================================================
"" -----------------------------------------------------------
"" 9. Move Cursor
"" -----------------------------------------------------------
"" ===================================================================


    " tab navigation
    :map  <C-up> :tabprevious<cr>
    :nmap <C-up> :tabprevious<cr>
    :imap <C-up> <ESC>:tabprevious<cr>i
    :map  <C-down> :tabnext<cr>
    :nmap <C-down> :tabnext<cr>
    :imap <C-down> <ESC>:tabnext<cr>i

    " split windows navigation
    :map  <C-S-down> <C-W>j
    :nmap <C-S-down> <C-W>j
    :map  <C-S-up> <C-W>k
    :nmap <C-S-up> <C-W>k
    :map  <C-S-left> <C-W>h
    :nmap <C-S-left> <C-W>h
    :map  <C-S-right> <C-W>l
    :nmap <C-S-right> <C-W>l


    " Shift-Fleche pour selectionner un bloc
    map <S-Up> vk
    vmap <S-Up> k
    map <S-Down> vj
    vmap <S-Down> j
    map <S-Right> v
    vmap <S-Right> l
    map <S-Left> v
    vmap <S-Left> h



"" ===================================================================
"" -----------------------------------------------------------
"" 10. Plugins
"" -----------------------------------------------------------
"" ===================================================================

    " Active les plugins
    " Active les filetype
    " Source automatically the plugin/ directory
    filetype plugin on


    if has("gui_running")

        " Color
        colors slate
        source $VIMRC/colors/neon.vim

    endif " gui_running


    " Detect file type
    augroup filetype
        " Remove ALL autocommands for the current group.
        autocmd!
        autocmd BufNewFile,BufRead *.txt,*.lib,*.hvsyn set filetype=human
        autocmd BufNewFile,BufRead *.tcl set filetype=tcl
        autocmd BufNewFile,BufRead *.py set filetype=python
        autocmd BufNewFile,BufRead *.*vim* set filetype=vim
        autocmd BufNewFile,BufRead *.v,*.vb,*.vi,*.sv set filetype=verilog
        autocmd BufNewFile,BufRead *.groovy set filetype=java
    augroup END

    autocmd FileType verilog setlocal tabstop=8 expandtab
    autocmd Filetype java setlocal omnifunc=javacomplete#Complete
    autocmd FileType make setlocal noexpandtab
    autocmd FileType mail,human setlocal formatoptions+=t textwidth=78
    autocmd FileType c,cpp,slang setlocal cindent tabstop=2
    autocmd FileType c setlocal formatoptions+=ro
    autocmd FileType perl setlocal smartindent
    autocmd FileType css setlocal smartindent
    autocmd FileType html setlocal formatoptions+=tl
    autocmd FileType html,css setlocal expandtab tabstop=4
    autocmd FileType xml setlocal expandtab tabstop=2

    " Align
    let g:DrChipTopLvlMenu= "&Perso.&Align"

    " Bufexplorer
    " comment the function BufExplorer_ReSize() to avoid to place the cursor
    " at the first line each time you toggle between windows
    let g:bufExplorerDefaultHelp=0       " Show default help
    let g:bufExplorerShowDirectories=0   " Show directories
    let g:bufExplorerShowRelativePath=1  " Show relative paths.
    let g:bufExplorerSortBy='name'       " Sort by the buffer's name.

    " WinManager
    "let g:winManagerWidth=""
    "let g:explWinSize=""
    :map <c-e> :WMToggle<cr>

    " Ctags
    let tlist_c_settings = 'c;d:macro;g:enum;s:struct;u:union;t:typedef; ' .
                    \ 'm:members;v:variable;l:locals;m:members;f:function'
    let tlist_cpp_settings = 'c++;n:namespace;v:variable;d:macro;t:typedef;' .
                    \ 'c:class;g:enum;s:struct;u:union;p:prototype;m:members;f:function'
    :map <c-t> :TlistToggle<cr>

    " Utl
    :map <c-h> :Utl<cr>


"    " Permet de commenter n'importe quel type de fichier
"    source $VIMRC/plugin/BlockComment.vim
"    " Utilise les fonctions grep
"    source $VIMRC/plugin/grep.vim
    "source $VIMRC/plugin/utils.vim
    "source $VIMRC/plugin/fexplore.vim
    "source $VIMRC/plugin/minibufexpl.vim




















""
"" ===================================================================
"" AutoCommands {{{
"" ===================================================================
""
"""source $VIMRUNTIME/../macros/let-modeline.vim
""
""     ,E = execute line
"" map ,E 0/\$<CR>w"yy$:<C-R>y<C-A>r!<C-E>
"" This command excutes a shell command from the current line and
"" reads in its output into the buffer.  It assumes that the command
"" starts with the fist word after the first '$' (the shell prompt
"" of /bin/sh).  Try ",E" on that line, ie place the cursor on it
"" and then press ",E":
"" $ ls -la
"" Note: The command line commands have been remapped to tcsh style!!
""
"" From the vim mailing list, Bob Hiestand's solution.
" vnoremap ,rev <esc>:execute "'<,'>g/^/m" line("'<")-1<cr>
" nnoremap ,rev :execute "%g/^/m" 0<cr>
""
"
""------ supprime la ligne courante si elle ne contient que des blancs
""------ l'intervalle [  ] contient un espace et une tabulation
"   noremap      ]!erase!        :.g/^[  ]*$/-j<CR>$
"
"let g:ft_ignore_pat = 'lst'
"
"
"  " Put these in an autocmd group, so that we can delete them easily.
"  augroup vimrcEx
"    au!
"
"    " This is disabled, because it changes the jumplist.  Can't use CTRL-O to go
"    " back to positions in previous files more than once.
"    if 0
"      " When editing a file, always jump to the last known cursor position.
"      " Don't do it when the position is invalid or when inside an event handler
"      " (happens when dropping a file on gvim).
"      autocmd BufReadPost *
"            \ if line("'\"") > 0 && line("'\"") <= line("$") |
"            \   exe "normal! g`\"" |
"            \ endif
"    endif
"  augroup END
"
"  ""source $VIMRUNTIME/settings/gz.set
"  if version < 600
"    source $VIMRUNTIME/mysettingfile.vim
"  endif
"endif " has("autocmd")
"" }}}
"
"
"" Loads FirstModeLine() {{{
"if !exists('*FirstModeLine')
"  Runtime plugin/let-modeline.vim
"endif
"if exists('*FirstModeLine')
"  aug ALL
"    au!
"    " To not interfer with Templates loaders
"    au BufNewFile * :let b:this_is_new_buffer=1
"    " Modeline interpretation
"    au BufEnter   * :call FirstModeLine()
"  aug END
"endif
"" }}}
"
"" global variable used by Triggers.vim in order to determine if some echoing
"" can be done or not yet.
"au VimEnter * :let g:loaded_vimrc = 1
"" As this must be done after the plugins are loaded, but before the very
"" end of the vim initialization, this phase has been moved to the .gvimrc
"

