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
  parser.add_argument('-q',dest='queue',default='general',type=str,
      help='Queue.'+dft)
  parser.add_argument('-l',dest='local',action='store_true',
      help='Run on the cluster'+dft)
  parser.add_argument('--ptype',dest='ptype',default=None,
      help='Processor type to enforce (skylake or broadwell).'+dft)
  parser.add_argument('-W','--wait',dest='wait',default=False,action='store_true',
      help='Wait for job to finish before returning.'+dft)
  args=parser.parse_args()

  qsub(inpfn=args.inpfn,nn=args.nn,time=args.time,queue=args.queue,ptype=args.ptype,wait=args.wait)

def qsub(inpfn,nn=1,time='1:00:00',queue='general',ptype=None,local=False,wait=False):

  ptypeline = [f"#SBATCH -C {ptype}"] if ptype is not None else []
  waitline = ["#SBATCH -W"] if wait else []

  if nn > 1:
    exelines = [
        "module load openmpi",
        "export OMP_NUM_THREADS 1",
        f"mpirun python3 -u {inpfn} &> {inpfn}.out"
      ]
  else:
    exelines = [f"python3 -u {inpfn} &> {inpfn}.out"]

  outlines = [
      "#!/bin/bash",
      "#SBATCH --exclusive",
      "#SBATCH -N {}".format(nn),
      "#SBATCH -t {}".format(time),
      "#SBATCH -J {}".format(inpfn),
      "#SBATCH -p {}".format(queue),
      "#SBATCH -o {}".format("slurm-%j.out"),
    ] + ptypeline + waitline + [
      "cd {}".format(os.getcwd()),
      "export PYTHONPATH={}".format(':'.join(sys.path)),
      "# These lines enable MKL for PySCF.",
      "module purge",
      "module load cmake slurm",
      "module load intel/mkl/2020",
      "export LD_PRELOAD=$MKLROOT/lib/intel64/libmkl_def.so:$MKLROOT/lib/intel64/libmkl_sequential.so:$MKLROOT/lib/intel64/libmkl_core.so",
      "module load gcc",
      "module load python3/3.7.3",
    ] + exelines

  qfn = "qsub"
  with open(qfn,'w') as outf:
    outf.write('\n'.join(outlines))

  if not local:
    print("Submitting python run.")
    print( sub.check_output(f"sbatch {qfn}",shell=True).decode() )
  else:
    print("Running job locally.")
    print( sub.check_output(f"bash {qfn}",shell=True) )

if __name__=='__main__':main()
