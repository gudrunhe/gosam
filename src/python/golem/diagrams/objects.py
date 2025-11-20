# vim: ts=3:sw=3:expandtab

from __future__ import annotations

import logging
import re
from collections.abc import Iterator, MutableSequence
from typing import Literal, final, override

import feyngraph as fg

import golem.algorithms.mandelstam
import golem.diagrams.methods as methods
from golem.model import aux, mass, width

logger = logging.getLogger(__name__)

LOOPMOMENTUM = "p1"


@final
class LoopIntegral:
    def __init__(self, props: list[fg.Propagator], momenta: list[Momentum], rank: int):
        self._propagators = props
        self._momenta = [p if p[LOOPMOMENTUM] > 0 else -p for p in momenta]
        self._rank = rank

        tmp = sorted(
            zip(self._momenta, props),
            key=lambda p: [
                p[0],
                mass(p[1].particle().name()),
                width(p[1].particle().name()),
            ],
        )
        self._sorted_momenta = [x[0] for x in tmp]
        self._sorted_propagators = [x[1] for x in tmp]

    @staticmethod
    def from_diagram(d: fg.Diagram) -> LoopIntegral:
        zerosum = {
            **{leg.momentum_str(): 1 for leg in d.incoming()},
            **{leg.momentum_str(): -1 for leg in d.outgoing()},
        }
        props = [p.normalize() for p in d.chord(0)]
        # Make sure that subsequent propagators share at least one vertex, otherwise the condition
        # S_ij = (r_i - r_j)^2 = p_i^2 assumed in the following steps cannot be fulfilled
        props_ordered = [props.pop(0)]
        while len(props) > 0:
            vertices = props_ordered[-1].vertices()
            for i, p in enumerate(props):
                if any(j in vertices for j in p.vertices()):
                    props_ordered.append(props.pop(i))
                    break
        props_ordered = [p for p in props_ordered if aux(p.particle().name()) != 1]
        momenta = [Momentum(p.momentum_str(), zerosum) for p in props_ordered]
        rk = methods.rank(d)
        return LoopIntegral(props_ordered, momenta, rk)

    def setRank(self, rk: int):
        self._rank = rk

    def is_scaleless(
        self,
        onshell: None | dict[str, str] = None,
        powfmt: str = "%s**%d",
        prefix: str = "s",
    ) -> bool:
        """
        Checks if the S-matrix has any non-zero entries.

        RETURNS

        True, if all entries are zero, False otherwise
        """
        prodfmt = "%s*%s"
        infix = ""
        suffix = ""

        zerosum = self._momenta[0].getZeroMomentum()
        num_in = len([x for x in list(zerosum.values()) if x == 1])
        num_out = len([x for x in list(zerosum.values()) if x == -1])
        _, mandel_subst = golem.algorithms.mandelstam.generate_mandelstam_set(
            num_in, num_out, prefix, suffix, infix, False
        )

        for i in range(1, self.size() + 1):
            pr_i = self._propagators[i - 1]
            ri = self._momenta[i - 1].rmomentum()
            mi = mass(pr_i.particle().name())
            wi = width(pr_i.particle().name())
            for j in range(i, self.size() + 1):
                pr_j = self._propagators[j - 1]
                rj = self._momenta[j - 1].rmomentum()
                mj = mass(pr_j.particle().name())
                wj = width(pr_j.particle().name())

                twoReS: dict[str, int] = {}
                twoImS: dict[str, int] = {}

                # Delta = add_momenta(1, ri, -1, rj)
                Delta = ri - rj
                for v1, c1 in list(Delta.items()):
                    i1 = int(v1[1:])
                    for v2, c2 in list(Delta.items()):
                        i2 = int(v2[1:])
                        terms = mandel_subst[i1 - 1][i2 - 1]
                        for symbol, coeff in list(terms.items()):
                            new_entry = c1 * c2 * coeff

                            if onshell is not None and symbol in onshell:
                                sym = str(onshell[symbol])
                            else:
                                sym = symbol

                            if sym == "0":
                                continue

                            if sym in twoReS:
                                twoReS[sym] += new_entry
                            else:
                                twoReS[sym] = new_entry

                if mi != "0":
                    sym = powfmt % (mi, 2)
                    if sym in twoReS:
                        twoReS[sym] += -2
                    else:
                        twoReS[sym] = -2

                    if wi != "0":
                        sym = prodfmt % (mi, wi)
                        if sym in twoImS:
                            twoImS[sym] += -2
                        else:
                            twoImS[sym] = -2
                if mj != "0":
                    sym = powfmt % (mj, 2)
                    if sym in twoReS:
                        twoReS[sym] += -2
                    else:
                        twoReS[sym] = -2

                    if wj != "0":
                        sym = prodfmt % (mj, wj)
                        if sym in twoImS:
                            twoImS[sym] += -2
                        else:
                            twoImS[sym] = -2

                keys = list(twoReS.keys())
                for sym in keys:
                    if twoReS[sym] == 0:
                        del twoReS[sym]
                keys = list(twoImS.keys())
                for sym in keys:
                    if twoImS[sym] == 0:
                        del twoImS[sym]

                if len(twoReS) > 0 or len(twoImS) > 0:
                    return False
        return True

    def getSMatrix(
        self,
        onshell: None | dict[str, int] = None,
        powfmt: str = "%s**%d",
        prodfmt: str = "%s*%s",
        prefix: str = "s",
        suffix: str = "",
        infix: str = "",
    ) -> dict[tuple[int, int], tuple[dict[str, int], dict[str, int]]]:
        """
        Returns a dict {(i,j): expr} where 'expr' is a
        pair (re, im) of dictionaries {symbol: coeff, symbol: coeff, ...};
        symbol can be an actual symbol, a product or a power.
        i and j run from 1 to N rather than 0 to N-1.
        """

        result: dict[tuple[int, int], tuple[dict[str, int], dict[str, int]]] = {}

        zerosum = self._momenta[0].getZeroMomentum()
        num_in = 0
        num_out = 0
        for x in list(zerosum.values()):
            if x == 1:
                num_in += 1
            elif x == -1:
                num_out += 1

        _, mandel_subst = golem.algorithms.mandelstam.generate_mandelstam_set(
            num_in, num_out, prefix, suffix, infix, False
        )

        for i in range(1, self.size() + 1):
            pr_i = self._propagators[i - 1]
            ri = self._momenta[i - 1].rmomentum()
            mi = mass(pr_i.particle().name())
            wi = width(pr_i.particle().name())
            for j in range(i, self.size() + 1):
                pr_j = self._propagators[j - 1]
                rj = self._momenta[j - 1].rmomentum()
                mj = mass(pr_j.particle().name())
                wj = width(pr_j.particle().name())

                twoReS: dict[str, int] = {}
                twoImS: dict[str, int] = {}

                # Delta = add_momenta(1, ri, -1, rj)
                Delta = ri - rj
                for v1, c1 in list(Delta.items()):
                    i1 = int(v1[1:])
                    for v2, c2 in list(Delta.items()):
                        i2 = int(v2[1:])
                        terms = mandel_subst[i1 - 1][i2 - 1]
                        for symbol, coeff in list(terms.items()):
                            new_entry = c1 * c2 * coeff

                            if onshell is not None and symbol in onshell:
                                sym = str(onshell[symbol])
                            else:
                                sym = symbol

                            if sym == "0":
                                continue

                            if sym in twoReS:
                                twoReS[sym] += new_entry
                            else:
                                twoReS[sym] = new_entry

                if mi != "0":
                    sym = powfmt % (mi, 2)
                    if sym in twoReS:
                        twoReS[sym] += -2
                    else:
                        twoReS[sym] = -2

                    if wi != "0":
                        sym = prodfmt % (mi, wi)
                        if sym in twoImS:
                            twoImS[sym] += +2
                        else:
                            twoImS[sym] = +2
                if mj != "0":
                    sym = powfmt % (mj, 2)
                    if sym in twoReS:
                        twoReS[sym] += -2
                    else:
                        twoReS[sym] = -2

                    if wj != "0":
                        sym = prodfmt % (mj, wj)
                        if sym in twoImS:
                            twoImS[sym] += +2
                        else:
                            twoImS[sym] = +2

                keys = list(twoReS.keys())
                for sym in keys:
                    if twoReS[sym] == 0:
                        del twoReS[sym]
                keys = list(twoImS.keys())
                for sym in keys:
                    if twoImS[sym] == 0:
                        del twoImS[sym]

                result[(i, j)] = (twoReS, twoImS)
                result[(j, i)] = (twoReS, twoImS)
        return result

    def getRank(self) -> int:
        return self._rank

    def canonical(self) -> tuple[LoopIntegral, IntegralTransformation]:
        """
        Return a pair (cli, ct), where
        cli is the canonical loop integral and
        ct is the transformation such that ct(self) == cli
        """
        ct = IntegralTransformation(self, 1, 0)
        cli = self

        for t in self.equivalence_transformations():
            dprime = t(self)

            if dprime <= cli:
                cli = dprime
                ct = t

        assert ct(self) == cli
        return (cli, ct)

    def pinched(self, pinches: list[int]) -> LoopIntegral:
        props: list[fg.Propagator] = []
        momenta: list[Momentum] = []
        for i, p in enumerate(self._propagators):
            if i not in pinches:
                props.append(p)
                momenta.append(self._momenta[i])
        return LoopIntegral(props, momenta, 0)

    def pinches(self) -> Iterator[tuple[LoopIntegral, list[int], list[int]]]:
        sel = [False] * self.size()

        while not all(sel):
            props: list[fg.Propagator] = []
            momenta: list[Momentum] = []
            indices: list[int] = []
            pinches: list[int] = []

            carry = True
            for i in range(len(sel)):
                old_val = sel[i]
                new_val = carry ^ old_val
                carry = carry and old_val
                sel[i] = new_val

                if new_val:
                    props.append(self._propagators[i])
                    momenta.append(self._momenta[i])
                    indices.append(i)
                else:
                    pinches.append(i)

            yield LoopIntegral(props, momenta, 0), indices, pinches

    @override
    def __hash__(self) -> int:
        if len(self._propagators) == 1:
            p = self._sorted_propagators[0].particle().name()
            return hash(3 * hash(mass(p)) + 5 * hash(width(p)))
        else:
            return sum(
                map(
                    lambda x: hash(
                        3 * hash(mass(x[0].particle().name()))
                        + 5 * hash(width(x[0].particle().name()))
                        + hash(x[1])
                    ),
                    zip(self._sorted_propagators, self._sorted_momenta),
                )
            )

    def __cmp__(self, other: LoopIntegral) -> int:
        def cmp_props(p1: fg.Propagator, p2: fg.Propagator) -> int:
            c1 = [mass(p1.particle().name()), width(p1.particle().name())]
            c2 = [mass(p2.particle().name()), width(p2.particle().name())]
            if c1 == c2:
                return 0
            elif c1 < c2:
                return -1
            else:
                return 1

        lp1 = self._sorted_propagators
        lp2 = other._sorted_propagators

        diff = len(lp1) - len(lp2)
        if diff > 0:
            return 1
        elif diff < 0:
            return -1

        if len(lp1) == 1:
            return cmp_props(lp1[0], lp2[0])

        for i in range(len(lp1)):
            diff = self._sorted_momenta[i].__cmp__(other._sorted_momenta[i])
            if diff != 0:
                return diff
            diff = cmp_props(lp1[i], lp2[i])
            if diff != 0:
                return diff
        return 0

    def __lt__(self, other: LoopIntegral) -> bool:
        return self.__cmp__(other) < 0

    def __le__(self, other: LoopIntegral) -> bool:
        return self.__cmp__(other) <= 0

    @override
    def __eq__(self, other: object) -> bool:
        if isinstance(other, LoopIntegral):
            return self.__cmp__(other) == 0
        else:
            return False

    def equivalence_transformations(self) -> Iterator[IntegralTransformation]:
        for i in range(0, self.size() + 1):
            yield IntegralTransformation(self, +1, i)
            yield IntegralTransformation(self, -1, i)

    def size(self) -> int:
        return len(self._propagators)

    @override
    def __str__(self) -> str:
        return "LoopIntegral(%s)" % "*".join(
            f"Prop({p.particle().name()}, {q})"
            for p, q in zip(self._propagators, self._momenta)
        )

    def rvector(self, j: int) -> Momentum:
        if j == 0:
            m = self._momenta[0].rmomentum()
            return m - m
        m = self._momenta[j - 1].rmomentum()

        return m

    def mass(self, j: int) -> str:
        return mass(self._propagators[j - 1].particle().name())

    def width(self, j: int) -> str:
        return width(self._propagators[j - 1].particle().name())

    def acceptIntegralTransformation(
        self, transform: BaseIntegralTransformation
    ) -> LoopIntegral:
        momenta = [transform.transformMomentum(p) for p in self._momenta]
        return LoopIntegral(self._propagators, momenta, self._rank)


class BaseIntegralTransformation:
    def __init__(self, s: int, r: Momentum):
        assert s == 1 or s == -1
        self._sign: int = s
        self._r: Momentum = r.copy()

        Q = Momentum(LOOPMOMENTUM, r.getZeroMomentum())
        self._Q1: Momentum = self._sign * Q - self._r

    @override
    def __str__(self) -> str:
        if self._sign > 0:
            s = ""
        else:
            s = "-"

        return "Q -> %sQ - (%s)" % (s, self.shift_vector())

    def sign(self) -> int:
        return self._sign

    def shift_vector(self, prefix: str = "k", suffix: str = "") -> str:
        return self._r.format(prefix, suffix)

    def relative(self, other: BaseIntegralTransformation) -> BaseIntegralTransformation:
        """
        Compute the relative transformation r such that
        self(li) == other(pli) <=> r(li) = pli

        self: Q1 -> Q' = s1 Q1 - r1
        other: Q2 -> Q' = s2 Q2 - r2
        => Q2 = s1 s2 Q1 - s2 (r1 - r2)
        """
        s1 = self.sign()
        s2 = other.sign()

        r1 = self._r
        r2 = other._r

        if s1 == s2:
            return BaseIntegralTransformation(1, r1 - r2)
        elif s1 == -1:
            return BaseIntegralTransformation(-1, r1 + r2)
        else:
            return BaseIntegralTransformation(-1, r1 + r2)

    def __call__(self, target: LoopIntegral) -> LoopIntegral:
        """
        PARAMETER

           target -- of type LoopIntegral
        """
        return target.acceptIntegralTransformation(self)

    def transformMomentum(self, p: Momentum) -> Momentum:
        p = self._Q1 + p.rmomentum()
        if p[LOOPMOMENTUM] < 0:
            return -p
        else:
            return p


class IntegralTransformation(BaseIntegralTransformation):
    """
    A class to represent the transformations of the form:
    Q --> Q' = s * Q - r_[i]
    """

    def __init__(self, loopintegral: LoopIntegral, sign: int, index: int):
        assert index >= 0 and index <= loopintegral.size()

        BaseIntegralTransformation.__init__(self, sign, loopintegral.rvector(index))


@final
class LoopCache:
    def __init__(self):
        # maps canonical topologies cli to a list of triples (di, li, ci)
        # where di is the diagram index, li is the loop integral of the
        # respective diagram and ci is a IntegralTransformation such that
        # ci(li) == cli
        self.topologies: dict[
            LoopIntegral, list[tuple[int, LoopIntegral, IntegralTransformation]]
        ] = {}
        self.diagrams: dict[int, fg.Diagram] = {}

        self.maxloopsize = 0
        self._roots: (
            None
            | dict[
                LoopIntegral,
                list[tuple[int, list[int], list[int], BaseIntegralTransformation]],
            ]
        ) = None

    def add(self, diagram: fg.Diagram, diagram_index: int):
        self.diagrams[diagram_index] = diagram
        loopintegral = LoopIntegral.from_diagram(diagram)
        size = loopintegral.size()
        if size > self.maxloopsize:
            self.maxloopsize = size

        cli, ci = loopintegral.canonical()

        if cli not in self.topologies:
            self.topologies[cli] = []
        self.topologies[cli].append((diagram_index, loopintegral, ci))

        # Invalidate Cache
        self._roots = None

    def partition(
        self,
    ) -> dict[
        LoopIntegral, list[tuple[int, list[int], list[int], BaseIntegralTransformation]]
    ]:
        if self._roots is not None:
            return self._roots

        roots: dict[
            LoopIntegral,
            list[tuple[int, list[int], list[int], BaseIntegralTransformation]],
        ] = {}

        # classify by loopsize
        cli_by_size: list[list[LoopIntegral]] = [
            [] for _ in range(self.maxloopsize + 1)
        ]
        for cli in list(self.topologies.keys()):
            ls = cli.size()
            cli_by_size[ls].append(cli)

        # pinches maps each maximal diagram to a list of all its
        # (canonical) pinches which are in the process
        pinches: dict[
            LoopIntegral, list[tuple[LoopIntegral, list[int], list[int]]]
        ] = {}
        # go through the list of cli's from the largest to the smallest
        for ls in range(self.maxloopsize, 0, -1):
            for cli in cli_by_size[ls]:
                cli_pinches: list[tuple[LoopIntegral, list[int], list[int]]] = []
                cli_pinches.append((cli, list(range(ls)), []))

                for pli, kept_indices, pinched_indices in cli.pinches():
                    pls = pli.size()
                    if pls == ls:
                        continue
                    cpli, _ = pli.canonical()
                    if cpli in cli_by_size[pls]:
                        assert cpli in self.topologies
                        cli_pinches.append((cpli, kept_indices, pinched_indices))
                        cli_by_size[pls].remove(cpli)
                pinches[cli] = cli_pinches

        for master_li, cli_list in list(pinches.items()):
            lst: list[tuple[int, list[int], list[int], BaseIntegralTransformation]] = []
            for cli, kept_indices, pinched_indices in cli_list:
                pli = master_li.pinched(pinched_indices)
                cpli, cpt = pli.canonical()
                for diagram_index, loopintegral, ci in self.topologies[cli]:
                    # self(li) == other(pli) <=> r(li) = pli
                    assert ci(loopintegral) == cpt(pli)
                    transform = ci.relative(cpt)
                    assert transform is not None, """
                     SHOULD NEVER HAPPEN
                     Could not find a group for diagram #%d
                     pli          = %s
                     loopintegral = %s
                     """ % (diagram_index, pli, loopintegral)
                    assert transform(loopintegral) == pli, """
                     li:        %s
                     pli:       %s
                     ci:        %s
                     cpt:       %s
                     cc:        %s
                     -----------------------------
                     pre-condition cc == ci(li) == cpt(pli) succeeded
                     -----------------------------
                     trans:     %s
                     trans(li): %s
                     -----------------------------
                     post-condition trans(li) == pli failed
                     -----------------------------
                     """ % (
                        loopintegral,
                        pli,
                        ci,
                        cpt,
                        ci(loopintegral),
                        transform,
                        transform(loopintegral),
                    )

                    lst.append(
                        (diagram_index, kept_indices, pinched_indices, transform)
                    )
            roots[master_li] = lst

        for root, lst in list(roots.items()):
            rk = 0
            lst.sort(key=lambda tpl: tpl[0])
            for diagram_index, kept_indices, pinched_indices, transform in lst:
                # This is the post condition
                assert root.pinched(pinched_indices) == transform(
                    LoopIntegral.from_diagram(self.diagrams[diagram_index])
                )

                new_rk = methods.rank(self.diagrams[diagram_index]) + len(
                    pinched_indices
                )
                if new_rk > rk:
                    rk = new_rk
            root.setRank(rk)

        self._roots = roots
        return roots


@final
class Momentum:
    def __init__(self, arg: str | dict[str, int], zero: str | dict[str, int]):
        if isinstance(arg, str):
            self._dict = self._parse_momentum(arg)
        else:
            self._dict = arg.copy()

        if isinstance(zero, str):
            self._zdict = self._parse_momentum(zero)
        else:
            self._zdict = zero.copy()

        self._normalize()

    def rmomentum(self) -> Momentum:
        result = self.copy()
        result[LOOPMOMENTUM] = 0
        return result

    def items(self) -> list[tuple[str, int]]:
        return list(self._dict.items())

    def _normalize(self):
        # bring into standard form:
        if len(self._dict) > 0:
            k0 = min(self._zdict.keys())
            v0 = self._zdict[k0]
            assert v0 == 1 or v0 == -1

            if k0 in self._dict:
                m0 = v0 * self._dict[k0]

                for k, z in list(self._zdict.items()):
                    if k in self._dict:
                        new_val = self._dict[k] - m0 * z
                    else:
                        new_val = -m0 * z
                    if new_val == 0:
                        del self._dict[k]
                    else:
                        self._dict[k] = new_val

    def onshell(self) -> bool:
        ld = len(self._dict)
        lz = len(self._zdict)

        return ld == 0 or ld == lz or ld == 1 or ld == lz - 1

    def copy(self) -> Momentum:
        return Momentum(self._dict, self._zdict)

    def __cmp__(self, other: Momentum) -> int:
        diff = len(self) - len(other)
        if diff > 0:
            return 1
        elif diff < 0:
            return -1

        diffv = self - other
        if len(diffv) == 0:
            return 0

        k0 = min(diffv._dict.keys())
        v0 = diffv[k0]
        if v0 > 0:
            return 1
        elif v0 < 0:
            return -1
        else:
            return 0

    def __lt__(self, other: Momentum) -> bool:
        return self.__cmp__(other) < 0

    @override
    def __eq__(self, other: object) -> bool:
        if isinstance(other, Momentum):
            return self.__cmp__(other) == 0
        else:
            return False

    @override
    def __hash__(self) -> int:
        result = 8950312
        for vec, coeff in list(self._dict.items()):
            result += 7 * (hash(vec) + coeff)
        return result

    def getZeroMomentum(self) -> dict[str, int]:
        return self._zdict

    @override
    def __str__(self) -> str:
        return self._format_momentum(self._dict)

    def format(self, prefix: str = "k", suffix: str = "") -> str:
        return self._format_momentum(self._dict, prefix, suffix)

    @override
    def __repr__(self) -> str:
        return "Momentum(%r, %r)" % (
            self._format_momentum(self._dict),
            self._format_momentum(self._zdict),
        )

    def __setitem__(self, index: str, value: int):
        if value == 0:
            if index in self._dict:
                del self._dict[index]
                self._normalize()
        else:
            self._dict[index] = value
            self._normalize()

    def __getitem__(self, index: str) -> int:
        if index in self._dict:
            return self._dict[index]
        else:
            return 0

    def _parse_momentum(self, mom: str) -> dict[str, int]:
        def classify(token: str) -> int:
            if token == "+":
                return 0
            elif token == "-":
                return 1
            elif token == "*":
                return 2
            elif token.isdigit():
                return 3
            else:
                return 4

        def expression(tokens: MutableSequence[str], types: MutableSequence[int]):
            result: dict[str, int] = {}

            def add_term(t: Literal[0] | tuple[int, str]):
                if t == 0:
                    return

                factor, symbol = t
                if symbol in result:
                    result[symbol] += factor
                else:
                    result[symbol] = factor

            while tokens:
                tt = types[-1]
                if tt == 0:
                    # consume token '+'
                    _ = tokens.pop()
                    _ = types.pop()
                    add_term(term(+1, tokens, types))
                elif tt == 1:
                    # consume token '-'
                    _ = tokens.pop()
                    _ = types.pop()
                    add_term(term(-1, tokens, types))
                elif tt == 3 or tt == 4:
                    # don't consume yet
                    add_term(term(+1, tokens, types))
                else:
                    raise SyntaxError("While parsing momentum %r" % mom)
            return result

        def term(
            sign: int, tokens: MutableSequence[str], types: MutableSequence[int]
        ) -> Literal[0] | tuple[int, str]:
            tt = types[-1]
            factor = sign
            if tt == 3:
                # number
                tok = tokens.pop()
                _ = types.pop()
                factor *= int(tok)

                if len(types) == 0:
                    if factor == 0:
                        return 0
                    else:
                        tt = -1
                else:
                    tt = types[-1]

                if tt != 2:
                    raise SyntaxError("While parsing momentum %r: '*' expected" % mom)

                _ = types.pop()
                _ = tokens.pop()
                tt = types[-1]

            if tt == 4:
                # symbol
                tok = tokens.pop()
                _ = types.pop()
                return (factor, tok)
            else:
                raise SyntaxError("While parsing momentum %r" % mom)

        tokens: list[str] = []
        for match in re.compile(r"\+|-|\*|[0-9A-Za-z_]+").finditer(mom):
            tokens.append(mom[match.start() : match.end()])

        tokens.reverse()
        token_types = list(map(classify, tokens))

        return expression(tokens, token_types)

    def _format_momentum(
        self, momentum: dict[str, int], prefix: str = "k", suffix: str = ""
    ) -> str:
        def str_coeff(num: int, flag: bool) -> str:
            if num == 1:
                if flag:
                    return "+"
                else:
                    return ""
            elif num == -1:
                return "-"
            elif num >= 0:
                if flag:
                    return "+%d*" % num
                else:
                    return "%d*" % num
            else:
                return "%d*" % num

        if LOOPMOMENTUM in momentum:
            m = str_coeff(momentum[LOOPMOMENTUM], False) + LOOPMOMENTUM
            flag = True
        else:
            m = ""
            flag = False

        if len(momentum) == 0:
            return "0"

        for vec, coeff in list(momentum.items()):
            if vec == LOOPMOMENTUM:
                continue
            svec = prefix + vec[1:] + suffix
            m += str_coeff(coeff, flag) + svec
            flag = True
        return m

    def __add__(self, other: Momentum) -> Momentum:
        return Momentum(self._add_momenta(1, self._dict, 1, other._dict), self._zdict)

    def __sub__(self, other: Momentum) -> Momentum:
        return Momentum(self._add_momenta(1, self._dict, -1, other._dict), self._zdict)

    def __mul__(self, other: int) -> Momentum:
        return Momentum(self._add_momenta(other, self._dict, 1, None), self._zdict)

    def __rmul__(self, other: int) -> Momentum:
        return Momentum(self._add_momenta(other, self._dict, 1, None), self._zdict)

    def __neg__(self) -> Momentum:
        return Momentum(self._add_momenta(-1, self._dict, 1, None), self._zdict)

    def __pos__(self) -> Momentum:
        return Momentum(self._add_momenta(-1, self._dict, 1, None), self._zdict)

    def __len__(self) -> int:
        return len(self._dict)

    def _add_momenta(
        self, f1: int, m1: dict[str, int] | None, f2: int, m2: dict[str, int] | None
    ) -> dict[str, int]:
        result: dict[str, int] = {}
        if m1 is not None:
            for vec, coeff in list(m1.items()):
                new_val = f1 * coeff
                if new_val != 0:
                    result[vec] = new_val

        if m2 is not None:
            for vec, coeff in list(m2.items()):
                if vec in result:
                    new_val = result[vec] + f2 * coeff
                    if new_val == 0:
                        del result[vec]
                    else:
                        result[vec] = new_val
                else:
                    new_val = f2 * coeff
                    if new_val != 0:
                        result[vec] = new_val
        return result
