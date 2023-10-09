# vim: ts=3:sw=3:expandtab
import golem.installation

PATTERN_DIAGRAMS_LO = "diagrams-0"
PATTERN_DIAGRAMS_CT = "diagrams-ct"
PATTERN_DIAGRAMS_NLO_VIRT = "diagrams-1"

PATTERN_PYXO_LO = "pyxotree"
PATTERN_PYXO_CT = "pyxoct"
PATTERN_PYXO_NLO_VIRT = "pyxovirt"

PATTERN_TOPOLOPY_LO = "topotree"
PATTERN_TOPOLOPY_CT = "topoct"
PATTERN_TOPOLOPY_VIRT = "topovirt"

AUTHORS = {
      "Gudrun Heinrich": ["gudrun@mpp.mpg.de"],
      "Stephen Jones": ["s.jones@cern.ch"],                 
      "Matthias Kerner": ["mkerner@physik.uzh.ch"],           
      "Jannis Lang": ["jannis.lang@kit.edu"],
      "Vitaly Magerya": ["vitaly.magerya@tx97.net"],         
      "Pierpaolo Mastrolia": ["Pierpaolo.Mastrolia@cern.ch"],
      "Giovanni Ossola": ["gossola@citytech.cuny.edu"],
      "Tiziano Peraro": ["peraro@mpp.mpg.de"],
      "Johannes Schlenk": ["johannes.schlenk@psi.ch"],
      "Ludovic Scyboz": ["ludovic.scyboz@physics.ox.ac.uk"],
      "Francesco Tramontano": ["Francesco.Tramontano@cern.ch"],
}

FORMER_AUTHORS = {
      "Gavin Cullen": ["gavin.cullen@desy.de"],
      "Hans van Deurzen": ["hdeurzen@mpp.mpg.de"],
      "Nicolas Greiner": ["greiner@mpp.mpg.de"],
      "Stephan Jahn": ["sjahn@mpp.mpg.de"],
      "Gionata Luisoni": ["luisonig@mpp.mpg.de"],
      "Edoardo Mirabella": ["mirabell@mpp.mpg.de"],
      "Joscha Reichel": ["joscha@mpp.mpg.de"],
      "Thomas Reiter": ["reiterth@mpp.mpg.de"],
      "Johann Felix von Soden-Fraunhofen": ["jfsoden@mpp.mpg.de"]
}


LICENSE = [
"",
"  This program is free software: you can redistribute it and/or modify",
"  it under the terms of the GNU General Public License either",
"  version 3, or (at your option) any later version.",
"",
#"  This program is distributed in the hope that it will be useful,",
#"  but WITHOUT ANY WARRANTY; without even the implied warranty of",
#"  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the",
#"  GNU General Public License for more details.",
#"",
#"  You should have received a copy of the GNU General Public License",
#"  along with this program.  If not, see http://www.gnu.org/licenses/.",
#"",
"  Scientific publications prepared using the present version of",
"  GoSam or any modified version of it or any code linking to GoSam",
"  or parts of it should make a clear reference to the publication:",
"",
"      G. Cullen et al.,",
"      ``GoSam-2.0: a tool for automated one-loop calculations",
"                        within the Standard Model and Beyond'',",
"      Eur. Phys. J. C 74 (2014) 8,  3001",
"      [arXiv:1404.7096 [hep-ph]]."

]

SCATTER_ASCIIART = [
   r'             \         . . . .   ',
   r'              \       . . .      ',
   r'               \     . .         ',
   r'                \   .            ',
   r'                 * *             ',
   r'     ====>>==== * * * ====<<==== ',
   r'                 * *             ',
   r'                .   \            ',
   r'             . .     \           ',
   r'          . . .       \          ',
   r'       . . . .         \         ']

GOLEM_ASCIIART = [
            r'   /==#==\   ',
            r'   | . . |   ',
            r' >-+ ~~~ +-< ',
            r'   |     |   ',
            r'  <__/~\__>  '
      ]

serifcap_asciiart = [
   r'  __   __   ___   __   __  __ ',
   r' / _) /  \ / __) (  ) (  \/  )',
   r'( (/\( () )\__ \ /__\  )    ( ',
   r' \__/ \__/ (___/(_)(_)(_/\/\_)']




ASCIIART = serifcap_asciiart

CLINES = [
            'GoSam',
            'An Automated One-Loop',
            'Matrix Element Generator',
            'Version %s Rev: %s' %
              ( ".".join(map(str,golem.installation.GOLEM_VERSION)),
                golem.installation.GOLEM_REVISION),
            '',
            '(c) The GoSam Collaboration 2011-2021',
            ''
      ]

MODEL_LOCAL = "model"

GOLEM_DIR_FILE_NAME = ".golem.dir"
