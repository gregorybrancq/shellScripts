"=============================================================================
" File : explorer.vim
" Author : M A Aziz Ahmed (aziz@123india.com)
" Last update : Fri Mar 17 2000
" Version : 1.1
"-----------------------------------------------------------------------------
" This file implements a file explorer. Latest version available at:
" http://www.freespeech.org/aziz/vim/my_macros/
"-----------------------------------------------------------------------------
" Just type ,e to launch the file explorer (this file should have been
" sourced) in a separate window. Type ,s to split the current window and
" launch explorer there. If the current buffer is modified, the window is
" anyway split (irrespective of ,e or ,s).
" It is also possible to delete files and rename files within explorer.
" (In UNIX, renaming doesn't seem to work, though!)
" The directory which explorer uses by default is determined by the 'browsedir'
" option.
"=============================================================================

nmap ,ve   :call VExplInitiate(0)<cr>
nmap ,vs   :call VExplInitiate(1)<cr>
nmap ,vi   :unlet g:verilog_explorer<cr>:call VExplInitiate(0)<cr>
map <M-F17> :call VOpen_pere()<CR>
map <C-F17> lbvey:<C-R>*<Home>b <End>.v<End><CR>
 
function! VExplInitiate(split, ...)
  let filename=expand("%:p:t")
  if (filename=="_vfileExplorer.tmp")
    echo "Already in file explorer"
  else
    let g:oldCh=&ch
    let &ch=2
    if (a:0==0)
      call VExplInitializeDirName("")
    else
      call VExplInitializeDirName(a:1)
    endif
    if (((&modified==1) && (&hidden==0)) || (a:split==1))
      sp ~/_vfileExplorer.tmp
      let b:splitWindow=1
    else
      e ~/_vfileExplorer.tmp
      let b:splitWindow=0
    endif
    call VExplSyntaxFile(filename)
    call VExplProcessFile(g:currDir)
  endif
endfunction

function! VExplInitializeDirName(dirName)
  if (a:dirName=="")
    if (exists("&bsdir"))
      if (&bsdir=="buffer")
        let startDir=expand("%:p:h")
      elseif ((!exists("g:currDir")) || (&bsdir=="current"))
        let startDir=getcwd()
      else
        let startDir=expand(g:currDir)
      endif
    elseif (!exists("g:currDir"))
      let startDir=getcwd()
    else
      let startDir=expand(g:currDir)
    endif
  else
    let startDir = a:dirName
  endif
  let g:currDir=(substitute(startDir,"\\","/","g"))."/"
  " In case the ending / was already a part of getcwd(), two //s would appear
  " at the end of g:currDir. So remove one of them
  let g:currDir=substitute(g:currDir,"//$","/","g")
  let g:currDir=substitute(g:currDir,"/./","/","g")
endfunction

function! VExplProcessFile(fileName)
  if ((isdirectory(a:fileName)) || (a:fileName==g:currDir."../"))
    "Delete all lines
    1,$d
    let oldRep=&report
    set report=1000
    if (a:fileName==g:currDir."../")
      let g:currDir=substitute(g:currDir,"/[^/]*/$","/","")
    else
      let g:currDir=a:fileName
    endif
    call VExplAddHeader()
    " exec("cd ".escape(g:currDir, ' '))
    call VExplDisplayFiles(g:currDir)
    normal zz
    if (isdirectory(@#))
      " Delete the previous buffer if the explorer was launched by means of
      " editing a directory
      bd! #
    else
      echo "Loaded contents of ".g:currDir
    endif
    let &report=oldRep
  elseif (filereadable(a:fileName))
    if (filereadable(@#))
       if (bufexists(@#))
          exec("b #")
       else
          exec("e! #")
       endif
    endif   
    exec("e! ".escape(a:fileName, ' '))
    call VExplCloseExplorer()
  endif
  let &modified=0
endfunction

function! VExplGetFileName()
  return substitute(g:currDir.getline("."), " ", "", "g")
endfunction

function! VExplAddHeader()
    " Give a very brief help
    let @f="\" <enter> : open file or directory\n"
    let @f=@f."\" q : quit file explorer\n"
    let @f=@f."\"---------------------------------------------------\n"
    let @f=@f.". ".g:currDir."\n"
    let @f=@f."\"---------------------------------------------------\n"
    put! f
    $ 
    d
endfunction


function! VExplDisplayFiles(dir)
  "let @f=glob(a:dir."*")
  if (!exists("g:verilog_explorer")) 
     let @v=system("/tools/utils/verilog_tools/simple_hier_print.pl *.v *.vb *.vi | sed 's:$:\.v:' | grep -v what_macro")
     let g:verilog_explorer="on"
  endif
  if (@v!="")
    normal mt
    put v
    .,$g/^/call VExplMarkDirs()
    normal `t
  endif
endfunction

function! VExplMarkDirs()
  let oldRep=&report
  set report=1000
  "Remove slashes if added
  s;/$;;e  
  "Removes all the leading slashes and adds slashes at the end of directories
  s;^.*\\\([^\\]*\)$;\1;e
  s;^.*/\([^/]*\)$;\1;e
  normal ^
  if (isdirectory(VExplGetFileName()))
    s;$;/;
  else
    " Move the file at the end so that directories appear first
    if (filereadable(VExplGetFileName())) 
       m$
    else
       d
    endif	
  endif
  let &report=oldRep
endfunction

function! VExplCloseExplorer()
  bd! ~/_vfileExplorer.tmp
  if (exists("g:oldCh"))
    let &ch=g:oldCh
  endif
endfunction
function! VExplBack2PrevFile()
  if ((@#!="") && (@#!="_vfileExplorer.tmp") && (b:splitWindow==0) && 
        \(isdirectory(@#)==0))
    exec("e #")
  endif
  call VExplCloseExplorer()
endfunction

function! VExplSyntaxFile(filename)
  if 1 || has("syntax") && exists("syntax_on") && !has("syntax_items")
    syn match browseSynopsis	"^\".*"
    syn match browseDirectory	"[^\"].*/$"
    let stringmatch=substitute( "syn match browseCurFile \"FILENAME\"", "FILENAME", a:filename, "")
    exec stringmatch
    echo(stringmatch)
    
    if !exists("g:did_browse_syntax_inits")
      let did_browse_syntax_inits = 1
      hi link browseSynopsis	PreProc
      hi link browseDirectory	Directory
      hi link browseCurFile	Statement
    endif
  endif
endfunction
      
function! VOpen_pere()
   let m = substitute(expand("%:p:t"), ".v$", "", "")
   let b:p = substitute(m, "^", "g:pere:", "")
   let tmp_filename = tempname()
   if (!exists(b:p))
	exe "! get_all_upper_module > "tmp_filename
	exe "source "tmp_filename
	exe "! \\rm -f "tmp_filename
   endif 	
   exec "exec \"b! \""b:p
endfunction

augroup verilogExplorer
  au!
  au BufEnter _vfileExplorer.tmp let oldSwap=&swapfile | set noswapfile
  au BufLeave _vfileExplorer.tmp let &swapfile=oldSwap
  au BufEnter _vfileExplorer.tmp nm <cr> :call VExplProcessFile(VExplGetFileName())<cr>
  au BufLeave _vfileExplorer.tmp nun <cr>
  au BufEnter _vfileExplorer.tmp nm q :call VExplBack2PrevFile()<cr>
  au BufLeave _vfileExplorer.tmp nun q
augroup end

"function! GenerateMenuHier()
"    call system("tail +6 ~/_vfileExplorer.tmp | sed 's:\( *\)\([^ ]*\):nmenu Verilog.Hier\:\".\1 \2\" \:b \2:' >! ~/_vfileExplorer.tmp.menu")
"    source ~/_vfileExplorer.tmp.menu
"endfunction
"
"function! OpenVerilogFile(modulename)
"    let filename =a:modulename.".v"
"    if (filereadable(filename))
"       if (bufexists(filename))
"          exec("b ".filename)
"       else
"          exec("e! ".filename)
"       endif
"    endif   
"endfunction
"
