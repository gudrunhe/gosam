# vim: ts=3:sw=3:expandtab
import sys, getopt
from shutil import copyfile

class TermError(Exception):
   def __init__(self, value):
      self.value = value
   def __str__(self):
      return repr(self.value)

def main(argv):
   inputfile = ''
   mprependfile = ''
   pprependfile = ''
   try:
      opts, args = getopt.getopt(argv,"hi:p:m:",["ifile=","mfile=","pfile="])
   except getopt.GetoptError:
      print 'test.py -i <inputfile> -m <mathprependfile> -p <paramprependfile>'
      sys.exit(2)
   for opt, arg in opts:
      if opt == '-h':
         print 'test.py -i <inputfile> -m <mathprependfile> -p <paramprependfile>'
         sys.exit()
      elif opt in ("-i", "--ifile"):
         inputfile = arg
      elif opt in ("-m", "--mfile"):
         mprependfile = arg
      elif opt in ("-p", "--mfile"):
         pprependfile = arg
  
   try:
      in_file = open(inputfile, 'r')

      # Build list of integrals
      with in_file as myfile:
         integrals = myfile.read().replace('\n','').replace(' ','')
         integrals = integrals.replace("PropVec","")
         intlist= integrals.split("+INT")
         for line in intlist:
            line = line.strip()
            if line:
               linelist = line.split("[]")
               print linelist
               if len(linelist) != 4:
                  raise TermError("Term: " + str(line) + ", does not consist of an integral and a familiy in " + inputfile)
               family = linelist[0].strip('( ,')
               integral = linelist[1].strip(' ,')
               order = linelist[2].strip(' ,')
               props = linelist[3].replace(',PropList(','').strip('() ')
               graph = family + "_" + integral.strip(', ').replace(',','').replace('-','m')
               moutputfile = graph + ".m"
               poutputfile = graph + ".input"
               proplist = "proplist = {" + props + "};"
               numerator = "numerator = {1};"
               powerlist = "powerlist = {" + integral + "};"
               # write math file
               copyfile(mprependfile,moutputfile)
               mout_file = open(moutputfile, 'a')
               mout_file.write(proplist + '\n')
               mout_file.write(numerator + '\n')
               mout_file.write(powerlist + '\n')
               mout_file.close()
               # write prep file
               copyfile(pprependfile,poutputfile)
               pout_file = open(poutputfile, 'a')
               pout_file.write("graph=" + graph + '\n')
               pout_file.write("epsord=" + order + '\n')
         #out_file.write(integrals)

   except IOError as ex:
      print "Error in tosecdec.py: ", ex
      sys.exit(3)
   except TermError as ex:
      print "Error in tosecdec.py: ", ex
      sys.exit(4)

   else:
      in_file.close()

if __name__ == "__main__":
   main(sys.argv[1:])

