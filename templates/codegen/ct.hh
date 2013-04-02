[% ' vim:ts=3:sw=3:expandtab:syntax=golem
   '
   '
   '
   '
   '
   '
   '
   '
   ' %]* vim: ts=3:sw=3:expandtab:syntax=form

#procedure ReplaceCT

*Fermionic Counter Term

Id Once  vertex(iv?,
   [field.RENO], idx1?,0,k1?,idx1L0?,+1,idx1C1?,
   [field.RENO], idx2?,0,k2?,idx2L0?,+1,idx2C1?,
   sDUMMY1?, idx3?,+1,k3?,idx3L1?,+3,idx3C3?,
   sDUMMY2?, idx4?,-1,k4?,idx4L1?,-3,idx4C3?)*
   proplorentz(+0,k1?,0,0,+0,idx2L0?,idx1L0?)*
   propcolor(+1,idx2C1?,idx1C1?)
   = d_(idx3L1,idx4L1)*d_(idx3C3,idx4C3)*deltaM(sDUMMY1);

#EndProcedure

