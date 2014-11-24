
# File completion
set filec

# limit descriptor 1024
limit coredumpsize 0

# History configuration
set histfile = $HOME/.history
set histdup  = erase
set ignoreeof
set savehist=40
set history=500
set savehist=(500 merge)

set new
set autolist = ambiguous
set listflags = -AF
set matchbeep = never
set printexitvalue
set notify

# Prompt before `rm *` is executed (if USER is set)
set rmstar

# list of directories in which cd should search
# for subdirectories
# if not present in current directory
set cdpath = (~ )


# Prompt
set prompt = "%{\033[1;39m%}%B%m%b%{\033[1;30m%}[%D.%W %P]%{\033[0m%} %{\033[1;34m%}%b%~%{\033[0m%} %B>%b "

