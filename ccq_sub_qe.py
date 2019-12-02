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
  parser.add_argument('-nn',dest='nn',default=1,type=int,
      help='Number of nodes.'+dft)
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
  parser.add_argument('--ptype',dest='ptype',default=None,
      help='Processor type to enforce (skylake or broadwell).'+dft)
  args=parser.parse_args()

  qsub(exe=args.exe,time=args.time,inpfn=args.inpfn,queue=args.queue,local=args.local,nn=args.nn,nk=args.nk,ni=args.ni,ptype=args.ptype)

def qsub(inpfn,exe='pw',local=False,nn=1,time='1:00:00',queue='ccq',nk=1,ni=1,ptype=None):
  ptypeline = [f"#SBATCH -C {ptype}"] if ptype is not None else []
  outlines = [
      f"#!/bin/bash",
      f"#SBATCH -N {nn}",
      f"#SBATCH --exclusive",
      f"#SBATCH -t {time}",
      f"#SBATCH -J {inpfn}",
      f"#SBATCH -p {queue}",
      f"#SBATCH -o {inpfn}.out",
      f"#SBATCH -e {inpfn}.out",
    ] + ptypeline + [
      f"cd %s"%os.getcwd(),
      f"module purge",
      f"module load slurm gcc openmpi2 lib/fftw3/3.3.8-openmpi2 intel/mkl",
      f"mpirun /mnt/home/bbusemeyer/bin/{exe}.x -input {inpfn} -nk {nk} -ni {ni}"
    ]

  with open('qsub.in','w') as outf:
    outf.write('\n'.join(outlines))

  if local:
    print( sub.check_output("bash ./qsub.in",shell=True).decode() )
  else:
    print( sub.check_output("sbatch ./qsub.in",shell=True).decode() )

if __name__=='__main__': main()
