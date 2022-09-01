#!/usr/bin/env python3

import argparse
import sys
import subprocess as sub
import os

def main():
  dft='(=%(default)s)'
  parser=argparse.ArgumentParser(sys.argv[0].split('/')[-1])
  parser.add_argument('inpfn',type=str,
      help='Input to be submitted.')
  parser.add_argument('-n',dest='nn',default=1,type=int,
      help='Number of nodes for MPI-enabled python scripts.'+dft)
  parser.add_argument('-t',dest='time',default='1:00:00',type=str,
      help='Time string.'+dft)
  parser.add_argument('-q',dest='queue',default='ccq,gen',type=str,
      help='Queue.'+dft)
  parser.add_argument('-l',dest='local',action='store_true',
      help='Run on the cluster'+dft)
  parser.add_argument('--ptype',dest='ptype',default=None,
      help='Processor type to enforce (skylake or broadwell).'+dft)
  parser.add_argument('-W','--wait',dest='wait',default=False,action='store_true',
      help='Wait for job to finish before returning.'+dft)
  parser.add_argument('-M','--modules',dest='extra_mods', default=[], nargs='+')
  args=parser.parse_args()

  ptype = args.ptype if args.ptype != 'none' else None

  qsub(inpfn=args.inpfn,nn=args.nn,time=args.time,queue=args.queue,ptype=ptype,wait=args.wait,extra_mods=args.extra_mods)

def qsub(inpfn,nn=1,time='1:00:00',queue='ccq,gen',ptype=None,local=False,wait=False,extra_mods=None):
  
  ptypeline = [f"#SBATCH -C {ptype}"]                     if ptype is not None else []
  waitline = ["#SBATCH -W"]                               if wait else []
  modlines = ["module purge"] + [f"module load {mod}" for mod in extra_mods] if extra_mods is not None else []

  outlines = [
      "#!/bin/bash",
      "#SBATCH --exclusive",
      "#SBATCH -N {}".format(nn),
      "#SBATCH -t {}".format(time),
      "#SBATCH -J {}".format(inpfn),
      "#SBATCH -p {}".format(queue),
      "#SBATCH -o {}".format("slurm-%j.out"),
    ] + ptypeline + waitline + modlines + [
      "module list",
      "cd {}".format(os.getcwd()),
     f"python3 -u {inpfn} &> {inpfn}.out",
   ]

  # Avoid script clashes.
  qfn, i = "qsub", 0
  while os.path.exists(qfn + str(i)): i += 1
  qfn = qfn + str(i)

  with open(qfn,'w') as outf:
    outf.write('\n'.join(outlines))

  if not local:
    print("Submitting python run.")
    print( sub.check_output(f"sbatch {qfn}",shell=True).decode() )
  else:
    print("Running job locally.")
    print( sub.check_output(f"bash {qfn}",shell=True).decode() )

if __name__=='__main__':main()
