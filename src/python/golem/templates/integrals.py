# vim: ts=3:sw=3

import golem.templates.kinematics
import golem.util.config
import golem.util.path
import golem.util.tools
from golem.diagrams.methods import is_nf, loopsize, massive_quark_self_energy, rank
from golem.util.config import Properties
from golem.util.parser import Template, TemplateError


class IntegralsTemplate(golem.templates.kinematics.KinematicsTemplate):
    def setup(
        self,
        loopcache,
        loopcache_tot,
        in_particles,
        out_particles,
        conf,
        heavy_quarks,
        lo_flags,
        nlo_flags,
        eprops,
        helicity_map,
    ):
        self.init_kinematics(
            conf, in_particles, out_particles, heavy_quarks, helicity_map
        )
        self._loopcache = loopcache
        self._loopcache_tot = loopcache_tot
        self._partitions = loopcache.partition()
        self._roots = sorted(self._partitions.keys())
        self._latex_names = golem.util.tools.getModel(conf).latex_parameters
        self._diagram_flags_0 = lo_flags
        self._diagram_flags_1 = nlo_flags
        self._eprops = eprops
        self._n_tree = int(conf["topolopy.count.tree"])

    def maxloopsize(self, *args, **opts):
        return self._format_value(self._loopcache.maxloopsize, **opts)

    def loopsize(self, *args, **opts):
        if "group" in opts:
            nopts = opts.copy()
            del nopts["group"]
            g = self._eval_int(opts["group"], **nopts)
            if g >= 0 and g < len(self._roots):
                ls = self._roots[g].size()
                return self._format_value(ls, **nopts)
            else:
                raise TemplateError("Unknown group in [% loopsize %]")
        elif "diagram" in opts:
            nopts = opts.copy()
            del nopts["diagram"]
            d = self._eval_int(opts["diagram"], **nopts)
            if d in list(self._loopcache.diagrams.keys()):
                ls = loopsize(self._loopcache.diagrams[d])
                return self._format_value(ls, **nopts)
            else:
                raise TemplateError("Unknown diagram in [% loopsize %]")
        else:
            raise TemplateError("[% loopsize %] without diagram= or group=")

    def groups(self, *args, **opts):
        nopts = opts.copy()
        for kw in ["loopsize", "first", "last", "index", "var", "rank"]:
            if kw in nopts:
                del nopts[kw]

        if "loopsize" in opts:
            ls = self._eval_int(opts["loopsize"], **nopts)
            fltr = []
            for i, root in enumerate(self._roots):
                if root.size() == ls:
                    fltr.append(i)
        else:
            fltr = list(range(len(self._roots)))

        if fltr:
            first_name = self._setup_name("first", "is_first", opts)
            last_name = self._setup_name("last", "is_last", opts)
            idx_name = self._setup_name("index", "index", opts)
            value_name = self._setup_name("var", "$_", opts)
            rank_name = self._setup_name("rank", "rank", opts)

            props = Properties()

            for idx, val in enumerate(fltr):
                is_first = val == fltr[0]
                is_last = val == fltr[-1]
                rk = self._roots[idx].getRank()

                props.setProperty(first_name, is_first)
                props.setProperty(last_name, is_last)
                props.setProperty(idx_name, idx)
                props.setProperty(value_name, val)
                props.setProperty(rank_name, rk)

                yield props

    def complex_mass_needed(self, *args, **opts):
        nopts = opts.copy()
        for kw in ["group"]:
            if kw in nopts:
                del nopts[kw]

        if "group" in opts:
            g = self._eval_int(opts["group"], **nopts)
            if g >= 0 and g < len(self._roots):
                fltr = []
                root = self._roots[g]

                size = root.size()
            else:
                raise TemplateError("Unknown group in [% complex_mass_needed %]")
        else:
            raise TemplateError("[% complex_mass_needed %] without 'group='")

        return any([str(root.width(i)) != "0" for i in range(1, size + 1)])

    def propagators(self, *args, **opts):
        nopts = opts.copy()
        for kw in [
            "group",
            "first",
            "last",
            "index",
            "shift",
            "prefix",
            "suffix",
            "momentum",
            "mass",
            "width",
            "select",
        ]:
            if kw in nopts:
                del nopts[kw]

        if "group" in opts:
            g = self._eval_int(opts["group"], **nopts)
            if g >= 0 and g < len(self._roots):
                fltr = []
                root = self._roots[g]

                size = root.size()
            else:
                raise TemplateError("Unknown group in [% propagators %]")
        else:
            raise TemplateError("[% propagators %] must be called per group")

        if "select" in opts:
            lst = self._eval_string(opts["select"])
            selection = list(map(int, lst.split(",")))
        else:
            selection = list(range(1, size + 1))

        if "shift" in opts:
            shift = int(opts["shift"])
        else:
            shift = 0

        if "prefix" in opts:
            s_prefix = opts["prefix"]
        else:
            s_prefix = "k"

        if "suffix" in opts:
            s_suffix = opts["suffix"]
        else:
            s_suffix = ""

        first_name = self._setup_name("first", "is_first", opts)
        last_name = self._setup_name("last", "is_last", opts)
        index_name = self._setup_name("index", "$_", opts)
        mom_name = self._setup_name("momentum", "momentum", opts)
        mass_name = self._setup_name("mass", "mass", opts)
        width_name = self._setup_name("width", "width", opts)

        mass_filter = self._setup_filter(["massive", "massless"], args)
        include_massive = "massive" in mass_filter
        include_massless = "massless" in mass_filter

        props = Properties()
        for i in selection:
            if str(root.mass(i)) == "0":
                if not include_massless:
                    continue
            else:
                if not include_massive:
                    continue

            props.setProperty(index_name, i + shift)
            props.setProperty(first_name, i == 1)
            props.setProperty(last_name, i == size)
            props.setProperty(mom_name, root.rvector(i).format(s_prefix, s_suffix))
            props.setProperty(mass_name, root.mass(i))
            props.setProperty(width_name, root.width(i))

            yield props

    def latex_parameter(self, *args, **opts):
        sym = self._eval_string(args[0])
        factors = []
        for factor in sym.split("*"):
            expo = factor.split("^")
            expo[0] = expo[0].strip()
            if expo[0] in self._latex_names:
                lname = self._latex_names[expo[0]]
            else:
                lname = expo[0]

            if len(expo) == 2:
                factors.append("%s^%s" % (lname, expo[1]))
            else:
                factors.append(lname)

        return "\\cdot{}".join(factors)

    def smat(self, *args, **opts):
        nopts = opts.copy()
        for kw in [
            "group",
            "first",
            "last",
            "rowindex",
            "colindex",
            "shift",
            "bol",
            "eol",
            "re",
            "im",
            "re.zero",
            "im.zero",
            "zero",
            "re",
            "im",
            "prefix",
            "infix",
            "suffix",
            "powfmt",
            "prodfmt",
        ]:
            if kw in nopts:
                del nopts[kw]

        if "prefix" in opts:
            s_prefix = opts["prefix"]
        else:
            s_prefix = "s"

        if "suffix" in opts:
            s_suffix = opts["suffix"]
        else:
            s_suffix = ""

        if "infix" in opts:
            s_infix = opts["infix"]
        else:
            s_infix = ""

        if "powfmt" in opts:
            powfmt = opts["powfmt"]
        else:
            powfmt = "%s**%d"

        if "prodfmt" in opts:
            prodfmt = opts["prodfmt"]
        else:
            prodfmt = "%s*%s"

        if "group" in opts:
            g = self._eval_int(opts["group"], **nopts)
            if g >= 0 and g < len(self._roots):
                fltr = []
                root = self._roots[g]

                onshell = {}
                for i in range(self._num_legs):
                    si = s_prefix + str(i + 1) + s_suffix
                    mi = str(self._masses[i])
                    if mi == "0":
                        onshell[si] = "0"
                    else:
                        onshell[si] = powfmt % (mi, 2)

                smatrix = root.getSMatrix(
                    onshell, powfmt, prodfmt, s_prefix, s_suffix, s_infix
                )
                size = root.size()
            else:
                raise TemplateError("Unknown group in [% smat %]")
        else:
            raise TemplateError("[% smat %] must be called per group")

        first_name = self._setup_name("first", "is_first", opts)
        last_name = self._setup_name("last", "is_last", opts)
        row_name = self._setup_name("rowindex", "rowindex", opts)
        col_name = self._setup_name("colindex", "colindex", opts)
        eol_name = self._setup_name("eol", "eol", opts)
        bol_name = self._setup_name("bol", "bol", opts)
        rez_name = self._setup_name("re.zero", "re.is_zero", opts)
        imz_name = self._setup_name("im.zero", "im.is_zero", opts)
        zero_name = self._setup_name("zero", "is_zero", opts)
        re_name = self._setup_name("re", "re", opts)
        im_name = self._setup_name("im", "im", opts)

        if "shift" in opts:
            shift = int(opts["shift"])
        else:
            shift = 0

        props = Properties()
        entries = []
        eol_entries = []
        bol_entries = []

        for i in range(1, size + 1):
            rng = []
            if "upper" in args or "lower" in args or "diagonal" in args:
                if "lower" in args:
                    rng.extend(list(range(1, i)))
                if "diagonal" in args:
                    rng.append(i)
                if "upper" in args:
                    rng.extend(list(range(i + 1, size + 1)))
            else:
                rng.extend(list(range(1, size + 1)))

            for j in rng:
                reSij, imSij = smatrix[(i, j)]

                if "nonzero" in args and "zero" not in args:
                    if len(reSij) == 0 and len(imSij) == 0:
                        continue
                elif "zero" in args and "nonzero" not in args:
                    if len(reSij) != 0 or len(imSij) != 0:
                        continue

                if "real" in args and "complex" not in args:
                    if len(imSij) != 0:
                        continue
                elif "complex" in args and "real" not in args:
                    if len(imSij) == 0:
                        continue

                if entries:
                    prev_i, prev_j = entries[-1]
                    if prev_i != i:
                        eol_entries.append((prev_i, prev_j))
                        bol_entries.append((i, j))
                else:
                    bol_entries.append((i, j))
                entries.append((i, j))

        if entries:
            eol_entries.append(entries[-1])

        N = len(entries)
        count = 0
        for i, j in entries:
            reSij, imSij = smatrix[(i, j)]

            sre = ";".join(
                ["%s:%s" % (coeff, sym) for sym, coeff in list(reSij.items())]
            )
            sim = ";".join(
                ["%s:%s" % (coeff, sym) for sym, coeff in list(imSij.items())]
            )

            props.setProperty(row_name, i + shift)
            props.setProperty(col_name, j + shift)
            props.setProperty(first_name, count == 0)
            props.setProperty(last_name, count == N - 1)
            props.setProperty(bol_name, (i, j) in bol_entries)
            props.setProperty(eol_name, (i, j) in eol_entries)
            props.setProperty(rez_name, len(reSij) == 0)
            props.setProperty(imz_name, len(imSij) == 0)
            props.setProperty(zero_name, len(imSij) == 0 and len(reSij) == 0)
            props.setProperty(re_name, sre)
            props.setProperty(im_name, sim)

            yield props

            count += 1

    def lo_flags(self, *args, **opts):
        if "diagram" in opts:
            nopts = opts.copy()
            del nopts["diagram"]
            d = self._eval_int(opts["diagram"], **nopts)
            result = []
            for key, value in list(self._diagram_flags_0.items()):
                if d in value:
                    result.append(str(key))
            return " ".join(result)
        else:
            return " ".join(map(str, list(self._diagram_flags_0.keys())))

    def nlo_flags(self, *args, **opts):
        if "group" in opts:
            nopts = opts.copy()
            del nopts["group"]
            g = self._eval_int(opts["group"], **nopts)
            if g >= 0 and g < len(self._roots):
                fltr = []
                root = self._roots[g]
                diagrams = set(
                    [idx for idx, keep, pinch, shift in self._partitions[root]]
                )
                result = []

                for key, lst in list(self._diagram_flags_1.items()):
                    if len(diagrams.intersection(lst)) > 0:
                        result.append(str(key))
                return " ".join(result)
            else:
                raise TemplateError("Unknown group in [% diagrams %]")
        else:
            return " ".join(map(str, list(self._diagram_flags_1.keys())))

    def diagram_sum(self, *args, **opts):
        return ",".join(map(str, self._eprops))

    def subdiagram_sum(self, *args, **opts):
        nopts = opts.copy()
        for kw in ["group", "var", "nf"]:
            if kw in nopts:
                del nopts[kw]
        if "group" in opts:
            g = self._eval_int(opts["group"], **nopts)
            value_name = self._setup_name("var", "$_", opts)
            nf_name = self._setup_name("nf", "is_nf", opts)
            nf_lst = set([])
            props = Properties()
            for idx in self._eprops[g]:
                if is_nf(self._loopcache_tot.diagrams[idx]):
                    nf_lst.add(idx)
                props.setProperty(nf_name, idx in nf_lst)
                props.setProperty(value_name, str(idx))
                yield props
        else:
            raise TemplateError("[% subdiagram_sum %] must be called per group")

    def use_flags_0(self, *args, **opts):
        return len(list(self._diagram_flags_0.keys())) > 1

    def use_flags_1(self, *args, **opts):
        return len(list(self._diagram_flags_1.keys())) > 1

    def min_diagram_1(self, *args, **opts):
        return str(min(self._loopcache.diagrams.keys()))

    def max_diagram_1(self, *args, **opts):
        return str(max(self._loopcache.diagrams.keys()))

    def min_diagram_0(self, *args, **opts):
        return 0

    def max_diagram_0(self, *args, **opts):
        return self._n_tree

    @staticmethod
    def ninjaidx_formula(nlegs, rk):
        # return max( rk - nlegs + 3 - max(3-nlegs,0) , -1)
        return max(rk - nlegs + 3 - max(3 - nlegs, 0), -1)

    @staticmethod
    def ninjaidxb_formula(nlegs, rk):
        return max(rk - nlegs + 2 - max(2 - nlegs, 0), -1)

    def diagrams(self, *args, **opts):
        nopts = opts.copy()
        for kw in [
            "loopsize",
            "group",
            "var",
            "pinches",
            "first",
            "last",
            "indices",
            "index",
            "shift",
            "rank",
            "ninjaidx",
            "ninjaidxb",
            "idxshift",
            "unpinched",
            "invert",
            "nf",
            "global_index",
            "mqse",
        ]:
            if kw in nopts:
                del nopts[kw]

        diagrams = self._loopcache.diagrams
        keep_lst = {}
        pinch_lst = {}
        shift_lst = {}
        rank_lst = {}
        ninjaidx_lst = {}
        ninjaidxb_lst = {}
        nf_lst = set([])
        top_se = set([])

        if "group" in opts:
            g = self._eval_int(opts["group"], **nopts)
            if g >= 0 and g < len(self._roots):
                fltr = []
                root = self._roots[g]
                for idx, keep, pinch, shift in self._partitions[root]:
                    fltr.append(idx)
                    keep_lst[idx] = keep
                    pinch_lst[idx] = pinch
                    shift_lst[idx] = shift
                    rank_lst[idx] = rank(diagrams[idx])
                    ninjaidx_lst[idx] = self.ninjaidx_formula(
                        loopsize(diagrams[idx]), rank_lst[idx]
                    )
                    ninjaidxb_lst[idx] = self.ninjaidxb_formula(
                        loopsize(diagrams[idx]), rank_lst[idx]
                    )
                    if is_nf(diagrams[idx]):
                        nf_lst.add(idx)
                    if massive_quark_self_energy(diagrams[idx]):
                        top_se.add(idx)
            else:
                raise TemplateError("Unknown group in [% diagrams %]")
        else:
            raise TemplateError("[% diagrams %] must be called per group")

        if "loopsize" in opts:
            ls = self._eval_int(opts["loopsize"], **nopts)
            fltr = list([d for d in fltr if loopsize(diagrams[d]) == ls])

        first_name = self._setup_name("first", "is_first", opts)
        last_name = self._setup_name("last", "is_last", opts)
        idx_name = self._setup_name("index", "index", opts)
        value_name = self._setup_name("var", "$_", opts)

        keep_name = self._setup_name("indices", "indices", opts)
        pinch_name = self._setup_name("pinches", "pinches", opts)
        shift_name = self._setup_name("shift", "shift", opts)
        sign_name = self._setup_name("sign", "sign", opts)
        rank_name = self._setup_name("rank", "rank", opts)
        ninjaidx_name = self._setup_name("ninjaidx", "ninjaidx", opts)
        ninjaidxb_name = self._setup_name("ninjaidxb", "ninjaidxb", opts)
        nf_name = self._setup_name("nf", "is_nf", opts)
        mqse_name = self._setup_name("mqse", "is_mqse", opts)
        globi_name = self._setup_name("global_index", "global_index", opts)
        flags_name = self._setup_name("flags", "flags", opts)

        if "idxshift" in opts:
            idxshift = int(opts["idxshift"])
        else:
            idxshift = 0

        if "unpinched" in opts:
            if len(opts["unpinched"].strip()) > 0:
                unpinched = list(map(int, str(self._eval_int(opts["unpinched"]))))
            else:
                unpinched = []
        else:
            unpinched = []

        unpinched = set(unpinched)

        if "invert" in opts:
            keep_null_diagrams = self._eval_bool(opts["invert"])
        else:
            keep_null_diagrams = False

        old_fltr = fltr
        fltr = []
        orig_index = {}

        for oi, diagram_index in enumerate(old_fltr):
            pinches = set(pinch_lst[diagram_index])
            some_pinch_is_zero = bool(pinches.intersection(unpinched))
            if keep_null_diagrams == some_pinch_is_zero:
                fltr.append(diagram_index)
                orig_index[diagram_index] = oi

        N = len(fltr)
        props = Properties()

        for idx, diagram_index in enumerate(fltr):
            is_first = idx == 0
            is_last = idx == N - 1

            pinches = set(pinch_lst[diagram_index])

            shift = shift_lst[diagram_index]
            if shift.sign() >= 0:
                qsign = "+"
            else:
                qsign = "-"

            shift_vec = shift.shift_vector()
            props.setProperty(first_name, is_first)
            props.setProperty(last_name, is_last)
            props.setProperty(value_name, diagram_index)
            props.setProperty(idx_name, idx)
            props.setProperty(
                keep_name,
                ",".join(map(str, [x + idxshift for x in keep_lst[diagram_index]])),
            )
            props.setProperty(
                pinch_name,
                ",".join(map(str, [x + idxshift for x in pinch_lst[diagram_index]])),
            )
            props.setProperty(shift_name, shift_vec)
            props.setProperty(sign_name, qsign)
            props.setProperty(rank_name, rank_lst[diagram_index])
            props.setProperty(ninjaidx_name, ninjaidx_lst[diagram_index])
            props.setProperty(ninjaidxb_name, ninjaidxb_lst[diagram_index])
            props.setProperty(globi_name, orig_index[diagram_index])
            props.setProperty(nf_name, diagram_index in nf_lst)
            props.setProperty(mqse_name, diagram_index in top_se)
            props.setProperty(
                flags_name,
                " ",  # " ".join(diagrams[diagram_index].filter_flags) TODO: filter flags
            )
            yield props
