# vim: ts=3:sw=3:expandtab

import re
import itertools
import sys

import golem.algorithms.mandelstam
import golem.util.tools
import golem.properties

import logging

logger = logging.getLogger(__name__)

LOOPMOMENTUM = "p1"


class Diagram:
    def __init__(self, *components):
        self._in_legs = {}
        self._out_legs = {}
        self._propagators = {}
        self._adjacency_list = {}
        self._adjacent_in = {}
        self._adjacent_out = {}
        self._vertices = {}
        self._nonprops = []

        self._zerosum = {}

        self._sign = 0

        self.filtered_by_momentum = False
        self.unitary_gauge = False
        self.use_MQSE = False

        for c in components:
            c.addToDiagram(self)

        for p in self._nonprops:
            self._merge(p)

        for p in list(self._propagators.values()):
            p.passZeroMomentum(self._zerosum)

        v_start = -1

        self._loop = []
        self._loop_vertices = []

        vertex_indices = list(self._vertices.keys())
        if len(vertex_indices) > 0:
            for idx in vertex_indices:
                if idx not in self._adjacency_list:
                    self._adjacency_list[idx] = []
            self._dfs(vertex_indices[0], set([]), set([]), self._loop, self._loop_vertices)

    def debug_diagram(self):
        print("debug_diagram:")
        print(" === IN LEGS:")
        for key, value in list(self._in_legs.items()):
            print("      %2d: %r" % (key, value))
        print(" === OUT LEGS:")
        for key, value in list(self._out_legs.items()):
            print("      %2d: %r" % (key, value))
        print(" === PROPAGATORS:")
        for key, value in list(self._propagators.items()):
            print("      %2d: %r" % (key, value))
        print(" === VERTICES:")
        for key, value in list(self._vertices.items()):
            print("      %2d: %r" % (key, value))
        print(" === ADJACENCY:")
        for key, value in list(self._adjacency_list.items()):
            print("      %2d: %r" % (key, value))

    def _merge(self, nprop):
        nkeep = nprop.v1
        rkeep = nprop.r1
        nkill = nprop.v2
        rkill = nprop.r2
        field = nprop.field

        assert nkeep != nkill

        # Eliminate vertex nkill
        v_kill = self._vertices[nkill]
        r_kill = v_kill.rank
        o_kill = v_kill.orders
        f_kill = v_kill.fields
        d_kill = len(f_kill)
        del self._vertices[nkill]
        v_keep = self._vertices[nkeep]
        d_keep = len(v_keep.fields)
        v_keep.rank += v_kill.rank
        for key in v_kill.orders:
            if key in v_keep.orders:
                v_keep.orders[key] += v_kill.orders[key]
            else:
                v_keep.orders[key] = v_kill.orders[key]
        f_keep = v_keep.fields

        i_keep = f_keep.index(field)
        i_kill = f_kill.index(field)

        f_keep[i_keep] = "<not assigned>"
        for i in range(i_kill - 1):
            f_keep.append("<not assigned>")

        r_map = {}

        ofs = 0
        for i, f in enumerate(f_kill):
            r = i + 1
            if f == field:
                assert i == i_kill
                continue
            if len(r_map) == 0:
                r_map[r] = i_keep + 1
            else:
                ofs += 1
                r_map[r] = d_keep + ofs
            v_keep.fields[r_map[r] - 1] = f

        for leg in list(self._in_legs.values()):
            if leg.v == nkill:
                leg.v = nkeep
                leg.r = r_map[leg.r]

        for leg in list(self._out_legs.values()):
            if leg.v == nkill:
                leg.v = nkeep
                leg.r = r_map[leg.r]

        if nkill in self._adjacent_in:
            if nkeep in self._adjacent_in:
                self._adjacent_in[nkeep].extend(self._adjacent_in[nkill])
            else:
                self._adjacent_in[nkeep] = self._adjacent_in[nkill]
            del self._adjacent_in[nkill]

        if nkill in self._adjacent_out:
            if nkeep in self._adjacent_out:
                self._adjacent_out[nkeep].extend(self._adjacent_out[nkill])
            else:
                self._adjacent_out[nkeep] = self._adjacent_out[nkill]
            del self._adjacent_out[nkill]

        for prop in list(self._propagators.values()):
            if prop.v1 == nkill:
                prop.v1 = nkeep
                prop.r1 = r_map[prop.r1]
            if prop.v2 == nkill:
                prop.v2 = nkeep
                prop.r2 = r_map[prop.r2]

        if nkill in self._adjacency_list:
            lst = self._adjacency_list[nkill]
            del self._adjacency_list[nkill]

            if nkeep in self._adjacency_list:
                self._adjacency_list[nkeep].extend(lst)
            else:
                self._adjacency_list[nkeep] = lst

    def getLoopIntegral(self, MQSE=True, checkrank=True):
        return LoopIntegral([self._propagators[abs(l)] for l in self._loop], self.rank(MQSE,checkrank))

    def colorforbidden(self):
        reps = []

        for l in list(self._in_legs.values()):
            if l.v in self._loop_vertices:
                c = abs(l.color)
                if c != 1:
                    reps.append(c)
        for l in list(self._out_legs.values()):
            if l.v in self._loop_vertices:
                c = abs(l.color)
                if c != 1:
                    reps.append(c)

        lp = list(map(abs, self._loop))
        for idx, p in list(self._propagators.items()):
            if idx in lp:
                continue
            if p.v1 in self._loop_vertices or p.v2 in self._loop_vertices:
                c = abs(p.color)
                if c != 1:
                    reps.append(c)
        return len(reps) == 1

    def rank(self, MQSE=True, checkrank=True):
        rk = 0
        for p in self._loop:
            twospin = abs(self._propagators[abs(p)].twospin)
            if twospin != 2 or (self.unitary_gauge and self._propagators[abs(p)].mass != "0"):
                rk += twospin

        for v in self._loop_vertices:
            rk += self._vertices[v].rank

        # Only relevant for the 'old way' of quark mass renormalisation
        if self.use_MQSE and MQSE and self.isMassiveQuarkSE() and rk < 2:
            return 2

        if rk > self.loopsize() + 1 and checkrank:
            logger.debug("{}".format(self))
            logger.critical(
                "Encountered diagram with rank {}, loopsize {} and rank - loopsize = {} > 1, which GoSam is unable to handle.".format(
                    rk, self.loopsize(), rk - self.loopsize()
                )
            )
            sys.exit("GoSam terminated due to an error")

        return rk

    def order(self, okey):
        tmporders = dict()
        for v in self._vertices:
            for key in self._vertices[v].orders.keys():
                if key in tmporders:
                    tmporders[key] += self._vertices[v].orders[key]
                else:
                    tmporders[key] = self._vertices[v].orders[key]
        try:
            if okey is None:
                return 0
            elif isinstance(okey, str):
                if okey in tmporders.keys():
                    return tmporders[okey]
                else:
                    return 0
            else:
                if str(okey) in tmporders.keys():
                    return tmporders[str(okey)]
                else:
                    return 0
        except:
            logger.critical("'{0}' cannot be used as key in order function.".format(okey))
            sys.exit("GoSam terminated due to an error")

    def VertexInfo(self):
        VInfo = dict()
        for v in self._vertices:
            tmporders = dict()
            vlabel = self._vertices[v].label
            if vlabel in VInfo:
                tmporders["multiplicity"] = VInfo[vlabel]["multiplicity"] + 1
            else:
                tmporders["multiplicity"] = 1
            for key in self._vertices[v].orders.keys():
                tmporders[key] = self._vertices[v].orders[key]
            VInfo[vlabel] = tmporders
        return VInfo

    def loopsize(self):
        return len(self._loop)

    def isMassiveBubble(self, idx=0, dct={}):
        """
        Returns if this diagram is a bubble with at least one
        massive propagator. As a side effect, the argument
        'dct' is modified if the result is True, such that
        it contains an entry:
           idx: (2spin1, color1, mass1, 2spin2, color2, mass2)

        In the case of a massive Tadpole the entry is of the format:

           idx: (2spin, color, mass)

        """
        if self.loopsize() > 2:
            return False
        loop_props = [self._propagators[abs(p)] for p in self._loop]
        in_out_props = []
        for indx, p in list(self._propagators.items()):
            if p not in loop_props:
                # add to in_out_props if the vertex is connected
                if p.v1 in self._loop_vertices or p.v2 in self._loop_vertices:
                    in_out_props.extend([p])
        if len(in_out_props) == 2:
            if in_out_props[0].momentum != in_out_props[1].momentum:
                return False
        if any([p.mass != "0" for p in loop_props]):
            entry = []
            for prop in loop_props:
                entry.extend([prop.twospin, prop.color, prop.mass, prop.width])
            for prop in in_out_props:
                entry.extend([prop.twospin, prop.color, prop.mass, prop.width])

            dct[idx] = tuple(entry)

            return True
        else:
            return False

    def isMassiveQuarkSE(self):
        if self.loopsize() != 2:
            return False

        if self.chord(None, massive=True, twospin=[1, -1], color=[3, -3]) != 1:
            return False

        if self.chord(None, massive=False, twospin=[2, -2], color=[8, -8]) != 1:
            return False

        for lv in self._loop_vertices:
            if self._vertices[lv].numlegs() != 3:
                return False

        if self.NPinloop():
            # exclude self-energy graphs with NP-vertex insertions
            # ToDo: this is potentially problematic but needed to
            # resolve issues with the chromomagentic operator CtG
            # => How to do mass renormalisation in presence of SMEFT operators?
            return False

        return True

    def NPinloop(self):
        for lv in self._loop_vertices:
            vertord = self._vertices[lv].get_orders()
            if False if "NP" not in vertord.keys() else (vertord["NP"] != 0):
                return True
        return False

    def isScaleless(self):
        powfmt = "%s**%d"
        prefix = "s"

        li = self.getLoopIntegral(checkrank=False)
        onshell = {}

        for l in list(self._in_legs.values()):
            mom = l.mom
            mass = l.mass

            imom = int(mom[1:])

            if str(mass) != "0":
                onshell[prefix + str(imom)] = powfmt % (mass, 2)
            else:
                onshell[prefix + str(imom)] = "0"
        for l in list(self._out_legs.values()):
            mom = l.mom
            mass = l.mass

            imom = int(mom[1:])

            if str(mass) != "0":
                onshell[prefix + str(imom)] = powfmt % (mass, 2)
            else:
                onshell[prefix + str(imom)] = "0"

        return li.is_scaleless(onshell, powfmt, prefix)

    def vertices(self, *fields):
        return sum([v.match(list(fields)) for v in list(self._vertices.values())])

    def loopvertices(self, *fields):
        return sum([self._vertices[v].match(list(fields)) for v in self._loop_vertices])

    def iprop(self, field, **opts):
        opts["zero"] = self._zerosum
        if "momentum" in opts:
            logger.warning(
                "Using the iprop function with the 'momentum' key in the Python filter can lead to inconsistencies in the crossings. Consider running GoSam with --no-crossings or using the iprop_momentum function instead."
            )
        return sum([p.match(field, **opts) for p in list(self._propagators.values())])

    def iprop_momentum(self, field, momentum):
        if sum([p.match(field, momentum) for p in list(self._propagators.values())]):
            self.filtered_by_momentum = True
            return True
        else:
            return False

    def legs(self, field, **opts):
        opts["zero"] = self._zerosum
        return sum([l.match(field, **opts) for l in [*self._in_legs.values(), *self._out_legs.values()]])

    def ext_legs_from_vertex(self, field, max_legs=1, is_ingoing=None):
        nlegs = len(self._vertices) * [0]
        for leg in list(self._in_legs.values()) + list(self._out_legs.values()):
            nlegs[leg.v - 1] += leg.match(field, is_ingoing=is_ingoing)
        if any(n > max_legs for n in nlegs):
            if is_ingoing is not None:
                self.filtered_by_momentum = True
            return True
        else:
            return False

    def vertex_with_external_legs(self, *fields, max_legs=1, is_ingoing=None):
        nlegs = len(self._vertices) * [0]
        for v in list(self._vertices.values()):
            if v.match(list(fields)):
                for leg in list(self._in_legs.values()) + list(self._out_legs.values()):
                    nlegs[leg.v - 1] += leg.v == v.index and (
                        leg.ingoing == is_ingoing if is_ingoing is not None else True
                    )
        if any(n > max_legs for n in nlegs):
            if is_ingoing is not None:
                self.filtered_by_momentum = True
            return True
        else:
            return False

    def chord(self, field, **opts):
        opts["zero"] = self._zerosum
        return sum([self._propagators[abs(p)].match(field, **opts) for p in self._loop])

    def bridge(self, field, **opts):
        opts["zero"] = self._zerosum
        return sum(
            [
                self._propagators[p].match(field, **opts)
                for p in set(self._propagators.keys()) - set(map(abs, self._loop))
            ]
        )

    def onshell(self, field, **opts):
        opts["zero"] = self._zerosum
        return sum(
            [
                self._propagators[abs(p)].match(field, **opts) and self._propagators[abs(p)].momentum.onshell()
                for p in set(self._propagators.keys()) - set(map(abs, self._loop))
            ]
        )

    def substituteZero(self, symbols):
        for p in list(self._propagators.values()):
            p.substituteZero(symbols)
        for l in list(self._in_legs.values()):
            l.substituteZero(symbols)
        for l in list(self._out_legs.values()):
            l.substituteZero(symbols)

    def _dfs(self, v, visited, dirty, loop, lvert):
        visited.add(v)
        loop_v = -1

        for e in self._adjacency_list[v]:
            if e in dirty:
                continue
            dirty.add(e)

            prop = self._propagators[e]
            next = prop.fro(v)
            if next in visited:
                # backwards edge, starts loop
                loop_v = next
                if prop.v1 == v:
                    loop.append(e)
                else:
                    loop.append(-e)
            else:
                r = self._dfs(next, visited, dirty, loop, lvert)
                if r >= 0:
                    loop_v = r

                    if prop.v1 == v:
                        loop.append(e)
                    else:
                        loop.append(-e)

        if loop_v >= 0:
            lvert.append(v)

        if v == loop_v:
            return -1
        else:
            return loop_v

    def addLeg(self, index, is_ingoing, leg):
        if is_ingoing:
            self._in_legs[index] = leg
            self._zerosum[leg.mom] = 1
            if leg.v not in self._adjacent_in:
                self._adjacent_in[leg.v] = []
            self._adjacent_in[leg.v].append(index)
        else:
            self._out_legs[index] = leg
            self._zerosum[leg.mom] = -1
            if leg.v not in self._adjacent_out:
                self._adjacent_out[leg.v] = []
            self._adjacent_out[leg.v].append(index)

    def addPropagator(self, index, prop):
        if prop.aux == 1:
            self._nonprops.append(prop)
        else:
            self._propagators[index] = prop
            if prop.v1 not in self._adjacency_list:
                self._adjacency_list[prop.v1] = []
            if prop.v2 not in self._adjacency_list:
                self._adjacency_list[prop.v2] = []

            self._adjacency_list[prop.v1].append(index)
            self._adjacency_list[prop.v2].append(index)

    def addVertex(self, index, vertex):
        self._vertices[index] = vertex

    def __str__(self):
        return "D(%s)" % (",".join(map(str, list(self._propagators.values()))))

    def __repr__(self):
        return "D(\n    %s\n)" % (",\n    ".join(map(str, [
            *list(l.__repr__() for l in self._in_legs.values()),
            *list(l.__repr__() for l in self._out_legs.values()),
            *list(p.__repr__() for p in self._propagators.values()),
            *list(v.__repr__() for v in self._vertices.values())
        ])))

    def isNf(self):
        return self.loopsize() == self.chord(None, massive=False, twospin=[1, -1], color=[3, -3])

    def QuarkBubbleMasses(self):
        if self.loopsize() == 2 and self.chord(None, massive=True, twospin=[1, -1], color=[3, -3]) == 2:
            masses = set([self._propagators[abs(p)].mass for p in self._loop])
            if len(masses) > 0:
                return list(masses)
        return []

    def ComplexQuarkBubbleMasses(self):
        masslist = []
        if self.loopsize() == 2 and self.chord(None, massive=True, twospin=[1, -1], color=[3, -3]) == 2:
            for p in self._loop:
                if len(self._propagators[abs(p)].mass) > 0 and len(self._propagators[abs(p)].width) > 0:
                    masses = self._propagators[abs(p)].mass
                    masslist.append(masses)
                    masses = self._propagators[abs(p)].width
                    masslist.append(masses)
            if len(masses) > 0:
                return masslist
        return []

    def EHCfound(self):
        vertex_indices = list(self._vertices.keys())
        found = False
        fields = [["g", "part21"], ["g", "part21"], ["H", "part25"]]
        for idx in vertex_indices:
            if self._vertices[idx].match(fields):
                found = True
        return found


class DiagramComponent:
    def addToDiagram(self, diagram):
        pass

    def substituteZero(self, symbols):
        pass

    def match_fields(self, rays, query):
        if len(rays) != len(query):
            return False
        if rays == query:
            return True
        if all(isinstance(q, (list, tuple, dict)) for q in query):
            for ref_fields in list(map(sorted, itertools.product(*query))):
                for ray in rays:
                    if ray in ref_fields:
                        ref_fields.remove(ray)
                    elif "'{}'".format(ray) in ref_fields:
                        ref_fields.remove("'{}'".format(ray))
                    elif "_" in ref_fields:
                        ref_fields.remove("_")
                    else:
                        break
                else:
                    return True
            return False
        elif all(isinstance(q, str) for q in query):
            for ray in rays:
                if ray in query:
                    query.remove(ray)
                elif "'{}'".format(ray) in query:
                    query.remove("'{}'".format(ray))
                elif "_" in query:
                    query.remove("_")
                else:
                    break
            else:
                return True
            return False
        else:
            return False


class Vertex(DiagramComponent):
    def __init__(self, index, rank, orders, label, *fields):
        self.index = index
        self.label = label
        self.rank = rank
        self.orders = orders
        self.fields = list(fields)

    def addToDiagram(self, diagram):
        return diagram.addVertex(self.index, self)

    def match(self, fields):
        rays = self.fields

        if len(fields) != len(rays):
            return False

        flist = []
        if fields is None:
            flist = None
        elif isinstance(fields, str):
            flist.append(fields)
        elif "__iter__" in fields.__class__.__dict__:
            if len(fields) == 0:
                flist = None
            else:
                if all(isinstance(l, (list, tuple, dict)) for l in fields):
                    if len(fields) > 1:
                        flist.extend([[str(e) for e in l] for l in fields])
                    else:
                        flist.extend([str(e) for e in fields[0]])
                else:
                    flist.extend([str(e) for e in fields])
        else:
            flist.append(str(fields))

        return self.match_fields(rays, flist) if flist else True

    def numlegs(self):
        return len(self.fields)

    def get_orders(self):
        return self.orders

    def __repr__(self):
        return (
            "Vertex("
            + (
                ", ".join(
                    ["index=%s" % self.index, "rank=%s" % self.rank, "orders=%s" % self.orders, "label=%s" % self.label]
                    + list(map(str, self.fields))
                )
            )
            + ")"
        )


class Propagator(DiagramComponent):
    def __init__(self, index, field, v1, r1, v2, r2, mom, mass, width, aux, twospin, color, self_conjugate, sign):
        self.index = index
        self.field = field
        self.v1 = v1
        self.v2 = v2
        self.r1 = r1
        self.r2 = r2
        self.mass = str(mass)
        self.sign = sign
        if mass == "0":
            self.width = "0"
        else:
            self.width = str(width)
        self.aux = aux
        self.twospin = twospin
        self.color = color
        self.self_conjugate = self_conjugate

        self._mom = mom

    def passZeroMomentum(self, zero):
        # self.zeromomentum = zero
        self.momentum = Momentum(self._mom, zero)
        if self.momentum[LOOPMOMENTUM] < 0:
            self.momentum = -self.momentum

    def __repr__(self):
        return "Propagator(index=%s, %s, v%sr%s, v%sr%s, %r, %s, %s, %s)" % (
            self.index,
            self.field,
            self.v1,
            self.r1,
            self.v2,
            self.r2,
            self.momentum,
            self.aux,
            self.twospin,
            self.color,
        )

    def copy(self, momentum=None):
        if momentum is None:
            mom = self.momentum
        else:
            mom = momentum
        p = Propagator(
            self.index,
            self.field,
            self.v1,
            self.r1,
            self.v2,
            self.r2,
            str(mom),
            self.mass,
            self.width,
            self.aux,
            self.twospin,
            self.color,
            self.self_conjugate,
            self.sign,
        )
        p.passZeroMomentum(self.momentum.getZeroMomentum())
        return p

    def __hash__(self):
        return 3 * hash(self.mass) + 5 * hash(self.width) + hash(self.momentum)

    def __cmp__(self, other):
        diff = self.momentum.__cmp__(other.momentum)
        if diff != 0:
            return diff

        if self.mass > other.mass:
            return 1
        elif self.mass < other.mass:
            return -1
        elif self.width > other.width:
            return 1
        elif self.width < other.width:
            return -1
        else:
            return 0

    def __lt__(self, other):
        return self.__cmp__(other) < 0

    def __eq__(self, other):
        return self.__cmp__(other) == 0

    def rmomentum(self):
        result = self.momentum.copy()
        result[LOOPMOMENTUM] = 0
        return result

    def __str__(self):
        if self.mass != "0":
            if self.width != "0":
                return "P(%s, %s, %s)" % (self.momentum, self.mass, self.width)
            else:
                return "P(%s, %s)" % (self.momentum, self.mass)
        else:
            return "P(%s)" % (self.momentum)

    def addToDiagram(self, diagram):
        return diagram.addPropagator(self.index, self)

    def fro(self, v):
        if v == self.v1:
            return self.v2
        elif v == self.v2:
            return self.v1
        else:
            return None

    def substituteZero(self, symbols):
        if self.mass in symbols:
            self.mass = "0"
            self.width = "0"
        elif self.width in symbols:
            self.width = "0"

    def match(self, field, momentum=None, twospin=None, massive=None, color=None, zero=None):
        if field is None:
            flist = None
        elif isinstance(field, str):
            flist = [field]
        elif "__iter__" in field.__class__.__dict__:
            if len(field) == 0:
                flist = None
            else:
                if all(isinstance(f, str) for f in field):
                    flist = [field]
                else:
                    raise SyntaxError("Argument 'field' of function 'match' must be a string or list of strings")
        else:
            raise SyntaxError("Argument 'field' of function 'match' must be a string or list of strings")

        if flist is not None and not self.match_fields([self.field], flist):
            return False

        if momentum is not None:
            md = Momentum(momentum, self.momentum.getZeroMomentum())

            if not (self.momentum == md or self.momentum == -md):
                return False

        if twospin is not None:
            if "__iter__" in twospin.__class__.__dict__:
                if all([s != self.twospin for s in twospin]):
                    return False
            else:
                if self.twospin != int(twospin):
                    return False

        if color is not None:
            if "__iter__" in color.__class__.__dict__:
                if all([c != self.color for c in color]):
                    return False
            else:
                if self.color != int(color):
                    return False

        if massive is not None:
            if (self.mass != "0") != massive:
                return False

        return True


class Leg(DiagramComponent):
    def __init__(self, index, is_ingoing, field, v, r, mom, mass, twospin, color, self_conjugate):
        self.index = index
        self.ingoing = is_ingoing
        self.field = field
        self.v = v
        self.r = r
        self.mom = mom
        self.mass = str(mass)
        self.twospin = twospin
        self.color = color
        self.self_conjugate = self_conjugate

    def substituteZero(self, symbols):
        if self.mass in symbols:
            self.mass = "0"

    def addToDiagram(self, diagram):
        return diagram.addLeg(self.index, self.ingoing, self)

    def __repr__(self):
        if self.ingoing:
            cl = "InLeg"
        else:
            cl = "OutLeg"
        return "%s(index=%s, %s, v%sr%s, %s, %s, %s)" % (
            cl,
            self.index,
            self.field,
            self.v,
            self.r,
            self.mom,
            self.twospin,
            self.color,
        )

    def match(self, field, is_ingoing=None, twospin=None, massive=None, color=None, zero=None):
        if field is None:
            flist = None
        elif isinstance(field, str):
            flist = [field]
        elif "__iter__" in field.__class__.__dict__:
            if len(field) == 0:
                flist = None
            else:
                if all(isinstance(f, str) for f in field):
                    flist = [field]
                else:
                    raise SyntaxError("Argument 'field' of function 'match' must be a string or list of strings")
        else:
            raise SyntaxError("Argument 'field' of function 'match' must be a string or list of strings")

        if flist is not None and not self.match_fields([self.field], flist):
            return False

        if is_ingoing is not None:
            if not self.ingoing == is_ingoing:
                return False

        if twospin is not None:
            if "__iter__" in twospin.__class__.__dict__:
                if all([s != self.twospin for s in twospin]):
                    return False
            else:
                if self.twospin != int(twospin):
                    return False

        if color is not None:
            if "__iter__" in color.__class__.__dict__:
                if all([c != self.color for c in color]):
                    return False
            else:
                if self.color != int(color):
                    return False

        if massive is not None:
            if (self.mass != "0") != massive:
                return False

        return True


class LoopIntegral:
    def __init__(self, loop_propagators, rank):
        self._propagators = [p.copy() for p in loop_propagators]
        self._rank = rank

        self._sorted_propagators = self._propagators[:]
        self._sorted_propagators.sort()

    def setRank(self, rk):
        self._rank = rk

    def is_scaleless(self, onshell={}, powfmt="%s**%d", prefix="s"):
        """
        Checks if the S-matrix has any non-zero entries.

        RETURNS

        True, if all entries are zero, False otherwise
        """
        prodfmt = "%s*%s"
        infix = ""
        suffix = ""

        zerosum = self._propagators[0].momentum.getZeroMomentum()
        num_in = len([x for x in list(zerosum.values()) if x == 1])
        num_out = len([x for x in list(zerosum.values()) if x == -1])
        mandel_names, mandel_subst = golem.algorithms.mandelstam.generate_mandelstam_set(
            num_in, num_out, prefix, suffix, infix, False
        )

        for i in range(1, self.size() + 1):
            pr_i = self._propagators[i - 1]
            ri = pr_i.rmomentum()
            mi = pr_i.mass
            wi = pr_i.width
            for j in range(i, self.size() + 1):
                pr_j = self._propagators[j - 1]
                rj = pr_j.rmomentum()
                mj = pr_j.mass
                wj = pr_j.width

                twoReS = {}
                twoImS = {}

                # Delta = add_momenta(1, ri, -1, rj)
                Delta = ri - rj
                for v1, c1 in list(Delta.items()):
                    i1 = int(v1[1:])
                    for v2, c2 in list(Delta.items()):
                        i2 = int(v2[1:])
                        terms = mandel_subst[i1 - 1][i2 - 1]
                        for symbol, coeff in list(terms.items()):
                            new_entry = c1 * c2 * coeff

                            if symbol in onshell:
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

    def getSMatrix(self, onshell={}, powfmt="%s**%d", prodfmt="%s*%s", prefix="s", suffix="", infix=""):
        """
        Returns a dict {(i,j): expr} where 'expr' is a
        pair (re, im) of dictionaries {symbol: coeff, symbol: coeff, ...};
        symbol can be an actual symbol, a product or a power.
        i and j run from 1 to N rather than 0 to N-1.
        """

        result = {}

        zerosum = self._propagators[0].momentum.getZeroMomentum()
        num_in = 0
        num_out = 0
        for x in list(zerosum.values()):
            if x == 1:
                num_in += 1
            elif x == -1:
                num_out += 1

        mandel_names, mandel_subst = golem.algorithms.mandelstam.generate_mandelstam_set(
            num_in, num_out, prefix, suffix, infix, False
        )

        for i in range(1, self.size() + 1):
            pr_i = self._propagators[i - 1]
            ri = pr_i.rmomentum()
            mi = pr_i.mass
            wi = pr_i.width
            for j in range(i, self.size() + 1):
                pr_j = self._propagators[j - 1]
                rj = pr_j.rmomentum()
                mj = pr_j.mass
                wj = pr_j.width

                twoReS = {}
                twoImS = {}

                # Delta = add_momenta(1, ri, -1, rj)
                Delta = ri - rj
                for v1, c1 in list(Delta.items()):
                    i1 = int(v1[1:])
                    for v2, c2 in list(Delta.items()):
                        i2 = int(v2[1:])
                        terms = mandel_subst[i1 - 1][i2 - 1]
                        for symbol, coeff in list(terms.items()):
                            new_entry = c1 * c2 * coeff

                            if symbol in onshell:
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

    def getRank(self):
        return self._rank

    def canonical(self):
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

    def pinched(self, pinches):
        props = []
        for i, p in enumerate(self._propagators):
            if i not in pinches:
                props.append(p)
        return LoopIntegral(props, 0)

    def pinches(self):
        sel = [False] * self.size()

        while not all(sel):
            props = []
            indices = []
            pinches = []

            carry = True
            for i in range(len(sel)):
                old_val = sel[i]
                new_val = carry ^ old_val
                carry = carry and old_val
                sel[i] = new_val

                if new_val:
                    props.append(self._propagators[i])
                    indices.append(i)
                else:
                    pinches.append(i)

            yield LoopIntegral(props, 0), indices, pinches

    def __hash__(self):
        if len(self._propagators) == 1:
            return hash(self._sorted_propagators[0].copy(LOOPMOMENTUM))
        else:
            return sum(map(hash, self._sorted_propagators))

    def __cmp__(self, other):
        lp1 = self._sorted_propagators
        lp2 = other._sorted_propagators

        diff = len(lp1) - len(lp2)
        if diff > 0:
            return 1
        elif diff < 0:
            return -1

        if len(lp1) == 1:
            p1 = lp1[0].copy(LOOPMOMENTUM)
            p2 = lp2[0].copy(LOOPMOMENTUM)
            return p1.__cmp__(p2)

        for p1, p2 in zip(lp1, lp2):
            diff = p1.__cmp__(p2)
            if diff != 0:
                return diff
        return 0

    def __lt__(self, other):
        return self.__cmp__(other) < 0

    def __le__(self, other):
        return self.__cmp__(other) <= 0

    def __eq__(self, other):
        return self.__cmp__(other) == 0

    def equivalence_transformations(self):
        for i in range(0, self.size() + 1):
            yield IntegralTransformation(self, +1, i)
            yield IntegralTransformation(self, -1, i)

    def size(self):
        return len(self._propagators)

    def __str__(self):
        return "LoopIntegral(%s)" % "*".join(map(str, self._propagators))

    def rvector(self, j):
        if j == 0:
            m = self._propagators[0].rmomentum()
            return m - m
        m = self._propagators[j - 1].rmomentum()

        return m

    def mass(self, j):
        return self._propagators[j - 1].mass

    def width(self, j):
        return self._propagators[j - 1].width

    def acceptIntegralTransformation(self, transform):
        props = [transform.transformPropagator(p) for p in self._propagators]
        return LoopIntegral(props, self._rank)


class BaseIntegralTransformation:
    def __init__(self, s, r):
        assert s == 1 or s == -1
        self._sign = s
        self._r = r.copy()

        Q = Momentum(LOOPMOMENTUM, r.getZeroMomentum())
        self._Q1 = self._sign * Q - self._r

    # def __add__(self, v):
    #   return BaseIntegralTransformation(self._sign, self._r + self._sign * v)
    #   #      add_momenta(1, self._r, self._sign, v))

    def __str__(self):
        if self._sign > 0:
            s = ""
        else:
            s = "-"

        return "Q -> %sQ - (%s)" % (s, self.shift_vector())

    def sign(self):
        return self._sign

    def shift_vector(self, prefix="k", suffix=""):
        return self._r.format(prefix, suffix)

    def relative(self, other):
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
        elif s2 == -1:
            return BaseIntegralTransformation(-1, r1 + r2)

    def __call__(self, target):
        """
        PARAMETER

           target -- of type LoopIntegral
        """
        return target.acceptIntegralTransformation(self)

    def transformPropagator(self, p):
        # return p.copy(add_momenta(1, self._Q1, 1, p.rmomentum()))
        return p.copy(self._Q1 + p.rmomentum())


class IntegralTransformation(BaseIntegralTransformation):
    """
    A class to represent the transformations of the form:
    Q --> Q' = s * Q - r_[i]
    """

    def __init__(self, loopintegral, sign, index):
        assert index >= 0 and index <= loopintegral.size()

        BaseIntegralTransformation.__init__(self, sign, loopintegral.rvector(index))


class TreeCache:
    def __init__(self):
        self.diagrams = {}

    def add(self, diagram, diagram_index):
        self.diagrams[diagram_index] = diagram

    def min(self) -> int:
        return min(self.diagrams.keys())

    def max(self) -> int:
        return max(self.diagrams.keys())


class LoopCache:
    def __init__(self):
        # maps canonical topologies cli to a list of triples (di, li, ci)
        # where di is the diagram index, li is the loop integral of the
        # respective diagram and ci is a IntegralTransformation such that
        # ci(li) == cli
        self.topologies = {}
        self.diagrams = {}

        self.maxloopsize = 0
        self._roots = None

    def add(self, diagram, diagram_index):
        self.diagrams[diagram_index] = diagram
        loopintegral = diagram.getLoopIntegral()
        size = loopintegral.size()
        if size > self.maxloopsize:
            self.maxloopsize = size

        cli, ci = loopintegral.canonical()
        # assert ci(loopintegral) == cli

        if cli not in self.topologies:
            self.topologies[cli] = []
        self.topologies[cli].append((diagram_index, loopintegral, ci))

        # Invalidate Cache
        self._roots = None

    def partition(self, MQSE=True):
        if self._roots is not None:
            return self._roots

        roots = {}

        # classify by loopsize
        cli_by_size = [[] for i in range(self.maxloopsize + 1)]
        for cli in list(self.topologies.keys()):
            ls = cli.size()
            cli_by_size[ls].append(cli)

        # pinches maps each maximal diagram to a list of all its
        # (canonical) pinches which are in the process
        pinches = {}
        # go through the list of cli's from the largest to the smallest
        for ls in range(self.maxloopsize, 0, -1):
            for cli in cli_by_size[ls]:
                cli_pinches = []
                cli_pinches.append((cli, list(range(ls)), []))

                for pli, kept_indices, pinched_indices in cli.pinches():
                    pls = pli.size()
                    if pls == ls:
                        continue
                    cpli, tmp = pli.canonical()
                    if cpli in cli_by_size[pls]:
                        assert cpli in self.topologies
                        cli_pinches.append((cpli, kept_indices, pinched_indices))
                        cli_by_size[pls].remove(cpli)
                pinches[cli] = cli_pinches

        for master_li, cli_list in list(pinches.items()):
            lst = []
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
                     """ % (loopintegral, pli, ci, cpt, ci(loopintegral), transform, transform(loopintegral))

                    lst.append((diagram_index, kept_indices, pinched_indices, transform))
            roots[master_li] = lst

        for root, lst in list(roots.items()):
            rk = 0
            lst.sort(key=lambda tpl: tpl[0])
            for diagram_index, kept_indices, pinched_indices, transform in lst:
                # This is the post condition
                assert root.pinched(pinched_indices) == transform(self.diagrams[diagram_index].getLoopIntegral())

                new_rk = self.diagrams[diagram_index].rank(MQSE) + len(pinched_indices)
                if new_rk > rk:
                    rk = new_rk
            root.setRank(rk)

        self._roots = roots
        return roots


class CTCache:
    def __init__(self):
        self.diagrams = {}

    def add(self, diagram, diagram_index):
        self.diagrams[diagram_index] = diagram


class Momentum:
    def __init__(self, arg, zero):
        if isinstance(arg, str):
            self._dict = self._parse_momentum(arg)
        else:
            self._dict = arg.copy()

        if isinstance(zero, str):
            self._zdict = self._parse_momentum(zero)
        else:
            self._zdict = zero.copy()

        self._normalize()

    def items(self):
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

    def onshell(self):
        ld = len(self._dict)
        lz = len(self._zdict)

        return ld == 0 or ld == lz or ld == 1 or ld == lz - 1

    def copy(self):
        return Momentum(self._dict, self._zdict)

    def __cmp__(self, other):
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

    def __lt__(self, other):
        return self.__cmp__(other) < 0

    def __eq__(self, other):
        return self.__cmp__(other) == 0

    def __hash__(self):
        result = 8950312
        for vec, coeff in list(self._dict.items()):
            result += 7 * (hash(vec) + coeff)
        return result

    def getZeroMomentum(self):
        return self._zdict

    def __str__(self):
        return self._format_momentum(self._dict)

    def format(self, prefix="k", suffix=""):
        return self._format_momentum(self._dict, prefix, suffix)

    def __repr__(self):
        return "Momentum(%r, %r)" % (self._format_momentum(self._dict), self._format_momentum(self._zdict))

    def __setitem__(self, index, value):
        if value == 0:
            if index in self._dict:
                del self._dict[index]
                self._normalize()
        else:
            self._dict[index] = value
            self._normalize()

    def __getitem__(self, index):
        if index in self._dict:
            return self._dict[index]
        else:
            return 0

    def _parse_momentum(self, mom):
        def classify(token):
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

        def expression(tokens, types):
            result = {}

            def add_term(t):
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
                    tokens.pop()
                    types.pop()
                    add_term(term(+1, tokens, types))
                elif tt == 1:
                    # consume token '-'
                    tokens.pop()
                    types.pop()
                    add_term(term(-1, tokens, types))
                elif tt == 3 or tt == 4:
                    # don't consume yet
                    add_term(term(+1, tokens, types))
                else:
                    raise SyntaxError("While parsing momentum %r" % mom)
            return result

        def term(sign, tokens, types):
            tt = types[-1]
            factor = sign
            if tt == 3:
                # number
                tok = tokens.pop()
                types.pop()
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

                types.pop()
                tokens.pop()
                tt = types[-1]

            if tt == 4:
                # symbol
                tok = tokens.pop()
                types.pop()
                return (factor, tok)
            else:
                raise SyntaxError("While parsing momentum %r" % mom)

        tokens = []
        for match in re.compile(r"\+|-|\*|[0-9A-Za-z_]+").finditer(mom):
            tokens.append(mom[match.start() : match.end()])

        tokens.reverse()
        token_types = list(map(classify, tokens))

        return expression(tokens, token_types)

    def _format_momentum(self, momentum, prefix="k", suffix=""):
        def str_coeff(num, flag):
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

    def __add__(self, other):
        return Momentum(self._add_momenta(1, self._dict, 1, other._dict), self._zdict)

    def __sub__(self, other):
        return Momentum(self._add_momenta(1, self._dict, -1, other._dict), self._zdict)

    def __mul__(self, other):
        return Momentum(self._add_momenta(other, self._dict, 1, None), self._zdict)

    def __rmul__(self, other):
        return Momentum(self._add_momenta(other, self._dict, 1, None), self._zdict)

    def __neg__(self):
        return Momentum(self._add_momenta(-1, self._dict, 1, None), self._zdict)

    def __pos__(self):
        return Momentum(self._add_momenta(-1, self._dict, 1, None), self._zdict)

    def __len__(self):
        return len(self._dict)

    def _add_momenta(self, f1, m1, f2, m2):
        result = {}
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


if __name__ == "__main__":
    diagram1 = Diagram(
        Leg(1, True, "A", 1, 3, "k1", "0", +2, 1, "A" == "A"),
        Leg(2, True, "A", 2, 3, "k2", "0", +2, 1, "A" == "A"),
        Leg(1, False, "A", 3, 3, "k3", "0", +2, 1, "A" == "A"),
        Leg(2, False, "A", 4, 3, "k4", "0", +2, 1, "A" == "A"),
        Propagator(1, "em", 2, 1, 1, 2, "-p1", "0", "0", 0, 1, 1, "em" == "ep", sign="-"),
        Propagator(2, "em", 1, 1, 3, 2, "-p1+k1", "me", "0", 0, 1, 1, "em" == "ep", sign="-"),
        Propagator(3, "em", 4, 1, 2, 2, "-p1-k2", "0", "0", 0, 1, 1, "em" == "ep", sign="-"),
        Propagator(4, "em", 3, 1, 4, 2, "-p1+k1-k3", "me", "0", 0, 1, 1, "em" == "ep", sign="-"),
        Vertex(1, 0, "ep", "em", "A"),
        Vertex(2, 0, "ep", "em", "A"),
        Vertex(3, 0, "ep", "em", "A"),
        Vertex(4, 0, "ep", "em", "A"),
    )

    diagram2 = Diagram(
        Leg(1, True, "A", 1, 3, "k1", "0", +2, 1, "A" == "A"),
        Leg(2, True, "A", 2, 3, "k2", "0", +2, 1, "A" == "A"),
        Leg(1, False, "A", 3, 3, "k3", "0", +2, 1, "A" == "A"),
        Leg(2, False, "A", 4, 3, "k4", "0", +2, 1, "A" == "A"),
        Propagator(1, "em", 2, 1, 1, 2, "-p1+k3-k4", "0", "0", 0, 1, 1, "em" == "ep", sign="-"),
        Propagator(2, "em", 1, 1, 3, 2, "-p1+k1+k3-k4", "me", "0", 0, 1, 1, "em" == "ep", sign="-"),
        Propagator(3, "em", 4, 1, 2, 2, "-p1-k2+k3-k4", "0", "0", 0, 1, 1, "em" == "ep", sign="-"),
        Propagator(4, "em", 3, 1, 4, 2, "-p1+k1-k3+k3-k4", "me", "0", 0, 1, 1, "em" == "ep", sign="-"),
        Vertex(1, 0, "ep", "em", "A"),
        Vertex(2, 0, "ep", "em", "A"),
        Vertex(3, 0, "ep", "em", "A"),
        Vertex(4, 0, "ep", "em", "A"),
    )

    li1 = diagram1.getLoopIntegral()
    li2 = diagram2.getLoopIntegral()

    pli1 = li1.pinched([3])
    pli2 = li2.pinched([3])

    print("pli1: %s" % pli1)
    print("pli2: %s" % pli2)

    cli1, cc1 = pli1.canonical()
    cli2, cc2 = pli2.canonical()

    assert cli1 == cli2
    print("canonical: %s" % cli1)

    print("cc1: %s" % cc1)
    print("cc2: %s" % cc2)

    assert cc1(pli1) == cc2(pli2)
    rt = cc1.relative(cc2)
    print(rt)
    assert rt(pli1) == pli2
