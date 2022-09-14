import argparse

import sage.all
from sage.misc.flatten import flatten
from sage.misc.randstate import set_random_seed
from sage.stats.basic_stats import mean

import saes
from config import BRED, BRES, FC, FR, reload
from saes import AES


seed = set_random_seed()

reload("config", "BRED", "BRES", "FC", "FR", "BG")
reload("saes", "AES")


def adjust_mem(mem):
    return f'{mem} MB' if mem < 1_000 else f'{round(mem / 1_000, 2)} GB'


def print_time(t, k):
    if k == 'guess_keys' and 'frequency' in t:
        print(f'{FC}Time of "{k}": {t[k] - t["frequency"]}{FR}', sep='\n')
        return

    try:
        print(f'{FC}Time of "{k}": {t[k]}{FR}', sep='\n')
    except KeyError:
        pass


parser = argparse.ArgumentParser()
parser.add_argument('-i', action='store_true')  # Dummy arg.
parser.add_argument('-n', type=int, default=1, choices=range(1, 11))
parser.add_argument('-r', type=int, default=2, choices=[1, 2, 4])
parser.add_argument('-c', type=int, default=2, choices=[1, 2, 4])
parser.add_argument('-e', type=int, default=4, choices=[4, 8])

parser.add_argument('--meth', type=str, default='subs', choices=['subs', 'ANF', 'fgb'])
parser.add_argument('--num', type=int, default=1)
parser.add_argument('--min', type=int, default=1)
parser.add_argument('--guess', type=int, default=0)
parser.add_argument('--wexp', type=int, default=0)
parser.add_argument('--red', default=False, action='store_true')
parser.add_argument('--rev', default=False, action='store_true')
parser.add_argument('--rnd', default=False, action='store_true')
parser.add_argument('--sim', default=False, action='store_true')
parser.add_argument('--sat', default=False, action='store_true')
parser.add_argument('--aux', default=False, action='store_true')
parser.add_argument('--dry', default=False, action='store_true')
parser.add_argument('--sep', default=False, action='store_true')
parser.add_argument('--ml', default=False, action='store_true')
parser.add_argument('--mlmeth', type=str, default='PAM', choices=['PAM', 'MSM', 'LSH'])
parser.add_argument('--psets', type=int, default=1)
parser.add_argument('--fstore', default=False, action='store_true')
parser.add_argument('--fload', default=False, action='store_true')
parser.add_argument('--fname', type=str, default='../in/data.txt')

args = parser.parse_args()

aes = AES(n=args.n, r=args.r, c=args.c, e=args.e)
print(f"{FC}Cipher: {aes}{FR}")

if args.aux:
    ps = aes.ps_aux_vars(n=args.num, sim=args.sim)
    print_time(aes.time_log(), 'ps_aux_vars')
else:
    if args.red:
        ps = aes.ps_red(ps_min=args.min,
                        ps_num=args.num,
                        meth=args.meth,
                        sim=args.sim)
        print_time(aes.time_log(), 'ps_red')
    else:
		## default branch
        ps = aes.ps_key_vars(n=args.num, sim=args.sim, meth=args.meth, fstore=args.fstore, fload=args.fload, fname=args.fname)
        print_time(aes.time_log(), 'ps_key_vars')
        if args.ml:
            firstl_txt,pil_txt,lastl_txt, pol_count, avg_pol_len, avg_mon_len = aes.ps_reduce_ml(ps, meth=args.mlmeth, num=args.num, psets=args.psets)
            print_time(aes.time_log(), 'ps_reduce_ml')
        else:
            firstl_txt=""
            pil_txt=""
            lastl_txt=""


print(f'{FC}Variables: {len(ps.vars)}{FR}')
if args.ml:
    print(f'{FC}Polynomials: {pol_count}{FR}')
    print(f'{FC}Avg length of polys: '
          f'{avg_pol_len}{FR}')
    print(f'{FC}Avg length of monomials: '
          f'{avg_mon_len}{FR}')
else:
    polys = flatten(ps.polys)
    print(f'{FC}Polynomials: {len(polys)}{FR}')
    print(f'{FC}Avg length of polys: '
          f'{round(mean([len(p) for p in polys]))}{FR}')
    print(f'{FC}Avg length of monomials: '
          f'{round(mean([m.deg() for p in polys for m in p.monomials()]))}{FR}')



if args.dry:
    exit()

if args.sat:
    print('Solver: SAT')
    if args.guess:
        keys = ps.guess_keys(guess=args.guess,
                             w_exp=args.wexp,
                             rnd=args.rnd,
                             reverse=args.rev)
        print_time(ps.time_log(), 'frequency')
    else:
        keys = ps.keys()
else:
    print('Solver: F4')
    if args.guess:
        keys = ps.guess_keys(guess=args.guess,
                             w_exp=args.wexp,
                             rnd=args.rnd,
                             reverse=args.rev,
                             meth='magma')
        print_time(ps.time_log(), 'frequency')
    else:
        ## default branch
        if args.sep:
            ml_gb = ps.magma_ml(firstl_txt,pil_txt,lastl_txt)
            print_time(ps.time_log(), 'magma_ml')
        else:
            ml_gb=[]
        keys = ps.keys(ml_gb, firstl_txt,pil_txt,lastl_txt, meth='magma', ml=args.ml, sep=args.sep)

    print(f'{FC}Used memory: {adjust_mem(ps.mem)}.{FR}')

if args.guess:
    print_time(ps.time_log(), 'guess_keys')
else:
    print_time(ps.time_log(), 'keys')

if not flatten(keys):
    print(f"{BRED}No valid keys found.{BRES}")
