" An example for a vimrc file.
"
"
" Maintainer:	Bram Moolenaar <Bram@vim.org>
" Last change:	2008 Dec 17
"
" To use it, copy it to
"     for Unix and OS/2:  ~/.vimrc
"	      for Amiga:  s:.vimrc
"  for MS-DOS and Win32:  $VIM\_vimrc
"	    for OpenVMS:  sys$login:.vimrc


"###########################################################
"########## Settings for Vundle to work. ###################
set nocompatible              " be iMproved, required
filetype off                  " required

" set the runtime path to include Vundle and initialize
set rtp+=~/.vim/bundle/Vundle.vim
call vundle#begin()
" alternatively, pass a path where Vundle should install plugins
"call vundle#begin('~/some/path/here')

" Julia syntax highlighting.
Plugin 'JuliaEditorSupport/julia-vim'
Plugin 'VundleVim/Vundle.vim'

" let Vundle manage Vundle, required
" You need to do `:PluginInstall syntastic` before uncommenting this line, I've found.
Plugin 'syntastic'

" The following are examples of different formats supported.
" Keep Plugin commands between vundle#begin/end.
" plugin on GitHub repo
" Plugin 'tpope/vim-fugitive'
" plugin from http://vim-scripts.org/vim/scripts.html
" Plugin 'L9'
" Git plugin not hosted on GitHub
" Plugin 'git://git.wincent.com/command-t.git'
" git repos on your local machine (i.e. when working on your own plugin)
" Plugin 'file:///home/gmarik/path/to/plugin'
" The sparkup vim script is in a subdirectory of this repo called vim.
" Pass the path to set the runtimepath properly.
" Plugin 'rstacruz/sparkup', {'rtp': 'vim/'}
" Install L9 and avoid a Naming conflict if you've already installed a
" different version somewhere else.
" Plugin 'ascenator/L9', {'name': 'newL9'}

" All of your Plugins must be added before the following line
call vundle#end()            " required
filetype plugin indent on    " required
" To ignore plugin indent changes, instead use:
"filetype plugin on
"
" Brief help
" :PluginList       - lists configured plugins
" :PluginInstall    - installs plugins; append `!` to update or just :PluginUpdate
" :PluginSearch foo - searches for foo; append `!` to refresh local cache
" :PluginClean      - confirms removal of unused plugins; append `!` to auto-approve removal
"
" see :h vundle for more details or wiki for FAQ
" Put your non-Plugin stuff after this line

" snakemake
au BufNewFile,BufRead Snakefile set syntax=snakemake
au BufNewFile,BufRead *.smk set syntax=snakemake

"########### End of settings for Vundle to work ############
"###########################################################
"
"###########################################################
"####### Syntatic settings #################################

" Recommended settings.
set statusline+=%#warningmsg#
set statusline+=%{SyntasticStatuslineFlag()}
set statusline+=%*

let g:syntastic_always_populate_loc_list = 1
let g:syntastic_auto_loc_list = 1
let g:syntastic_check_on_open = 1
let g:syntastic_check_on_wq = 0

" python3 mode.
let g:syntastic_python_python_exec = 'python3'
let g:syntastic_python_checkers = ['flake8']
let g:syntastic_quiet_messages = { "type": "style" }
" problem with includes.
"let g:syntastic_cpp_include_dirs = [ '../include', 'include','./include','/mnt/home/bbusemeyer/lib/afqmclab-gcc/include','/mnt/home/bbusemeyer/lib/gtest/include' ]
let g:syntastic_cpp_remove_include_errors=1

"####### End Syntatic settings #############################
"###########################################################

" When started as "evim", evim.vim will already have done these settings.
if v:progname =~? "evim"
  finish
endif

" Use Vim settings, rather than Vi settings (much better!).
" This must be first, because it changes other options as a side effect.
set nocompatible

" allow backspacing over everything in insert mode
set backspace=indent,eol,start


" Don't use Ex mode, use Q for formatting
map Q gq

" CTRL-U in insert mode deletes a lot.  Use CTRL-G u to first break undo,
" so that you can undo CTRL-U after inserting a line break.
inoremap <C-U> <C-G>u<C-U>

" In many terminal emulators the mouse works just fine, thus enable it.
if has('mouse')
  "set mouse=a
endif

" Switch syntax highlighting on, when the terminal has colors
" Also switch on highlighting the last used search pattern.
if &t_Co > 2 || has("gui_running")
  syntax on
  set hlsearch
endif

"autocmd BufWinLeave * mkview
"autocmd BufWinEnter * silent loadview 

" # Function to permanently delete views created by 'mkview'
function! MyDeleteView()
    let path = fnamemodify(bufname('%'),':p')
    " vim's odd =~ escaping for /
    let path = substitute(path, '=', '==', 'g')
    if empty($HOME)
    else
        let path = substitute(path, '^'.$HOME, '\~', '')
    endif
    let path = substitute(path, '/', '=+', 'g') . '='
    " view directory
    let path = &viewdir.'/'.path
    call delete(path)
    echo "Deleted: ".path
endfunction

" # Command Delview (and it's abbreviation 'delview')
command Delview call MyDeleteView()
" Lower-case user commands: http://vim.wikia.com/wiki/Replace_a_builtin_command_using_cabbrev
cabbrev delview <c-r>=(getcmdtype()==':' && getcmdpos()==1 ? 'Delview' : 'delview')<CR>

" Julia filetype detection.
if v:version < 704
  " NOTE: this line fixes an issue with the default system-wide lisp ftplugin
  "       which didn't define b:undo_ftplugin on older Vim versions
  "       (*.jl files are recognized as lisp)
  autocmd BufRead,BufNewFile *.jl    let b:undo_ftplugin = "setlocal comments< define< formatoptions< iskeyword< lisp<"
endif
autocmd BufRead,BufNewFile *.jl      set filetype=julia

set omnifunc=LaTeXtoUnicode#omnifunc

" Fix python fuck around.
function! SetupPython()
    " Here, you can have the final say on what is set.  So
    " fixup any settings you don't like.
    setlocal softtabstop=2
    setlocal tabstop=2
    setlocal shiftwidth=2
endfunction
command! -bar SetupPython call SetupPython()

filetype plugin indent on
autocmd FileType tex setlocal wrap spell
autocmd FileType text setlocal wrap spell
autocmd FileType markdown setlocal wrap spell

set nobackup
set nowrap         " turn off the fucking wrap around
set linebreak      " if the wrap around is on, don't break words
set history=50	   " keep 50 lines of command line history
set ruler		   " show the cursor position all the time
set showcmd		   " display incomplete commands
set incsearch	   " do incremental searching
set tabstop=2      " makes tabs of width 2
set shiftwidth=2   " indents by 2
set expandtab      " use spaces instead of tabs
set number         " numbers the lines
set wildmenu       " tab completion
set fdm=indent     " Folding mode
set tw=0           " Textwidth=0 means no width.
set t_Co=256       " Number of colors available.

set background=light
colorscheme mydelek
