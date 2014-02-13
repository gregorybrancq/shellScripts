

amenu 80.110 &Perso.&Toggle\ Fold :call ToggleFold()<CR>
amenu 80.120 &Perso.Fold\ Options.Des&activate<Tab>zi zi<CR>
amenu 80.130 &Perso.Fold\ Options.De&velop<Tab>zR zR<CR>
amenu 80.140 &Perso.Fold\ Options.&Reduce<Tab>zM zM<CR>
amenu 80.199 &Perso.-SEP1- :

amenu 80.211 &Perso.&Tabstop.? :set tabstop=
amenu 80.212 &Perso.&Tabstop.4 :set tabstop=4<cr>
amenu 80.213 &Perso.&Tabstop.8 :set tabstop=8<cr>
amenu 80.221 &Perso.&Wrap.On  :set wrap<cr>:set guioptions+=b<cr>
amenu 80.222 &Perso.&Wrap.Off :set nowrap<cr>:set guioptions-=b<cr>
amenu 80.299 &Perso.-SEP2- :

amenu 80.301 &Perso.WinManager<Tab><c-e> <c-e><CR>
amenu 80.302 &Perso.Order\ the\ bufexplorer<Tab>s s<CR>
amenu 80.303 &Perso.Toggles\ the\ pathname<Tab>p p<CR>
amenu 80.399 &Perso.-SEP3- :

amenu 80.401 &Perso.TagList<Tab><c-t> <c-t><CR>
amenu 80.499 &Perso.-SEP4- :



fun ToggleFold()
	if (g:fold_enable == 1)
		:set nofoldenable
		:set foldcolumn=0
		let g:fold_enable=0
	else
		:set foldenable
		:set foldcolumn=5
		let g:fold_enable=1
	endif
endfun
