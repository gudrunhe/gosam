* vim: ts=3:sw=3
CFunction dcolor(symmetric), dcolor8(symmetric);

#procedure colorlibrary
* Precomputed rules for certain common combinations of generators
        Repeat;
                 Id Once f(idx1C8?,idx3C8?,idx4C8?)*f(idx2C8?,idx4C8?,idx3C8?) =
		        - 2*NC*T(idx1C8,iDUMMY1,iDUMMY2)*T(idx2C8,iDUMMY2,iDUMMY1);
                 Sum iDUMMY1, iDUMMY2;
        EndRepeat;
* Star-Triangle relation f-f-f
	Id f(idx1C8?,idx4C8?,idx5C8?)*
			f(idx2C8?,idx5C8?,idx6C8?)*
			f(idx3C8?,idx6C8?,idx4C8?) =
		TR * NC * f(idx1C8,idx2C8,idx3C8);
* Star-Triangle relation f-T-T
	Id T(idx1C8?, idx1C3?, idx3C3?) *
			T(idx2C8?, idx3C3?, idx2C3?) *
			f(idx1C8?,idx2C8?,idx3C8?) =
		T(idx3C8,idx1C3,idx2C3)*i_*TR*NC;
* Star-Triangle relation T-T-T
	Id T(idx1C8, idx1C3, idx2C3) *
			T(idx2C8, idx2C3, idx3C3) *
			T(idx1C8,idx3C3,idx4C3) =
		- T(idx2C8,idx1C3,idx4C3)*TR/NC;
#endprocedure

#procedure liealgebra
	Repeat;
		Id Once f(idx1C8?, idx2C8?, idx3C8)*T(idx3C8?, idx1C3?, idx2C3?) =
	   	- T(idx1C8,idx1C3,iDUMMY1)*T(idx2C8,iDUMMY1,idx2C3)*i_
			+ T(idx1C8,iDUMMY1,idx2C3)*T(idx2C8,idx1C3,iDUMMY1)*i_;
		Sum iDUMMY1;
	EndRepeat;
#endprocedure

#procedure coloralgebra(INPAR)
*   Brackets f4, f;
.sort:coloralgebra first;
*   Keep Brackets;

   #if `INPAR'
	   InParallel;
	#endif
   Repeat;
      Id Once dcolor8(idx1C8?, idx2C8?) =
         T(idx1C8,iDUMMY1,iDUMMY2)*T(idx2C8,iDUMMY2,iDUMMY1)/TR;
      Sum iDUMMY1, iDUMMY2;
   EndRepeat;
	Repeat;
		Id Once f4(idx1C8?, idx2C8?, idx3C8?, idx4C8?) =
			f(idx1C8, idx2C8, iDUMMY1) *
			f(idx3C8, idx4C8, iDUMMY1);

		Sum iDUMMY1;
	EndRepeat;

	#call colorlibrary
	#call liealgebra

	Repeat;
		Id Once f(idx1C8?, idx2C8?, idx3C8?) = - i_ / TR * 
			(
				+ T(idx1C8, iDUMMY1, iDUMMY2) *
				  T(idx2C8, iDUMMY2, iDUMMY3) *
				  T(idx3C8, iDUMMY3, iDUMMY1)
				- T(idx3C8, iDUMMY1, iDUMMY2) *
				  T(idx2C8, iDUMMY2, iDUMMY3) *
				  T(idx1C8, iDUMMY3, iDUMMY1)
			);
		Sum iDUMMY1, iDUMMY2, iDUMMY3;

		#call liealgebra
	EndRepeat;

* Before we go on we need to be sure that the T_ij have their
* indices in the correct order.
   #If "X`INIFUNDAMENTAL'X" != "XX"
      #Do ic={`INIFUNDAMENTAL',}
         Id inpcolor(`ic', idx1C3?) * T(idx2C8?, idx1C3?, idx3C3?) =
				inpcolor(`ic', idx1C3) * fDUMMY1(idx2C8, idx1C3, idx3C3);
         Id inpcolor(`ic', idx1C3?) * T(idx2C8?, idx3C3?, idx1C3?) =
				inpcolor(`ic', idx1C3) * fDUMMY1(idx2C8, idx1C3, idx3C3);
      #EndDo
   #EndIf
   #If "X`FINFUNDAMENTAL'X" != "XX"
      #Do ic={`FINFUNDAMENTAL',}
         Id outcolor(`ic', idx1C3?) * T(idx2C8?, idx1C3?, idx3C3?) =
				outcolor(`ic', idx1C3) * fDUMMY1(idx2C8, idx1C3, idx3C3);
         Id outcolor(`ic', idx1C3?) * T(idx2C8?, idx3C3?, idx1C3?) =
				outcolor(`ic', idx1C3) * fDUMMY1(idx2C8, idx1C3, idx3C3);
      #EndDo
   #EndIf

   Repeat;
		Id fDUMMY1(idx1C8?, idx2C3?, idx3C3?) * T(idx4C8?, idx3C3?, idx5C3?) =
			T(idx1C8, idx2C3, idx3C3) * fDUMMY1(idx4C8, idx3C3, idx5C3);
		Id fDUMMY1(idx1C8?, idx2C3?, idx3C3?) * T(idx4C8?, idx5C3?, idx3C3?) =
			T(idx1C8, idx2C3, idx3C3) * fDUMMY1(idx4C8, idx3C3, idx5C3);
   EndRepeat;
	Id fDUMMY1(idx1C8?, idx2C3?, idx3C3?) = T(idx1C8, idx2C3, idx3C3);

	Repeat;
		Id T(idx0C8?, idx1C3?, idx1C3?) = 0;

                Id dcolor(idx1C3?, idx0C3?) * dcolor(idx0C3?, idx2C3?) =
			dcolor(idx1C3, idx2C3);

		Id dcolor(idx1C3?, idx0C3?) * T(idx3C8?, idx0C3?, idx2C3?) =
			T(idx3C8, idx1C3, idx2C3);
		Also T(idx3C8?, idx1C3?, idx0C3?) * dcolor(idx0C3?, idx2C3?) =
			T(idx3C8, idx1C3, idx2C3);
		Also dcolor(idx1C3?, idx1C3?) = NC;

		Id T(idx0C8?, idx1C3?, idx2C3?) * T(idx0C8?, idx3C3?, idx4C3?) =
			TR * (
				+ dcolor(idx1C3, idx4C3) * dcolor(idx2C3, idx3C3)
				- 1/NC * dcolor(idx1C3, idx2C3) * dcolor(idx3C3, idx4C3)
			);
	EndRepeat;

	Id dcolor(idx1C3?, idx2C3?) = d_(idx1C3, idx2C3);

*   Brackets inpcolor, outcolor, T, delta, dcolor;
.sort:coloralgebra last;
*   Keep Brackets;
	#call colorbasis
#endprocedure
