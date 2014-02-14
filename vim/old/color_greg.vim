
" Remove all existing highlighting and set the defaults.
hi clear

set background=light
if exists("syntax_on")
  syntax reset
endif

hi Normal       guifg=black     guibg=DarkGray
hi Comment      term=bold       ctermfg=4       guifg=Purple
hi Constant     term=underline  ctermfg=Magenta guifg=DeepSkyBlue4
hi Link     	term=underline  ctermfg=Magenta guifg=LightSteelBlue
hi Special      term=bold       ctermfg=Magenta guifg=firebrick4
hi Identifier   term=underline  ctermfg=Blue    guifg=Blue
hi Statement    term=bold       ctermfg=DarkRed gui=NONE        guifg=Brown
hi PreProc      term=underline  ctermfg=Magenta guifg=Purple
hi Define      	term=underline  ctermfg=Magenta guifg=PaleTurquoise4
hi Type         term=underline  ctermfg=Blue    gui=NONE        guifg=SteelBlue
hi Visual       term=reverse    ctermfg=Yellow  ctermbg=Red     gui=NONE        guifg=Black    guibg=DarkRed
hi Search       term=reverse    ctermfg=Black   ctermbg=Black    gui=NONE   	guifg=LightRed       guibg=DarkRed
hi Tag          term=bold       ctermfg=DarkGreen guifg=DarkGreen
hi Error        term=reverse    ctermfg=15      ctermbg=9       guibg=Red       guifg=White
hi Todo         term=standout   ctermbg=NONE 	ctermfg=Black   guifg=Blue      guibg=DarkGray
hi StatusLine	guibg=#c2bfa5 	guifg=white 	gui=none
hi StatusLineNC	guibg=#c2bfa5 	guifg=grey35 	gui=none

hi! link MoreMsg        Comment
hi! link ErrorMsg       Visual
hi! link WarningMsg     ErrorMsg
hi! link Question       Comment
hi link String	        Constant
hi link Character	Constant
hi link Boolean	        Constant
hi link Float		Number
hi link Function	Identifier
hi link Conditional	Statement
hi link Repeat	        Statement
hi link Label		Statement
hi link Operator	Statement
hi link Keyword		Statement
hi link Exception	Statement
hi link Include		PreProc
hi link Macro		PreProc
hi link PreCondit	PreProc
hi link StorageClass	Type
hi link Structure	Type
hi link Typedef		Type
hi link SpecialChar	Special
hi link Delimiter	Special
hi link SpecialComment	Special
hi link Debug		Special

