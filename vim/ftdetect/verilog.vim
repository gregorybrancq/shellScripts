" Vim syntax file
" Language:	Verilog
" Maintainer:	Mun Johl <mj@core.rose.hp.com>
" Last Update:  Fri Feb 20 08:47:46 PST 1998

" Remove any old syntax stuff hanging around
syn clear

" A bunch of useful Verilog keywords
syn keyword verilogStatement   disable assign deassign force release
syn keyword verilogStatement   parameter function endfunction
syn keyword verilogStatement   always initial module endmodule or
syn keyword verilogStatement   task endtask
syn keyword verilogStatement   input output inout reg wire time
syn keyword verilogStatement   posedge negedge wait
syn keyword verilogStatement   buf pullup pull0 pull1 pulldown
syn keyword verilogStatement   tri0 tri1 tri trireg
syn keyword verilogStatement   wand wor triand trior
syn keyword verilogStatement   defparam
syn keyword verilogStatement   integer real
syn keyword verilogLabel       begin end fork join
syn keyword verilogConditional if else case casex casez default endcase
"syn keyword verilogConditional   ? :
syn keyword verilogRepeat        forever repeat while for
"syn keyword verilogUnaryOperator ! ~ & ~& | ^| ^ ~^
"syn keyword verilogBinaryOperator + - * / % == != === !== && || < <= > >=
"syn keyword verilogBinaryOperator >> << ^~/rhome/ogu/vim/verilog.vim

syn keyword verilogTodo contained TODO

syn match   verilogOperator "[&|~><!)(*#%@+/=?:;}{,.\^\-\[\]]"

syn region  verilogComment start="/\*" end="\*/"
syn match   verilogComment "//.*"

syn match   verilogDefine "`[a-zA-Z0-9_]\+\>"
syn match   verilogGlobal "$[a-zA-Z0-9_]\+\>"

syn match   verilogConstant "\<[A-Z][A-Z0-9_]\+\>"

syn match   verilogNumber "\(\<[0-9]\+\|\)'[bdh][0-9a-fxzA-F]\+\>"
syn match   verilogNumber "\<[+-]\=[0-9]\+\>"

syn region  verilogString start=+"+  end=+"+
"Modify the following as needed.  The trade-off is performance versus
"functionality.
syn sync lines=50

if !exists("did_verilog_syntax_inits")
  let did_verilog_syntax_inits = 1
 " The default methods for highlighting.  Can be overridden later

  hi link verilogCharacter       Character
  hi link verilogConditional     Conditional
  hi link verilogRepeat          Repeat
  hi link verilogString          String
  hi link verilogTodo            Todo

  hi link verilogComment   Comment
  hi link verilogConstant  Todo
  hi link verilogLabel     PreCondit
  hi link verilogNumber    Special
  hi link verilogOperator  Type
  hi link verilogStatement Statement
  hi link verilogGlobal    PreProc
  hi link verilogDefine    Define
endif

let b:com_begin ='//'
let b:com_end =''
let b:unc_begin ='//*'
let b:unc_end =''


let b:current_syntax = "verilog"



so ~/.vim/ftdetect/verilog_explorer.vim
so ~/.vim/ftdetect/verilog_indent.vim


"insertion d'un commentaire sous forme de cadre : alt-c
":map ã o0i   //********************************************************************o0i   //*                                                                  *o0i   //********************************************************************k_4lR
":iab al always @) yyp_d$i      beginyyp_cwendkyyp_cw  if yyp_cwelseyyp_cw  kkyyp_cw  k$a()kk0t)a
":iab ac always @() yyp_d$i      beginyyp_cwendkyyp_cw  if yyp_cwelseyyp_cw  kkyyp_cw k$s(~resetn)kk0t(laposedge clk_fir or negedge resetnjjj$s
":iab sm always @) yyp_d$i      beginyyp_cwendkyyp_cw  case (_state)^yyp_Daendcaseyykp_cw      S_	: beginyypp_Dadefault   : _next_state <=  ;k_cw     Wdwxcw  endyykp_cw  if ()yyp_Daelseyykp_Da   _next_state <=  ;yyjpkkkkkkk0t)a
":iab be beginyypp_cwendk_cw 
":iab ie if )yyppp_Da   k_Daelsek_Da   k0t)a
":iab ca case )yyppp_Daendcasek_Da   defaultk_Da   k0t)a
":iab cx casex )yyppp_Daendcasek_Da   defaultk_Da   k0t)a
":iab //a //********************************************************************
":iab //b //*                                                                  *0lllR
":iab //c //********************************************************************kyypO//*                                                                  *0lllR
":iab mo moduleyyp_Daendmodulekk$a
":iab pa parameter
":iab ne negedge
":iab po posedge
":iab as assign
":iab in input
":iab ou output
":iab wi wire
":iab if if )ha
":ab sig2inst so ~/vim/sig_to_inst.vim
" Fonctions speciales pour Verilog
" Add register declaration
":map r lbve"ry?^reg oreg          "rpA;
" Add wire declaration
":map w lbve"ry?^wireowire         "rpA;
" Add bus register declaration
":map br lbve"ry?^reg oreg [x:x]   "rpA;j/x:x
" Add bus wire declaration
":map bw lbve"ry?^wireowire [x:x]   "rpA;j/x:x

