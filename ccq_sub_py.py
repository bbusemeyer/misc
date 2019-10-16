
import argparse
import sys

def main():
  dft='(=%(default)s)'
  parser=argparse.ArgumentParser(sys.argv[0].split('/')[-1])
  parser.add_argument('inpfn',type=str,
      help='Input to be submitted.')
  parser.add_argument('-np',default=12,type=int,
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
      "#SBATCH -N {}".format(nnode),
      "#SBATCH --exclusive",
      "#SBATCH -t {}".format(time),
      "#SBATCH -J {}".format(loc),
      "#SBATCH -p ccq",
      "#SBATCH -o qsub.py.out",
      "#SBATCH -e qsub.py.out",
      "os.chdir('{}')".format(os.getcwd()+'/'+loc),
      "sys.path = {}".format(['.']+sys.path), 
      "# End of sbatch header.",
      "",
    ]

  with open('qsub.py','w') as outf:
    outf.write('\n'.join(outlines))
    outf.write(open(inpfn,'r').read())

  if local:
    print( sub.check_output("python3 ./qsub.py &> qsub.py.out",shell=True).decode() )
  else:
    print( sub.check_output("sbatch ./qsub.in",shell=True).decode() )

if __name__=='__main__':main()
