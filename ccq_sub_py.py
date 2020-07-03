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
  parser.add_argument('-t',dest='time',default='1:00:00',type=str,
      help='Time string.'+dft)
  parser.add_argument('-q',dest='queue',default='gen',type=str,
      help='Queue.'+dft)
  parser.add_argument('-l',dest='local',action='store_true',
      help='Run on the cluster'+dft)
  parser.add_argument('--ptype',dest='ptype',default=None,
      help='Processor type to enforce (skylake or broadwell).'+dft)
  args=parser.parse_args()

  qsub(time=args.time,inpfn=args.inpfn,queue=args.queue,ptype=args.ptype)

def qsub(inpfn,time='1:00:00',queue='gen',ptype=None):
  ptypeline = [f"#SBATCH -C {ptype}"] if ptype is not None else []
  outlines = [
      "#!/bin/bash",
      "#SBATCH --exclusive",
      "#SBATCH -N 1",
      "#SBATCH -t {}".format(time),
      "#SBATCH -J {}".format(inpfn),
      "#SBATCH -p {}".format(queue),
    ] + ptypeline + [
      "cd {}".format(os.getcwd()),
      "export PYTHONPATH={}".format(':'.join(sys.path)),
      "python3 -u {} &> {}.out".format(inpfn,inpfn)
    ]

  with open('qsub','w') as outf:
    outf.write('\n'.join(outlines))

  print("Submitting python run.")
  print( sub.check_output("sbatch ./qsub",shell=True).decode() )

if __name__=='__main__':main()
