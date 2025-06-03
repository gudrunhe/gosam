


include ../Makefile.conf

pc17_gghh_CFLAGS= \
		-I../pc17_gghh/helicity0/ \
		-I../pc17_gghh/matrix/ \
		-I../pc17_gghh/common/

pc17_gghh_LDFLAGS=$(shell ${SHELL} ../pc17_gghh/config.sh -plibs)

pc17_gghh_DEPS=$(shell ${SHELL} ../pc17_gghh/config.sh -deps)

pc17_gghh_OBJECTS=../pc17_gghh/matrix/matrix.o


pc16_gghh_CFLAGS= \
		-I../pc16_gghh/helicity0/ \
		-I../pc16_gghh/matrix/ \
		-I../pc16_gghh/common/

pc16_gghh_LDFLAGS=$(shell ${SHELL} ../pc16_gghh/config.sh -plibs)

pc16_gghh_DEPS=$(shell ${SHELL} ../pc16_gghh/config.sh -deps)

pc16_gghh_OBJECTS=../pc16_gghh/matrix/matrix.o



pb0_gghh_CFLAGS= \
		-I../pb0_gghh/helicity0/ \
		-I../pb0_gghh/matrix/ \
		-I../pb0_gghh/common/

pb0_gghh_LDFLAGS=$(shell ${SHELL} ../pb0_gghh/config.sh -plibs)

pb0_gghh_DEPS=$(shell ${SHELL} ../pb0_gghh/config.sh -deps)

pb0_gghh_OBJECTS=../pb0_gghh/matrix/matrix.o


pb1_gghh_CFLAGS= \
		-I../pb1_gghh/helicity0/ \
		-I../pb1_gghh/matrix/ \
		-I../pb1_gghh/common/

pb1_gghh_LDFLAGS=$(shell ${SHELL} ../pb1_gghh/config.sh -plibs)

pb1_gghh_DEPS=$(shell ${SHELL} ../pb1_gghh/config.sh -deps)

pb1_gghh_OBJECTS=../pb1_gghh/matrix/matrix.o



pt18_gghh_CFLAGS= \
		-I../pt18_gghh/helicity0/ \
		-I../pt18_gghh/matrix/ \
		-I../pt18_gghh/common/

pt18_gghh_LDFLAGS=$(shell ${SHELL} ../pt18_gghh/config.sh -plibs)

pt18_gghh_DEPS=$(shell ${SHELL} ../pt18_gghh/config.sh -deps)

pt18_gghh_OBJECTS=../pt18_gghh/matrix/matrix.o


pt19_gghh_CFLAGS= \
		-I../pt19_gghh/helicity0/ \
		-I../pt19_gghh/matrix/ \
		-I../pt19_gghh/common/

pt19_gghh_LDFLAGS=$(shell ${SHELL} ../pt19_gghh/config.sh -plibs)

pt19_gghh_DEPS=$(shell ${SHELL} ../pt19_gghh/config.sh -deps)

pt19_gghh_OBJECTS=../pt19_gghh/matrix/matrix.o



.PHONY: pt19_gghh_test.exe pt18_gghh_test.exe clean very-clean
.SUFFIXES:



pt19_gghh_test.o:%.o:%.f90
		$(vecho) "-> Compiling $@ .."
		$(Q) $(FC) $(FC_OPTS) $(pc16_gghh_CFLAGS) $(pb1_gghh_CFLAGS) $(pt19_gghh_CFLAGS) $(FCFLAGS) -c -o $@ $<

ph_pt19_gghh_test.o:%.o:%.f
		$(vecho) "-> Compiling $@ .."
		$(Q) $(FC) $(FC_OPTS) $(pc16_gghh_CFLAGS) $(pb1_gghh_CFLAGS) $(pt19_gghh_CFLAGS) $(FCFLAGS) -c -o $@ $<

pt19_gghh_test.exe: pt19_gghh_test.o $(pc16_gghh_OBJECTS) $(pc16_gghh_DEPS) $(pb1_gghh_OBJECTS) $(pb1_gghh_DEPS) $(pt19_gghh_OBJECTS) $(pt19_gghh_DEPS)
		$(vecho) "-> Creating executable $@ .."
		$(Q) $(FC) -o $@ $+ $(pc16_gghh_LDFLAGS) $(pb1_gghh_LDFLAGS) $(pt19_gghh_LDFLAGS) $(LDFLAGS)




pt18_gghh_test.o:%.o:%.f90
		$(vecho) "-> Compiling $@ .."
		$(Q) $(FC) $(FC_OPTS) $(pb0_gghh_CFLAGS) $(pc17_gghh_CFLAGS) $(pt18_gghh_CFLAGS) $(FCFLAGS) -c -o $@ $<

ph_pt18_gghh_test.o:%.o:%.f
		$(vecho) "-> Compiling $@ .."
		$(Q) $(FC) $(FC_OPTS) $(pc17_gghh_CFLAGS) $(pb0_gghh_CFLAGS) $(pt18_gghh_CFLAGS) $(FCFLAGS) -c -o $@ $<

pt18_gghh_test.exe: pt18_gghh_test.o $(pc17_gghh_OBJECTS) $(pc17_gghh_DEPS) $(pb0_gghh_OBJECTS) $(pb0_gghh_DEPS) $(pt18_gghh_OBJECTS) $(pt18_gghh_DEPS)
		$(vecho) "-> Creating executable $@ .."
		$(Q) $(FC) -o $@ $+ $(pc17_gghh_LDFLAGS) $(pb0_gghh_LDFLAGS) $(pt18_gghh_LDFLAGS) $(LDFLAGS)



clean:
	$(Q)rm -f *.o *.mod *.exe


very-clean: clean
	$(Q)rm -f filelist-source
