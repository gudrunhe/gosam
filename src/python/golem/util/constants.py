# vim: ts=3:sw=3:expandtab
import golem.installation

AUTHORS = {
    "Jens Braun": ["jens.braun2@.kit.edu"],
    "Benjamin Campillo Aveleira": ["benjamin.campillo@kit.edu"],
    "Gudrun Heinrich": ["gudrun.heinrich@kit.edu"],
    "Marius Hoefer": ["marius.hoefer@kit.edu"],
    "Stephen Jones": ["stephen.jones@durham.ac.uk"],
    "Matthias Kerner": ["matthias.kerner@kit.edu"],
    "Jannis Lang": ["jannis.lang@partner.kit.edu"],
    "Vitaly Magerya": ["vitaly.magerya@tx97.net"]
}

FORMER_AUTHORS = {
    "Gavin Cullen": ["gavin.cullen@desy.de"],
    "Hans van Deurzen": ["hdeurzen@mpp.mpg.de"],
    "Nicolas Greiner": ["greiner@mpp.mpg.de"],
    "Stephan Jahn": ["sjahn@mpp.mpg.de"],
    "Gionata Luisoni": ["luisonig@mpp.mpg.de"],
    "Pierpaolo Mastrolia": ["Pierpaolo.Mastrolia@cern.ch"],
    "Edoardo Mirabella": ["mirabell@mpp.mpg.de"],
    "Giovanni Ossola": ["gossola@citytech.cuny.edu"],
    "Tiziano Peraro": ["peraro@mpp.mpg.de"],
    "Joscha Reichel": ["joscha@mpp.mpg.de"],
    "Thomas Reiter": ["reiterth@mpp.mpg.de"],
    "Johannes Schlenk": ["johannes.schlenk@psi.ch"],
    "Ludovic Scyboz": ["ludovic.scyboz@physics.ox.ac.uk"],
    "Johann Felix von Soden-Fraunhofen": ["jfsoden@mpp.mpg.de"],
    "Francesco Tramontano": ["Francesco.Tramontano@cern.ch"],
}


LICENSE = [
    "",
    "  This program is free software: you can redistribute it and/or modify",
    "  it under the terms of the GNU General Public License either",
    "  version 3, or (at your option) any later version.",
    "",
    # "  This program is distributed in the hope that it will be useful,",
    # "  but WITHOUT ANY WARRANTY; without even the implied warranty of",
    # "  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the",
    # "  GNU General Public License for more details.",
    # "",
    # "  You should have received a copy of the GNU General Public License",
    # "  along with this program.  If not, see http://www.gnu.org/licenses/.",
    # "",
    "  Scientific publications using GoSam or any modified version of",
    "  it or any code linking to GoSam or parts of it should make a clear",
    "  reference to the publications:",
    "",
    "      G. Cullen et al.,",
    "      ``Automated One-Loop Calculations with GoSam'',",
    "      Eur. Phys. J. C 72 (2012), 1889",
    "      [arXiv:1111.2034 [hep-ph]].",
    "",
    "      G. Cullen et al.,",
    "      ``GoSam-2.0: a tool for automated one-loop calculations",
    "        within the Standard Model and Beyond'',",
    "      Eur. Phys. J. C 74 (2014) 8,  3001",
    "      [arXiv:1404.7096 [hep-ph]].",
    "",
    "      J. Braun et al.,",
    "      ``One-Loop Calculations in Effective Field Theories",
    "        with GoSam-3.0'',",
    "      [arXiv:2507.23549 [hep-ph]].",
]

SCATTER_ASCIIART = [
    r"             \         . . . .   ",
    r"              \       . . .      ",
    r"               \     . .         ",
    r"                \   .            ",
    r"                 * *             ",
    r"     ====>>==== * * * ====<<==== ",
    r"                 * *             ",
    r"                .   \            ",
    r"             . .     \           ",
    r"          . . .       \          ",
    r"       . . . .         \         ",
]

GOLEM_ASCIIART = [r"   /==#==\   ", r"   | . . |   ", r" >-+ ~~~ +-< ", r"   |     |   ", r"  <__/~\__>  "]

serifcap_asciiart = [
    r"  __   __   ___   __   __  __ ",
    r" / _) /  \ / __) (  ) (  \/  )",
    r"( (/\( () )\__ \ /__\  )    ( ",
    r" \__/ \__/ (___/(_)(_)(_/\/\_)",
]


ASCIIART = serifcap_asciiart

CLINES = [
    "GoSam",
    "An Automated One-Loop",
    "Matrix Element Generator",
    "Version %s Rev: %s" % (".".join(map(str, golem.installation.GOLEM_VERSION)), golem.installation.GOLEM_REVISION),
    "",
    "(c) The GoSam Collaboration 2011-2025",
    "",
]

MODEL_LOCAL = "model"

GOLEM_DIR_FILE_NAME = ".golem.dir"
