#!/usr/bin/env python3

import argparse
import sys
import os
import subprocess as sub

def main():
  dft='(=%(default)s)'
  parser=argparse.ArgumentParser(sys.argv[0].split('/')[-1])
  parser.add_argument('inpfn',type=str,
      help='Input to be submitted.')
  parser.add_argument('-t',dest='time',default='1:00:00',type=str,
      help='Time string.'+dft)
  parser.add_argument('-q',dest='queue',default='ccq',type=str,
      help='Queue.'+dft)
  parser.add_argument('-l',dest='local',action='store_true',
      help='Run on the cluster'+dft)
  args=parser.parse_args()

  qsub(time=args.time,inpfn=args.inpfn,queue=args.queue,local=args.local)

def qsub(inpfn,local=False,time='1:00:00',queue='ccq'):
  outlines = [
      "#!/usr/bin/env python3",
      "##################################",
      "#SBATCH --exclusive",
      "#SBATCH -N 1",
      "#SBATCH -t {}".format(time),
      "#SBATCH -J {}".format(inpfn),
      "#SBATCH -p ccq",
      "#SBATCH -o qsub.py.out",
      "#SBATCH -e qsub.py.out",
      "import os,sys",
      "os.chdir('{}')".format(os.getcwd()),
      "sys.path = {}".format(['.']+sys.path), 
      "# End of sbatch header.",
      "##################################",
      "",
    ]

  with open('qsub.py','w') as outf:
    outf.write('\n'.join(outlines))
    outf.write(open(inpfn,'r').read())

  if local:
    print( sub.check_output("python3 ./qsub.py &> qsub.py.out",shell=True).decode() )
  else:
    print( sub.check_output("sbatch ./qsub.py",shell=True).decode() )

if __name__=='__main__':main()
