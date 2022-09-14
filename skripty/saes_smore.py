"""Scalable AES and its polynomial systems."""

from __future__ import annotations

import itertools
from ast import literal_eval
from functools import reduce

from brial import *
from sage.all import *
from sage.crypto.boolean_function import BooleanFunction as BoolFun
from sage.crypto.mq import sr
from sage.misc.flatten import flatten
from sage.misc.prandom import randint, randrange, sample, shuffle
from sage.parallel.decorate import parallel
from sage.rings.finite_rings.finite_field_constructor import GF
from sage.rings.polynomial import pbori
from sage.rings.polynomial.pbori import BooleanMonomial, BooleanPolynomial
from sage.rings.polynomial.pbori import BooleanPolynomialIdeal as BPIdeal
from sage.rings.polynomial.polynomial_ring_constructor import \
    BooleanPolynomialRing_constructor as BPRing
from sage.rings.polynomial.polynomial_ring_constructor import PolynomialRing


from config import (BG, BRES, FC, FILE_OUTPUT, FR, KEY_LIMIT, NCPUS,
                    PRINT_DETAILS, PT_LIMIT, reload, Timer)

reload('config', 'BG', 'BRES', 'FC', 'FR')
reload('config', 'FILE_OUTPUT', 'KEY_LIMIT', 'PT_LIMIT', 'PRINT_DETAILS',
       'NCPUS')


class Addict(dict):
    def __add__(self, b):
        return Addict(
            {k: self.get(k, 0) + b.get(k, 0)
             for k in set(self) | set(b)})

    def key_sort(self, rev=True):
        return Addict(
            [i for i in sorted(self.items(), key=lambda i: i[0], reverse=rev)])

    def val_sort(self, rev=True):
        return Addict(
            [i for i in sorted(self.items(), key=lambda i: i[1], reverse=rev)])


def _par(function, data):
    ## vola funkci tolikrat, kolik je prvku v data
    return [item[1] for item in function(data)]


class PolynomialSystem(metaclass=Timer):
    def __init__(self, **kwargs):
        self.mem = 0
        self._prev_degs = None
        self._prev_hash = None
        self._prev_w_exp = None
        self._vars_freqs = [None]
        self._degs_freqs = [None]

        for k, v in kwargs.items():
            setattr(self, k, v)

    def _sat_variety(self, polys):
        from sage.sat.boolean_polynomials import solve

        sol = solve(polys, s_threads=1)
        self.mem = 0
        return [] if not sol else [
            [k[1] for k in sorted(key.items(), reverse=True)] for key in sol
        ]


    def magma_ml(self,firstl_txt,pil_txt,lastl_txt):
        try:
            magma.eval('42;')
        except:
            pass
        magma.eval(firstl_txt)
        for pol_arr in pil_txt:
            for pol in pol_arr:
                magma.eval(pol)
        gb = magma.eval(lastl_txt)
        return gb


    def _magma_variety(self, ml_gb, firstl_txt,pil_txt,lastl_txt, polys, faugere=True, ml=False, sep=False):
        from sage.interfaces.magma import magma
        try:
            magma.eval('42;')
        except:
            pass

        M_MAX = 10_000

        def mrep(s, d):
            return s if not d else mrep(s.replace(*d.popitem()), d)


        if ml:
            if sep:
                gb=ml_gb
            else:
                magma.eval(firstl_txt)
                for pol_arr in pil_txt:
                    for pol in pol_arr:
                        magma.eval(pol)
                gb = magma.eval(lastl_txt)
        else:

            faugere = 'Faugere,' if faugere else ''

            # orders = {'lex': 'lex', 'deglex': 'glex', 'degrevlex': 'grevlex'}

            BPR_m = (
                f'P{mrep(f"{polys[0].ring().gens()}", {"(": "<", ")": ">"})} := '
                f'BooleanPolynomialRing({polys[0].ring().n_variables()}, '
                '"grevlex");\n\n')
            magma.eval(BPR_m)

            polys_m = []
            polys_txt = ''
            for poly, i in zip(polys, range(len(polys))):
                if not poly:
                    continue

                mons = poly.monomials()
                chunks = [mons[m:m + M_MAX] for m in range(0, len(mons), M_MAX)]
                

                magma.eval(f'p{i} := 0;\n')

                for chunk in chunks:
                    magma.eval(f'p{i} := p{i} + ' + ' + '.join(f'{m}'
                                                               for m in chunk))

                polys_m += [f'p{i}']

                if FILE_OUTPUT:
                    polys_txt += f'p{i} := {poly};\n\n'


            gb_m = (f'gb := GroebnerBasis(Ideal({polys_m}):'
                    f' {faugere} Boolean, HFE);\n\n'
                    'gb;\n')

            if FILE_OUTPUT:
                #with open('../out/magma.txt', 'w') as f:
                with open('../out/magma_old.txt', 'w') as f:
                    f.write(BPR_m + polys_txt + gb_m)

            gb = magma.eval(gb_m)


        self.mem = int(magma.eval('GetMaximumMemoryUsage()')) // 1_000_000
        if gb[2] == '1':
            return []

        if PRINT_DETAILS:
            print(f'{FC}A Gröbner basis computed. '
                  f'Attempting to obtain the variety.{FR}')

        v = magma.eval('Variety(Ideal(gb));')
        return literal_eval(mrep(v, {'<': '[', '>': ']'}))

    def _keys(self, subs, variety):
        subs = Addict({self.ring(k): v
                       for k, v in subs.items()}).key_sort().items()
        vars_txt = [f'{v}' for v in self.vars]
        org_key = self.org_key.list()
        keys = []
        for key in (v[-len(org_key):] for v in variety):
            if len(key) < len(org_key):
                for k, v in subs:
                    key.insert(vars_txt.index(f'{k}'), v)

            for pt, ct in zip(self.pt, self.ct):
                with sr.AllowZeroInversionsContext(self.aes):
                    if ct not in [
                            self.aes(P=pt, K=self.aes.vector(key)),
                            self.aes(P=pt, K=self.aes.vector(key[::-1]))
                    ]:
                        break
            else:
                keys += [key]

                if PRINT_DETAILS:
                    print(f'{BG}A valid key found.{BRES}', end='')

                    if org_key in [key, key[::-1]]:
                        print(' (This key matches the original key.)')
                    else:
                        print()

        return keys

    def _variety(self, ml_gb, firstl_txt,pil_txt,lastl_txt, polys, faugere=True, meth='sat', ml=False, sep=False):
        if meth == 'magma':
            return self._magma_variety(ml_gb, firstl_txt,pil_txt,lastl_txt, polys, faugere, ml, sep)
        elif meth == 'sat':
            return self._sat_variety(polys)
        else:
            raise ValueError('Unknown meth.')

    def subs(self, subs={}, polys=None, par=True):
        def adjust_poly(poly):
            return ring(poly.subs(subs))

        @parallel(ncpus=NCPUS)
        def par_adjust_poly(poly):
            return adjust_poly(poly)

        vars_txt = [f'{v}' for v in self.vars]
        ring = self.ring.remove_var(
            *[self.vars[vars_txt.index(f'{k}')] for k in subs])
        polys = flatten(polys) if polys else flatten(self.polys)

        return _par(par_adjust_poly, polys) if par else list(
            map(adjust_poly, polys))

    def guess_keys(self,
                   polys=None,
                   guess=0,
                   rnd=False,
                   reverse=False,
                   degs=False,
                   w_exp=0,
                   faugere=True,
                   meth='sat'):
        @parallel(ncpus=NCPUS)
        def obtain_key(*guess):
            subs = dict(zip(vars_, guess))
            return self._keys(
                subs,
                self._variety(self.subs(subs, polys, par=False), faugere,
                              meth)), self.mem

        self.mem = 0
        polys = flatten(polys) if polys else flatten(self.polys)

        if rnd:
            vars_ = sample(self.vars, guess)
        else:
            vars_ = list(
                self.frequency(
                    polys=polys,
                    degs=degs,
                    w_exp=w_exp,
                ).val_sort(not reverse))[:guess]

        if PRINT_DETAILS:
            print(f'{FC}Frequencies computed.{FR}')

        res = _par(obtain_key, list(itertools.product((0, 1), repeat=guess)))
        self.mem = max([e[1] for e in res])
        return [e[0][0] for e in res if e[0]]

    def keys(self, ml_gb, firstl_txt,pil_txt,lastl_txt, subs={}, faugere=True, meth='sat', ml=False, sep=False):
        self.mem = 0
        if ml:
            return self._keys(
            subs, self._variety(ml_gb, firstl_txt,pil_txt,lastl_txt, [], faugere, meth, ml, sep))
        else:
            return self._keys(
            subs, self._variety(ml_gb, firstl_txt,pil_txt,lastl_txt, self.subs(subs, self.polys), faugere, meth, ml, sep))


    def reduce(self, polys=None):
        @parallel(ncpus=NCPUS)
        def add_closest(p):
            closest_poly = 0
            prev_similarity = 0
            p_monomials = set(p.monomials())

            for poly in flatten(polys[1:]):
                if p == poly:
                    continue

                similarity = len(p_monomials.intersection(poly.monomials()))
                if similarity > prev_similarity:
                    closest_poly = poly
                    prev_similarity = similarity

            red_p = p + closest_poly

            return red_p if 0 < len(red_p) < len(p) else p

        polys = polys if polys else self.polys

        return _par(add_closest, polys[0])

    def frequency(self,
                  polys=None,
                  target='vars',
                  degs=True,
                  w_exp=1,
                  red=True):
        @parallel(ncpus=NCPUS)
        def vars_freq(p):
            vars_ = [
                Addict({k: 0
                        for k in p.variables()}) for _ in range(p.deg() + 1)
            ]

            degrees = [0] * (p.deg() + 1)

            for m in p.monomials():
                deg = m.deg()
                degrees[deg] += 1
                for v in m.variables():
                    vars_[deg][v] += weights[deg]

            if degs:
                return aggregate([
                    Addict({k: v // degrees[i]
                            for k, v in vars_[i].items()})
                    for i in range(1, len(degrees)) if degrees[i]
                ], True)

            return aggregate(vars_, True)

        @parallel(ncpus=NCPUS)
        def degs_freq(p):
            degs = Addict({k: 0 for k in range(p.deg() + 1)})
            for m in p.monomials():
                degs[m.deg()] += 1
            return degs

        def aggregate(data, red):
            return reduce(lambda a, b: a + b, data) if red else data

        polys = flatten(polys) if polys else flatten(self.polys)
        polys_hash = hash(tuple(polys))

        if target == 'vars':
            if (self._prev_degs == degs and self._prev_w_exp == w_exp
                    and self._prev_hash == polys_hash and self._vars_freqs[0]):
                return aggregate(self._vars_freqs[0], red)

            weights = [d**w_exp for d in range(len(self.vars) + 1)]

            dest_var = self._vars_freqs
            fun = vars_freq

        elif target == 'degs':
            if self._prev_hash == polys_hash and self._degs_freqs[0]:
                return aggregate(self._degs_freqs[0], red)

            dest_var = self._degs_freqs
            fun = degs_freq

        else:
            raise ValueError('Unknown target.')

        dest_var[0] = _par(fun, polys)
        self._prev_hash = polys_hash
        self._prev_degs = degs
        self._prev_w_exp = w_exp

        return aggregate(dest_var[0], red)

    def key_bits(self,
                 polys=None,
                 guess=0,
                 sort=True,
                 reverse=False,
                 degs=False,
                 w_exp=1,
                 faugere=True,
                 meth='sat'):
        @parallel(ncpus=NCPUS)
        def obtain_variety(*guess):
            subs = dict(zip(vars_, guess))
            return self._variety(self.subs(subs, polys, par=False), faugere,
                                 meth)

        polys = flatten(polys) if polys else flatten(self.polys)

        if sort:
            vars_ = list(
                self.frequency(
                    polys=polys,
                    degs=degs,
                    w_exp=w_exp,
                ).val_sort(not reverse))[:guess]
        else:
            vars_ = sample(self.vars, guess)

        if PRINT_DETAILS:
            print(f'{FC}Frequencies computed.{FR}')

        varietes = [
            v[0] for v in _par(obtain_variety,
                               list(itertools.product((0, 1), repeat=guess)))
            if v
        ]

        return [dict(zip(self.vars, v)) for v in varietes]


class AES(sr.SR_gf2, metaclass=Timer):
    def __init__(self, n=1, r=1, c=1, e=4, star=False, **kwargs):
        super().__init__(n, r, c, e, star, gf2=True, order='lex', **kwargs)
        self.s_size = r * c * e

    def _ps_raw(self, n=1, sim=False, key=None, fstore=False, fload=False, fname="../out/data.txt"):
        def generate_pt():
            ## generate PT
            if not ps_raw['pt']:
                return self.vector(
                    [randrange(0, 2) for i in range(self.s_size)])

            for _ in range(PT_LIMIT):
                if sim:
                    pt = ps_raw['pt'][0].list()
                    i = randint(0, self.s_size - 1)
                    pt[i] = 1 - pt[i]
                else:
                    pt = [randrange(0, 2) for i in range(self.s_size)]

                pt = self.vector(pt)

                if pt not in forbidden_pt and pt not in ps_raw['pt']:
                    return pt

            raise ValueError(
                'The polynomial system could not be created because too many '
                'polynomial systems were requested.')
        
        ps_raw = {'order': 'lex'}
        ps_raw['aes'] = self

        for _ in range(KEY_LIMIT):
            ##generate key
            ps_raw['org_key'] = key if key else self.vector(
                [randrange(0, 2) for i in range(self.s_size)])
            ps_raw['pt'] = []
            ps_raw['ct'] = []
            ps_raw['ps'] = []
            forbidden_pt = []

            if fstore:
                with open(fname, 'w') as f:
                    f.write(f"{ps_raw['org_key']}\n")
            if fload:
                with open(fname, 'r') as f:
                    lines=f.readlines()
                fkey=[]
                for i in range(self.s_size):
                    if lines[i][1] == '0':
                        fkey.append(0)
                    else:
                        fkey.append(1)
                ps_raw['org_key'] = self.vector([i for i in fkey])
                lines=lines[self.s_size:]

            for _ in range(n): 
                for _ in range(PT_LIMIT):
                    if fload:
                        fpt=[]
                        for i in range(self.s_size):
                            if lines[i][1] == '0':
                                fpt.append(0)
                            else:
                                fpt.append(1)
                        pt = self.vector([i for i in fpt])
                        lines=lines[self.s_size:]
                    else:
                        pt = generate_pt()

                    try:
                        ## make CT from PT and key
                        ct = self(P=pt, K=ps_raw['org_key'])
                        ps, _ = self.polynomial_system(P=pt, C=ct)
                    except ZeroDivisionError:
                        forbidden_pt += [pt]
                        continue

                    if fstore:
                        with open(fname, 'a') as f:
                            f.write(f"{pt}\n")


                    ps_raw['pt'] += [pt]
                    ps_raw['ct'] += [ct]
                    ps_raw['ps'] += [ps]
                    break

                else:
                    break

            else:
                break

        else:
            raise ValueError(
                'The polynomial system could not be created due to too many '
                '0-inversions.')

        ps_raw['ring'] = ps.ring()
        ps_raw['vars'] = ps.ring().gens()
        
        return ps_raw

    def gen_key(self):
        return self.vector([randrange(0, 2) for i in range(self.s_size)])

    ##make polynomials
    def ps_key_vars(self, n=1, meth='subs', sim=False, key=None, fstore=False, fload=False, fname="../out/data.txt"):
        def sboxes_gb(sboxes):
            return (BPIdeal(
                BPRing(names=sbox[0].variables(),
                       order=f'deglex({W_NUM}), deglex({W_NUM})'),
                sbox).groebner_basis()[:W_NUM]
                    for sbox in (sboxes[i:i + SBOX_OFFSET]
                                 for i in range(0, len(sboxes), SBOX_OFFSET)))

        def sep_lm(polys):
            return {f'{p.lm()}': p.subs({p.lm(): 0}) for p in polys}

        def sub_vars(polys, vars_):
            @parallel(ncpus=NCPUS)
            def substitute_variables(poly):
                return pbori.substitute_variables(ring, gens, poly)

            if not polys:
                return []
            else:
                gens = [
                    ring(vars_[f'{i}']) if f'{i}' in vars_ else ring(i)
                    for i in polys[0].ring().gens()
                ]

                return _par(substitute_variables, list(polys))

        @parallel(ncpus=NCPUS)
        def elim_aux_vars(ps):
            @parallel(ncpus=NCPUS)
            def trim_poly(poly):
                return ring.remove_var(*elim_vars)(poly)

            w_vars = {}
            s_vars = {}
            elim_vars = []
            ps_raw_it = iter(ps.parts())
            for r_polys, ks_polys in zip(ps_raw_it, ps_raw_it):
                vars_to_sub = {}
                x_vars = {}

                # Express the key schedule in the vars of the initial key.
                for sbox in sboxes_gb(ks_polys[self.s_size:]):
                    x_vars.update(sep_lm(sbox))

                elim_vars += list(x_vars.keys())
                s_vars = sep_lm(
                    sub_vars(sub_vars(ks_polys[:self.s_size], x_vars), s_vars))

                vars_to_sub.update(s_vars)

                # Express the round in the vars of the initial key.
                for sbox in sboxes_gb(r_polys[self.s_size:]):
                    vars_to_sub.update(sep_lm(sub_vars(sbox, w_vars)))

                elim_vars += list(w_vars.keys()) + list(vars_to_sub.keys())
                polys = sub_vars(r_polys[:self.s_size], vars_to_sub)
                w_vars = sep_lm(polys)
            return _par(trim_poly, polys)

        @parallel(ncpus=NCPUS)
        def anf(pt, ct):
            @parallel(ncpus=NCPUS)
            def poly_anf(i):
                def ct_vec(i):
                    with sr.AllowZeroInversionsContext(self):
                        return [
                            c[i][0] for c in (self(P=pt, K=self.vector(k))
                                              for k in itertools.product(
                                                  (0, 1), repeat=self.s_size))
                        ]

                return BoolFun(ct_vec(i)).algebraic_normal_form() + ct[i][0]

            return _par(poly_anf, list(range(self.s_size)))

        def fgb(poly_systems):
            import fgb_sage

            nonlocal ring
            R = PolynomialRing(GF(2), len(ring.variable_names()),
                               ', '.join(ring.variable_names()))
            ring = ring.remove_var(*ring.gens()[:-self.s_size])
            polys = [
                flatten(
                    fgb_sage.eliminate([R(p) for p in flatten(ps.parts())],
                                       R.gens()[:-self.s_size],
                                       matrix_bound=2**27,
                                       max_base=2**27,
                                       verbosity=0,
                                       threads=NCPUS).parts())
                for ps in poly_systems
            ]

            @parallel(ncpus=NCPUS)
            def adjust_polys(polys):
                @parallel(ncpus=NCPUS)
                def adjust_poly(poly):
                    return ring(poly)

                return _par(adjust_poly, polys)

            return _par(adjust_polys, polys)
        ps = self._ps_raw(n, sim, key, fstore, fload, fname)
        ring = ps['ring']

        if self.e == 8:
            W_NUM = 8
            SBOX_OFFSET = 24
        else:
            W_NUM = 4
            SBOX_OFFSET = 12

        if meth == 'subs':
            ps['polys'] = _par(elim_aux_vars, ps['ps'])
        elif meth == 'ANF':
            ps['polys'] = _par(anf, list(zip(ps['pt'], ps['ct'])))
        elif meth == 'fgb':
            ps['polys'] = fgb(ps['ps'])
        else:
            raise ValueError('Unknown meth.')

        ring = ps['polys'][0][0].ring()
        ps['ring'] = ring
        ps['vars'] = ring.gens()
        
        return PolynomialSystem(**ps)

    def ps_aux_vars(self, n=1, sim=False, key=None):
        ps = self._ps_raw(n, sim, key)
        ps['polys'] = [[p for ss in s.parts() for p in ss] for s in ps['ps']]

        return PolynomialSystem(**ps)

    def ps_red(self, ps_lim=10, ps_min=1, ps_num=1, meth='subs', sim=True):
        @parallel(ncpus=NCPUS)
        def trim_poly(poly):
            return ring(poly)

        if ps_num > self.s_size:
            raise ValueError(f"'ps_num' cannot be greater than {self.s_size}")

        for _ in range(KEY_LIMIT):
            ps_cnt = 0
            key = self.gen_key()
            polys = []
            aux_polys = []
            pt = []
            ct = []
            _vars = set()

            for _ in range(ps_lim):
                new_polys = None

                try:
                    ps = self.ps_key_vars(n=ps_num,
                                          meth='subs',
                                          sim=True,
                                          key=key)
                except ValueError:
                    break

                new_polys = ps.reduce()
                new_vars = set(flatten([p.variables() for p in new_polys]))
                tmp_vars = _vars | new_vars
                if len(tmp_vars) > len(_vars) or (len(_vars) == len(ps.vars)
                                                  and ps_cnt < ps_min):
                    ps_cnt += 1
                    polys += new_polys
                    aux_polys += ps.ps
                    pt += ps.pt
                    ct += ps.ct
                    _vars = tmp_vars

                if PRINT_DETAILS:
                    print(f'{FC}Variables in the system: {len(_vars)}{FR}')

                if len(_vars) == len(ps.vars) and ps_cnt >= ps_min:
                    break

            if new_polys:
                break
            else:
                continue

        else:
            raise ValueError('The polynomial system could not be created due '
                             'to too many 0-inversions.')

        ring = ps.ring.remove_var(*set(ps.ring.gens()) - _vars)
        ps.ring = ring
        ps.polys = _par(trim_poly, polys)
        ps.vars = ring.gens()
        ps.ps = aux_polys
        ps.pt = pt
        ps.ct = ct

        return ps


    def ps_reduce_ml(self,ps,meth='PAM',num=1, psets=1):
        import copy
        from random import sample
        import numpy as np

        print("before ml:",datetime.datetime.now().time()) ##pomtisk
        bits=ps.org_key.nrows()
        rng=range(bits*num)
        ##array polyns to return
        polys=[[],[],[]]
        ##all polynomials in one flat array
        allpolys = flatten(ps.polys)
        
        ###choose method of reduction
        if meth == "PAM":
            s=0
            for pset in [2,4,8]:
                dists = np.empty(shape=[num*bits,bits*pset], dtype=int)
                meds=sample(rng,bits*pset)
                for p in rng:
                    for i in range(bits*pset):
                        d=len(allpolys[p] + allpolys[meds[i]])
                        dists[p][i]=d
                cost=sum(np.amin(dists, axis=1))
                lidxs=np.argmin(dists, axis=1)
                labels=np.take(meds,lidxs)
                flag=True
                while flag:
                    flag=False
                    for i in range(bits*pset):
                        pidxs=np.where(labels == meds[i])
                        new_dists=np.copy(dists)
                        for pi in pidxs[0]:
                            if pi==meds[i]:
                                continue
                            for p in rng:
                                d=len(allpolys[p] + allpolys[pi])
                                new_dists[p][i]=d
                            new_cost=sum(np.amin(new_dists, axis=1))
                            if new_cost < cost:
                                flag=True
                                dists=np.copy(new_dists)
                                cost=new_cost
                                meds[i]=pi
                                lidxs=np.argmin(dists, axis=1)
                                labels=np.take(meds,lidxs)
                print("while end:",datetime.datetime.now().time()) ##pomtisk

                ##for each cluster find closest polynomials
                for i in range(bits*pset):
                    pidxs=np.where(labels == meds[i])
                    if len(pidxs[0]) == 1:
                        ##cluster has 1 polynomial
                        polys[s].append(allpolys[pidxs[0][0]])
                    elif len(pidxs[0]) == 2:
                        ##cluster has 2 polynomials - take xor
                        polys[s].append(allpolys[pidxs[0][0]] + allpolys[pidxs[0][1]])
                    elif len(pidxs[0]) == 0:
                        continue
                        #polys[s].append(0)
                    else:
                        ##calculate dist for each 2 polynomials in cluster
                        cl_dist = len(allpolys[pidxs[0][0]] + allpolys[pidxs[0][1]])
                        cl_idx = [pidxs[0][0],pidxs[0][1]]
                        for i in range(len(pidxs[0])):
                            j=i+1
                            while j < len(pidxs[0]):
                                new_dist = len(allpolys[pidxs[0][i]] + allpolys[pidxs[0][j]])
                                if (new_dist < cl_dist) and (new_dist > 0):
                                    cl_dist = new_dist
                                    cl_idx = [pidxs[0][i],pidxs[0][j]]
                                j+=1
                        ##xor of best pair
                        polys[s].append(allpolys[cl_idx[0]] + allpolys[cl_idx[1]])
                print("PAM end:",datetime.datetime.now().time()) ##pomtisk
                s+=1

        elif meth == "MSM":

            ###find LM and degLM for grevlex oreder
            kv=allpolys[0].ring().gens()
            lm_mons=[]
            lm_degs = np.empty(shape=[num*bits], dtype=int)
            lm_idxs = np.empty(shape=[num*bits], dtype=int)
            for i in rng:
                mons=allpolys[i].monomials()
                lm=mons[0]
                lm_mons.append(lm)
                lm_degs[i]=lm.deg()
                lm_idxs[i]=i
                for m in mons:
                    mdeg=m.deg()
                    if m == lm_mons[i]:
                        continue
                    elif mdeg > lm_degs[i]:
                        lm_mons[i]=m
                        lm_degs[i]=mdeg
                        mv=m.variables()
                        lmv=lm_mons[i].variables()
                        flag=0
                        k=0
                        vi=-1
                        while not flag:
                            k-=1
                            if mv[vi] == lmv[vi]:
                                vi-=1
                                continue
                            if lmv[vi] == kv[k]:
                                flag=1
                                lm_mons[i]=m
                                lm_degs[i]=mdeg
                            if mv[vi] == kv[k]:
                                flag=2

            ##sort arrays by degLM
            polysxorlm=[]
            polysxoridx=[]
            polysxorflags=[[],[],[]]
            while len(lm_degs):
                idxs=np.where(lm_degs == lm_degs.min())
                for idx in idxs[0]:
                    polysxorlm.append(f'{lm_mons[lm_idxs[idx]]}')
                    polysxoridx.append(lm_idxs[idx])
                    polysxorflags[0].append(True)
                    polysxorflags[1].append(True)
                    polysxorflags[2].append(True)
                lm_degs=np.delete(lm_degs,idxs[0])
                lm_idxs=np.delete(lm_idxs, idxs[0])
            print("sort:",datetime.datetime.now().time()) ##pomtisk

            ##xor polynomials with same LM from smallest deg
            s=0
            for pset in [2,4,8]:
                count=0
                flagend=False
                for i in rng[:-1]:
                    if flagend:
                        break
                    if polysxorflags[s][i]:
                        j=i+1
                        while len(polysxorlm[i]) == len(polysxorlm[j]):
                            if polysxorlm[i] == polysxorlm[j]:
                                polysxorflags[s][j]=False
                                if polysxorflags[s][i]:
                                    polysxorflags[s][i]=False
                                    polys[s].append(allpolys[polysxoridx[i]] + allpolys[polysxoridx[j]])
                                    count += 1
                                    if count >= bits*pset:
                                        flagend=True
                                    break
                            j+=1
                            if j == num*bits:
                                break

                ##for now just add other polynomials if not enough xors
            ##needed from 3.rund
                while count < bits*pset:
                    polys[s].append(allpolys[count])
                    count+=1
                print("MSM end:",datetime.datetime.now().time()) ##pomtisk
                s+=1


        else: ##LSH
            ##make shingles from polynomials
            shingles = []
            for poly in allpolys:
                shingles.append(set(poly.monomials()))
            ##make dict shingles
            shingles_all = set().union(*shingles)
            shingles_dict = {}
            for i, shingle in enumerate(list(shingles_all)):
                shingles_dict[shingle] = i

            ##PIECES OF CODE ARE TAKEN FROM:
            ##https://www.pinecone.io/learn/locality-sensitive-hashing/
            ##https://github.com/pinecone-io/examples/blob/master/locality_sensitive_hashing_traditional/testing_lsh.ipynb

            ##make bin vectors for polynomials from shingles_dict
            allpolys_vec = []
            for shingle_set in shingles:
                vec = np.zeros(len(shingles_dict))
                for shingle in shingle_set:
                    idx = shingles_dict[shingle]
                    vec[idx] = 1
                allpolys_vec.append(vec)
            allpolys_vec = np.stack(allpolys_vec)

            ##parameters according to size of dict
            if allpolys_vec.shape[1] < 1000:
                resolution = 50
                b=10
            elif allpolys_vec.shape[1] < 10000:
                resolution = 100
                b=20
            else:
                resolution = 500
                b=100

            ##minhash
            len_dict = len(shingles_dict.keys())
            minhash = np.zeros((resolution, len_dict))
            for i in range(resolution):
                permutation = np.random.permutation(len(shingles_dict)) + 1
                minhash[i, :] = permutation.copy()
            minhash = minhash.astype(int)

            ##make signatures from minhash
            signatures = []
            for vector in allpolys_vec:
                # get index locations of every 1 value in vector
                idx = np.nonzero(vector)[0].tolist()
                # use index locations to pull only +ve positions in minhash
                shingles_minhash = minhash[:, idx]
                # find minimum value in each hash vector
                signature = np.min(shingles_minhash, axis=1)
                signatures.append(signature)

            signatures = np.stack(signatures)

            from itertools import combinations
            class LSH:
                buckets = []
                counter = 0
                def __init__(self, b):
                    self.b = b
                    for i in range(b):
                        self.buckets.append({})

                def make_subvecs(self, signature):
                    l = len(signature)
                    assert l % self.b == 0
                    r = int(l / self.b)
                    # break signature into subvectors
                    subvecs = []
                    for i in range(0, l, r):
                        subvecs.append(signature[i:i+r])
                    return np.stack(subvecs)

                def add_hash(self, signature):
                    subvecs = self.make_subvecs(signature).astype(str)
                    for i, subvec in enumerate(subvecs):
                        subvec = ','.join(subvec)
                        if subvec not in self.buckets[i].keys():
                            self.buckets[i][subvec] = []
                        self.buckets[i][subvec].append(self.counter)
                    self.counter += 1

                def check_candidates(self):
                    candidates = []
                    for bucket_band in self.buckets:
                        keys = bucket_band.keys()
                        for bucket in keys:
                            hits = bucket_band[bucket]
                            if len(hits) > 1:
                                candidates.extend(combinations(hits, 2))
                    return set(candidates)

            lsh = LSH(b)
            for sig in signatures:
                lsh.add_hash(sig)
            candidate_pairs = lsh.check_candidates()

            ##sort pairs by dist
            sorted_candidates=[]
            for pair in list(candidate_pairs):
                d=len(allpolys[pair[0]] + allpolys[pair[1]])
                sorted_candidates.append((d,pair[0],pair[1]))
            sorted_candidates.sort()

            ##take xor of best pairs
            s=0
            for pset in [2,4,8]:
                count=0
                i=0
                while count<bits*pset:
                    if sorted_candidates[i][0] == 0:
                        i+=1
                        continue
                    polys[s].append(allpolys[sorted_candidates[i][1]] + allpolys[sorted_candidates[i][2]])
                    count+=1
                    i+=1
                print("LSH end:",datetime.datetime.now().time()) ##pomtisk
                s+=1

        #sets=["2","4","8"]
        firstl_txt=["2","4","8"]
        lastl_txt=["2","4","8"]
        pil_txt=[[],[],[]]
        pol_count=[]
        avg_pol_len=[]
        avg_mon_len=[]
        for s in range(3):
            ##make magma commands
            mmax=10000
            pil_txt[s]=[]
            lastl_txt[s]="gb := GroebnerBasis(Ideal(["
            for i in range(len(polys[s])):
                pi=f"p{i}"
                lastl_txt[s]+=f"'{pi}', "
                pil_txt_arr=[]
                pil_txt_arr.append(f"{pi} := 0;\n\n")
                if polys[s][i] != 0:
                    count=0
                    count_more=0
                    mons = polys[s][i].monomials()
                    chunks = [mons[m:m + mmax] for m in range(0, len(mons), mmax)]
                    for ch in chunks:
                        pol_ret=f'{pi} := {pi} + '
                        for m in ch:
                            pol_ret+=f'{m} + '
                        pol_ret=pol_ret.rstrip(" + ")
                        pol_ret+=";\n\n"
                        pil_txt_arr.append(pol_ret)
                pil_txt[s].append(pil_txt_arr)
            
            lastl_txt[s]=lastl_txt[s].rstrip(", ")
            lastl_txt[s]+="]): Faugere, Boolean, HFE);\n\ngb;\n"
            firstl_txt[s]="P<"
            kv_txt=f'{polys[s][0].ring().gens()}'
            kv_txt=kv_txt.strip("()")
            firstl_txt[s]+=f'{kv_txt}> := BooleanPolynomialRing({bits}, "grevlex");\n\n'

#            with open(f"../out/magma{s}.txt", 'w') as f:
#                f.write(f"{firstl_txt[s]}")
#            with open(f"../out/magma{s}.txt", 'a') as f:
#                for pol_arr in pil_txt[s]:
#                    for pol in pol_arr:
#                        f.write(f"{pol}")
#                f.write(f"{lastl_txt[s]}")
#                
            pol_count.append(len(polys[s]))
            avg_pol_len.append(round(mean([len(p) for p in polys[s]])))
            avg_mon_len.append(round(mean([m.deg() for p in polys[s] for m in p.monomials()])))



        return firstl_txt,pil_txt,lastl_txt,pol_count, avg_pol_len, avg_mon_len


