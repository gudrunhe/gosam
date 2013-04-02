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
      "Thomas Reiter": ["reiterth@mpp.mpg.de"],
      "Giovanni Ossola": ["gossola@citytech.cuny.edu"],
      "Francesco Tramontano": ["francesco.tramontano@cern.ch"],
      "Pierpaolo Mastrolia": ["pierpaolo.mastrolia@cern.ch"],
      "Gudrun Heinrich": ["gudrun@mpp.mpg.de"],
      "Nicolas Greiner": ["greiner@mpp.mpg.de"],
      "Gavin Cullen": ["gavin.cullen@desy.de"],
      "Gionata Luisoni": ["gionata.luisoni@durham.ac.uk"]
}

LICENSE = [
"",
"",
"    This program is free software: you can redistribute it and/or modify",
"    it under the terms of the GNU General Public License as published by",
"    the Free Software Foundation, either version 3 of the License, or",
"    (at your option) any later version.",
"",
"    This program is distributed in the hope that it will be useful,",
"    but WITHOUT ANY WARRANTY; without even the implied warranty of",
"    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the",
"    GNU General Public License for more details.",
"",
"    You should have received a copy of the GNU General Public License",
"    along with this program.  If not, see <http://www.gnu.org/licenses/>.",
"",
"    Scientific publications prepared using the present version of",
"    GoSam or any modified version of it or any code linking to",
"    GoSam or parts of it should make a clear reference to the publication:",
"",
"        G. Cullen et al.,",
"        ``Automated One-Loop Calculations with GoSam'',",
"        arXiv:1111.2034 [hep-ph]"
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
            '(c) The GoSam Collaboration 2011-2013',
            ''
      ]

MODEL_LOCAL = "model"

GOLEM_DIR_FILE_NAME = ".golem.dir"
