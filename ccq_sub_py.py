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
  parser.add_argument('-q',dest='queue',default='gen',type=str,
      help='Queue.'+dft)
  parser.add_argument('-l',dest='local',action='store_true',
      help='Run on the cluster'+dft)
  parser.add_argument('--ptype',dest='ptype',default=None,
      help='Processor type to enforce (skylake or broadwell).'+dft)
  args=parser.parse_args()

  qsub(inpfn=args.inpfn,nn=args.nn,time=args.time,queue=args.queue,ptype=args.ptype)

def qsub(inpfn,nn=1,time='1:00:00',queue='gen',ptype=None,local=False):

  ptypeline = [f"#SBATCH -C {ptype}"] if ptype is not None else []

  if nn > 1:
    exelines = [
        "module load openmpi",
        "export OMP_NUM_THREADS 1",
        "mpirun python3 -u {inp} &> {inp}.out".format(inp=inpfn),
      ]
  else:
    exelines = ["python3 -u {inp} &> {inp}.out".format(inp=inpfn)]

  outlines = [
      "#!/bin/bash",
      "#SBATCH --exclusive",
      "#SBATCH -N {}".format(nn),
      "#SBATCH -t {}".format(time),
      "#SBATCH -J {}".format(inpfn),
      "#SBATCH -p {}".format(queue),
    ] + ptypeline + [
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

  with open('qsub','w') as outf:
    outf.write('\n'.join(outlines))

  if not local:
    print("Submitting python run.")
    print( sub.check_output("sbatch ./qsub",shell=True).decode() )
  else:
    print("Running job locally.")
    print( sub.check_output("bash ./qsub",shell=True) )

if __name__=='__main__':main()
