# vim: ts=3:sw=3:expandtab

from golem.util.config import Property
from golem.util.path import golem_path


process_name = Property(
    "process_name",
    """\
   A symbolic name for this process. This name will be used
   as a prefix for the Fortran modules.

   Golem will insert an underscore after this prefix.
   If the process name is left blank no prefix will be used
   and no extra underscore will be generated.
   """,
    str,
    "",
)

process_path = Property(
    "process_path",
    """\
   The path to which all Form output is written.
   If no absolute path is given, the path is interpreted relative
   to the working directory from which gosam.py is run.

   Example:
   process_path=/scratch/golem_processes/process1
   """,
)

qgraf_in = Property(
    "in",
    """\
   A comma-separated list of initial state particles.
   Which particle names are valid depends on the
   model file in use.

   Examples (Standard Model):
   1) in=u,u~
   2) in=e+,e-
   3) in=g,g
   """,
    list,
)

qgraf_out = Property(
    "out",
    """\
   A comma-separated list of final state particles.
   Which particle names are valid depends on the
   model file in use.

   Examples (Standard Model):
   1) out=H,u,u~
   2) out=e+,e-,gamma
   3) out=b,b~,t,t~
   """,
    list,
)

model = Property(
    "model",
    """\
   This option allows the selection of a model for the
   Feynman rules. It has to conform with one of four possible
   formats:

   1) model=<name>
   2) model=<path>, <name>
   3) model=<path>, <number>
   4) model=FeynRules, <path>

   Format 1) searches for the model files <name>, <name>.hh
   and <name>.py in the models/ directory under the installation
   path of Golem.

   Format 2) is similar to format 1) but <path> is used instead
   of the models/ directory of the Golem installation

   Format 3) expects the files func<number>.mdl, lgrng<number>.mdl,
   prtcls<number>.mdl and vars<number>.mdl in the directory <path>.
   These files need to be in CalcHEP/CompHEP format.

   Format 4) expects a UFO model in the directory specified by <path>.
   """,
    list,
    "smdiag",
)

model_options = Property(
    "model.options",
    """\
   If the model in use supports options they can be passed via this
   property.

   For builtin models, the option "ewchoose"
   automatically selects the EW scheme used.
   """,
    list,
    "ewchoose",
)

qgraf_power = Property(
    "order",
    """\
   A 3-tuple <coupling>,<born>,<virt> where <coupling> denotes
   a function of the qgraf style file which can be used as
   an argument in a 'vsum' statement. For the standard model
   file 'sm' there are two such functions, 'gs' which counts
   powers of the strong coupling and 'gw' which counts powers
   of the weak coupling. <born> is the sum of powers for the
   tree level amplitude and <virt> for the virtual amplitude.
   The line
      order = gs, 4, 6
   would select all diagrams which have (gs)^4 at tree level
   and all loop graphs with (gs)^6.

   Note: The line
      order = gw, 2, 2
   does not imply that no virtual corrections are calculated.
   Instead, for the virtual corrections diagrams are chosen
   with the same order in gw but higher order in gs.

   In other models with more than two different coupling
   constants additional 'vsum' statements, which can be passed
   via the qgraph.verbatim option, might be needed
   to select the correct set of diagrams.

   The user can also use QCD instead of gs and QED instead of gw.

   If the last number is omitted no virtual corrections are
   calculated.

   See also: qgraf.options, qgraf.verbatim
   """,
    list,
)

helicities = Property(
    "helicities",
    """\
   A list of helicities to be calculated. An empty list
   means that all possible helicities should be generated.

   The helicities are specified as a string of characters
   according to the following table:

      spin massive  |  'm'  '-'  '0'   '+'   'k'
        0   YES/NO  | ---- ----    0  ----  ----
      1/2   YES/NO  | ---- -1/2 ----  +1/2  ----
        1     NO    | ----   -1 ----    +1  ----
        1    YES    | ----   -1    0    +1  ----
      3/2     NO    | -3/2 ---- ----  ----  +3/2
      3/2    YES    | -3/2 -1/2 ----  +1/2  +3/2
        2     NO    |   -2 ---- ----  ----    +2
        2    YES    |   -2   -1    0    +1    +2

   Please, note that 'k' and 'm' are not in use yet but reserved
   for future extensions to higher spins.

   The characters correspond to particle 1, 2, ... from left to
   right.

   Examples:
      # e+, e- --> gamma, gamma:
      # Only three helicities required; the other ones are
      # either zero or can be obtained by symmetry
      # transformations.
      helicities=+-++,+-+-,+---;

   Multiple helicities can be encoded in patterns, which are expanded
   at the time of code generation. Patterns can have one of the following
   forms:
      [+-], [+-0], [+0] etc. : the bracket expands to one of the symbols
            in the bracket at a time.
      EXAMPLE
            helicities=[+-]+[+-0]
            # expands to 6 different helicities:
            # helicities=+++, ++-, ++0, -++, -+-, -+0
      [a=+-], etc. : as above, but the helicity is also assigned to the
            symbol and can be reused.
      EXAMPLE
            helicities=[i=+-]+i+
            # expands to two helicities
            # helicities=++++, -+-+
      [ab=+-0], etc. : as above, the first symbol is assigned the helicity,
            the second is minus the helicity
      EXAMPLE
            helicities=[qQ=+-][pP=+-]PQ[+-0]
            # expands to 12 helicities
            # helicities=++--+,++---,++--0,+-+-+,+-+--,+-+-0,\\
            #            -+-++,-+-+-,-+-+0,--+++,--++-,--++0

   """,
    list,
)

qgraf_options = Property(
    "qgraf.options",
    """\
   A list of options which is passed to qgraf via the 'options' line.
   Possible values (as of qgraf.3.1.1) are zero, one or more of:
      onepi, onshell, nosigma, nosnail, notadpole, floop
      topol

   Please, refer to the QGraf documentation for details.
   """,
    list,
    "onshell,notadpole,nosnail",
    options=["onepi", "onshell", "nosigma", "nosnail", "notadpole", "floop", "topol"],
)

qgraf_verbatim = Property(
    "qgraf.verbatim",
    """\
   This option allows to send verbatim lines to
   the file qgraf.dat. This can be useful if the user
   wishes to put additional restricitons to the selected diagrams.
   This option is mainly inteded for the use of the operators
      rprop, iprop, chord, bridge, psum
   Note, that the use of 'vsum' might interfer with the
   option qgraf.power.

   Example:
   qgraf.verbatim=\\
      # no top quarks: \\n\\
      true=iprop[T, 0, 0];\\n\\
      # at least one Higgs:\\n\\
      false=iprop[H, 0, 0];\\n


   Please, refer to the QGraf documentation for details.

   See also: qgraf.options, order
   """,
    str,
    "",
)

qgraf_verbatim_lo = Property(
    "qgraf.verbatim.lo",
    """\
   Same as qgraf.verbatim but only applied to LO diagrams.

   See also: qgraf.verbatim, qgraf.verbatim.nlo
   """,
    str,
    "",
)

qgraf_verbatim_nlo = Property(
    "qgraf.verbatim.nlo",
    """\
   Same as qgraf.verbatim but only applied to NLO diagrams.

   See also: qgraf.verbatim, qgraf.verbatim.nlo
   """,
    str,
    "",
)

qgraf_verbatim_ct = Property(
    "qgraf.verbatim.ct",
    """\
   Same as qgraf.verbatim but only applied to CT diagrams.

   See also: qgraf.verbatim, qgraf.verbatim.nlo
   """,
    str,
    "",
)

zero = Property(
    "zero",
    """\
   A list of symbols that should be treated as identically
   zero throughout the whole calculation. All of these
   symbols must be defined by the model file.
   If you do not use built-in models, you probably
   need to overwrite the default value.

   Examples:
   1) # Light masses are set to zero here:
      zero=me,mU,mD,mS
   2) # Diagonal CKM matrix:
      zero=VUS, VUB, CVDC, CVDT, \\
           VCD, VCB, CVSU, CVST, \\
           VTD, VTS, CVBU, CVBC
      one=  VUD,  VCS,  VTB, \\
           CVDU, CVSC, CVBT

   See also: model, one
   """,
    list,
    "mU,mD,mS,mC,mB,me,mmu",
)

one = Property(
    "one",
    """\
   A list of symbols that should be treated as identically
   one throughout the whole calculation. All of these
   symbols must be defined by the model file.

   Example:
   one=gs, e

   See also: model, zero
   """,
    list,
)

qgraf_bin = Property(
    "qgraf.bin",
    """\
   Points to the QGraf executable.

   Example:
   qgraf.bin=/home/my_user_name/bin/qgraf
   """,
    str,
    "qgraf",
)

form_bin = Property(
    "form.bin",
    """\
   Points to the Form executable.

   Examples:
   1) # Use TForm:
      form.bin=tform
   2) # Use non-standard location:
      form.bin=/home/my_user_name/bin/form
   """,
    str,
    "tform",
)

form_threads = Property(
    "form.threads",
    """\
   Number of Form threads.

   Example:
   form.threads=4
   runs tform, the parallel version of FORM, on 4 cores.
   """,
    int,
    2,
)

form_workspace = Property(
    "form.workspace",
    """\
   Size of the heap (in megabytes) used by FORM.

   Example (for machines with <= 2GB RAM):
   form.workspace=100
   set WorkSpace to 100M in FORM via form.set file.
   """,
    int,
    1000,
)


form_tmp = Property(
    "form.tempdir",
    """\
   Temporary directory for Form. Should point to a directory
   on a local disk.

   Examples:
   form.tempdir=/tmp
   form.tempdir=/scratch
   """,
    str,
    "/tmp",
)

template_path = Property(
    "templates",
    """\
   Path pointing to the directory containing the template
   files for the process. If not set, GoSam uses the directory
   <gosam_git_path>/templates, where <gosam_git_path> is the 
   path into which the GoSam git has been cloned.

   The directory must contain a file called 'template.xml'
   """,
    str,
    "",
)

sum_diagrams = Property(
    "diagsum",
    """\
   Flag whether or not 1-loop diagrams with the same propagators
   should be summed before the algebraic reduction.
   """,
    bool,
    True,
)

sum_helicities = Property(
    "helsum",
    """\
   Flag whether or not 1-loop diagrams should be analytically
   summed over all helicities
   """,
    bool,
    False,
    experimental=True,
)

renorm = Property(
    "renorm",
    """\
   Indicates if the UV counterterms should be generated.

   Examples:
   renorm=true
   renorm=false
   """,
    bool,
    True,
    experimental=True,
)

formopt_level = Property(
    "formopt.level",
    """\
   There are three levels of Horner Scheme
   offered and the number here will specify
   which one we use. It can only be 1,2 or 3.

   Examples:
   formopt.level=3

   """,
    str,
    "2",
)

regularisation_scheme = Property(
    "regularisation_scheme",
    """\
         Sets the used regularisation scheme.
         Possible values: dred (recommended), cdr
      """,
    str,
    "dred",
)

reduction_programs = Property(
    "reduction_programs",
    """\
        Specifies the reduction libraries which should be supported.

        Possible values: ninja golem95

        See also reduction_interoperation, reduction_interoperation_rescue.
      """,
    list,
    "ninja",
    options=["ninja", "golem95"],
)

polvec_method = Property(
    "polvec",
    """\
          Evaluate the polarisation vector
          'numerical' or 'explicit'.
     """,
    str,
    "numerical",
    options=["numerical", "explicit"],
)

DEFAULT_EXTENSIONS = "".split(",")

extensions = Property(
    "extensions",
    """\
   A list of extension names which should be activated for the
   code generation.

   Build system related extensions:

   f77          --- in combination with the BLHA interface it generates
                    an olp_module.f90 linkable with Fortran77

   Other extensions:
   gaugecheck   --- modify gauge boson wave functions to allow for
                    a limited gauge check (introduces gauge*z variables)
   customspin2prop --- replace the propagator of spin-2 particles
                       with a custom function (read the manual for this).
   quadruple    --- make a quadruple precision copy of the code (this
                    works only with ninja).

   """,
    #   olp_badpts   --- (OLP interface only): allows to stear the numbering
    #                    of the files containing bad points from the MC
    #
    #   olp_daemon   --- (OLP interface only): generates a C-program providing
    #   ninja        --- enable Ninja for the reduction
    #   golem95      --- enable Golem95 for the reduction
    #   qshift       --- apply the shift of Q already at the FORM level
    #   numpolvec    --- evaluate polarisation vectors numerically
    #   tracify      --- transform loop momenta into traces before running
    #                    the numerics
    list,
    ",".join(DEFAULT_EXTENSIONS),
    options=[
        "golem95",
        "dred",
        "qshift",
        "avh_olo",
        "gaugecheck",
        "derive",
        "generate-all-helicities",
        "olp_daemon",
        "olp_badpts",
        "olp_blha1",
        "numpolvec",
        "f77",
        "no-fr5",
        "ninja",
        "customspin2prop",
        "cdr",
        "noderive",
        "tracify",
        "quadruple"
    ],
)

select_lo_diagrams = Property(
    "select.lo",
    """\
   A list of integer numbers, indicating leading order diagrams to be
   selected. If no list is given, all diagrams are selected.
   Otherwise, all diagrams not in the list are discarded.

   The list may contain ranges:

   select.lo=1,2,5:10:3, 50:53

   which is equivalent to

   select.lo=1,2,5,8,50,51,52,53

   See also: select.nlo, filter.lo, filter.nlo
   """,
    list,
    sep=",",
)

select_nlo_diagrams = Property(
    "select.nlo",
    """\
   A list of integer numbers, indicating one-loop diagrams to be selected.
   If no list is given, all diagrams are selected.
   Otherwise, all diagrams   not in the list are discarded.

   The list may contain ranges:

   select.nlo=1,2,5:10:3, 50:53

   which is equivalent to

   select.nlo=1,2,5,8,50,51,52,53

   See also: select.lo, filter.lo, filter.nlo
   """,
    list,
    sep=",",
)

select_ct_diagrams = Property(
    "select.ct",
    """\
   A list of integer numbers, indicating EFT counterterm diagrams to be
   selected. If no list is given, all diagrams are selected.
   Otherwise, all diagrams not in the list are discarded.

   The list may contain ranges:

   select.ct=1,2,5:10:3, 50:53

   which is equivalent to

   select.ct=1,2,5,8,50,51,52,53

   See also: select.nlo, filter.lo, filter.nlo
   """,
    list,
    sep=",",
)

filter_lo_diagrams = Property(
    "filter.lo",
    """\
   A python function which provides a filter for tree diagrams.

   filter.lo=lambda d: d.iprop(Z) == 1 \\
      and d.vertices(Z, U, Ubar) == 0

   The following methods of the diagram class can be used:

   * d.rank() = the maximum rank in Q possible for this diagram
   * d.loopsize() = the number of propagators in the loop
   * d.vertices(field1, field2, ...) = number of vertices
       with the given fields
   * d.loopvertices(field1, field2, ...) = number of vertices
       with the given fields; only those vertices which have
       at least one loop propagator attached to them
   * d.iprop(field, momentum="...", twospin=..., massive=True/False,
                                                            color=...) =
       the number of propagators with the given properties:
        - field: a field or list of fields
        - momentum: a string denoting the momentum through this propagator,
               such as "k1+k2"
        - twospin: two times the spin (integer number)
        - massive: select only propagators with/without a non-zero mass
        - color: one of the numbers 1, 3, -3 or 8, or a list of
                 these numbers
   * d.iprop_momentum(field, momentum="...") = True when the diagram contains
      a propagator of field with the specified momentum, False otherwise 
   * d.chord(...) = number of loop propagators with the given properties;
       the arguments are the same as in iprop
   * d.bridge(...) = number of non-loop propagators with the given
       properties; the arguments are the same as in iprop
   * d.order(coupling) = total power of diagrams with respect to specified 
      coupling. Only works whit UFO models. The coupling must be defined 
      in the UFO model's coupling_orders.py and listed in the 'order_names'
      property of the GoSam config/runcard.

   Note: Using d.iprop(field, momentum="...") in olp-mode can lead to 
         inconsistencies in the automatically generated crossings. This
         can be circumvented by running GoSam with the option --no-crossings
         or using the iprop_momentum function, which tracks invalid crossings.
   
   See also: filter.nlo, select.lo, select.nlo
   """,
    str,
    "",
)

filter_nlo_diagrams = Property(
    "filter.nlo",
    """\
   A python function which provides a filter for loop diagrams.

   See filter.lo for more explanation.
   """,
    str,
    "",
)

filter_ct_diagrams = Property(
    "filter.ct",
    """\
   A python function which provides a filter for eft counterterm diagrams.

   See filter.ct for more explanation.
   """,
    str,
    "",
)

filter_module = Property(
    "filter.module",
    """\
   A python file of predefined functions which should be available
   in filters.

   Example:

   filter.module=filter.py
   filter.nlo=my_nlo_filter("vertices.txt")
   filter.lo=my_nlo_filter("vertices.txt")

   ------ filter.py -----

   class my_nlo_filter_class:
      def __init__(self, fname):
         self.fields = []
         with open(fname, 'r') as f:
            for line in f.readlines():
               fields = map(lambda s: s.strip(),
                     line.split(","))
               self.fields.append(fields)

      def __call__(self, diag):
         for lst in self.fields:
            if diag.vertices(*lst) > 0:
               return False
         return True

   ----------------------

   See filter.lo, filter.nlo
   """,
    str,
    "",
)

debug_flags = Property(
    "debug",
    """\
   A list of debug flags.
   Currently, the words 'lo', 'nlo' and 'all' are supported.
   """,
    list,
    options=["nlo", "lo", "numpolvec", "all"],
)

reference_vectors = Property(
    "reference-vectors",
    """\
   A list of reference vectors for massive and higher spin particles.
   For vectors which are not assigned here, the program picks a
   reference vector automatically.

   Each entry of the list has to be of the form <index>:<index>

   EXAMPLE

   in=g,u
   out=t,W+
   reference-vectors=1:2,3:4,4:3

   In this example, the gluon (particle 1) takes the momentum k2
   as reference momentum for the polarisation vector. The massive
   top quark (particle 3) uses the light-cone projection l4 of the
   W-boson as reference direction for its own momentum splitting.
   Similarly, the momentum of the W-boson is split into a direction
   l4 and one along l3.

   If cycles are generated in the list (l3 has to be known in order
   to determine l4 and vice versa in the above example) they must be
   at most of length two. For the reference momenta of lightlike
   gauge bosons the length of cycles does not matter, e.g.

   in=g,g
   out=g,g
   reference-vectors=1:2,2:3,3:4,4:1
   """,
    list,
)

abbrev_color = Property(
    "abbrev.color",
    """\
   The program in use for the generation of color related abbreviations.
   The value should be one of:
      form           color algebra and optimization in form
      none           color algebra in form, no optimization
   """,
    str,
    "form",
    options=["form", "none"],
    hidden=True,
)

abbrev_limit = Property(
    "abbrev.limit",
    """\
   Maximum number of instructions per subroutine when calculating
   abbreviations, if this number is positive.
   """,
    str,
    "500",
)

r2 = Property(
    "r2",
    """\
   The algorithm how to treat the R2 term:

   implicit    -- mu^2 terms are kept in the numerator and reduced
                  at runtime
   explicit    -- mu^2 terms are reduced analytically
   """,
    str,
    "explicit",
    options=["implicit", "explicit"],
)

crossings = Property(
    "crossings",
    """\
   A list of crossed processes derived from this process.

   For each process in the list a module similar to matrix.f90 is
   generated.

   Example:

   process_name=ddx_uux
   in=1,-1
   out=2,-2

   crossings=dxd_uux: -1 1 > 2 -2, ud_ud: 2 1 > 2 1
   """,
    list,
)

symmetries = Property(
    "symmetries",
    """\
   Specifies the symmetries of the amplitude.

   This information is used when the list of helicities is generated.

   Possible values are:

   * flavour    -- no flavour changing interactions
            When calculating the list of helicities, fermion lines
       of PDGs 1-6 are assumed not to mix.

   * family     -- flavour changing only within families
            When calculating the list of helicities, fermion lines
       of PDGs 1-6 are assumed to mix only within families,
       i.e. a quark line connecting a up with a down quark would
       be considered, while up-bottom is not.
   * lepton     -- means for leptons what 'flavour' means for quarks
   * generation -- means for leptons what 'family' means for quarks
   * parity     -- the amplitude is invariant under parity tranformation.
                   === Parity is not implemented yet.
   * <n>=<h>    -- restriction of particle helicities,
            e.g. 1=-, 2=+ specifies helicities of particles 1 and 2
   * %<n>=<h>   -- restriction by PDG code,
            e.g. %23=+- specifies the helicity of all Z-bosons to be
            '+' and '-' only (no '0' polarisation).

            %<n> refers to both +n and -n
            %+<n> refers to +n only
            %-<n> refers to -n only
   """,
    list,
)

pyxodraw = Property(
    "pyxodraw",
    """\
   Specifies whether to draw any diagrams or not.
   """,
    bool,
    True,
    hidden=True,
)

config_renorm_beta = Property(
    "renorm_beta",
    """\
   Sets the name of the same variable in config.f90

   Activates or disables beta function renormalisation

   QCD only
   """,
    bool,
    True,
)

config_renorm_logs = Property(
    "renorm_logs",
    """\
   Sets the name of the same variable in config.f90

   Activates or disables the logarithmic finite terms
   of all UV counterterms

   QCD only
   """,
    bool,
    True,
)

config_renorm_mqse = Property(
    "renorm_mqse",
    """\
   Sets the name of the same variable in config.f90

   Activates or disables the UV counterterm coming from the
   massive quark propagators

   QCD only
   """,
    bool,
    True,
)

config_renorm_decoupling = Property(
    "renorm_decoupling",
    """\
   Sets the name of the same variable in config.f90

   Activates or disables UV counterterms coming from
   massive quark loops

   QCD only
   """,
    bool,
    True,
)

config_renorm_mqwf = Property(
    "renorm_mqwf",
    """\
   Sets the name of the same variable in config.f90

   Activates or disables UV countertems coming from
   external massive quarks

   QCD only
   """,
    bool,
    True,
)

config_renorm_gamma5 = Property(
    "renorm_gamma5",
    """\
   Sets the same variable in config.f90

   Activates finite renormalisation for axial couplings in the
   't Hooft-Veltman scheme

   QCD only, works only with built-in model files.
   """,
    bool,
    True,
)

config_renorm_yukawa = Property(
    "renorm_yukawa",
    """\
   Sets the same variable in config.f90

   Enables renormalization of Yukawa coupling. Two schemes are
   possible: On-Shell and MSbar.

   QCD only.

   See also: MSbar_yukawa
   """,
    bool,
    True,
)

config_renorm_eftwilson = Property(
    "renorm_eftwilson",
    """\
   Sets the same variable in config.f90

   Enables renormalization of EFT Wilson coefficients.
   Works only with special New Physics UFO models, con-
   taining 'NP' as additional coupling order. 'order_names'
   must be specified and explicitly contain 'NP'.
   """,
    bool,
    False,
    experimental=True,
)

config_renorm_ehc = Property(
    "renorm_ehc",
    """\
   Sets the same variable in config.f90

   Turns on the finite renormalisation of effective Higgs-gluon
   vertices. Implemented for models in the heavy-top limit like
   smehc. Should not be used when counterterms for Wilson coeffi-
   cients are supplyed by means of a UFO model (see 'renorm_eft_wilson'). 
   CAUTION: 
   This will only work if the Higgs-gluon vertices factorize from the 
   amplitude, i.e. the number of Higgs-gluon couplings is the same for 
   all Born diagrams!
   """,
    bool,
    False,
    experimental=True,
)

config_reduction_interoperation = Property(
    "reduction_interoperation",
    """
   Default reduction library.

   Possible values are: ninja, golem95

   Sets the same variable in config.f90. A value of '-1' lets GoSam decide
   depending on reduction_libraries

   See common/config.f90 for details.
   """,
    str,
    -1,
)

config_reduction_interoperation_rescue = Property(
    "reduction_interoperation_rescue",
    """
   Rescue reduction program.

   Sets the same variable in config.f90. A value of '-1' lets GoSam
   decide.

   See common/config.f90 for details.
   """,
    str,
    -1,
)

config_nlo_prefactors = Property(
    "nlo_prefactors",
    """
   Sets the same variable in config.f90. The values have the
   following meaning:

   0: A factor of alpha_(s)/2/pi is not included in the NLO result
   1: A factor of 1/8/pi^2 is not included in the NLO result
   2: The NLO includes all prefactors

   Note, however, that the factor of 1/Gamma(1-eps) is not
   included in any of the cases.

   Please note, that nlo_prefactors=0 is enforced temporary in test.f90
   for better testing. In OLP interface mode (BLHA/BLHA2), the default is
   nlo_prefactors=2.
   """,
    int,
    0,
    options=["0", "1", "2"],
)

config_PSP_check = Property(
    "PSP_check",
    """\
   Sets the same variable in config.f90

   Activates Phase-Space Point test for the full amplitude.

   !!Works only for QCD and with built-in model files!!
   """,
    bool,
    True,
)

config_PSP_rescue = Property(
    "PSP_rescue",
    """\
   Sets the same variable in config.f90

   Activates Phase-Space Point rescue based on the estimated
   accuracy on the finite part. It needs PSP_check=True.
   The accuracy is estimated using information on the single
   pole accuracy and on the stability of the finite part
   under rotation of the phase space point.

   !!Works only for QCD and with built-in model files!!
   """,
    bool,
    False,
)

config_PSP_verbosity = Property(
    "PSP_verbosity",
    """\
   Sets the same variable in config.f90

   Sets the verbosity of the PSP_check.
   verbosity = False: no output
   verbosity = True : bad point are written into gs_badpts.log
   !!Works only for QCD and with built-in model files!!
   """,
    bool,
    False,
)

config_PSP_chk_th1 = Property(
    "PSP_chk_th1",
    """\
   Sets the same variable in config.f90

   Threshold to activate accept the point without further
   treatments. The number has to be an integer indicating the
   wished minimum number of digits accuracy on the pole. For poles
   more precise than this threshold the finite part is not checked.
   !!Works only for QCD and with built-in model files!!
   """,
    int,
    8,
)

config_PSP_chk_th2 = Property(
    "PSP_chk_th2",
    """\
   Sets the same variable in config.f90

   Threshold to declare a PSP as bad point, based of the precision
   of the pole.  Points with precision less than this threshold are
   directly reprocessed with the rescue system (if available), or
   declared as unstable. According to the verbosity level set, such
   points are written to a file and not used when the code is
   interfaced to an external Monte Carlo using the new BLHA
   standards.
   !!Works only for QCD and with built-in model files!!
   """,
    int,
    3,
)

config_PSP_chk_th3 = Property(
    "PSP_chk_th3",
    """\
   Sets the same variable in config.f90

   Threshold to declare a PSP as bad point, based on the precision
   of the finite part estimated with a rotation. According to the
   verbosity level set, such points are written to a file and not
   used when the code is interfaced to an external Monte Carlo
   using the new BLHA standards.
   !!Works only for QCD and with built-in model files!!
   """,
    int,
    5,
)


config_PSP_chk_li1 = Property(
    "PSP_chk_li1",
    """\
   Sets the same variable in config.f90. For loop-induced
   processes, it is used instead of PSP_chk_th1.

   It is precision of the pole part (which should be zero) in
   comparison to the finite part. If the pole part is at least
   PSP_chk_li1 orders smaller than the finite part, the point is
   accepted without any other check.

   The number has to be an integer.
   """,
    int,
    16,
)

config_PSP_chk_li2 = Property(
    "PSP_chk_li2",
    """\
   Sets the same variable in config.f90. For loop-induced
   processes, it is used instead of PSP_chk_th2.

   Threshold to declare a PSP as bad point, based of the precision
   of the pole in comparison to the finite part. Points with
   precision less than this threshold are directly reprocessed with
   the rescue system (if available), or declared as unstable.
   According to the verbosity level set, such points are written to
   a file and not used when the code is interfaced to an external
   Monte Carlo using the new BLHA standards.
   """,
    int,
    7,
)

config_PSP_chk_li3 = Property(
    "PSP_chk_li3",
    """\
   Sets the same variable in config.f90. For loop-induced
   processes, it is used instead of PSP_chk_th3.

   Threshold to declare a PSP as bad point, based on the precision
   of the finite part estimated with a rotation. Points with
   precision less than this threshold are reprocessed with the
   rescue system (if available) or declared as unstable.  According
   to the verbosity level set, such points are written to a file
   and not used when the code is interfaced to an external Monte
   Carlo using the new BLHA standards.
   """,
    int,
    6,
)

config_PSP_chk_li4 = Property(
    "PSP_chk_li4",
    """\
   Sets the same variable in config.f90. Similar to PSP_chk_li2,
   but for the rescue system (by default Golem95).

   Threshold to declare a PSP as bad point in the rescue system,
   based on the precision of the pole part in comparison to the
   finite part. According to the verbosity level set, such points
   are written to a file and not used when the code is interfaced
   to an external Monte Carlo using the new BLHA standards.
   """,
    int,
    19,
)


config_PSP_chk_kfactor = Property(
    "PSP_chk_kfactor",
    """\
   Sets the same variable in config.f90

   Threshold on the k-factor to perform a rotation check on the PSP. 
   !!Works only for QCD and with built-in model files!!
   """,
    str,
    1000,
)

config_PSP_chk_method = Property(
    "PSP_chk_method",
    """\
   This option can be used to overwrite the automatic phase-space point
   test method enabled with PSP_check=True.
   Except in some BSM scenarios, the user does not need to change this.

   Possible options:
   Automatic    - chooses automatically a suitable phase-space point test
                  method (default).
   PoleRotation - check first the pole and then rotate if necessary.
   Rotation     - force a rotation check on every phase space point.
   LoopInduced  - check that the pole part is zero and rotate if necessary.
                  Needed e.g. for interferience between BSM Born and
                  SM loop-induced virtual.
   """,
    str,
    "Automatic",
    options=["automatic", "polerotation", "rotation", "loopinduced"],
)


form_factor_lo = Property(
    "form_factor_lo",
    """\
   This option allows to define a form factor which LO results are multiplied with.
   Example: form_factor_lo="(1000._ki**2/(1000._ki**2+dotproduct(vecs(2,:)+vecs(3,:),vecs(2,:)+vecs(3,:))))"
   """,
    str,
    "",
    experimental=True,
)

form_factor_nlo = Property(
    "form_factor_nlo",
    """\
   This option allows to define a form factor which NLO/loop-induced results are multiplied with.
   """,
    str,
    "",
    experimental=True,
)


order_names = Property(
    "order_names",
    """\
   A list of additional coupling order that should be 
   tracked throughout the amplitude generation. Relevant for
   correct EFT treatment. Only works in combination with UFO
   models. All couplings listed must be defined in the model's
   coupling_orders.py file.

   Example:
   order_names=QCD,NP,QL
   """,
    list,
    default="",
    experimental=True,
)

enable_truncation_orders = Property(
    "enable_truncation_orders",
    """\
   Whether or not to generate extra code to assess different
   truncation orders in EFT calculations. Only works with a
   New Physics UFO model containing 'NP' as additional coupling
   order. 'order_names' must be specified and explicitly contain
   'NP'. When set to False (default) no truncation is performed,
   i.e. the amplitude is squared in the naive way.
   """,
    bool,
    False,
    experimental=True,
)

use_vertex_labels = Property(
    "use_vertex_labels",
    """\
   Whether or not to print the vertex label in the process.pdf. Can only
   be activated when using a UFO model file.
   """,
    bool,
    False,
    experimental=True,
)

all_mandelstam = Property(
    "all_mandelstam",
    """\
   If 'false' momentum conservation is used to reduce the set of independent
   Mandelstam invariants in the construction of the amplitude. This option
   can cause problems with numeric stability of the real radiation ampli-
   tudes when the accuracy of the phase space point is bad, i.e. momentum
   conservation is fulfilled to significantly less than double precision.
   In that case it is better to use the full set of Mandelstam invariants,
   without using momentum conservation relations.
   """,
    bool,
    False,
    experimental=True,
)

flavour_groups = Property(
    "flavour_groups",
    """\
   Defines which flavours should be considered equivalent, i.e. grouped
   together during channel generation in olp mode. Only relevant if crossings
   are generated. Uses pdg codes.

   Examples:

   flavour_groups=1:2:3:4:5
   -> completely flavour blind process with five light quark-flavours

   flavour_groups=1:3:5,2:4
   -> distinguish up- and down-type quark-flavours

   flavour_groups=
   -> each flavour treated separately (default)
   """,
    list,
    "",
    experimental=True,
)

respect_generations = Property(
    "respect_generations",
    """\
   Boolean determining whether or not the quark generation should be taken into
   account when the flavour_groups feature is used to find crossing relations among
   olp channels. Is relevant if flavour changing vertices appear (Assuming diagonal CKM!).

   Examples:

   respect_generations=False and flavour_groups=1:3:5,2:4
   -> (c cb to d db) and (u ub to s sb) are crossings of (u ub to d db)

   respect_generations=True and flavour_groups=1:3:5,2:4
   -> (c cb to d db) is a crossing of (u ub to s sb) but not of (u ub to d db)

   Default is respect_generations=False.
   """,
    bool,
    False,
    experimental=True,
)

MSbar_yukawa = Property(
    "MSbar_yukawa",
    """\
    List of quarks with Yukawa couplings which shall be renormalised in the MSbar 
    scheme instead of the default OS scheme. Can also be used to renormalise Yukawa 
    couplings of particles with mass set to zero while still keeping their coupling 
    to the Higgs.

    Examples:
    MSbar_yukawa=B
    -> Yukawa coupling of bottom to Higgs will be renormalised in the MSbar scheme, 
       even if mB=0 (as long as Hbb coupling still exist)

    See also: renorm_yukawa
    """,
     list,
     "",
     experimental=True,
)

use_MQSE = Property(
    "use_MQSE",
    """\
    Whether or not to scan 1-loop amplitudes for massive quark self energies and
    insert the appropriate mass counterterm during the form step. Used mainly for
    debugging purposes.

    """,
     bool,
     False,
     experimental=True,
)

meson_buildtype = Property(
    "meson.buildtype",
    """\
   Build-type passed to meson as the '-Dbuildtype=<buildtype>' option. 
   The respective buildtypes represent:
                           Debug Symbols        Optimization level
      plain                false                plain
      debug                true                 0
      debugoptimized       true                 2
      release              false                3
      minsize              true                 s
   """,
    str,
    default="release",
    options=["plain", "debug", "debugoptimized", "release", "minsize"],
)

meson_arch = Property(
    "meson.arch",
    """\
   CPU architecture passed to the compiler as the '-march=<arch>' option. 
   By default, GCC generates code for a generic x86-64 CPU. When using the
   'native' option, GCC uses all possible instructions available on the 
   currenly used CPU. This can result in faster executing code, but may make
   the libraries / executables unusable on other CPUs. For all possible 
   options, see the GCC documentation.
   """,
    str,
    default="x86-64",
)

unitary_gauge = Property(
    "unitary_gauge",
    """\
   Use unitary gauge propagators for the massive vector bosons instead of 
   Feynman gauge propagators.
    """,
    bool,
    default=False,
)

properties = [
    process_name,
    process_path,
    qgraf_in,
    qgraf_out,
    model,
    model_options,
    qgraf_power,
    zero,
    one,
    renorm,
    sum_helicities,
    regularisation_scheme,
    helicities,
    qgraf_options,
    qgraf_verbatim,
    qgraf_verbatim_lo,
    qgraf_verbatim_nlo,
    sum_diagrams,
    reduction_programs,
    polvec_method,
    extensions,
    debug_flags,
    select_lo_diagrams,
    select_nlo_diagrams,
    select_ct_diagrams,
    filter_lo_diagrams,
    filter_nlo_diagrams,
    filter_ct_diagrams,
    filter_module,
    config_renorm_beta,
    config_renorm_mqwf,
    config_renorm_decoupling,
    config_renorm_mqse,
    config_renorm_logs,
    config_renorm_gamma5,
    config_renorm_yukawa,
    config_renorm_eftwilson,
    config_renorm_ehc,
    config_reduction_interoperation,
    config_reduction_interoperation_rescue,
    config_nlo_prefactors,
    config_PSP_check,
    config_PSP_rescue,
    config_PSP_verbosity,
    config_PSP_chk_th1,
    config_PSP_chk_th2,
    config_PSP_chk_th3,
    config_PSP_chk_kfactor,
    config_PSP_chk_li1,
    config_PSP_chk_li2,
    config_PSP_chk_li3,
    config_PSP_chk_li4,
    config_PSP_chk_method,
    reference_vectors,
    abbrev_color,
    abbrev_limit,
    template_path,
    qgraf_bin,
    form_bin,
    form_threads,
    form_tmp,
    form_workspace,
    r2,
    symmetries,
    crossings,
    formopt_level,
    pyxodraw,
    form_factor_lo,
    form_factor_nlo,
    order_names,
    enable_truncation_orders,
    use_vertex_labels,
    all_mandelstam,
    flavour_groups,
    respect_generations,
    MSbar_yukawa,
    use_MQSE,
    meson_buildtype,
    meson_arch,
    unitary_gauge,
]

REDUCTION_EXTENSIONS = ["golem95", "ninja"]


def getExtensions(conf):
    ext_name = str(extensions)
    ext_set = []

    ext_sets = {}

    for key in conf:
        parts = key.split(".")
        if parts[-1].lower().strip() == ext_name:
            if len(parts) >= 2 and "installed" in parts[0].lower():
                continue
            prefix = ".".join(parts[:-1])
            lst = []
            ext_sets[prefix] = lst
            for s in conf.getListProperty(key, delimiter=","):
                lst.append(s.lower())
            lst.sort()
    keys = sorted(ext_sets.keys())
    for key in keys:
        lst = ext_sets[key]
        for ext in lst:
            if ext not in ext_set:
                ext_set.append(ext)

    return list(ext_set)


def setInternals(conf):
    extensions = getExtensions(conf)
    conf["__INTERNALS__"] = [
        "__GENERATE_DERIVATIVES__",
        "__DERIVATIVES_AT_ZERO__",
        "__REGULARIZATION_DRED__",
        "__REGULARIZATION_HV__",
        "__REQUIRE_FR5__",
        "__GAUGE_CHECK__",
        "__NUMPOLVEC__",
        "__REDUCE_HELICITIES__",
        "__OLP_DAEMON__",
        "__OLP_TRAILING_UNDERSCORE__",
        "__OLP_CALL_BY_VALUE__",
        "__OLP_TO_LOWER__",
        "__OLP_BADPTSFILE_NUMBERING__",
        "__OLP_MODE__",
        "__OLP_BLHA1__",
        "__OLP_BLHA2__",
        "__GENERATE_NINJA_TRIPLE__",
        "__GENERATE_NINJA_DOUBLE__",
        "__CUSTOM_SPIN2_PROP__",
        "__EWCHOOSE__",
    ]

    conf["__GENERATE_DERIVATIVES__"] = "derive" in extensions
    conf["__DERIVATIVES_AT_ZERO__"] = "derive" in extensions

    conf["__GENERATE_NINJA_TRIPLE__"] = "ninja" in extensions
    conf["__GENERATE_NINJA_DOUBLE__"] = "ninja" in extensions

    conf["__CUSTOM_SPIN2_PROP__"] = "customspin2prop" in extensions

    conf["__REGULARIZATION_DRED__"] = "dred" in extensions
    conf["__REGULARIZATION_HV__"] = not "dred" in extensions

    conf["__GAUGE_CHECK__"] = "gaugecheck" in extensions
    conf["__NUMPOLVEC__"] = "numpolvec" in extensions
    conf["__REDUCE_HELICITIES__"] = "generate-all-helicities" not in extensions
    conf["__OLP_DAEMON__"] = "olp_daemon" in extensions
    conf["__OLP_TRAILING_UNDERSCORE__"] = "f77" in extensions
    conf["__OLP_CALL_BY_VALUE__"] = "f77" not in extensions
    conf["__OLP_TO_LOWER__"] = "f77" in extensions
    conf["__OLP_BADPTSFILE_NUMBERING__"] = "olp_badpts" in extensions
    conf["__OLP_BLHA1__"] = "olp_blha1" in extensions
    conf["__OLP_BLHA2__"] = not "olp_blha1" in extensions
    if not "__OLP_MODE__" in conf:
        conf["__OLP_MODE__"] = False

    # conf["__REQUIRE_FR5__"] = "dred" not in extensions \
    #    and "no-fr5" not in extensions
    conf["__REQUIRE_FR5__"] = False
