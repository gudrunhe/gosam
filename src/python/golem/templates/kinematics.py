# vim: ts=3:sw=3:expandtab
import golem
import golem.algorithms.mandelstam
import golem.algorithms.color
import golem.util.tools

from golem.util.config import Properties, split_power
import golem.util.parser
from golem.model import MODEL_OPTIONS


class KinematicsTemplate(golem.util.parser.Template):
    """
    Implements a template that has knowledge about the
    kinematics of the process, especially, massive and
    light-like vectors and Mandelstam variables.
    """

    def init_kinematics(self, conf, in_particles, out_particles, tree_signs, heavy_quarks, helicity_map, ct_signs):
        self._mandel_stack = []
        zeroes = golem.util.tools.getZeroes(conf)
        self._zeroes = zeroes
        ones = golem.util.tools.getOnes(conf)
        self._ones = ones

        self._model = golem.util.tools.getModel(conf)
        self._modeltype = conf.getProperty("modeltype")
        if not self._modeltype:
            self._modeltype = conf.getProperty("model")

        props = Properties()
        props["order"] = conf[golem.properties.coupling_power]
        props.setProperty("modeltype", self._modeltype)

        num_in = len(in_particles)
        num_out = len(out_particles)
        num_legs = num_in + num_out

        self._num_in = num_in
        self._num_out = num_out
        self._num_legs = num_legs

        all_mndlst = conf.getProperty(golem.properties.all_mandelstam)

        self._all_mndlst = all_mndlst

        self._helicity_map = helicity_map
        self._heavy_quarks = heavy_quarks
        self._complex_masses = conf["complex_masses"]
        self._ehc = conf["ehc"]

        self._references = golem.algorithms.helicity.reference_vectors(conf, in_particles, out_particles)

        self._name = []
        self._masses = []
        self._lightlike = []
        self._twospin = []
        self._spin = []
        self._color = []
        self._acolor = []
        self._helicities = []
        self._latex = []
        self._helicity_stack = []
        self._mapping_stack = []
        self._current_helicity_list_stack = []
        self._current_mapping_list_stack = []
        self._color_stack = []
        self._cs_stack = []
        self._cs_line_stack = []
        self._cs_trace_stack = []
        self._field_info = []
        self._tree_signs = tree_signs
        self._ct_signs = ct_signs
        # self._tree_flows = tree_flows
        self._crossings = []
        self._charge = []

        self._msubs_stack = []

        self._listed_flags = set()
        self._listed_flags_length = 0

        for i, crossing in enumerate(conf.getProperty(golem.properties.crossings)):
            if ":" in crossing:
                pos = crossing.index(":")
                self._crossings.append(crossing[:pos].strip())

        self._flavour_groups = []
        self._flavour_dict = {}
        for i, fg in enumerate(conf.getProperty(golem.properties.flavour_groups)):
            if fg == "":
                break
            for flv in list(map(int, fg.split(":"))):
                self._flavour_dict[flv] = (i, "fg" + str(i))
                self._flavour_dict[-flv] = (i, "fgbar" + str(i))
            self._flavour_groups.append(list(map(int, fg.split(":"))))

        def get_qed_sign(pdg, sign):
            if (pdg > 0 and pdg < 20 and sign > 0) or (pdg < 0 and pdg > -20 and sign < 0):
                qed_sign = 1
            elif (pdg > 0 and pdg < 20 and sign < 0) or (pdg < 0 and pdg > -20 and sign > 0):
                qed_sign = -1
            elif pdg == 24:
                qed_sign = -1
            elif pdg == -24:
                qed_sign = 1
            else:
                qed_sign = 0

            return qed_sign

        def examine_particle(p, sign):
            name = str(p)
            mass = p.getMass(zeroes)
            twospin = p.getSpin()
            color = sign * p.getColor()
            acolor = p.getColor()
            latex = p.getLaTeXName()
            charge = p.getCharge()

            self._name.append(name)
            self._masses.append(mass)
            self._latex.append(latex)

            qed_sign = get_qed_sign(p.getPDGCode(), sign)
            self._charge.append(qed_sign * charge)
            # if p.getPDGCode() > 0:
            # if p.getField().lower()=='u' or p.getField().lower()=='c' or p.getField().lower()=='t':
            # self._charge.append(-charge*sign)
            # elif p.getField().lower()=='d' or p.getField().lower()=='s' or p.getField().lower()=='b':
            # self._charge.append(charge*sign)
            # elif p.getPDGCode()==24:
            # self._charge.append(-charge*sign)
            # else:
            # self._charge.append(charge*sign)
            # else:
            # if p.getField().lower()=='ubar' or p.getField().lower()=='cbar' or p.getField().lower()=='tbar':
            # self._charge.append(charge*sign)
            # elif p.getField().lower()=='dbar' or p.getField().lower()=='sbar' or p.getField().lower()=='bbar':
            # self._charge.append(-charge*sign)
            # elif p.getPDGCode()==-24:
            # self._charge.append(-charge*sign)
            # else:
            # self._charge.append(-charge*sign)

            self._lightlike.append(not p.isMassive(zeroes))

            self._twospin.append(twospin)
            if twospin % 2 == 0:
                self._spin.append(str(twospin / 2))
            else:
                self._spin.append("%d/2" % twospin)

            self._color.append(color)
            self._acolor.append(acolor)
            self._helicities.append(p.getHelicityStates(zeroes))
            field_info = (str(p), p.getPartner(), sign)
            self._field_info.append(field_info)

        ################# end examine_particle(p)

        for ini in in_particles:
            examine_particle(ini, +1)

        identical_particles = {}
        for fin in out_particles:
            examine_particle(fin, -1)
            if str(fin) in identical_particles:
                identical_particles[str(fin)] += 1
            else:
                identical_particles[str(fin)] = 1
        symmetry_factor = 1
        for multi in list(identical_particles.values()):
            fact = golem.util.tools.factorial(multi)
            symmetry_factor *= fact

        props.setProperty("num_in", num_in)
        props.setProperty("num_out", num_out)
        props.setProperty("num_legs", num_legs)
        props.setProperty("num_helicities", golem.util.tools.product(list(map(len, self._helicities))))
        props.setProperty("in_helicities", golem.util.tools.product(list(map(len, self._helicities[:num_in]))))
        props.setProperty("symmetry_factor", symmetry_factor)
        props.setProperty("charge", self._charge)

        # predict the number of colors:
        F = 0
        AF = 0
        G = 0
        for color in self._color:
            if color == -3:
                AF += 1
            elif color == 3:
                F += 1
            elif abs(color) == 8:
                G += 1
            elif abs(color) == 1:
                pass
            else:
                assert False, "Color representation %d is not covered yet." % color
        if F != AF:
            props.setProperty("num_colors", 0)
        else:
            props.setProperty("num_colors", golem.algorithms.color.num_colors(F, G))

        self._properties = props
        self._mandel = golem.algorithms.mandelstam.mandelstam_calc(num_in, num_out, all_inv=all_mndlst)
        self._mandel_parts = golem.algorithms.mandelstam.mandelstam_calc(
            num_in, num_out, prefix="", infix=" ", suffix="", all_inv=all_mndlst
        )

        helic = {}
        for i in range(num_legs):
            helic[i] = self._helicities[i]

        self._helicity_comb = [h for h in golem.util.tools.enumerate_helicities(conf)]

        self._helicity_map = helicity_map

    def crossed_color(self, *args, **opts):
        cri = [prop.getIntegerProperty("$_") for prop in self.crossing()]
        crs = [int(prop.getProperty("sign") + "1") for prop in self.crossing()]

        ini_indices = list(range(self._num_in))
        fin_indices = list(range(self._num_in, self._num_in + self._num_out))

        use_indices = ini_indices + fin_indices
        sel_indices = []

        if "initial" in args:
            use_indices = sel_indices
            sel_indices.extend(ini_indices)
        if "final" in args:
            use_indices = sel_indices
            sel_indices.extend(fin_indices)

        first_name = self._setup_name("first", "is_first", opts)
        last_name = self._setup_name("last", "is_last", opts)
        index_name = self._setup_name("index", "index", opts)
        var_name = self._setup_name("var", "$_", opts)

        color = [self._color[i - 1] for i in cri]

        last = len(use_indices) - 1
        props = Properties()
        for count, idx in enumerate(use_indices):
            is_first = count == 0
            is_last = count == last

            props.setProperty(first_name, str(is_first))
            props.setProperty(last_name, str(is_last))
            props.setProperty(index_name, str(idx))
            props.setProperty(var_name, str(color[idx]))
            yield props

    def crossed_helicities(self, *args, **opts):
        cri = [prop.getIntegerProperty("$_") for prop in self.crossing()]
        crs = [int(prop.getProperty("sign") + "1") for prop in self.crossing()]

        ini_indices = list(range(self._num_in))
        fin_indices = list(range(self._num_in, self._num_in + self._num_out))

        use_indices = ini_indices + fin_indices
        sel_indices = []

        if "initial" in args:
            use_indices = sel_indices
            sel_indices.extend(ini_indices)
        if "final" in args:
            use_indices = sel_indices
            sel_indices.extend(fin_indices)

        first_name = self._setup_name("first", "is_first", opts)
        last_name = self._setup_name("last", "is_last", opts)
        index_name = self._setup_name("index", "index", opts)
        var_name = self._setup_name("var", "$_", opts)

        num_helis = [len(self._helicities[i - 1]) for i in cri]

        last = len(use_indices) - 1
        props = Properties()
        for count, idx in enumerate(use_indices):
            is_first = count == 0
            is_last = count == last

            props.setProperty(first_name, str(is_first))
            props.setProperty(last_name, str(is_last))
            props.setProperty(index_name, str(idx))
            props.setProperty(var_name, str(num_helis[idx]))
            yield props

    def crossed_symmetry_factor(self, *args, **opts):
        cri = [prop.getIntegerProperty("$_") for prop in self.crossing()]
        crs = [int(prop.getProperty("sign") + "1") for prop in self.crossing()]
        fields = self._field_info

        fin = list(range(self._num_in, self._num_in + self._num_out))
        fin_indices = [cri[i] for i in fin]
        fin_signs = [crs[i] for i in fin]

        particles = {}
        for idx, sign in zip(fin_indices, fin_signs):
            field, anti, f_sign = fields[idx - 1]
            if sign == -1:
                prtcl = anti
            else:
                prtcl = field

            if prtcl in particles:
                particles[prtcl] += 1
            else:
                particles[prtcl] = 1

        symmetry_factor = 1
        for multi in list(particles.values()):
            fact = golem.util.tools.factorial(multi)
            symmetry_factor *= fact

        return str(symmetry_factor)

    def __call__(self, *conf):
        for chunk in golem.util.parser.Template.__call__(self, self._properties, *conf):
            yield chunk

    def effective_higgs(self, *args, **opts):
        ehc = self._setup_name("ehc", "is_ehc", opts)
        props = Properties()
        props[ehc] = self._ehc

        yield props

    def quark_loop_masses(self, *args, **opts):
        quark_masses = self._heavy_quarks
        complex_masses = self._complex_masses

        if "prefix" in opts:
            prefix = opts["prefix"]
        else:
            prefix = ""
        var_name = self._setup_name("var", prefix + "$_", opts)
        first_name = self._setup_name("first", prefix + "is_first", opts)
        last_name = self._setup_name("last", prefix + "is_last", opts)
        real_mass = self._setup_name("real_mass", prefix + "is_real", opts)
        complex_mass = self._setup_name("complex_mass", prefix + "is_complex", opts)

        props = Properties()
        complex_mass_list = []

        for term in complex_masses.split(","):
            complex_mass_list.append(term)
        N = len(complex_mass_list) // 2

        if N > 0:
            for i, mass in enumerate(complex_mass_list[::2]):
                props[first_name] = i == 0
                props[last_name] = i == N - 1
                if len(complex_mass_list) > 1:
                    if str(complex_mass_list[2 * i + 1]) != "0":
                        width = complex_mass_list[2 * i + 1]
                        props[var_name] = "sqrt(" + mass + "**2-i_*" + mass + "*" + width + ")"
                        props[real_mass] = False
                        props[complex_mass] = True
                    else:
                        props[var_name] = mass
                        props[real_mass] = True
                        props[complex_mass] = False
                else:
                    props[var_name] = mass
                    props[real_mass] = True
                    props[complex_mass] = False

                yield props

    def tree_sign(self, *args, **opts):
        if len(args) == 0:
            raise golem.util.parser.TemplateError("[% tree_sign %] without diagram number.")

        diag = self._eval_int(args[0])

        if diag in self._tree_signs:
            return str(self._tree_signs[diag])
        else:
            raise golem.util.parser.TemplateError("[% tree_sign %] with unknown diagram number.")

    def ct_sign(self, *args, **opts):
        if len(args) == 0:
            raise golem.util.parser.TemplateError("[% ct_sign %] without diagram number.")

        diag = self._eval_int(args[0])

        if diag in self._ct_signs:
            return str(self._ct_signs[diag])
        else:
            raise golem.util.parser.TemplateError("[% ct_sign %] with unknown diagram number.")

    def _OBSOLETE_tree_flow(self, *args, **opts):
        first_name = self._setup_name("first", "is_first", opts)
        last_name = self._setup_name("last", "is_last", opts)
        index_name = self._setup_name("index", "index", opts)
        var_name = self._setup_name("var", "$_", opts)
        props = Properties()

        if len(args) == 0:
            raise golem.util.parser.TemplateError("[% tree_flow %] without diagram number.")

        diag = self._eval_int(args[0])

        if diag not in self._tree_flows:
            raise golem.util.parser.TemplateError("[% tree_sign %] with unknown diagram number.")

        flow = self._tree_flows[diag]
        N = len(flow)

        for i, l in enumerate(flow.keys()):
            is_first = i == 0
            is_last = i == N - 1
            value = flow[l]

            props.setProperty(first_name, str(is_first))
            props.setProperty(last_name, str(is_last))
            props.setProperty(index_name, str(l))
            props.setProperty(var_name, str(value))
            yield props

    def crossings(self, *args, **opts):
        first_name = self._setup_name("first", "is_first", opts)
        last_name = self._setup_name("last", "is_last", opts)
        index_name = self._setup_name("index", "index", opts)
        var_name = self._setup_name("var", "$_", opts)

        l = len(self._crossings)

        props = golem.util.config.Properties()
        for i, name in enumerate(self._crossings):
            props.setProperty(first_name, i == 0)
            props.setProperty(last_name, i >= l - 1)
            props.setProperty(index_name, i)
            props.setProperty(var_name, name)
            yield props

    def return_PDG(self, p):
        return p.getPDGCode()

    def crossing(self, *args, **opts):
        first_name = self._setup_name("first", "is_first", opts)
        last_name = self._setup_name("last", "is_last", opts)
        index_name = self._setup_name("index", "index", opts)
        var_name = self._setup_name("var", "$_", opts)
        sign_name = self._setup_name("sign", "sign", opts)

        initial = [str(golem.util.tools.interpret_particle_name(n, self._model)) for n in self.initial().split(",")]
        final = [str(golem.util.tools.interpret_particle_name(n, self._model)) for n in self.final().split(",")]
        field_info = self._field_info
        flvgrps = self._flavour_groups

        if flvgrps == []:
            use_flvgrps = False
        else:
            use_flvgrps = True
            flvgrps_dict = self._flavour_dict

        # Try to directly match the particle names first:
        mapping, unmatched = self.find_mapping(field_info, initial, final)

        # Any unmatched particles? -> check if we use flavour groups, otherwise exit with error
        if len(unmatched) != 0:
            if not use_flvgrps:
                raise golem.util.parser.TemplateError("No valid crossing found (%s)." % ",".join(map(str, unmatched)))
            else:
                # translate 'field_info' into flavour_groups, using k to distinguish different quarks form the same flavour group
                k = [1 for _ in range(len(flvgrps))]
                field_info_fg = [None for _ in range(len(field_info))]
                skip = [False for _ in range(len(field_info))]
                for i, fti in enumerate(field_info):
                    if skip[i]:
                        continue
                    pdgf = self.return_PDG(golem.util.tools.interpret_particle_name(fti[0], self._model))
                    pdga = self.return_PDG(golem.util.tools.interpret_particle_name(fti[1], self._model))
                    if pdgf in flvgrps_dict and pdga in flvgrps_dict:
                        fgf = flvgrps_dict[pdgf]
                        fga = flvgrps_dict[pdga]
                        s_fgf = fgf[1] + str(k[fgf[0]])
                        s_fga = fga[1] + str(k[fgf[0]])
                        k[fgf[0]] = k[fgf[0]] + 1
                    else:
                        fgf = str(pdgf)
                        fga = str(pdga)
                    for j, ftj in enumerate(field_info):
                        if skip[j]:
                            continue
                        if ftj[0] == fti[0] and ftj[1] == fti[1]:
                            field_info_fg[j] = (fgf, fga, ftj[2])
                            skip[j] = True
                        elif ftj[1] == fti[0] and ftj[0] == fti[1]:
                            field_info_fg[j] = (fga, fgf, ftj[2])
                            skip[j] = True

                # translate 'initial' and 'final' into flavour_groups, using k to distinguish different quarks form the same flavour group
                k = [1 for _ in range(len(flvgrps))]
                curr_chan = [
                    (
                        golem.util.tools.interpret_particle_name(p, self._model).getPDGCode(),
                        golem.util.tools.interpret_particle_name(p, self._model).getPartnerPDGCode(),
                    )
                    for p in initial + final
                ]
                initial_fg = [None for _ in range(len(initial))]
                final_fg = [None for _ in range(len(final))]
                skip = [False for _ in range(len(curr_chan))]
                for i, fti in enumerate(curr_chan):
                    if skip[i]:
                        continue
                    if fti[0] in flvgrps_dict and fti[1] in flvgrps_dict:
                        fgf = flvgrps_dict[fti[0]]
                        fga = flvgrps_dict[fti[1]]
                        s_fgf = fgf[1] + str(k[fgf[0]])
                        s_fga = fga[1] + str(k[fgf[0]])
                        k[fgf[0]] = k[fgf[0]] + 1
                    else:
                        fgf = str(fti[0])
                        fga = str(fti[1])
                    for j, ftj in enumerate(curr_chan):
                        if skip[j]:
                            continue
                        if ftj[0] == fti[0]:
                            if j < len(initial):
                                initial_fg[j] = fgf
                            else:
                                final_fg[j - len(initial)] = fgf
                            skip[j] = True
                        elif ftj[1] == fti[0]:
                            if j < len(initial):
                                initial_fg[j] = fga
                            else:
                                final_fg[j - len(initial)] = fga
                            skip[j] = True

                # Try to match the flavour groups
                mapping, unmatched = self.find_mapping(field_info_fg, initial_fg, final_fg)

                # Still any unmatched particles? -> exit with error
                if len(unmatched) != 0:
                    raise golem.util.parser.TemplateError(
                        "No valid crossing found (%s)." % ",".join(map(str, unmatched))
                    )

        props = golem.util.config.Properties()

        l = len(mapping)
        i = 0
        for new_vec, old_vec in list(mapping.items()):
            props.setProperty(first_name, i == 0)
            props.setProperty(last_name, i >= l - 1)
            i += 1

            if old_vec < 0:
                sign = "-"
            else:
                sign = "+"

            props.setProperty(index_name, new_vec)
            props.setProperty(var_name, abs(old_vec))
            props.setProperty(sign_name, sign)
            yield props

    def find_mapping(self, field_info, initial, final):
        avail = set(range(1, len(field_info) + 1))
        mapping = {}
        unmatched = []

        for i, field in enumerate(initial):
            found = 0
            for j in avail:
                f, a, s = field_info[j - 1]
                if s == 1 and field == f:
                    found = j
                    break
                elif s == -1 and field == a:
                    found = -j
                    break
            if found != 0:
                mapping[i + 1] = found
                avail.remove(abs(found))
            else:
                unmatched.append((i, field))

        l = len(initial)
        for k, field in enumerate(final):
            found = 0
            for j in avail:
                f, a, s = field_info[j - 1]
                if s == -1 and field == f:
                    found = j
                    break
                elif s == 1 and field == a:
                    found = -j
                    break
            if found != 0:
                mapping[k + l + 1] = found
                avail.remove(abs(found))
            else:
                unmatched.append((i, field))

        return (mapping, unmatched)

    def loqcd(self, *args, **opts):
        """
        Deduct the number of QCD couplings at LO

        args -- optional list of names that refer to QCD couplings
        """
        if args:
            names = [s.lower() for s in args]
        else:
            names = ["qcd", "gg", "gs"]

        order = [s.strip().lower() for s in self._properties.getProperty("order").split(",")]
        if order[0] in names:
            # coupling is qcd
            if order[1] == "none":
                # we just assume the LO QCD order is NLO - 2
                return str(int(order[2]) - 2)
            else:
                return str(int(order[1]))
        else:
            # coupling is ew
            # over all number of tree level couplings (qcd+qed)
            lo_couplings = self._num_legs - 2
            if order[1] == "none":
                # we just assume the LO EW order is NLO - 2
                return str(lo_couplings - (int(order[2]) - 2))
            else:
                return str(lo_couplings - int(order[1]))

    def isqcd(self, *args, **opts):
        """
        Deduct the correction type

        args -- optional list of names that refer to QCD couplings
        """
        if args:
            names = [s.lower() for s in args]
        else:
            names = ["qcd", "gg", "gs"]

        orders = split_power(self._properties.getProperty("order"))
        if not orders:
            return False

        order = [str(s).strip().lower() for s in orders[0]]
        if len(order) < 3:
            return False

        if order[0] in names:
            # coupling is qcd
            if order[1] == "none":
                return True
            else:
                return int(order[1]) < int(order[2])
        else:
            # coupling is ew
            if order[1] == "none":
                return False
            else:
                return int(order[1]) >= int(order[2])

    def particles(self, *args, **opts):
        inout_filter = self._setup_filter(["initial", "final"], args)
        mass_filter = self._setup_filter(["massive", "lightlike"], args)

        if "prefix" in opts:
            prefix = opts["prefix"]
        else:
            prefix = ""
        name_name = self._setup_name("name", prefix + "name", opts)
        index_name = self._setup_name("index", prefix + "index", opts)
        out_index_name = self._setup_name("out_index", prefix + "out_index", opts)
        helicity_name = self._setup_name("hel", prefix + "hel", opts)
        mass_name = self._setup_name("mass", prefix + "mass", opts)
        spin_name = self._setup_name("spin", prefix + "spin", opts)
        twospin_name = self._setup_name("2spin", prefix + "2spin", opts)
        lightlike_name = self._setup_name("lightlike", prefix + "is_lightlike", opts)
        massive_name = self._setup_name("massive", prefix + "is_massive", opts)
        ini_name = self._setup_name("initial", prefix + "is_initial", opts)
        fin_name = self._setup_name("final", prefix + "is_final", opts)
        color_name = self._setup_name("color", prefix + "color", opts)
        latex_name = self._setup_name("latex", prefix + "latex", opts)
        reference_name = self._setup_name("reference", prefix + "reference", opts)
        n_sc = self._setup_name("n_sc", prefix + "n_sc", opts)
        n_sc1 = self._setup_name("n_sc1", prefix + "n_sc1", opts)
        charge_name = self._setup_name("charge", prefix + "charge", opts)

        first_name = self._setup_name("first", prefix + "is_first", opts)
        last_name = self._setup_name("last", prefix + "is_last", opts)

        is_first = True
        base = 1
        nsc = -1

        color_filter = []
        spin_filter = []
        charge_filter = []

        if "white" in args:
            color_filter.extend([1, -1])
        if "colored" in args:
            color_filter.extend([3, -3, 8, -8])
        if "fundamental" in args:
            color_filter.extend([-3, 3])
        if "quarks" in args:
            color_filter.append(3)
        if "anti-quarks" in args:
            color_filter.append(-3)
        if ("adjoint" in args) or ("gluons" in args):
            color_filter.extend([-8, 8])

        if len(color_filter) == 0:
            color_filter = [1, -1, 3, -3, 8, -8]

        if "scalar" in args:
            spin_filter.append(0)
        if "spinor" in args:
            spin_filter.extend([-1, 1])
        if "vector" in args:
            spin_filter.extend([-2, 2])
        if "vectorspinor" in args:
            spin_filter.extend([-3, 3])
        if "tensor" in args:
            spin_filter.extend([-4, 4])

        if "boson" in args:
            spin_filter.extend([-4, -2, 0, 2, 4])
        if "fermion" in args:
            spin_filter.extend([-3, -1, 3, 1])
        if "charged" in args:
            charge_filter.extend([1.0, -1.0, 1.0 / 3.0, -1.0 / 3.0, 2.0 / 3.0, -2.0 / 3.0])

        if len(spin_filter) == 0:
            spin_filter = [-4, -3, -2, -1, 0, 1, 2, 3, 4]

        props = Properties()

        if "initial" in inout_filter:
            start_index = 0
        else:
            start_index = self._num_in

        if "final" in inout_filter:
            end_index = self._num_legs
        else:
            end_index = self._num_in

        # when using "particles" as iterator, which is the last object 
        # depends on applied filters, so we have to run the loop twice
        last_index = start_index
        for index in range(start_index, end_index):
            if self._lightlike[index]:
                if "lightlike" not in mass_filter:
                    continue
            else:
                if "massive" not in mass_filter:
                    continue

            color = self._color[index]
            if color not in color_filter:
                continue

            tspin = self._twospin[index]
            if tspin not in spin_filter:
                continue

            charge = self._charge[index]
            # if charge not in charge_filter:
            # continue

            last_index = index
            

        for index in range(start_index, end_index):
            if self._lightlike[index]:
                if "lightlike" not in mass_filter:
                    continue
            else:
                if "massive" not in mass_filter:
                    continue

            color = self._color[index]
            if color not in color_filter:
                continue

            tspin = self._twospin[index]
            if tspin not in spin_filter:
                continue

            charge = self._charge[index]
            # if charge not in charge_filter:
            # continue

            if index==last_index:
                props.setProperty(last_name, True)
            else:
                props.setProperty(last_name, False)

            props.setProperty(first_name, is_first)
            is_first = False
            props.setProperty(name_name, self._name[index])
            props.setProperty(index_name, index + base)
            props.setProperty(mass_name, self._masses[index])
            props.setProperty(spin_name, self._spin[index])
            props.setProperty(twospin_name, self._twospin[index])
            props.setProperty(latex_name, self._latex[index])
            props.setProperty(lightlike_name, self._lightlike[index])
            props.setProperty(massive_name, not self._lightlike[index])
            props.setProperty(ini_name, index < self._num_in)
            props.setProperty(charge_name, charge)
            if index >= self._num_in:
                props.setProperty(out_index_name, index + base - self._num_in)
            else:
                props.setProperty(
                    out_index_name, "[%% ' ERROR: initial state particle, %s not defined. ' %%]" % out_index_name
                )

            if len(self._helicity_stack) > 0:
                if index in self._helicity_stack[-1]:
                    props.setProperty(helicity_name, self._helicity_stack[-1][index])
                else:
                    props.setProperty(
                        helicity_name, "[%% ' ERROR: %s not defined for this particle. ' %%]" % helicity_name
                    )
            elif len(self._current_helicity_list_stack) > 0:
                sym = golem.algorithms.helicity.heli_to_symbol
                symbol_plus = self._setup_name("symbol_plus", sym[+1], opts)
                symbol_minus = self._setup_name("symbol_minus", sym[-1], opts)
                symbol_plus2 = self._setup_name("symbol_plus2", sym[+2], opts)
                symbol_minus2 = self._setup_name("symbol_minus2", sym[-2], opts)
                symbol_zero = self._setup_name("symbol_zero", sym[0], opts)
                symbols = {-2: symbol_minus2, -1: symbol_minus, 0: symbol_zero, +1: symbol_plus, +2: symbol_plus2}
                encoded_h = golem.util.tools.encode_helicity(self._current_helicity_list_stack[-1][0][1], symbols)
                if index in encoded_h:
                    props.setProperty(helicity_name, encoded_h[index])
                else:
                    props.setProperty(
                        helicity_name, "[%% ' ERROR: %s not defined for this particle. ' %%]" % helicity_name
                    )

            if index in self._references:
                refk = self._references[index]
                if refk.startswith("k"):
                    props.setProperty(reference_name, int(refk[1:]))
                else:
                    assert refk.startswith("l")
                    props.setProperty(reference_name, -int(refk[1:]))
            else:
                props.setProperty(reference_name, 0)

            props.setProperty(fin_name, index >= self._num_in)
            props.setProperty(color_name, color)
            nsc += 2
            nsc1 = nsc + 1
            props.setProperty(n_sc, nsc)
            props.setProperty(n_sc1, nsc1)
            yield props

    def pairs(self, *args, **opts):
        if "prefix" in opts:
            prefix = opts["prefix"]
        else:
            prefix = ""

        inout1_filter = self._setup_filter(["initial1", "final1"], args)
        inout2_filter = self._setup_filter(["initial2", "final2"], args)
        mass1_filter = self._setup_filter(["massive1", "lightlike1"], args)
        mass2_filter = self._setup_filter(["massive2", "lightlike2"], args)

        index1_name = self._setup_name("index1", prefix + "index1", opts)
        mass1_name = self._setup_name("mass1", prefix + "mass1", opts)
        spin1_name = self._setup_name("spin1", prefix + "spin1", opts)
        twospin1_name = self._setup_name("2spin1", prefix + "2spin1", opts)
        lightlike1_name = self._setup_name("lightlike1", prefix + "is_lightlike1", opts)
        massive1_name = self._setup_name("massive1", prefix + "is_massive1", opts)
        ini1_name = self._setup_name("initial1", prefix + "is_inital1", opts)
        fin1_name = self._setup_name("final1", prefix + "is_final1", opts)
        color1_name = self._setup_name("color1", prefix + "color1", opts)
        latex1_name = self._setup_name("latex1", prefix + "latex1", opts)

        index2_name = self._setup_name("index2", prefix + "index2", opts)
        mass2_name = self._setup_name("mass2", prefix + "mass2", opts)
        spin2_name = self._setup_name("spin2", prefix + "spin2", opts)
        twospin2_name = self._setup_name("2spin2", prefix + "2spin2", opts)
        lightlike2_name = self._setup_name("lightlike2", prefix + "is_lightlike2", opts)
        massive2_name = self._setup_name("massive2", prefix + "is_massive2", opts)
        ini2_name = self._setup_name("initial2", prefix + "is_inital2", opts)
        fin2_name = self._setup_name("final2", prefix + "is_final2", opts)
        color2_name = self._setup_name("color2", prefix + "color2", opts)
        out_index1_name = self._setup_name("out_index1", prefix + "out_index1", opts)
        out_index2_name = self._setup_name("out_index2", prefix + "out_index2", opts)
        helicity1_name = self._setup_name("hel1", prefix + "hel1", opts)
        helicity2_name = self._setup_name("hel2", prefix + "hel2", opts)
        reference1_name = self._setup_name("reference1", prefix + "reference1", opts)
        reference2_name = self._setup_name("reference2", prefix + "reference2", opts)
        latex2_name = self._setup_name("latex2", prefix + "latex2", opts)
        n_color_corr = self._setup_name("n_color_corr", prefix + "n_color_corr", opts)
        n_sc = self._setup_name("n_sc", prefix + "n_sc", opts)
        charge1_name = self._setup_name("charge1", prefix + "charge1", opts)
        charge2_name = self._setup_name("charge2", prefix + "charge2", opts)
        photon1_name = self._setup_name("photon1", prefix + "photon1", opts)

        first_name = self._setup_name("first", prefix + "is_first", opts)
        is_first = True
        base = 1
        nres = 0
        nsc = -3

        color1_filter = []
        if "white1" in args:
            color1_filter.extend([1, -1])
        if "colored1" in args:
            color1_filter.extend([3, -3, 8, -8])
        if "fundamental1" in args:
            color1_filter.extend([-3, 3])
        if "quarks1" in args:
            color1_filter.append(3)
        if "anti-quarks1" in args:
            color1_filter.append(-3)
        if ("adjoint1" in args) or ("gluons1" in args):
            color1_filter.extend([-8, 8])

        if len(color1_filter) == 0:
            color1_filter = [1, -1, 3, -3, 8, -8]

        color2_filter = []
        if "white2" in args:
            color2_filter.extend([1, -1])
        if "colored2" in args:
            color2_filter.extend([3, -3, 8, -8])
        if "fundamental2" in args:
            color2_filter.extend([-3, 3])
        if "quarks2" in args:
            color2_filter.append(3)
        if "anti-quarks2" in args:
            color2_filter.append(-3)
        if ("adjoint2" in args) or ("gluons2" in args):
            color2_filter.extend([-8, 8])

        if len(color2_filter) == 0:
            color2_filter = [1, -1, 3, -3, 8, -8]

        charge1_filter = []
        if "charged1" in args:
            charge1_filter.extend([1.0, -1.0, 1.0 / 3.0, -1.0 / 3.0, 2.0 / 3.0, -2.0 / 3.0])

        charge2_filter = []
        if "charged2" in args:
            charge2_filter.extend([1.0, -1.0, 1.0 / 3.0, -1.0 / 3.0, 2.0 / 3.0, -2.0 / 3.0])

        photon1_filter = []
        if "photon1" in args:
            photon1_filter.extend(["A"])

        props = Properties()

        if "initial1" in inout1_filter:
            start1_index = 0
        else:
            start1_index = self._num_in

        if "final1" in inout1_filter:
            end1_index = self._num_legs
        else:
            end1_index = self._num_in

        if "initial2" in inout2_filter:
            start2_index = 0
        else:
            start2_index = self._num_in

        if "final2" in inout2_filter:
            end2_index = self._num_legs
        else:
            end2_index = self._num_in

        for index1 in range(start1_index, end1_index):
            if self._lightlike[index1]:
                if "lightlike1" not in mass1_filter:
                    continue
            else:
                if "massive1" not in mass1_filter:
                    continue

            color1 = self._color[index1]
            if color1 not in color1_filter:
                continue

            charge1 = self._charge[index1]
            # if charge1 not in charge1_filter:
            # continue

            photon1 = self._field_info[index1][0]
            # if photon1 not in photon1_filter:
            # continue

            props.setProperty(index1_name, index1 + base)
            props.setProperty(mass1_name, self._masses[index1])
            props.setProperty(spin1_name, self._spin[index1])
            props.setProperty(twospin1_name, self._twospin[index1])
            props.setProperty(lightlike1_name, self._lightlike[index1])
            props.setProperty(massive1_name, not self._lightlike[index1])
            props.setProperty(ini1_name, index1 < self._num_in)
            props.setProperty(fin1_name, index1 >= self._num_in)
            props.setProperty(color1_name, color1)
            props.setProperty(latex1_name, self._latex[index1])
            props.setProperty(charge1_name, charge1)
            props.setProperty(photon1_name, photon1)
            if index1 >= self._num_in:
                props.setProperty(out_index1_name, index1 + base - self._num_in)
            else:
                props.setProperty(
                    out_index1_name, "[%% ' ERROR: initial state particle, %s not defined. ' %%]" % out_index1_name
                )

            if len(self._helicity_stack) > 0:
                if index1 in self._helicity_stack[-1]:
                    props.setProperty(helicity1_name, self._helicity_stack[-1][index1])
                else:
                    props.setProperty(
                        helicity1_name, "[%% ' ERROR: %s not defined for this particle. ' %%]" % helicity1_name
                    )

            if index1 in self._references:
                refk = self._references[index1]
                if refk.startswith("k"):
                    props.setProperty(reference1_name, int(refk[1:]))
                else:
                    assert refk.startswith("l")
                    props.setProperty(reference1_name, -int(refk[1:]))
            else:
                props.setProperty(reference1_name, 0)
            start2 = start2_index
            if "ordered" in args:
                if start2 < index1:
                    start2 = index1

            for index2 in range(start2, end2_index):
                if (index2 == index1) and ("distinct" in args):
                    continue

                if self._lightlike[index2]:
                    if "lightlike2" not in mass2_filter:
                        continue
                else:
                    if "massive2" not in mass2_filter:
                        continue

                color2 = self._color[index2]
                if color2 not in color2_filter:
                    continue

                charge2 = self._charge[index2]
                # if charge2 not in charge2_filter:
                # continue

                if index2 >= self._num_in:
                    props.setProperty(out_index2_name, index2 + base - self._num_in)
                else:
                    props.setProperty(
                        out_index2_name, "[%% ' ERROR: initial state particle, %s not defined. ' %%]" % out_index2_name
                    )
                if len(self._helicity_stack) > 0:
                    if index2 in self._helicity_stack[-1]:
                        props.setProperty(helicity2_name, self._helicity_stack[-1][index2])
                    else:
                        props.setProperty(
                            helicity2_name, "[%% ' ERROR: %s not defined for this particle. ' %%]" % helicity2_name
                        )
                if index2 in self._references:
                    refk = self._references[index2]
                    if refk.startswith("k"):
                        props.setProperty(reference2_name, int(refk[1:]))
                    else:
                        assert refk.startswith("l")
                        props.setProperty(reference2_name, -int(refk[1:]))
                else:
                    props.setProperty(reference2_name, 0)

                props.setProperty(index2_name, index2 + base)
                props.setProperty(mass2_name, self._masses[index2])
                props.setProperty(spin2_name, self._spin[index2])
                props.setProperty(twospin2_name, self._twospin[index2])
                props.setProperty(lightlike2_name, self._lightlike[index2])
                props.setProperty(massive2_name, not self._lightlike[index2])
                props.setProperty(ini2_name, index2 < self._num_in)
                props.setProperty(fin2_name, index2 >= self._num_in)
                props.setProperty(color2_name, color2)
                props.setProperty(first_name, is_first)
                props.setProperty(latex2_name, self._latex[index2])
                props.setProperty(charge2_name, charge2)
                #            props.setProperty(n_color_corr, index2+1+(self._num_legs)*(index1)-index1*(index1-1)/2-index1)
                if index1 != index2:
                    nsc += 4
                    nres += 1
                props.setProperty(n_color_corr, nres)
                props.setProperty(n_sc, nsc)
                is_first = False
                yield props

    def zeroes(self, *args, **opts):
        if "shift" in opts:
            shift = self._eval_int(opts["shift"])
        else:
            shift = 0

        prefix = self._setup_name("prefix", "", opts)
        var_name = self._setup_name("var", prefix + "$_", opts)
        first_name = self._setup_name("first", prefix + "is_first", opts)
        last_name = self._setup_name("last", prefix + "is_last", opts)
        index_name = self._setup_name("index", prefix + "index", opts)

        zeroes = self._zeroes

        props = Properties()
        lasti = len(zeroes) - 1
        for i, z in enumerate(zeroes):
            props.setProperty(var_name, z)
            props.setProperty(index_name, i + shift)
            props.setProperty(first_name, i == 0)
            props.setProperty(last_name, i == lasti)

            yield props

    def ones(self, *args, **opts):
        if "shift" in opts:
            shift = self._eval_int(opts["shift"])
        else:
            shift = 0

        prefix = self._setup_name("prefix", "", opts)
        var_name = self._setup_name("var", prefix + "$_", opts)
        first_name = self._setup_name("first", prefix + "is_first", opts)
        last_name = self._setup_name("last", prefix + "is_last", opts)
        index_name = self._setup_name("index", prefix + "index", opts)

        ones = self._ones

        props = Properties()
        lasti = len(ones) - 1
        for i, z in enumerate(ones):
            props.setProperty(var_name, z)
            props.setProperty(index_name, i + shift)
            props.setProperty(first_name, i == 0)
            props.setProperty(last_name, i == lasti)

            yield props

    def mandelstam(self, *args, **opts):
        zero_filter = self._setup_filter(["zero", "non-zero"], args)
        zero_name = self._setup_name("zero", "is_zero", opts)
        nzero_name = self._setup_name("non-zero", "is_non-zero", opts)
        symbol_name = self._setup_name("symbol", "symbol", opts)
        first_name = self._setup_name("first", "is_first", opts)
        index_name = self._setup_name("index", "index", opts)
        gindex_name = self._setup_name("global_index", "global_index", opts)

        sym_prefix = self._setup_name("sym_prefix", "es", opts)
        sym_suffix = self._setup_name("sym_suffix", "", opts)
        sym_infix = self._setup_name("sym_infix", "", opts)

        props = Properties()
        is_first = True

        idx = 0
        gidx = 0
        for parts, vecs in list(self._mandel_parts.items()):
            gidx += 1
            default_name = "s" + "".join(parts.split())
            name = sym_prefix + sym_infix.join(parts.split()) + sym_suffix

            is_massive = True
            if len(vecs) == 1:
                mass = self._masses[vecs[0] - 1]
                is_massive = mass != "0"

            if is_massive:
                if "non-zero" not in zero_filter:
                    continue
            else:
                if "zero" not in zero_filter:
                    continue

            idx += 1

            props.setProperty(symbol_name, name)
            props.setProperty(zero_name, not is_massive)
            props.setProperty(nzero_name, is_massive)
            props.setProperty(first_name, is_first)
            props.setProperty(index_name, idx)
            props.setProperty(gindex_name, gidx)

            is_first = False
            self._mandel_stack.append(default_name)
            yield props
            self._mandel_stack.pop()

    def mandelstam_expression(self, *args, **opts):
        index1_name = self._setup_name("index1", "index1", opts)
        mass1_name = self._setup_name("mass1", "mass1", opts)
        spin1_name = self._setup_name("spin1", "spin1", opts)
        twospin1_name = self._setup_name("2spin1", "2spin1", opts)
        lightlike1_name = self._setup_name("lightlike1", "is_lightlike1", opts)
        massive1_name = self._setup_name("massive1", "is_massive1", opts)
        ini1_name = self._setup_name("initial1", "is_inital1", opts)
        fin1_name = self._setup_name("final1", "is_final1", opts)
        color1_name = self._setup_name("color1", "color1", opts)

        index2_name = self._setup_name("index2", "index2", opts)
        mass2_name = self._setup_name("mass2", "mass2", opts)
        spin2_name = self._setup_name("spin2", "spin2", opts)
        twospin2_name = self._setup_name("2spin2", "2spin2", opts)
        lightlike2_name = self._setup_name("lightlike2", "is_lightlike2", opts)
        massive2_name = self._setup_name("massive2", "is_massive2", opts)
        ini2_name = self._setup_name("initial2", "is_inital2", opts)
        fin2_name = self._setup_name("final2", "is_final2", opts)
        color2_name = self._setup_name("color2", "color2", opts)

        symbol = self._mandel_stack[-1]
        vecs = self._mandel[symbol]

        is_first_term = True
        count_terms = (len(vecs) * (len(vecs) + 1)) // 2
        props = Properties()
        for i in range(len(vecs)):
            # i == j term
            vec1 = abs(vecs[i]) - 1
            mass1 = self._masses[vec1]
            color1 = self._color[vec1]
            count_terms -= 1
            props.setProperty(index1_name, vec1 + 1)
            props.setProperty(index2_name, vec1 + 1)
            props.setProperty(massive1_name, not self._lightlike[vec1])
            props.setProperty(massive2_name, not self._lightlike[vec1])
            props.setProperty(lightlike1_name, self._lightlike[vec1])
            props.setProperty(lightlike2_name, self._lightlike[vec1])
            props.setProperty(mass1_name, mass1)
            props.setProperty(mass2_name, mass1)
            props.setProperty(spin1_name, self._spin[vec1])
            props.setProperty(spin2_name, self._spin[vec1])
            props.setProperty(twospin1_name, self._twospin[vec1])
            props.setProperty(twospin2_name, self._twospin[vec1])
            props.setProperty(ini1_name, vec1 < self._num_in)
            props.setProperty(ini2_name, vec1 < self._num_in)
            props.setProperty(fin1_name, vec1 >= self._num_in)
            props.setProperty(fin2_name, vec1 >= self._num_in)
            props.setProperty(color1_name, color1)
            props.setProperty(color2_name, color1)

            if mass1 != "0":
                props.setProperty("term_mass", mass1)
                props.setProperty("term_coeff", "1")
                props.setProperty("term_is_mass", True)
                props.setProperty("is_first_term", is_first_term)
                props.setProperty("is_last_term", count_terms == 0)
                yield props
                is_first_term = False

            props.setProperty("term_is_mass", False)
            props.setProperty("term_mass", "[% ERROR: 'term_mass' not defined here. %]")
            props.setProperty("term_coeff", "2")

            for j in range(i + 1, len(vecs)):
                count_terms -= 1
                vec2 = abs(vecs[j]) - 1
                mass2 = self._masses[vec2]
                color2 = self._color[vec2]

                props.setProperty(index2_name, vec2 + 1)
                props.setProperty(massive2_name, not self._lightlike[vec2])
                props.setProperty(lightlike2_name, self._lightlike[vec2])
                props.setProperty(mass2_name, mass2)
                props.setProperty(spin2_name, self._spin[vec2])
                props.setProperty(twospin2_name, self._twospin[vec2])
                props.setProperty(ini2_name, vec2 < self._num_in)
                props.setProperty(fin2_name, vec2 >= self._num_in)
                props.setProperty(color2_name, color2)
                props.setProperty("is_first_term", is_first_term)
                props.setProperty("is_last_term", count_terms == 0)
                yield props
                is_first_term = False

    def mandelstam_subs(self, *args, **opts):
        if "prefix" in opts:
            prefix = opts["prefix"]
        else:
            prefix = ""

        if "shift" in opts:
            shift = int(opts["shift"])
        else:
            shift = 1

        index_filter = self._setup_filter(["upper", "lower", "diagonal"], args)
        include_upper = "upper" in index_filter
        include_lower = "lower" in index_filter
        include_diagonal = "diagonal" in index_filter

        index1_name = self._setup_name("index1", prefix + "index1", opts)
        index2_name = self._setup_name("index2", prefix + "index2", opts)
        index_name = self._setup_name("index", prefix + "index", opts)
        first_name = self._setup_name("first", prefix + "is_first", opts)
        last_name = self._setup_name("last", prefix + "is_last", opts)

        fmt_prefix = self._setup_name("fmt_prefix", "es", opts)
        fmt_suffix = self._setup_name("fmt_suffix", "", opts)
        fmt_infix = self._setup_name("fmt_infix", "", opts)

        all_mndlst = self._all_mndlst

        m_vars, m_subs = golem.algorithms.mandelstam.generate_mandelstam_set(
            self._num_in, self._num_out, prefix=fmt_prefix, infix=fmt_infix, suffix=fmt_suffix, all_inv=all_mndlst
        )

        num_legs = self._num_legs
        props = Properties()

        indices = []
        for i in range(num_legs):
            for j in range(num_legs):
                if i == j:
                    if not include_diagonal:
                        continue
                elif i > j:
                    if not include_lower:
                        continue
                else:
                    if not include_upper:
                        continue
                indices.append((i, j))

        last_idx = len(indices) - 1
        for idx, pair in enumerate(indices):
            i, j = pair
            subs = m_subs[i][j]

            props.setProperty(index1_name, i + shift)
            props.setProperty(index2_name, j + shift)
            props.setProperty(index_name, idx)

            props.setProperty(first_name, idx == 0)
            props.setProperty(last_name, idx == last_idx)
            self._msubs_stack.append((fmt_prefix, fmt_suffix, subs))
            yield props
            self._msubs_stack.pop()

    def mandelstam_subs_rhs(self, *args, **opts):
        if len(self._msubs_stack) == 0:
            raise golem.util.parser.TemplateError("[% mandelstam_subs_rhs %] must be inside [% mandelstam_subs %]")

        if "prefix" in opts:
            prefix = opts["prefix"]
        else:
            prefix = ""

        if "shift" in opts:
            shift = int(opts["shift"])
        else:
            shift = 0

        var_name = self._setup_name("var", prefix + "$_", opts)
        coeff_name = self._setup_name("coeff", prefix + "coeff", opts)
        exponent_name = self._setup_name("exponent", prefix + "exponent", opts)
        index_name = self._setup_name("index", prefix + "index", opts)
        first_name = self._setup_name("first", prefix + "is_first", opts)
        last_name = self._setup_name("last", prefix + "is_last", opts)

        prefix, suffix, subs = self._msubs_stack[-1]
        mandel1 = dict(list(zip([prefix + str(i) + suffix for i in range(1, self._num_legs + 1)], self._masses)))

        terms = []
        for v, c in list(subs.items()):
            if v in mandel1:
                mv = str(mandel1[v]).strip()
                if mv == "0":
                    continue
                terms.append((c, mv, 2))
            else:
                if v == "0":
                    continue
                terms.append((c, v, 1))

        props = Properties()
        last_idx = len(terms) - 1
        for idx, term in enumerate(terms):
            c, v, e = term
            props.setProperty(first_name, idx == 0)
            props.setProperty(last_name, idx == last_idx)
            props.setProperty(index_name, idx == idx + shift)
            props.setProperty(var_name, v)
            props.setProperty(coeff_name, c)
            props.setProperty(exponent_name, e)

            yield props

    def _OBSOLETE_latex_color_base(self, *args, **opts):
        """
        Enumerates all color structures for this process in
        LaTeX format.
        """

        var_name = self._setup_name("var", "$_", opts)
        rhs_name = self._setup_name("expr", "expr", opts)

        first_name = self._setup_name("first", "is_first", opts)
        last_name = self._setup_name("last", "is_last", opts)

        result = ""
        quarks = []
        aquarks = []
        gluons = []
        particles = []
        colored = []
        wf = []
        for i in range(len(self._color)):
            c = self._color[i]
            if c == 3:
                color_index = "i_%d" % (i + 1)
                quarks.append(color_index)
                colored.append(i + 1)
                wf.append("q^{(%d)}_{%s}" % (i + 1, color_index))
            elif c == -3:
                color_index = "j_%d" % (i + 1)
                aquarks.append(color_index)
                colored.append(i + 1)
                wf.append("\\bar{q}^{(%d)}_{%s}" % (i + 1, color_index))
            elif c == 8 or c == -8:
                color_index = "A_%d" % (i + 1)
                gluons.append(color_index)
                colored.append(i + 1)
                wf.append("g_{(%d)}^{%s}" % (i + 1, color_index))
            else:
                continue
            particles.append(color_index)

        total_colors = int(self._properties["num_colors"])

        num_color = 0
        for lines, traces in golem.algorithms.color.colorbasis(quarks, aquarks, gluons):
            num_color += 1

            s_lines = wf[:]
            for line in lines:
                N = len(line)
                if N == 2:
                    s_lines.append("\\delta_{%s%s}" % (line[0], line[1]))
                else:
                    string = []
                    for aidx in line[1 : N - 2]:
                        string.append("T^{%s}" % (aidx))
                    string.append("T^{%s}" % (line[N - 2]))
                    s_lines.append("(%s)_{%s%s}" % ("".join(string), line[0], line[N - 1]))

            for tr in traces:
                N = len(tr)
                string = []
                for aidx in tr[1:N]:
                    string.append("T^{%s}" % aidx)
                string.append("T^{%s}" % tr[0])
                s_lines.append("\\mathrm{tr}\\{%s\\}" % "".join(string))

            props = golem.util.config.Properties()
            props.setProperty(var_name, num_color)
            props.setProperty(rhs_name, "".join(s_lines) if len(s_lines) > 0 else "1")

            props.setProperty(first_name, num_color == 1)
            props.setProperty(last_name, num_color == total_colors)

            yield props

    def color_mapping(self, *args, **opts):
        if len(self._color_stack) == 0:
            raise golem.util.parser.TemplateError(
                " [% @for color_mapping %] " + "must be inside [% @for helicities %]."
            )

        prefix = self._setup_name("prefix", "", opts)
        first_name = self._setup_name("first", prefix + "is_first", opts)
        last_name = self._setup_name("last", prefix + "is_last", opts)
        index_name = self._setup_name("index", prefix + "index", opts)
        var_name = self._setup_name("var", prefix + "$_", opts)

        if "shift" in opts:
            shift = int(opts["shift"])
        else:
            shift = 0

        lst = self._color_stack[-1]

        if lst is None:
            lst = [(i, 1, False) for i in range(self._num_legs)]

        L = self._num_legs

        props = Properties()
        for i, ci in enumerate(lst):
            is_first = i == 0
            is_last = i == L - 1

            props.setProperty(first_name, is_first)
            props.setProperty(last_name, is_last)
            props.setProperty(index_name, shift + i)
            props.setProperty(var_name, shift + ci)

            yield props

    def helicity_mapping(self, *args, **opts):
        """
        Iterates over the currently set helicity mapping
        """

        if len(self._mapping_stack) == 0:
            raise golem.util.parser.TemplateError(
                " [% @for helicity_mapping %] "
                + "must be inside [% @for helicities %] or [% @for unique_helicity_mappings %]."
            )

        prefix = self._setup_name("prefix", "", opts)
        first_name = self._setup_name("first", prefix + "is_first", opts)
        last_name = self._setup_name("last", prefix + "is_last", opts)
        index_name = self._setup_name("index", prefix + "index", opts)
        var_name = self._setup_name("var", prefix + "$_", opts)
        sign_name = self._setup_name("sign", prefix + "sign", opts)
        parity_name = self._setup_name("parity", prefix + "parity", opts)

        if "shift" in opts:
            shift = int(opts["shift"])
        else:
            shift = 0

        lst = self._mapping_stack[-1]

        if lst is None:
            lst = [(i, 1, False) for i in range(self._num_legs)]

        L = self._num_legs

        props = Properties()
        for i, mapping in enumerate(lst):
            k, m, p = mapping
            is_first = i == 0
            is_last = i == L - 1

            props.setProperty(first_name, is_first)
            props.setProperty(last_name, is_last)
            props.setProperty(index_name, shift + i)
            props.setProperty(var_name, shift + k)
            props.setProperty(sign_name, m)
            props.setProperty(parity_name, p)

            yield props

    def helicities(self, *args, **opts):
        """
        Enumerates all helicities possible with this
        kinematics.

        opts:
           symbol_plus=+    symbol used for helicity +1
           symbol_minus=-   symbol used for helicity -1
           symbol_zero=0    symbol used for helicity  0
           symbol_plus2=p   symbol used for helicity +2 (not yet in use)
           symbol_minus2=m  symbol used for helicity -2 (not yet in use)
           base=0           where to count from
           var=helicity     name for the index of the current helicity
           where=variable<op>value
                            variable is the name of a variable giving the
                            index of a particle. <op> is one of
                            .eq. .ne. .gt. .lt. .ge. .le.
                            value is one of the above symbols. example
                            where=index1.ge.0
                            where=index.ne.0
                            more than one value can be given separated by
                            commas, which then are combined via 'and'

        Depending on the spin of the particle the symbols have different
        meanings:

        spin massive  |  'm'  '-'  '0'   '+'   'p'
          0   YES/NO  | ---- ----    0  ----  ----
        1/2   YES/NO  | ---- -1/2 ----  +1/2  ----
          1     NO    | ----   -1 ----    +1  ----
          1    YES    | ----   -1    0    +1  ----
        3/2     NO    | -3/2 ---- ----  ----  +3/2
        3/2    YES    | -3/2 -1/2 ----  +1/2  +3/2
          2     NO    |   -2 ---- ----  ----    +2
          2    YES    |   -2   -1    0    +1    +2
        """
        sym = golem.algorithms.helicity.heli_to_symbol
        symbol_plus = self._setup_name("symbol_plus", sym[+1], opts)
        symbol_minus = self._setup_name("symbol_minus", sym[-1], opts)
        symbol_plus2 = self._setup_name("symbol_plus2", sym[+2], opts)
        symbol_minus2 = self._setup_name("symbol_minus2", sym[-2], opts)
        symbol_zero = self._setup_name("symbol_zero", sym[0], opts)
        base = int(self._setup_name("base", "0", opts))
        prefix = self._setup_name("prefix", "", opts)
        var_name = self._setup_name("var", prefix + "helicity", opts)
        first_name = self._setup_name("first", prefix + "is_first", opts)
        last_name = self._setup_name("last", prefix + "is_last", opts)
        generated_name = self._setup_name("is_generated", prefix + "generated", opts)
        map_index = self._setup_name("map.index", prefix + "map.index", opts)
        map_perm = self._setup_name("map.permutation", prefix + "map.permutation", opts)
        map_gauge_set = self._setup_name("map.gauge_set", prefix + "map.gauge_set", opts)

        largs = [a.lower() for a in args]

        generated_only = "generated" in largs

        symbols = {-2: symbol_minus2, -1: symbol_minus, 0: symbol_zero, +1: symbol_plus, +2: symbol_plus2}

        isymbols = {}
        for s, v in list(symbols.items()):
            isymbols[v] = s

        isymbols.setdefault(100)

        pfilter = {}

        if "where" in opts:
            and_list = opts["where"].split(",")
            for s_expr in and_list:
                tokens = s_expr.split(".")

                where_name = tokens[0]
                where_index = self._eval_int(where_name) - 1
                where_op = tokens[1]
                where_val = isymbols[tokens[2]]
                if where_op == "eq":
                    pfilter[where_index] = [where_val]
                elif where_op == "ne":
                    pfilter[where_index] = list(range(-100, where_val)) + list(range(where_val + 1, 100))
                elif where_op == "le":
                    pfilter[where_index] = list(range(-100, where_val + 1))
                elif where_op == "ge":
                    pfilter[where_index] = list(range(where_val, 100))
                elif where_op == "lt":
                    pfilter[where_index] = list(range(-100, where_val))
                elif where_op == "gt":
                    pfilter[where_index] = list(range(where_val + 1, 100))
                else:
                    pfilter[where_index] = []

        props = Properties()
        i = base
        l = len(self._helicity_comb)
        for h, mapping in zip(self._helicity_comb, self._helicity_map):
            gi, lst, color_basis, permutation, gauge_set = mapping

            is_generated = i - base == gi

            if generated_only and not is_generated:
                i += 1
                continue

            h = golem.util.tools.encode_helicity(h, symbols)
            skip = False
            for idx, sym in list(h.items()):
                if idx in pfilter:
                    isym = isymbols[sym]
                    if isym not in pfilter[idx]:
                        skip = True
                        break
            if not skip:
                props.setProperty(first_name, i == base)
                props.setProperty(last_name, i - base >= l - 1)
                props.setProperty(var_name, i)
                props.setProperty(generated_name, is_generated)
                props.setProperty(map_index, gi + base)
                props.setProperty(map_perm, permutation.cycles(1))
                props.setProperty(map_gauge_set, gauge_set)
                self._helicity_stack.append(h)
                self._mapping_stack.append(lst)
                self._color_stack.append(color_basis)
                yield props
                self._color_stack.pop()
                self._mapping_stack.pop()
                self._helicity_stack.pop()
            i += 1

    def unique_helicity_mappings(self, *args, **opts):
        """
        Enumerates all unique helicity mappings for the current helicity list.
        """
        props = Properties()
        lightlike_vector_indices = [
            i
            for i in range(len(self._lightlike))
            if self._lightlike[i] and (self._twospin[i] == 2 or self._twospin[i] == -2)
        ]
        unique_mappings = []
        for i, mapping in enumerate(self._helicity_map):
            lightlike_vector_helicities = [self._helicity_comb[i][k] for k in lightlike_vector_indices]
            if (lightlike_vector_helicities, mapping[1]) not in unique_mappings:
                unique_mappings.append((lightlike_vector_helicities, mapping[1]))

        for lv_helicities, mapping in unique_mappings:
            current_helicities = []
            current_mappings = []
            for i in range(len(self._helicity_comb)):
                if self._helicity_map[i][1] == mapping and all(
                    self._helicity_comb[i][lightlike_vector_indices[k]] == lv_helicities[k]
                    for k in range(len(lv_helicities))
                ):
                    current_helicities.append((i, self._helicity_comb[i]))
                    current_mappings.append(self._helicity_map[i])

            self._mapping_stack.append(mapping)
            self._current_helicity_list_stack.append(current_helicities)
            self._current_mapping_list_stack.append(current_mappings)
            yield props
            self._mapping_stack.pop()
            self._current_helicity_list_stack.pop()
            self._current_mapping_list_stack.pop()

    def current_helicities(self, *args, **opts):
        """
        Enumerates all helicities with the current helicity mapping. See 'helicities' for details.
        """

        if len(self._current_helicity_list_stack) == 0:
            raise golem.util.parser.TemplateError(
                " [% @for current_helicities %] " + "must be inside [% @for unique_helicity_mappings %]."
            )

        sym = golem.algorithms.helicity.heli_to_symbol
        symbol_plus = self._setup_name("symbol_plus", sym[+1], opts)
        symbol_minus = self._setup_name("symbol_minus", sym[-1], opts)
        symbol_plus2 = self._setup_name("symbol_plus2", sym[+2], opts)
        symbol_minus2 = self._setup_name("symbol_minus2", sym[-2], opts)
        symbol_zero = self._setup_name("symbol_zero", sym[0], opts)
        base = int(self._setup_name("base", "0", opts))
        prefix = self._setup_name("prefix", "", opts)
        var_name = self._setup_name("var", prefix + "helicity", opts)
        first_name = self._setup_name("first", prefix + "is_first", opts)
        last_name = self._setup_name("last", prefix + "is_last", opts)
        generated_name = self._setup_name("is_generated", prefix + "generated", opts)
        map_index = self._setup_name("map.index", prefix + "map.index", opts)
        map_perm = self._setup_name("map.permutation", prefix + "map.permutation", opts)
        map_gauge_set = self._setup_name("map.gauge_set", prefix + "map.gauge_set", opts)

        largs = [a.lower() for a in args]

        generated_only = "generated" in largs

        symbols = {-2: symbol_minus2, -1: symbol_minus, 0: symbol_zero, +1: symbol_plus, +2: symbol_plus2}

        isymbols = {}
        for s, v in list(symbols.items()):
            isymbols[v] = s

        isymbols.setdefault(100)

        pfilter = {}

        if "where" in opts:
            and_list = opts["where"].split(",")
            for s_expr in and_list:
                tokens = s_expr.split(".")

                where_name = tokens[0]
                where_index = self._eval_int(where_name) - 1
                where_op = tokens[1]
                where_val = isymbols[tokens[2]]
                if where_op == "eq":
                    pfilter[where_index] = [where_val]
                elif where_op == "ne":
                    pfilter[where_index] = list(range(-100, where_val)) + list(range(where_val + 1, 100))
                elif where_op == "le":
                    pfilter[where_index] = list(range(-100, where_val + 1))
                elif where_op == "ge":
                    pfilter[where_index] = list(range(where_val, 100))
                elif where_op == "lt":
                    pfilter[where_index] = list(range(-100, where_val))
                elif where_op == "gt":
                    pfilter[where_index] = list(range(where_val + 1, 100))
                else:
                    pfilter[where_index] = []

        props = Properties()
        l = len(self._helicity_comb)
        for h, mapping in zip(self._current_helicity_list_stack[-1], self._current_mapping_list_stack[-1]):
            gi, _, color_basis, permutation, gauge_set = mapping
            is_generated = h[0] - base == gi

            if generated_only and not is_generated:
                continue

            helicity = golem.util.tools.encode_helicity(h[1], symbols)
            skip = False
            for idx, sym in list(helicity.items()):
                if idx in pfilter:
                    isym = isymbols[sym]
                    if isym not in pfilter[idx]:
                        skip = True
                        break
            if not skip:
                props.setProperty(first_name, h[0] == base)
                props.setProperty(last_name, h[0] - base >= l - 1)
                props.setProperty(var_name, h[0])
                props.setProperty(generated_name, is_generated)
                props.setProperty(map_index, gi + base)
                props.setProperty(map_perm, permutation.cycles(1))
                props.setProperty(map_gauge_set, gauge_set)
                self._helicity_stack.append(helicity)
                self._color_stack.append(color_basis)
                yield props
                self._color_stack.pop()
                self._helicity_stack.pop()

    def modified_helicity(self, *args, **opts):
        if (len(self._helicity_stack) > 0) and ("modify" in opts) and ("to" in opts):
            sym = golem.algorithms.helicity.heli_to_symbol
            symbol_plus = self._setup_name("symbol_plus", sym[+1], opts)
            symbol_minus = self._setup_name("symbol_minus", sym[-1], opts)
            symbol_plus2 = self._setup_name("symbol_plus2", sym[+2], opts)
            symbol_minus2 = self._setup_name("symbol_minus2", sym[-2], opts)
            symbol_zero = self._setup_name("symbol_zero", sym[0], opts)
            base = int(self._setup_name("base", "0", opts))
            prefix = self._setup_name("prefix", "", opts)
            var_name = self._setup_name("var", prefix + "helicity", opts)

            symbols = {-2: symbol_minus2, -1: symbol_minus, 0: symbol_zero, +1: symbol_plus, +2: symbol_plus2}

            key = opts["modify"]
            value = opts["to"]
            index = self._eval_int(key) - 1
            helicity = self._helicity_stack[-1].copy()
            helicity[index] = value

            i = base
            for h in self._helicity_comb:
                h = golem.util.tools.encode_helicity(h, symbols)
                if h == helicity:
                    props = Properties()
                    props.setProperty(var_name, str(i))
                    yield props
                i += 1

    def _compute_program(self):
        # Calculate dependencies between auxiliary vectors
        lst = sorted(self._references.keys())

        # Example: self._references = {0: 'l2', 1: 'l1', 2: 'l2', 3: 'l2'}
        #          self._masses = ['m', 'm', 'm', '0']
        dependencies = {}
        for i in lst:
            vector = self._references[i]
            mass = self._masses[i]
            if mass == "0":
                continue
            if vector.startswith("l"):
                idx = int(vector[1:]) - 1
                dependencies[i] = set([idx])
            else:
                dependencies[i] = set()
        # Now: dependencies = {
        #  0: set(['l2']),
        #  1: set(['l1']),
        #  2: set(['l2'])}

        for i in list(dependencies.keys()):
            d = dependencies[i]
            new_d = set(d)
            flag = True
            while flag:
                d = frozenset(new_d)
                for j in d:
                    new_d.update(dependencies[j])

                flag = new_d != d
            dependencies[i] = new_d
        # Now: dependencies = {
        #  1: set(['l1', 'l2']),
        #  2: set(['l1', 'l2']),
        #  3: set(['l1', 'l2'])}

        # Program: a list of instructions encoded as:
        #   [i]    == ligt_cone_decomposition(k_i, ref_i)
        #   [i, j] == symmetric splitting of k_i and k_j
        program = []
        available = set()
        while len(dependencies) > 0:
            success = False
            indep = list([i for i in list(dependencies.keys()) if len(dependencies[i]) == 0])
            for i in indep:
                program.append([i])
                success = True

            if success:
                available.update(indep)
            else:
                # try splittings
                for i, depi in list(dependencies.items()):
                    li = "l%d" % (i + 1)
                    for j, depj in list(dependencies.items()):
                        if j <= i:
                            continue
                        lj = "l%d" % (j + 1)
                        if self._references[i] == lj and self._references[j] == li:
                            success = True
                            program.append([i, j])
                            available.update([i, j])
                            break
            if success:
                for i in available:
                    if i in dependencies:
                        del dependencies[i]
                for i in list(dependencies.keys()):
                    dependencies[i].difference_update(available)
            else:
                raise golem.util.parser.TemplateError("Cannot create initialization for kinematics")

        return program

    def instructions(self, *args, **opts):
        """
        Enumerates a sequence of instructions to initialize
        the l-momenta.

        [% @for instructions opcode=<name>
           index1=<name> mass1=<name>
           index2=<name> mass2=<name>
        %]
           [%opcode%] -- either 1 or 2
           [%index%]  -- the number of the leg.
           [%mass%]  -- the mass of the corresponding external vector
        """
        opcode_name = self._setup_name("opcode", "opcode", opts)
        index1_name = self._setup_name("index1", "index1", opts)
        index2_name = self._setup_name("index2", "index2", opts)
        mass1_name = self._setup_name("mass1", "mass1", opts)
        mass2_name = self._setup_name("mass2", "mass2", opts)
        first_name = self._setup_name("first", "is_first", opts)
        last_name = self._setup_name("last", "is_last", opts)

        program = self._compute_program()
        references = self._references

        last = len(program) - 1

        for index, inst in enumerate(program):
            props = Properties()
            props.setProperty(first_name, index == 0)
            props.setProperty(last_name, index == last)
            props.setProperty(opcode_name, len(inst))

            props.setProperty(index1_name, inst[0] + 1)
            props.setProperty(mass1_name, self._masses[inst[0]])
            if len(inst) == 1:
                ref = self._references[inst[0]]
                j = int(ref[1:])
                mass = self._masses[j - 1]
                props.setProperty(index2_name, j)
                props.setProperty(mass2_name, mass)
            else:
                props.setProperty(index2_name, inst[1] + 1)
                props.setProperty(mass2_name, self._masses[inst[1]])

            index += 1
            yield props

    def color_basis(self, *args, **opts):
        if "prefix" in opts:
            prefix = opts["prefix"]
        else:
            prefix = ""

        if "shift" in opts:
            shift = int(opts["shift"])
        else:
            shift = 0

        if "index_shift" in opts:
            index_shift = int(opts["index_shift"])
        else:
            index_shift = 0

        index_name = self._setup_name("index", prefix + "index", opts)
        first_name = self._setup_name("first", prefix + "is_first", opts)
        last_name = self._setup_name("last", prefix + "is_last", opts)

        quarks = []
        aquarks = []
        gluons = []
        particles = []
        sort = []
        wf = []
        for i in range(self._num_in):
            color = self._acolor[i]
            this_wf = "i:%d:%d:%d" % (i + shift, i + shift, abs(color))

            wf.append(this_wf)
            if color == 3:
                quarks.append(this_wf)
            elif color == -3:
                aquarks.append(this_wf)
            elif color == 8:
                gluons.append(this_wf)

        for i in range(self._num_out):
            color = self._acolor[self._num_in + i]
            this_wf = "o:%d:%d:%d" % (i + shift, i + self._num_in + shift, abs(color))

            wf.append(this_wf)
            if color == 3:
                aquarks.append(this_wf)
            elif color == -3:
                quarks.append(this_wf)
            elif abs(color) == 8:
                gluons.append(this_wf)

        cs = []
        for lines, traces in golem.algorithms.color.colorbasis(quarks, aquarks, gluons):
            wf_copy = wf[:]
            lines_copy = []

            for line in lines:
                N = len(line)
                if N == 2:
                    for i in range(len(wf_copy)):
                        if wf_copy[i] == line[0]:
                            wf_copy[i] = line[1]
                else:
                    lines_copy.append(line)

            cs.append((wf_copy, lines_copy, traces[:]))

        props = Properties()
        last_idx = len(cs) - 1
        for idx, c in enumerate(cs):
            wf, lines, traces = c

            props.setProperty(index_name, idx + index_shift)
            props.setProperty(first_name, idx == 0)
            props.setProperty(last_name, idx == last_idx)

            self._cs_stack.append((wf, lines, traces))
            yield props
            self._cs_stack.pop()

    def color_wf(self, *args, **opts):
        if len(self._cs_stack) == 0:
            raise golem.util.parser.TemplateError("[% color_wf %] must be inside [% color_basis %]")
        if "prefix" in opts:
            prefix = opts["prefix"]
        else:
            prefix = ""

        if "shift" in opts:
            shift = int(opts["shift"])
        else:
            shift = 0

        index_name = self._setup_name("index", prefix + "index", opts)
        gindex_name = self._setup_name("gindex", prefix + "gindex", opts)
        lindex_name = self._setup_name("lindex", prefix + "lindex", opts)
        io_name = self._setup_name("io", prefix + "io", opts)
        rep_name = self._setup_name("rep", prefix + "rep", opts)
        first_name = self._setup_name("first", prefix + "is_first", opts)
        last_name = self._setup_name("last", prefix + "is_last", opts)

        color_name = self._setup_name("color", prefix + "color", opts)
        acolor_name = self._setup_name("acolor", prefix + "acolor", opts)

        wf, lines, traces = self._cs_stack[-1]

        props = Properties()
        last_idx = len(wf) - 1

        for idx, the_wf in enumerate(wf):
            io, io_idx, g_idx, r = the_wf.split(":")
            props.setProperty(index_name, idx + shift)
            props.setProperty(io_name, io)
            props.setProperty(rep_name, r)
            props.setProperty(lindex_name, io_idx)
            props.setProperty(gindex_name, g_idx)
            props.setProperty(first_name, idx == 0)
            props.setProperty(last_name, idx == last_idx)
            props.setProperty(color_name, self._color[idx])
            props.setProperty(acolor_name, self._acolor[idx])
            yield props

    def color_lines(self, *args, **opts):
        if len(self._cs_stack) == 0:
            raise golem.util.parser.TemplateError("[% color_lines %] must be inside [% color_basis %]")

        if "prefix" in opts:
            prefix = opts["prefix"]
        else:
            prefix = ""

        if "shift" in opts:
            shift = int(opts["shift"])
        else:
            shift = 0

        index_name = self._setup_name("index", prefix + "index", opts)
        first_name = self._setup_name("first", prefix + "is_first", opts)
        last_name = self._setup_name("last", prefix + "is_last", opts)

        first_io = self._setup_name("first_io", prefix + "first_io", opts)
        first_rep = self._setup_name("first_rep", prefix + "first_rep", opts)
        first_gidx = self._setup_name("first_gidx", prefix + "first_gidx", opts)
        first_lidx = self._setup_name("first_lidx", prefix + "first_lidx", opts)

        last_io = self._setup_name("last_io", prefix + "last_io", opts)
        last_rep = self._setup_name("last_rep", prefix + "last_rep", opts)
        last_gidx = self._setup_name("last_gidx", prefix + "last_gidx", opts)
        last_lidx = self._setup_name("last_lidx", prefix + "last_lidx", opts)

        wf, lines, traces = self._cs_stack[-1]

        props = Properties()
        last_idx = len(lines) - 1

        for idx, the_line in enumerate(lines):
            first_idx = the_line[0]
            last_idx = the_line[-1]
            fio, flidx, fgidx, fr = first_idx.split(":")
            lio, llidx, lgidx, lr = last_idx.split(":")

            props.setProperty(index_name, idx + shift)
            props.setProperty(first_name, idx == 0)
            props.setProperty(last_name, idx == last_idx)

            props.setProperty(first_io, fio)
            props.setProperty(first_gidx, fgidx)
            props.setProperty(first_lidx, flidx)
            props.setProperty(first_rep, fr)
            props.setProperty(last_io, lio)
            props.setProperty(last_gidx, lgidx)
            props.setProperty(last_lidx, llidx)
            props.setProperty(last_rep, lr)

            self._cs_line_stack.append(the_line[1:-1])
            yield props
            self._cs_line_stack.pop()

    def color_traces(self, *args, **opts):
        if len(self._cs_stack) == 0:
            raise golem.util.parser.TemplateError("[% color_traces %] must be inside [% color_basis %]")

        if "prefix" in opts:
            prefix = opts["prefix"]
        else:
            prefix = ""

        if "shift" in opts:
            shift = int(opts["shift"])
        else:
            shift = 0

        index_name = self._setup_name("index", prefix + "index", opts)
        first_name = self._setup_name("first", prefix + "is_first", opts)
        last_name = self._setup_name("last", prefix + "is_last", opts)

        wf, lines, traces = self._cs_stack[-1]

        props = Properties()
        last_idx = len(traces) - 1

        first_trace_index = 0

        for idx, the_trace in enumerate(traces):
            props.setProperty(index_name, idx + shift)
            props.setProperty(first_name, idx == 0)
            props.setProperty(last_name, idx == last_idx)

            self._cs_trace_stack.append((first_trace_index, the_trace))
            yield props
            self._cs_trace_stack.pop()
            first_trace_index += len(the_trace)

    def color_line_elements(self, *args, **opts):
        if len(self._cs_line_stack) == 0:
            raise golem.util.parser.TemplateError("[% color_line_elements %] must be inside [% color_lines %]")

        do_reversed = "reversed" in args

        if "prefix" in opts:
            prefix = opts["prefix"]
        else:
            prefix = ""

        if "shift" in opts:
            shift = int(opts["shift"])
        else:
            shift = 0

        index_name = self._setup_name("index", prefix + "index", opts)
        prev_name = self._setup_name("prev", prefix + "prev", opts)
        first_name = self._setup_name("first", prefix + "is_first", opts)
        last_name = self._setup_name("last", prefix + "is_last", opts)

        gindex_name = self._setup_name("gindex", prefix + "gindex", opts)
        lindex_name = self._setup_name("lindex", prefix + "lindex", opts)
        io_name = self._setup_name("io", prefix + "io", opts)
        rep_name = self._setup_name("rep", prefix + "rep", opts)

        line = self._cs_line_stack[-1]
        last_idx = len(line) - 1

        props = Properties()
        if do_reversed:
            line = reversed(line)
        prev = -1
        for idx, element in enumerate(line):
            props.setProperty(index_name, idx + shift)
            props.setProperty(prev_name, prev + shift)
            props.setProperty(first_name, idx == 0)
            props.setProperty(last_name, idx == last_idx)

            io, io_idx, g_idx, r = element.split(":")
            props.setProperty(io_name, io)
            props.setProperty(rep_name, r)
            props.setProperty(lindex_name, io_idx)
            props.setProperty(gindex_name, g_idx)

            yield props
            prev = idx

    def color_trace_elements(self, *args, **opts):
        if len(self._cs_trace_stack) == 0:
            raise golem.util.parser.TemplateError("[% color_trace_elements %] must be inside [% color_traces %]")

        do_reversed = "reversed" in args

        if "prefix" in opts:
            prefix = opts["prefix"]
        else:
            prefix = ""

        if "shift" in opts:
            shift = int(opts["shift"])
        else:
            shift = 0

        index_name = self._setup_name("index", prefix + "index", opts)
        prev_name = self._setup_name("prev", prefix + "prev", opts)
        first_name = self._setup_name("first", prefix + "is_first", opts)
        last_name = self._setup_name("last", prefix + "is_last", opts)

        gindex_name = self._setup_name("gindex", prefix + "gindex", opts)
        lindex_name = self._setup_name("lindex", prefix + "lindex", opts)
        io_name = self._setup_name("io", prefix + "io", opts)
        rep_name = self._setup_name("rep", prefix + "rep", opts)

        first_trace_index, trace = self._cs_trace_stack[-1]

        props = Properties()
        last_idx = len(trace) - 1

        if do_reversed:
            trace = reversed(trace)
        prev = last_idx
        for idx, element in enumerate(trace):
            props.setProperty(index_name, idx + shift + first_trace_index)
            props.setProperty(prev_name, prev + shift + first_trace_index)
            props.setProperty(first_name, idx == 0)
            props.setProperty(last_name, idx == last_idx)

            io, io_idx, g_idx, r = element.split(":")
            props.setProperty(io_name, io)
            props.setProperty(rep_name, r)
            props.setProperty(lindex_name, io_idx)
            props.setProperty(gindex_name, g_idx)

            yield props
            prev = idx

    def olp_spin_correlated_twist(self, *args, **opts):
        index_name = self._setup_name("index", "index", opts)
        var_name = self._setup_name("var", "$_", opts)
        sign_name = self._setup_name("sign", "sign", opts)
        crossed_particles = [prop.getIntegerProperty("$_") for prop in self.crossing()]
        orig_particles = [prop.getIntegerProperty("index") for prop in self.crossing()]
        gluons = [prop.getIntegerProperty("index") for prop in self.particles("gluons")]
        colored = [prop.getIntegerProperty("index") for prop in self.particles("colored")]

        for i in range(len(crossed_particles)):
            if not crossed_particles[i] in gluons:
                continue
            orig_pos_ii = orig_particles[i] - 1
            cros_pos_ii = crossed_particles[i] - 1
            for j in range(len(crossed_particles)):
                if not crossed_particles[j] in colored:
                    continue
                if i == j:
                    continue
                orig_pos_jj = orig_particles[j] - 1
                cros_pos_jj = crossed_particles[j] - 1
                sign_temp = "+"
                if (orig_pos_ii > 1 and cros_pos_ii <= 1) or (orig_pos_ii <= 1 and cros_pos_ii > 1):
                    sign_temp = "-"
                props = Properties()
                props.setProperty(var_name, str(2 * (orig_pos_ii + orig_pos_jj * self._num_legs) + 1))
                props.setProperty(index_name, str(2 * (cros_pos_ii + cros_pos_jj * self._num_legs) + 1))
                props.setProperty(sign_name, "+")
                yield props
                props.setProperty(var_name, str(2 * (orig_pos_ii + orig_pos_jj * self._num_legs) + 2))
                props.setProperty(index_name, str(2 * (cros_pos_ii + cros_pos_jj * self._num_legs) + 2))
                props.setProperty(sign_name, sign_temp)
                yield props

    def olp_color_correlated_twist(self, *args, **opts):
        def calcpos(ix, jx):
            if ix < jx:
                ##return ix-1+(jx-1)*(jx-2)//2 +1
                return ix + jx * (jx - 1) // 2
            else:
                ##return jx-1+(ix-1)*(ix-2)//2 +1
                return jx + ix * (ix - 1) // 2

        index_name = self._setup_name("index", "index", opts)
        var_name = self._setup_name("var", "$_", opts)
        crossed_particles = [prop.getIntegerProperty("$_") for prop in self.crossing()]
        orig_particles = [prop.getIntegerProperty("index") for prop in self.crossing()]
        colored = [prop.getIntegerProperty("index") for prop in self.particles("colored")]
        # crossed_colored = list(crossed_particles)
        # for i in crossed_particles:
        # if i not in colored:
        # del crossed_colored[crossed_colored.index(i)]

        # for i in range(len(colored)-1):
        # for j in range(i+1,len(colored)):
        # if not ( colored[i]== crossed_colored[i] and colored[j]==crossed_colored[j]):
        #  props=Properties()
        # props.setProperty(var_name, str(calcpos(colored[i],colored[j])))
        # props.setProperty(index_name, str(calcpos(crossed_colored[i],crossed_colored[j])))
        # yield props

        for i in range(len(crossed_particles)):
            if not crossed_particles[i] in colored:
                continue
            orig_pos_ii = orig_particles[i] - 1
            for j in range(len(crossed_particles)):
                if not crossed_particles[j] in colored:
                    continue
                if i >= j:
                    continue
                orig_pos_jj = orig_particles[j] - 1
                props = Properties()
                props.setProperty(index_name, str(calcpos(crossed_particles[i] - 1, crossed_particles[j] - 1) + 1))
                props.setProperty(var_name, str(calcpos(orig_pos_ii, orig_pos_jj) + 1))
                yield props

    def ewchoose(self, *args, **opts):
        if "ewchoose" in golem.model.MODEL_OPTIONS:
            return golem.model.MODEL_OPTIONS["ewchoose"]
        else:
            return False

    def starting_choice(self, *args, **opts):
        if self.e_not_one(args, opts):
            if golem.model.MODEL_OPTIONS["users_choice"] == "0":
                return "2"
            else:
                return golem.model.MODEL_OPTIONS["users_choice"]
        else:
            if golem.model.MODEL_OPTIONS["users_choice"] == "0":
                return "2"
            else:
                return golem.model.MODEL_OPTIONS["users_choice"]

    def e_not_one(self, *args, **opts):
        ones = golem.model.MODEL_ONES
        if "e" in ones:
            e_not_one = False
        else:
            e_not_one = True
        return e_not_one

    def flags_filter(self, *args, **opts):
        assert args == ("$_",)
        flags = self._stack[-1]["$_"]
        ret = ""
        for f in flags.split():
            if f not in self._listed_flags:
                self._listed_flags_length += len(f)
                if self._listed_flags_length > 80:
                    self._listed_flags_length = 0
                    ret = ret + "\\\n "
                    self._listed_flags_length += len(f)
                ret = ret + f + " "
                self._listed_flags.add(f)
        if self._stack[-1]["is_last"] == "True":
            ret = ret.rstrip()
        return ret

    def reset_flags_filter(self, *args, **opts):
        self._listed_flags = set()
        self._listed_flags_length = 0
        return ""
