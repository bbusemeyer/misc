alias less='less -r'       # raw control characters
alias whence='type -a'     # where, of a sort
alias grep='grep --color'  # show differences in colour
alias l='less -r'
alias R='R -q'
alias mkddir='mkdir `date "+%F"`'
alias py='python'
alias gpp='g++'
alias tp='trash-put'
alias tarp='tar --use-compress-program=pigz'
alias backupto='rsync -aui --delete ~/Desktop ~/Pictures ~/Documents ~/programs ~/Music ~/projects ~/tools ~/bin ~/.bash* ~/.vim ~/.*rc ~/.matplotlib'
alias mcrypt='mcrypt -u'
alias ppl='python ~/tools/plotter.py'

# tools shortcuts
alias rr='~/tools/record_run.sh'
alias pssh='~/tools/physics_ssh.sh'
alias pscp='~/tools/physics_scp.sh'
alias psftp='~/tools/physics_sftp.sh'
alias cssh='~/tools/cs_ssh.sh'
alias cscp='~/tools/cs_scp.sh'
alias csftp='~/tools/cs_sftp.sh'
alias ry='~/tools/recycle.sh'

# Ma's local ip's
desktop2='192.168.2.102'

# Dr. Wagner's office computer:
hawk='busemey2@hawk.physics.illinois.edu'
# Taub supercomputer
taub='busemey2@taub.campuscluster.illinois.edu'
# Office computer 
ver='brian@veritas.physics.illinois.edu'
# Argonne Mira supercomputer.
mira='busemey@mira.alcf.anl.gov'

backuplist='./Desktop ./Pictures ./Documents ./homework ./programs ./Music ./projects ./tools ./.bash* ./.*rc .matplotlib/ .vim/'
