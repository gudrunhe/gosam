# vim: ts=3:sw=3:expandtab
import sys, getopt
from string import maketrans

def main(argv):
   inputfile = ''
   outputfile = ''
   try:
      opts, args = getopt.getopt(argv,"hi:o:",["ifile=","ofile="])
   except getopt.GetoptError:
      print 'test.py -i <inputfile> -o <outputfile>'
      sys.exit(2)
   for opt, arg in opts:
      if opt == '-h':
         print 'test.py -i <inputfile> -o <outputfile>'
         sys.exit()
      elif opt in ("-i", "--ifile"):
         inputfile = arg
      elif opt in ("-o", "--ofile"):
         outputfile = arg
   #print 'Input file is "' + inputfile + '"'
   #print 'Output file is "' + outputfile + '"'
  
   try:
      in_file = open(inputfile, 'r')
      out_file = open(outputfile, 'w')

      # Build list of integrals
      with in_file as myfile:
         integrals = myfile.read().replace('\n','').replace("INT",'\n').strip()
         translate_in = ","
         translate_out = " "
         translate_table = maketrans(translate_in,translate_out)
         integrals = integrals.translate(translate_table," +()[]")
         #print integrals
         out_file.write(integrals)

   except IOError as ex:
         print "Error in toreduze.py: ", ex
         sys.exit(3)

   else:
      in_file.close()
      out_file.close()

if __name__ == "__main__":
   main(sys.argv[1:])

