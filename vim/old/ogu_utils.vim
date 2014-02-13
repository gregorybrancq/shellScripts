" return list of all buffers
func! BufList()
	let ix = 1
	let rons_hack = exists("*getbufvar")
	let buflist = ''
	while ix <= bufnr("$")
		if bufname(ix) != ''
                        exe "let buflist = \"".buflist.bufname(ix)." \""  
		endif
		let ix = ix + 1
	endwhile
	return buflist
endfunc

function! MenuOnOff()
  let menu_on =matchstr(&guioptions,"m")
  if (menu_on=="m")
    set guioptions-=mT
  else
    set guioptions+=mT
    am &Help.-sepron-  :
    am &Help.Global\ Help  :call GlobalHelp()<cr>
  endif
endfunction
func! GlobalHelp()
    e $VIMGLOBAL/Global.txt
    exe "normal \<c-w>o"
endfunc

" return list of all buffers
func! NextFont()
    if (!exists("g:font_ix"))
        let g:font_ix = 0
    endif
	if filereadable(expand("~/vim/gui_fonts.vim"))
        e ~/vim/gui_fonts.vim
    else
	    e $VIMGLOBAL/fonts_list.vim
    endif
    exe ":"g:font_ix
    exe getline(line("."))
    let g:font_ix = g:font_ix + 1
    exe ":$"
    if (g:font_ix > line("$"))
        let g:font_ix = 0
    endif
    bd
    echo("New font = ".&guifont)
    echohl Question
    call input("Press RETURN or enter command to continue")
    echohl None
endfunc
:com! NextFont call NextFont()
:map ² :NextFont

" use a2ps for printing
" PR : print current buffer
" PR expand("%") : print current file
" PRA : print all buffers
func! PR(...)

        let i = 1
        let filename = ''
        let buffer = 0
        exe "let nargs=a:" . 0

        while i <= nargs
           exe "let tmp = a:" . i
           exe "let filename = \"".filename.tmp." \""
           let i = i + 1
        endwhile
        
	" if no filename is specified, get current buffer filename
        if filename == ''
                let filename = expand("%")
                let extension = expand("%:e")
                let full_name = expand("%:p")
                let buffer = 1
        endif
        
        if filename == *
                let filename = BufList()
        endif
        
        
        if buffer == 1
               let tmp_filename = tempname()
               exe "let tmp_filename = \"".tmp_filename.".".extension." \""
               exe "1,$ yank y"
               exe "e "tmp_filename
               exe "0 put y"
               exe "w "tmp_filename
               exe "!a2ps --center-title=".filename." --footer=".full_name." ".tmp_filename." "
               exe "bd"
        else
               exe "! /tools/bin/print "filename
        endif
endfunc
:com! -nargs=? PR call PR(<f-args>)

func! PRINTALL()
    let buf_list =BufList()
    call PRINT(buf_list) 
endfunc
:com! PRA call PRINTALL()

" replace close command by save and close if modified, 
" the last window is replace by the next buffer
" the last buffer close vim
func! Close(...)
        let i = 2
        let bang = a:1
        exe "let nargs=a:" . 0
	let filename=''

        while i <= nargs
           "exe "echo a:" . i
           exe "let tmp = a:" . i
           exe "let filename = \"".filename.tmp." \""
           let i = i + 1
        endwhile
        
	    " if no filename is specified, get current buffer filename
        if filename == ''
                let filename = expand("%")
        endif
        let error = 0
        let saved = 0
        if filename != ''
                " save if file has been modifed:
                if ( &mod || filename != expand("%"))
                        if (bang == 0)
        	                let errmsg = ""
        	                exe 'w' filename
                                if (errmsg != "")
                                        let error = 1
                                else
                                        let saved = 1
                                endif
                        else
        	                let errmsg = ""
        	                exe 'w!' filename
                                if (errmsg != "")
                                        let error = 1
                                else
                                        let saved = 1
                                endif
                        endif
        	endif
                " mention that it has been saved
                if saved == 1
                        echo filename "saved ..."
                        :let key=input("Press Return")
                endif
        	if error == 0
                        bdelete
        	endif
        endif
        
        let new_filename = expand("%")
        " check if it is the last open window
        if new_filename == ''
                q
                q
        endif
endfunc
:com! -bang -nargs=? C call Close(<bang> "0",<f-args>)
:cab c C

func! Comment(com_begin,...)
        let i = 1
        let com_begin =a:com_begin
        let com_end =''
        if a:0 !=0
                let com_end =a:1
        endif
        exe "s¤^¤".com_begin."¤"
        exe "s¤$¤".com_end."¤"
endfunc
func! Uncomment(com_begin,...)
        let i = 1
        let com_begin =a:com_begin
        let com_end =''
        if a:0 !=0
                let com_end =a:1
        endif
        exe "s¤".com_begin."¤¤"
        exe "s¤".com_end."$¤¤"
endfunc

function! CheckBoldFont()
    let bold =matchstr(&guifont,"bold")
    if bold=="bold"
        so $VIMCOLOR/color_nobold.gvimrc
    endif
endfunction

function! Port2pin_func() range
  let pos = a:firstline
  while pos <= a:lastline
    exe ":" pos
    :s:\(\<[^ /*-+,;:	]*\>\):.\1			(\1):
    let pos = pos + 1
  endwhile
endfunction
com! -range Port2pin :<line1>,<line2> call Port2pin_func()

function! Get_verilog_line (line_nbr)
    let verilog_line = substitute(getline(a:line_nbr),"//.*","", "")
    let verilog_line = substitute(verilog_line,"{.*}","", "")
    let verilog_line = substitute(verilog_line,"(.*)","", "")
    return substitute(verilog_line,"\"[^\"]\"","", "")
endfunction
function! Get_verilog_comment (line_nbr)
    return substitute(getline(a:line_nbr),"//.*","", "")
endfunction

"
"à modifier :
"   virer les Get_verilog_line
"   à chaque ligne : s'il y a des commentaires : les pousser sur la ligne suivante
"   les récupérer à la fin du traitement
"
"   dans les déclarations on peut avoir des virgules insérées dans de la concaténation : pousser {...} sur la ligne suivante
"   de meme avec du texte
"

function! Verilog_format_func(...) range
    if (a:0 == 0)
        let first_line = 1
        let last_line = line("$")
    elseif (a:0 == 1)
        let first_line = a:1
        let last_line = a:1
    else
        let first_line = a:1
        let last_line = a:2
    endif
  let pos = first_line
  let word = ""
  let previous_word = ""
  let tab_ix = 0
  let begin_pos = ""
  let case_pos = ""
  let function_pos = ""
  let task_pos = ""
  let bracket_pos = ""
  let module_declaration = 0
  let declaration = ""
  let declaration_ix = 0
  let declaration_tmp= ""
  while pos <= last_line
    retab
    exe ":" pos
    :s/^ *//
    :s/ *$//
    :s/$/ /
    "
    let i = tab_ix
    let previous_word = word
    let word = ""
    "
    let keyword = "^begin "
    if (matchstr(getline("."),keyword,0) != "")
        let word = keyword
        if (previous_word == "^if " || previous_word == "^else " || previous_word == "^always " || previous_word == "^for " || previous_word == "^initial " || previous_word == "^while "  || previous_word == "^repeat "  || previous_word == "^forever " || previous_word == "^case " || previous_word == "^casex " || previous_word == "^casez ")
            let i = i - 1
        else
            let tab_ix = tab_ix + 1
        endif
        let begin_pos = i." ".begin_pos
    elseif (matchstr(substitute(substitute( getline("."), "//.*", "\<begin\>", " begin "), "", "", "")," begin ",0) != "")
        let word = keyword
        let tab_ix = tab_ix + 1
        let begin_pos = i." ".begin_pos
    endif
    "
    let keyword = "^end "
    if matchstr(getline("."),keyword,0) != ""
        let word = keyword
        let i = matchstr(begin_pos,"[0-9]*",0)
        if i == ""
            let i = i - 1
        endif
        let j = match(begin_pos," ",0)
        let begin_pos = matchstr(begin_pos,"[0-9].*",j)
        let tab_ix = i
    endif
    "
    let keyword = "^assign "
    if matchstr(getline("."),keyword,0) != ""
        let i = 0
        let tab_ix = 0
        exe ":".pos."s/assign */assign	/"
    endif
    "
    let keyword = "{ "
    if substitute(Get_verilog_line("."),".*{","{","") == "{ "
        let word = keyword
        let i = tab_ix
        let bracket_pos = i." ".bracket_pos
        let tab_ix = tab_ix + 1
        "echo "{"
    endif
    "
    let keyword = "}"
    if substitute(substitute(Get_verilog_line("."),"}.*","}",""),"^ *"," ","") == " }"
        let word = keyword
        let i = matchstr(bracket_pos,"[0-9]*",0)
        let tab_ix = i
        if i == ""
            let i = i - 1
            let tab_ix = tab_ix - 1
        endif
        "echo "}"
    endif
    "
    let keyword = "^task "
    if matchstr(getline("."),keyword,0) != ""
        let word = keyword
        let task_pos = i." ".task_pos
        let tab_ix = tab_ix + 1
        let declaration_ix = 1
    endif
    "
    let keyword = "^endtask "
    if matchstr(getline("."),keyword,0) != ""
        let word = keyword
        let i = matchstr(task_pos,"[0-9]*",0)
        if i == ""
            let i = i - 1
        endif
        let j = match(task_pos," ",0)
        let task_pos = matchstr(task_pos,"[0-9].*",j)
        let tab_ix = tab_ix - 1
        let declaration_ix = 0
    endif
    "
    let keyword = "^function "
    if matchstr(getline("."),keyword,0) != ""
        let word = keyword
        let i = 0
        let function_pos = i." ".function_pos
        let tab_ix = 1
        let declaration_ix = 1
    endif
    "
    let keyword = "^endfunction "
    if matchstr(getline("."),keyword,0) != ""
        let word = keyword
        let i = matchstr(function_pos,"[0-9]*",0)
        if i == ""
            let i = i - 1
        endif
        let j = match(function_pos," ",0)
        let function_pos = matchstr(function_pos,"[0-9].*",j)
        let tab_ix = tab_ix - 1
        let declaration_ix = 0
    endif
    "
    let keyword = "^case "
    if matchstr(getline("."),keyword,0) != ""
        let word = keyword
        let case_pos = i." ".case_pos
        let tab_ix = tab_ix + 1
    endif
    let keyword = "^casex "
    if matchstr(getline("."),keyword,0) != ""
        let word = keyword
        let case_pos = i." ".case_pos
        let tab_ix = tab_ix + 1
    endif
    let keyword = "^casez "
    if matchstr(getline("."),keyword,0) != ""
        let word = keyword
        let case_pos = i." ".case_pos
        let tab_ix = tab_ix + 1
    endif
    "
    let keyword = "^endcase "
    if matchstr(getline("."),keyword,0) != ""
        let word = keyword
        let i = matchstr(case_pos,"[0-9]*",0)
        if i == ""
            let i = i - 1
        endif
        let j = match(case_pos," ",0)
        let case_pos = matchstr(case_pos,"[0-9].*",j)
        let tab_ix = tab_ix - 1
    endif
    "
    let keyword = "^if "
    if matchstr(getline("."),keyword,0) != ""
        let word = keyword
        if previous_word == "^else "
            exe ":" pos - 1
            :join
            :s/ *if/ if/
            let pos = pos - 1
            let i = 0
        else
            let tab_ix = tab_ix + 1
        endif
    endif
    "
    let keyword = "^else "
    if matchstr(getline("."),keyword,0) != ""
        let word = keyword
        if previous_word !="^end "
            let i = i - 1
        else
            let tab_ix = tab_ix + 1
        endif
    endif
    "
    let keyword = "^module "
    if matchstr(getline("."),keyword,0) != ""
        let word = keyword
        let i = 0
        let tab_ix = tab_ix + 1
        let module_declaration = 1
    elseif (module_declaration == 1)
        if matchstr(Get_verilog_line("."),";",0) == ";"
            let tab_ix = 0
            let module_declaration = 0
        else
            let i = 2
        endif
    endif
    let keyword = "^endmodule "
    if matchstr(getline("."),keyword,0) != ""
        let i = 0
        let tab_ix = 0
    endif
    "
    let keyword = "^."
    if matchstr(getline("."),keyword,0) == "."
        let i = 2
        let tab_ix = 0
    endif
    "
    if (matchstr(getline("."),"^input ",0) != "" || matchstr(getline("."),"^output ",0) != "" || matchstr(getline("."),"^reg ",0) != "" || matchstr(getline("."),"^wire ",0) != "" || matchstr(getline("."),"^inout ",0) != "" || matchstr(getline("."),"^input[",0) != "" || matchstr(getline("."),"^output[",0) != "" || matchstr(getline("."),"^reg[",0) != "" || matchstr(getline("."),"^wire[",0) != "" || matchstr(getline("."),"^inout[",0) != "" || matchstr(getline("."),"^real ",0) != "" || matchstr(getline("."),"^integer ",0) != "")
        let keyword = substitute(Get_verilog_line("."), "[ \[].*", "", "")
        let declaration = keyword
        let i = declaration_ix
        let range = ""
        let range_start = match(Get_verilog_line("."),"[",0)
        let range_end = match(Get_verilog_line("."),"]",0)
        if (range_start > 0 && range_end > range_start)
            let range = strpart(Get_verilog_line("."),range_start,(range_end-range_start+1))
            :s/] */]/g
        endif
        exe ":".pos."s/^".keyword." */".keyword." /"
        if match(Get_verilog_line(pos),",",0) != -1
            exe ":s/,/; ".keyword." ".range."/"
            :s/^ *//
            :s/ */ /
            "echo "-".getline(".")."-"
            "echo "- ".keyword." ".range." -"
            if getline(".") == " ".keyword." ".range." "
                join
            endif
            exe ":".pos."retab"
        endif
        if keyword == "reg"
            exe ":".pos."s/".keyword."/".keyword."	/"
        endif
        exe ":".pos."s/^ *//"
        exe ":".pos."s/  */	/"
    endif
    "
    if i < 0
        let i = 0
    endif
    while i
        :s/^/	/
        let i = i - 1
    endwhile
    "
    let pos = pos + 1
    "
  endwhile
endfunction
com! -range VFormat call Verilog_format_func(<line1>,<line2>)
