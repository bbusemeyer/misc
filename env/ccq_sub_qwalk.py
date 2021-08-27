#!/usr/bin/env python3
import subprocess as sub
import os

def main():
  import argparse
  import sys
  dft='(=%(default)s)'
  parser=argparse.ArgumentParser(sys.argv[0].split('/')[-1])
  parser.add_argument('inpfn',type=str,
      help='QWalk input to be submitted.')
  parser.add_argument('-np',default=12,type=int,
      help='Number of processors per node.'+dft)
  parser.add_argument('-nn',default=1,type=int,
      help='Number of nodes.'+dft)
  parser.add_argument('-t',dest='time',default='500:00:00',type=str,
      help='Time string.'+dft)
  parser.add_argument('-q',dest='queue',default='batch',type=str,
      help='Queue.'+dft)
  parser.add_argument('-l',dest='local',action='store_true',
      help='Run locally'+dft)
  args=parser.parse_args()

  qsub(nn=args.nn,np=args.np,time=args.time,inpfn=args.inpfn,queue=args.queue,local=args.local)

def qsub(inpfn,local=False,nn=1,np=12,time='1:00:00',queue='batch'):
  outlines = [
      "#!/bin/bash",
      "#PBS -l nodes=%d:ppn=%d"%(nn,np),
      "#PBS -l walltime=%s"%time,
      "#PBS -N %s"%inpfn,
      "#PBS -e $PBS_JOBID.err",
      "#PBS -o $PBS_JOBID.out",
      "#PBS -q %s"%queue,
      "cd %s"%os.getcwd(),
      "module purge",
      "module load gcc",
      "module load intel/mkl",
      "module load openmpi",
      "mpirun -n %d /mnt/home/bbusemeyer/bin/qwalk %s &> %s.out"%(nn*np,inpfn,inpfn),
    ]

  with open('qsub.in','w') as outf:
    outf.write('\n'.join(outlines))

  if local:
    print( sub.check_output("bash ./qsub.in",shell=True).decode() )
  else:
    raise NotImplementedError("Need to put slurm options in.")
    print( sub.check_output("sbatch ./qsub.in",shell=True).decode() )

if __name__=='__main__': main()
