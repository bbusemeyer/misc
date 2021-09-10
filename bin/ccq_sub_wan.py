#!/usr/bin/env python3
import subprocess as sub
import os

def main():
  import argparse
  import sys
  dft='(=%(default)s)'
  parser=argparse.ArgumentParser(sys.argv[0].split('/')[-1])
  parser.add_argument('inpfn',type=str,
      help='PW input to be submitted.')
  parser.add_argument('-np',default=12,type=int,
      help='Number of processors per node.'+dft)
  parser.add_argument('-nn',default=1,type=int,
      help='Number of nodes.'+dft)
  parser.add_argument('-t',dest='time',default='500:00:00',type=str,
      help='Time string.'+dft)
  parser.add_argument('-q',dest='queue',default='batch',type=str,
      help='Queue.'+dft)
  parser.add_argument('-c',dest='cluster',action='store_true',
      help='Run on the cluster'+dft)
  args=parser.parse_args()
  parser.add_argument('-pp',dest='pp',action='store_true',
      help='Pre-processing flag for Wannier90.'+dft)

  qsub(nn=args.nn,np=args.np,time=args.time,inpfn=args.inpfn,queue=args.queue,cluster=args.cluster,pp=args.pp)

def qsub(inpfn,pp=False,cluster=False,nn=1,np=12,time='1:00:00',queue='batch'):
  if pp: flags = '-pp'
  else: flags = ''
  outlines = [
      "#!/bin/bash",
      "cd %s"%os.getcwd(),
      "module purge",
      "module load intel",
      "module load intel/compiler",
      "module load intel/license",
      "module load intel/mkl",
      "module load intel/mpi",
      "mpirun -n %d /mnt/home/bbusemeyer/bin/wannier90.x %s %s &> %s.out"%(nn*np,flags,inpfn,inpfn),
    ]

  with open('qsub.in','w') as outf:
    outf.write('\n'.join(outlines))

  if cluster:
    print( sub.check_output("sbatch ./qsub.in",shell=True).decode() )
  else:
    print( sub.check_output("bash ./qsub.in",shell=True).decode() )

if __name__=='__main__': main()
