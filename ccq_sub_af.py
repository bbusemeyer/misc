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
  parser.add_argument('-nn',dest='nn',default=1,type=int,
      help='Number of nodes.'+dft)
  parser.add_argument('-ppn',dest='ppn',default='all',
      help='Number of procs per node.'+dft)
  parser.add_argument('-t',dest='time',default='1:00:00',type=str,
      help='Time string.'+dft)
  parser.add_argument('-q',dest='queue',default='ccq',type=str,
      help='Queue.'+dft)
  parser.add_argument('-l',dest='local',action='store_true',
      help='Run locally.'+dft)
  parser.add_argument('-nk',dest='nk',default=1,type=int,
      help='Number of QE "pools" corresponding to division of kpoints.'+dft)
  parser.add_argument('-ni',dest='ni',default=1,type=int,
      help='Number of QE "images" corresponding to division of phonon qpoints.'+dft)
  parser.add_argument('-C','--ptype',dest='ptype',default='skylake',type=str,
      help='Processor type to enforce (skylake, broadwell, or rome), "any" will allow any.'+dft)
  args=parser.parse_args()

  qsub(exe=args.exe,time=args.time,queue=args.queue,local=args.local,nn=args.nn,ppn=args.ppn,ptype=args.ptype)

def qsub(exe='afqmc-srsu',local=False,nn=1,ppn='all',time='1:00:00',queue='ccq',ptype='skylake',preempt=False,jobname=None,wait=False):
  if ppn != 'all': ppn = int(ppn)
  ptypeline = [f"#SBATCH -C {ptype}"] if ptype != 'any' else []
  waitline = ["#SBATCH -W"] if wait else []
  npopt = f"-np {nn*ppn}" if ppn!="all" else ''


  if jobname is None: jobname = exe
  outlines = [
      "#!/bin/bash",
      f"#SBATCH -N {nn}",
      "#SBATCH --exclusive",
      f"#SBATCH -t {time}",
      f"#SBATCH -J {jobname}",
      f"#SBATCH -p {queue}",
      ] + ptypeline + waitline + [
      "cd %s"%os.getcwd(),
       "export AFQMCLAB_DIR=\"${HOME}/lib/afqmclab-gcc\"",
      "module purge",
      "module load slurm gcc cmake openmpi/1.10.7-hfi intel/mkl/2017-4 python3 lib/hdf5/1.8.21 lib/gmp/6.1.2 lib/fftw3/3.3.8",
      f"mpirun {npopt} ${{HOME}}/bin/{exe} &> {exe}.out",
    ]

  with open('qsub','w') as outf:
    outf.write('\n'.join(outlines))

  if local:
    stdout = sub.check_output("bash ./qsub",shell=True).decode() 
  else:
    stdout = sub.check_output("sbatch ./qsub",shell=True).decode()

  print(stdout)

  return stdout

if __name__=='__main__': main()
