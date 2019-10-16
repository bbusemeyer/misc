#!/usr/bin/env python3
import subprocess as sub
import os

def main():
  import argparse
  import sys
  dft='(=%(default)s)'
  parser=argparse.ArgumentParser(sys.argv[0].split('/')[-1])
  parser.add_argument('exe',type=str,
      help='Executible to be called. Follow %s.x pattern.')
  parser.add_argument('inpfn',type=str,
      help='Input to be submitted.')
  parser.add_argument('-t',dest='time',default='1:00:00',type=str,
      help='Time string.'+dft)
  parser.add_argument('-q',dest='queue',default='ccq',type=str,
      help='Queue.'+dft)
  parser.add_argument('-c',dest='cluster',action='store_true',
      help='Run on the cluster'+dft)
  args=parser.parse_args()

  qsub(exe=args.exe,time=args.time,inpfn=args.inpfn,queue=args.queue,cluster=args.cluster)

def qsub(inpfn,exe='pw',cluster=False,nn=1,time='1:00:00',queue='ccq'):
  assert nn==1,"Not tested for nn!=1."
  outlines = [
      "#!/bin/bash",
      "#SBATCH -N {}".format(nn),
      "#SBATCH --exclusive",
      "#SBATCH -t {}".format(time),
      "#SBATCH -J {}".format(inpfn),
      "#SBATCH -p {}".format(queue),
      "import sys",
      "import os",
      "cd %s"%os.getcwd(),
      "module purge",
      "module load intel",
      "module load intel/compiler",
      "module load intel/license",
      "module load intel/mkl",
      "module load intel/mpi",
      "mpirun /mnt/home/bbusemeyer/bin/%s.x < %s &> %s.out"%(exe,inpfn,inpfn),
    ]

  with open('qsub.in','w') as outf:
    outf.write('\n'.join(outlines))

  if cluster:
    print( sub.check_output("sbatch ./qsub.in",shell=True).decode() )
  else:
    print( sub.check_output("bash ./qsub.in",shell=True).decode() )

if __name__=='__main__': main()
