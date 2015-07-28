# vim: ts=3:sw=3:expandtab
import sys, getopt, os
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
   formfile = ''
   try:
      opts, args = getopt.getopt(argv,"hi:",["ifile="])
   except getopt.GetoptError:
      print 'test.py -i <inputfile>'
      sys.exit(2)
   for opt, arg in opts:
      if opt == '-h':
         print 'test.py -i <inputfile>'
         sys.exit()
      elif opt in ("-i", "--ifile"):
         inputfile = arg
  
   try:
      in_file = open(inputfile + ".log", 'r')
      fout_file = open(inputfile + ".hh", 'w')
      if not os.path.isdir(inputfile):
         os.makedirs(inputfile)
      
      # Build list of integrals
      with in_file as myfile:
         integrals = myfile.read().replace('\n','').replace(' ','')
         integrals = integrals.replace("PropVec","")
         intlist= integrals.split("+INT")
         for line in intlist:
            line = line.strip()
            if line:
               linelist = line.split("[]")
               if len(linelist) != 5:
                  raise TermError("Term: " + str(line) + ", does not consist of an integral and a familiy in " + inputfile + ".log")
               family = linelist[0].strip('( ,')
               tidrs = linelist[1].strip(' ,')
               integral = linelist[2].strip(' ,')
               order = linelist[3].strip(' ,')
               props = linelist[4].replace(',PropList(','').strip(') ')
#               if linelist[1].count(",1") >= 7:
#                  if int(order) == 0:
#                     print linelist
               mypowerlist = integral.split(",")
               intt = 0
               intr = 0
               ints = 0
               for pow in mypowerlist:
                  if int(pow) > 0:
                     intt+= 1
                     intr+= int(pow)
                  else:
                     ints-= int(pow)
               graph = family + "pow" + integral.strip(', ').replace(',','').replace('-','m')
               moutputfile = os.path.join(inputfile, graph + ".m")
               poutputfile = os.path.join(inputfile, graph + ".input")
               proplist = "proplist = {" + props + "};"
               numerator = "numerator = {1};"
               powerlist = "powerlist = {" + integral + "};"
               # write math file
               copyfile(inputfile + ".m",moutputfile)
               mout_file = open(moutputfile, 'a')
               mout_file.write(proplist + '\n')
               mout_file.write(numerator + '\n')
               mout_file.write(powerlist + '\n')
               mout_file.close()
               # write prep file
               copyfile(inputfile + ".input",poutputfile)
               pout_file = open(poutputfile, 'a')
               pout_file.write("graph=" + graph + '\n')
               pout_file.write("epsord=" + order + '\n')
               pout_file.close()
               fout_file.write("Id INT(" + family + "," + tidrs + ",[]," + integral + ") = " + family + "pow" + integral.replace(',','').replace('-','m') +  ";\n")
         fout_file.write('\n')
         #out_file.write(integrals)

   except IOError as ex:
      print "Error in tosecdec.py: ", ex
      sys.exit(3)
   except TermError as ex:
      print "Error in tosecdec.py: ", ex
      sys.exit(4)

   else:
      in_file.close()
      fout_file.close()

if __name__ == "__main__":
   main(sys.argv[1:])

