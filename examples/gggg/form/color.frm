* In Ref. [1] (see README) the amplitude is expressed in terms of the
* four traces T_{ad}^{1234}, T_{ad}^{1324} and T_{ad}^{1342}, where
* T_{ad}^{ijkl} = tr{T^i T^j T^k T^l}, T^a_{bc} = i f^{abc}
*
* In order to compute the squared amplitude we need to know the
* color correlation matrix. We use
*
* c1 = T_{ad}^{1234}
* c2 = T_{ad}^{1324}
* c3 = T_{ad}^{1342}

Indices i1,i2,i3,i4;
Indices j1,j2,j3,j4;
CTensor Tad(cyclic), f(antisymmetric), t, d(symmetric);
Symbols TR, NC, NA, CF, CA;

.global

Global CC11 = Tad(i1,i2,i3,i4) * Tad(i1,i2,i3,i4);
Global CC12 = Tad(i1,i2,i3,i4) * Tad(i1,i3,i2,i4);
Global CC13 = Tad(i1,i2,i3,i4) * Tad(i1,i3,i4,i2);
Global CC22 = Tad(i1,i3,i2,i4) * Tad(i1,i3,i2,i4);
Global CC23 = Tad(i1,i3,i2,i4) * Tad(i1,i3,i4,i2);
Global CC33 = Tad(i1,i3,i4,i2) * Tad(i1,i3,i4,i2);

Sum i1,i2,i3,i4;
* Here we already see that CC11=CC22=CC33 and C12=C23.
.sort

Repeat;
   Id once Tad(i1?, i2?, i3?, i4?) = 
      f(i1,j1,j2)*f(i2,j2,j3)*f(i3,j3,j4)*f(i4,j4,j1);
   Sum j1,j2,j3,j4;
EndRepeat;

Repeat;
   Id once f(i1?, i2?, i3?) = (-i_)/TR * (
   	+ t(i1, j1, j2) * t(i2, j2, j3) * t(i3, j3, j1)
   	- t(i3, j1, j2) * t(i2, j2, j3) * t(i1, j3, j1)
   );
   Sum j1,j2,j3;

   Repeat;
      Id once f(i1?, i2?, i3?) * t(i3?, j1?, j2?) = -i_ *
      (
         + t(i1, j1, j3) * t(i2, j3, j2)
	 - t(i2, j1, j3) * t(i1, j3, j2)
      );
      Sum j3;
   EndRepeat;
EndRepeat;

.sort

Repeat;
   Id t(i1?, j1?, j2?) * t(i1?, j3?, j4?) = TR * (
      d(j1,j4) * d(j3,j2) - 1/NC * d(j1,j2) * d(j3,j4)
   );

   Repeat;
      Id d(j1?,j4?) * t(i1?,j1?,j2?) = t(i1,j4,j2);
      Id d(j2?,j4?) * t(i1?,j1?,j2?) = t(i1,j1,j4);
      Id d(j1?,j2?) * d(j2?, j3?) = d(j1,j3);
      Id d(j1?,j1?) = NC;
   EndRepeat;
EndRepeat;

Repeat Id NC^2 = NA + 1;
Id TR^4*NA = dum_(2*TR^4*NA)/2;
Brackets dum_;
.sort
Collect dum_;
Id dum_(12 + 12*NA ) = 12 * dum_(NA + 1);
Id dum_(13 + 14*NA + NA^2) = dum_(NA+13) * dum_(NA+1);

Id dum_(NA+1) = dum_(NC*NC);
Id dum_(NA+13) = NC*NC+12;

Brackets dum_;
Print;

* The output is as follows
*  CC11 = (2*TR^4*NA)*NC^2 * (NC^2 + 12);
*  CC12 = (2*TR^4*NA)*NC^2 * 12;
*  CC13 = (2*TR^4*NA)*NC^2 * 12;
*  CC22 = (2*TR^4*NA)*NC^2 * (NC^2 + 12);
*  CC23 = (2*TR^4*NA)*NC^2 * 12;
*  CC33 = (2*TR^4*NA)*NC^2 * (NC^2 + 12);
*  Hence we can write
*
*                         { (NA + 13)      12         12    }
*  CC = 2*TR^4*NA*NC^2 *  {     12     (NA + 13)      12    }
*                         {     12         12     (NA + 13) }
.end
