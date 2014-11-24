

##
## Gestion de la couleur pour 'ls' (exportation de LS_COLORS)
##

if ($?TERM) then
    if ($TERM == dumb) then
        set ls_options=""
    else
        set ls_options="--color"
    endif

    #eval `dircolors -c ~/.dircolors`
    alias ls 'ls'
    alias l  'ls -F $ls_options'
    alias ll 'ls -alFh $ls_options'
    alias lt 'ls -rtalFh $ls_options'
    alias lS 'ls -rtalFhS $ls_options'
    alias c  'ls -lF $ls_options'
    alias d  'ls -AF $ls_options'
endif


##
## Basic
##

alias cp         'cp'
alias mv         'mv'
alias rm         'rm -f'
alias pwd        'echo $cwd'
alias h          'history'
alias .          'clear;echo $cwd'
alias ap         'cd ..;echo $cwd'
alias app        'cd ../..;echo $cwd'
alias appp       'cd ../../..;echo $cwd'
alias apppp      'cd ../../../..;echo $cwd'
alias appppp     'cd ../../../../..;echo $cwd'
alias apppppp    'cd ../../../../../..;echo $cwd'
alias appppppp   'cd ../../../../../../..;echo $cwd'
alias apppppppp  'cd ../../../../../../../..;echo $cwd'
alias appppppppp 'cd ../../../../../../../../..;echo $cwd'
alias m          'more'
alias j          'jobs -l'
alias ki         'kill -9 \!*'

alias duS        'du -H --max-depth=1 | sort -h -r'

alias dt         "date '+DATE: %d/%m/%y%nTIME: %H:%M:%S'"
alias so         'source'
alias xx         'exit'

alias rmswp      'find -type f -name ".*.sw*" -exec rm -f {} \;'
alias rmsvn      'find -name ".svn" -exec rm -fr {} \;'
alias rmasic     'find -type l -name "ASIC" | xargs rm'
alias rmpyc      'find -type f -name "*.pyc" | xargs rm'

alias grepm      'grep -rsiH \!*'


##
## Process
##

alias pss        'ps -edf | grep greg | more'
alias psh        'ps -eo pcpu,args | sort -rn | head'
alias pst        'pss | grep firefox | grep -v grep; pss | grep thunder | grep -v grep; pss | grep skype | grep -v grep'
alias psnx       'pss | grep nx | grep -v grep'


##
## Prog
##

alias fr         'setxkbmap fr'
alias lp2p       'a2ps -s duplex'

alias v          'vim -g -geom 100x50 \!*'

alias tk         'tkdiff \!*'
alias tkg        'git tkdiff \!*'
alias tkgc       'git tkdiffc \!*'

alias it        'install_tools \!*'

## Webex
alias webex     'setenv LD_LIBRARY_PATH "/opt/java/jre-8u25_i586/lib/i386:/opt/java/jre-8u25_i586/lib/i386/client"; linux32 firefox'


##
## GIT
##

alias gsta      'git status \!*'
alias gst       'git status -uno \!*'
alias gci       'git commit -m \!*'
alias glog      'git log --name-status \!*'


##
## Machine
##

alias ss         'ssh -X \!*'
alias login      'rlogin $HOST -l'

alias ssp        'ssh -X gregory@portable'
alias ssc        'ssh -X gregory@chablis'
alias ssk        'ssh -X gregory@kenny'
alias ssz        'ssh -X gregory@mazis'
alias ssf        'ssh -Y fpga@kenny'
alias sse        'ssh -Y edatools@kenny'



