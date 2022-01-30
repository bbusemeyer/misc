" Vim color file
" Maintainer:	Bram Moolenaar <Bram@vim.org>
" Last Change:	2001 Jul 23

" This is the default color scheme.  It doesn't define the Normal
" highlighting, it uses whatever the colors used to be.

" Set 'background' back to the default.  The value can't always be estimated
" and is then guessed.
hi clear Normal
set bg&

" Remove all existing highlighting and set the defaults.
hi clear

" Load the syntax highlighting defaults, if it's enabled.
if exists("syntax_on")
  syntax reset
endif

let colors_name = "mydefault"

hi Folded term=standout ctermfg=7 ctermbg=235 guifg=DarkBlue guibg=LightGrey
hi SpellBad term=reverse ctermbg=1 gui=undercurl guisp=Red
hi SpellCap term=reverse ctermbg=4 gui=undercurl guisp=Blue
hi Special term=bold ctermfg=219 guifg=Orange

" vim: sw=2
