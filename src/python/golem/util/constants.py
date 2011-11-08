# vim: ts=3:sw=3:expandtab
import golem.installation

generate_gauge_var = True

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
            'Version %s' % 
               ".".join(map(str,golem.installation.GOLEM_VERSION)),
            '',
            '(c) The GoSam Collaboration 2011',
            ''
      ]

MODEL_LOCAL = "model"

GOLEM_DIR_FILE_NAME = ".golem.dir"
