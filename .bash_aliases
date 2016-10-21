alias less='less -r'       # raw control characters
alias whence='type -a'     # where, of a sort
alias grep='grep --color'  # show differences in colour
alias l='less -r'
alias R='R -q'
alias mkddir='mkdir `date "+%F"`'
alias py='python3 -u'
alias py2='python2 -u'
alias rm='rm -i'
alias tra='trash'
#alias python='python3 -u'
alias gpp='g++'
alias tp='trash-put'
alias tarp='tar --use-compress-program=pigz'
alias backupto='rsync -aui --delete ~/Desktop ~/Pictures ~/Documents ~/programs ~/Music ~/projects ~/tools ~/bin ~/.bash* ~/.vim ~/.*rc'
alias mcrypt='mcrypt -u'
alias ppl='python ~/tools/plotter.py'
alias rsync='rsync --progress'
alias qs='qstat -a'
alias notebook="google-chrome; jupyter notebook"
alias update="sudo apt-get update; sudo apt-get dist-upgrade; sudo apt-get autoremove"

# Spelling fixes.
alias dc="sl"

# tools shortcuts
alias rr='~/tools/record_run.sh'
alias pssh='~/tools/physics_ssh.sh'
alias pscp='~/tools/physics_scp.sh'
alias psftp='~/tools/physics_sftp.sh'
alias cssh='~/tools/cs_ssh.sh'
alias cscp='~/tools/cs_scp.sh'
alias csftp='~/tools/cs_sftp.sh'
alias ry='~/tools/recycle.sh'

# git shortcuts.
alias gs='git status'
alias gc='git commit'
alias gp='git push'
alias ga='git add'

# Globus Endpoints.
gmira='alcf#dtn_mira'
gtaub='illinois#iccp'
glap='busemey2#laptop'

# Ma's local ip's
desktop2='192.168.2.102'

# Lucas's office computer:
hawk='busemey2@hawk.physics.illinois.edu'
# Taub supercomputer
taub='busemey2@taub.campuscluster.illinois.edu'
# Office computer 
#ver='brian@veritas.physics.illinois.edu'
ver='brian@128.174.249.177'
# Argonne Mira supercomputer.
mira='busemey@mira.alcf.anl.gov'
# Globus CLI
glob='busemey2@cli.globusonline.org'

backuplist='./Desktop ./Pictures ./Documents ./homework ./programs ./Music ./projects ./tools ./.bash* ./.*rc .matplotlib/'
