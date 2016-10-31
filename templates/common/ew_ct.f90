[%' vim: syntax=golem
'%]module     [% process_name asprefix=\_ %]_ew_ct  
      implicit none
      complex*16, dimension(1:2) :: ddrr
contains
      
      
      subroutine ew_ren()
      implicit none
      integer i1,i2,i3
      complex*16 sw,cw,sw2,cw2,sw4,cw4,alpha,el2,alsu4pi
      common/couplings/sw,sw2,sw4,cw,cw2,cw4,alpha,el2,alsu4pi

      real*8 vv(1:3)

      real*8 deltauv,mudim,dimf1,dimf2,eulergamma
      common/dimreg/deltauv,mudim,dimf1,dimf2,eulergamma
      complex*16 cone,zero,ii
      common/complexunit/cone,zero,ii
      logical masslesswf,dred
      common/ewoptions/masslesswf,dred
      logical noqed
      common/qedswitch/noqed
      complex*16 bbe0,bbe1,inte0,inte1,inte2
      complex*16 ct(0:1)
      real*8 born0,born1,oldres0,oldres1,sommaoo0,sommaoo1
      real*8 sommatt0,sommatt1,sommann0,sommann1,dxxll(0:1),dxxrr(0:1)
      real*8 dttll(0:1),dttrr(0:1),dnnll(0:1),dnnrr(0:1)
      real*8 deltatestll,deltatestrr,norn(1:9)
      logical debug
      parameter(debug=.false.)
      complex*16 coeff
      common/cmscoeff/coeff(2)
      save  /cmscoeff/
      real*8 ss,scale
      real*8 pi,pis
      common/pigreco/pi,pis
      save /deltas/
      integer ini
      data ini/0/
      save ini
      include 'dzdecl.h'
      !include 'ddrrdecl.h'
      include 'declmasses.h'
      mudim=1d0
!      mudim=1d0!scale
!      ss=1358478.9134523999d0!70d0
      if(ini.eq.0) then
         ini=1
         call init
         call init_scalars
         call delta_z
         call computectcoeff
         if(dred) then
            write(*,*)'dred ct'
         else
            write(*,*)'cdr ct'
         endif
         write(*,*)'********************************************'
         write(*,*)'********************************************'
         write(*,*)'***                                      ***'
         write(*,*)'***   LO=gs**2 * amp(4)                  ***'
         write(*,*)'***  NLO=gs**2 * amp(3) * alpha_elm/2/pi ***'
         write(*,*)'***   (stands for 2 re M_1*M_0           ***'
         write(*,*)'***                                      ***'
         write(*,*)'********************************************'
         write(*,*)'********************************************'
         coeff(1)=ddmw2(1)
         coeff(2)=ddmw2(2)
      endif
!       ct(0) = 0.5d0*ddzul(1)+0.5d0*ddzdl( 1) &
!              +0.5d0*ddzel(1)+0.5d0*ddznel(1) &
!              +ddee( 1) -ddswsw(1) -0.5d0*ddrr(1) &
!              +ddee( 1) -ddswsw(1) -0.5d0*ddrr(1) &
!              +coeff(1)/(ss*(1d0,0d0)-mw2)
! !
!       ct(1) = 0.5d0*ddzul(2)+0.5d0*ddzdl( 2) &
!              +0.5d0*ddzel(2)+0.5d0*ddznel(2) &
!              +ddee( 2) -ddswsw(2) -0.5d0*ddrr(2) &
!              +ddee( 2) -ddswsw(2) -0.5d0*ddrr(2) &
!              +coeff(2)/(ss*(1d0,0d0)-mw2)
!       
!       ct=ct/alsu4pi

      end subroutine ew_ren

      subroutine init
      implicit none
      include 'declmasses.h'
      include 'realparam.h'
      real*8 rmw,rmz,rmh,wwidth,zwidth,hwidth
      real*8 rmt,Twidth
      logical masslesswf,dred
      common/ewoptions/masslesswf,dred
      real*8 pi,pis
      common/pigreco/pi,pis
      real*8 deltauv,mudim,dimf1,dimf2,eulergamma
      common/dimreg/deltauv,mudim,dimf1,dimf2,eulergamma
      complex*16 gnm,gnp,glm,glp,gum,gup,gdm,gdp
      common/vectorassial/gnm,gnp,glm,glp,gum,gup,gdm,gdp
      real*8 qu,qd,ql,qnu
      common/charges/qu,qd,qnu,ql
      real*8 charvec
      common/vecchar/charvec(-24:24)
      integer i1
      complex*16 sw,cw,sw2,cw2,sw4,cw4,alpha,el2,alsu4pi
      common/couplings/sw,sw2,sw4,cw,cw2,cw4,alpha,el2,alsu4pi
      real*8 i3l,i3n,i3d,i3u
      common/ctisospin/i3l,i3n,i3d,i3u
      complex*16 cone,zero,ii
      common/complexunit/cone,zero,ii
      real*8 g2,gfermi
      common/weakcoup/g2
      real*8 lambda2
      common/photmass/lambda2
      real*8 unite
      common/unitcharge/unite                            
      real*8 epsilon
      common/epsi/epsilon
      real*8 scale
      common/scalale/scale
      logical noqed
      common/qedswitch/noqed
      logical gmuscheme
      common/schemeewcorr/gmuscheme
      logical cmpxmasses
      common/ccomplexmasses/cmpxmasses

      gmuscheme=.true.

!   external parameres

      me=ctme
      mm=ctmm
      mtl=ctmtl
      mu=ctmu
      md=ctmd
      mc=ctmc
      ms=ctms
      mb=ctmb
      alpha=ctalpha*(1.d0,0.d0)
      rmw=ctrmw
      rmz=ctrmz
      rmt=ctrmt
      rmh=ctrmh
      Wwidth=ctWwidth
      Zwidth=ctZwidth
      Hwidth=ctHwidth
      Twidth=ctTwidth 
      gfermi=ctgfermi

!* constants
      cone = (1.d0,0.d0)
      zero = (0.d0,0.d0)
      ii   = (0.d0,1.d0)

      pi = 3.1415926535897932384626433832795029d0
      pis= pi*pi

      eulergamma= 0.577215664901532860606512090082d0

      deltauv = -15d0

      scale = mudim
      epsilon = 1d-40

      lambda2 = 1d-6

      dimf1= log(4d0*pi) - eulergamma
      dimf1= 0d0

      dimf2= 6d0*eulergamma**2 &
            + pis &
            - 12d0*eulergamma*log(4d0*pi) &
            + 6d0*(log(4d0*pi))**2
      dimf2= dimf2/12d0
      dimf2= 0d0

      me2= me*me
      mm2= mm*mm
      mtl2= mtl*mtl

      mu2= mu*mu
      md2= md*md

      mc2= mc*mc
      ms2= ms*ms

      mb2= mb*mb

      el2     = alpha*4.d0*pi
      alsu4pi = alpha/4d0/pi
      unite=sqrt(4*pi*alpha)

      qu = +2.d0/3.d0
      qd = -1.d0/3.d0
      qnu=  0.d0
      ql = -1.d0

      do i1=-24,24
         charvec(i1)=0d0
      enddo
      charvec(-24)=-1d0
      charvec(-4 )=-qu
      charvec(-3 )=-qd
      charvec(-2 )=-qu
      charvec(-1 )=-qd
      charvec(+1 )=+qd
      charvec(+2 )=+qu
      charvec(+3 )=+qd
      charvec(+4 )=+qu
      charvec(+24)=+1d0

      mw2= rmw*rmw - (0.d0,1.d0)*rmw*wwidth
      mz2= rmz*rmz - (0.d0,1.d0)*rmz*Zwidth
      mh2= rmh*rmh - (0.d0,1.d0)*rmh*hwidth
      mt2= rmt*rmt - (0.d0,1.d0)*rmt*Twidth

      mw = sqrt(mw2)
      mz = sqrt(mz2)
      mh = sqrt(mh2)
      mt = sqrt(mt2)

      cw = mw/mz
      cw2= cw*cw
      sw2= 1.d0-cw2
      sw = sqrt(sw2)

      sw4= sw2*sw2
      cw4= cw2*cw2
!*
!* couplings of vectors to fermions
!*
!* given the expression (gv - ga gam_5) it is decomposed as 
!*
!* (gv - ga gam_5)= gm omega- + gp omega+ (see eqs. (a.14) and (a.15) 
!* and comment after eq. (6.13) of arxiv:0709.1075 (denner fortschritte), 
!* where omega- = (1 - gam_5)/2 and omega+ = (1 + gam_5)/2 (see eq. (2.9) 
!* of arxiv:0709.1075). as a consequence
!*
!* gv= (gm+gp)/2
!* ga= (gm-gp)/2
!*
!* gm= gv + ga
!* gp= gv - ga
!*
!* using eq. (a.14) of arxiv:0709.1075 (Denner Fortschritte) 
!* (in agreement (for the gfm couplings) with Dittmaier-Kramer prd65 073007) 
!*
      i3l=-0.5d0
      i3n=+0.5d0
      i3d=-0.5d0
      i3u=+0.5d0

      glm= (-0.5d0*cone - sw2 * ql)/sw/cw  !charged leptons
      glp= -sw/cw*ql
      gnm= +0.5d0/sw/cw                    !neutrinos
      gnp= 0.d0
      gum= (+0.5d0*cone - sw2 * qu)/sw/cw  !quarks
      gup= -sw/cw*qu
      gdm= (-0.5d0*cone - sw2 * qd)/sw/cw
      gdp= -sw/cw*qd

!      masslesswf=.true. 
      masslesswf=.false.! per confonto LoopTools

      noqed=.false.
      dred=.true.       ! per ora

      cmpxmasses=.false.!.true.!.false.

      g2= gfermi / sqrt(2.d0) * 8.d0*mw2
      return
      end subroutine init

      subroutine printo
      implicit none
      include 'declmasses.h'
      include 'realparam.h'
      real*8 rmw,rmz,rmh,wwidth,zwidth,hwidth
      real*8 rmt,Twidth
      logical masslesswf,dred
      common/ewoptions/masslesswf,dred
      real*8 pi,pis
      common/pigreco/pi,pis
      real*8 deltauv,mudim,dimf1,dimf2,eulergamma
      common/dimreg/deltauv,mudim,dimf1,dimf2,eulergamma
      complex*16 gnm,gnp,glm,glp,gum,gup,gdm,gdp
      common/vectorassial/gnm,gnp,glm,glp,gum,gup,gdm,gdp
      real*8 qu,qd,ql,qnu
      common/charges/qu,qd,qnu,ql
      real*8 charvec
      common/vecchar/charvec(-24:24)
      integer i1
      complex*16 sw,cw,sw2,cw2,sw4,cw4,alpha,el2,alsu4pi
      common/couplings/sw,sw2,sw4,cw,cw2,cw4,alpha,el2,alsu4pi
      real*8 i3l,i3n,i3d,i3u
      common/ctisospin/i3l,i3n,i3d,i3u
      complex*16 cone,zero,ii
      common/complexunit/cone,zero,ii
      real*8 g2,gfermi
      common/weakcoup/g2
      real*8 lambda2
      common/photmass/lambda2
      real*8 unite
      common/unitcharge/unite
      real*8 epsilon
      common/epsi/epsilon
      real*8 scale
      common/scalale/scale
      logical noqed
      common/qedswitch/noqed

      logical gmuscheme
      common/schemeewcorr/gmuscheme
       write(*,*) 'PARAMETRS   '
       write(*,*) 'deltauv,mudim'
       write(*,*) deltauv
       write(*,*) mudim
       write(*,*) 'mw,mz,mh,mh2,mw2,mz2'
       write(*,*) mw
       write(*,*) mz
       write(*,*) mh
       write(*,*) mh2
       write(*,*) mw2
       write(*,*) mz2
       write(*,*) 'me,mm,mtl,me2,mm2,mtl2'
       write(*,*) me
       write(*,*) mm
       write(*,*) mtl
       write(*,*) me2
       write(*,*) mm2
       write(*,*) mtl2
       write(*,*) 'mu,md,mu2,md2'
       write(*,*) mu
       write(*,*) md
       write(*,*) mu2
       write(*,*) md2
       write(*,*) 'mc,ms,mc2,ms2'
       write(*,*) mc
       write(*,*) ms
       write(*,*) mc2
       write(*,*) ms2
       write(*,*) 'mt,mb,mt2,mb2'
       write(*,*) mt
       write(*,*) mb
       write(*,*) mt2
       write(*,*) mb2
       write(*,*) 'gnm,gnp,glm,glp,gum,gup,gdm,gdp'
       write(*,*) gnm
       write(*,*) gnp
       write(*,*) glm
       write(*,*) glp
       write(*,*) gum
       write(*,*) gup
       write(*,*)gdm
       write(*,*) gdp
       write(*,*) 'qu,qd,ql,qnu' 
       write(*,*) qu 
       write(*,*) qd 
       write(*,*) ql
       write(*,*) qnu
       write(*,*) 'sw,cw,sw2,cw2,sw4,cw4,alpha,el2,alsu4pi'
       write(*,*) sw 
       write(*,*) cw 
       write(*,*) sw2 
       write(*,*) cw2
       write(*,*) sw4
       write(*,*) cw4
       write(*,*) alpha
       write(*,*) el2
       write(*,*) alsu4pi
       write(*,*) 'lambda,dimf1,dimf2'
       write(*,*) lambda2
       write(*,*) dimf1
       write(*,*) dimf2
      end subroutine printo


      subroutine delta_z
      implicit none
      include 'dzdecl.h'
      include 'declmasses.h'
!      include 'ddrrdecl.h'
      real*8 epsilon
      common/epsi/epsilon
      logical masslesswf,dred
      common/ewoptions/masslesswf,dred
      real*8 xx
!  auxiliary parameters
      real*8 pi,pis
      common/pigreco/pi,pis      
      complex*16 gnm,gnp,glm,glp,gum,gup,gdm,gdp
      common/vectorassial/gnm,gnp,glm,glp,gum,gup,gdm,gdp
      real*8 qu,qd,ql,qnu
      common/charges/qu,qd,qnu,ql
      complex*16 sw,cw,sw2,cw2,sw4,cw4,alpha,el2,alsu4pi
      common/couplings/sw,sw2,sw4,cw,cw2,cw4,alpha,el2,alsu4pi
      complex*16 cone,zero,ii
      common/complexunit/cone,zero,ii
      logical noqed
      common/qedswitch/noqed

      complex*16 swtmw2(0:2)
      complex*16 swt0(0:2)
      complex*16 swtpmw2(0:2)
      complex*16 sazt0(0:2)
      complex*16 saztmz2(0:2)
      complex*16 sztmz2(0:2)
      complex*16 szt0(0:2)
      complex*16 sztpmz2(0:2)
      complex*16 sat0(0:2),satp0(0:2)
      complex*16 shh(0:2),shhp(0:2)
      complex*16 qdelzne(0:2),qdelznm(0:2),qdelznt(0:2)
      complex*16 qdelze(0:2) ,qdelzm(0:2) ,qdelztl(0:2)
      complex*16 qdelzu(0:2) ,qdelzd(0:2)
      complex*16 qdelzc(0:2) ,qdelzs(0:2)
      complex*16 qdelzt(0:2) ,qdelzb(0:2)

      complex*16 qderze(0:2) ,qderzm(0:2) ,qderztl(0:2)
      complex*16 qderzu(0:2) ,qderzd(0:2)
      complex*16 qderzc(0:2) ,qderzs(0:2)
      complex*16 qderzt(0:2) ,qderzb(0:2)

      complex*16 sel(0:2) ,ser(0:2), ses(0:2)
      complex*16 sml(0:2) ,smr(0:2), sms(0:2)
      complex*16 stll(0:2),stlr(0:2),stls(0:2)
      complex*16 sul(0:2) ,sur(0:2), sus(0:2)
      complex*16 sdl(0:2) ,sdr(0:2), sds(0:2)
      complex*16 scl(0:2) ,scr(0:2), scs(0:2)
      complex*16 ssl(0:2) ,ssr(0:2), sss(0:2)
      complex*16 stl(0:2) ,str(0:2), sts(0:2)
      complex*16 sbl(0:2) ,sbr(0:2), sbs(0:2)
      complex*16 ttt(0:2) ,convt
      complex*16 stpl(0:2) ,stpr(0:2), stps(0:2)

      complex*16 tmp2,tmp1,tmp0,c

      logical cmpxmasses
      common/ccomplexmasses/cmpxmasses

      real*8 pppr
      integer i1
      logical debug
      parameter(debug=.false.)

      if(masslesswf) then
         xx=0d0
      else
         xx=1d0
      endif

      c=cone ! alias
      call      sigmawt(zero,     swt0)
      call      sigmawt(dble(mw2)*cone,     swtmw2)
      call      sigmawtp(dble(mw2)*cone,     swtpmw2)
      call sigmaazt(zero,sazt0)
      call sigmaazt(dble(mz2)*cone,saztmz2)
      call sigmazzt(dble(mz2)*cone,sztmz2)
      call sigmazzt(          zero,szt0)
      call sigmazztp(dble(mz2)*cone,sztpmz2 )      
      call sigmahh(   dble(mh2)*cone,shh)
      call sigmahhp(  dble(mh2)*cone,shhp)
      call sigmaaat( zero,sat0)
      call sigmaaatp(zero,satp0)
! tadpole
      call deltatad(ttt,convt)
! fermion
      call deltazfl(qnu*c,gnm*c,gnp*c,zero,me2*c, qdelzne)
      call deltazfl(qnu*c,gnm*c,gnp*c,zero,mm2*c, qdelznm)
      call deltazfl(qnu*c,gnm*c,gnp*c,zero,mtl2*c,qdelznt)
!
      call deltazfl(ql*c,glm*c,glp*c,me2*c   ,zero    ,qdelze )
      call deltazfl(ql*c,glm*c,glp*c,mm2*c   ,zero    ,qdelzm )
      call deltazfl(ql*c,glm*c,glp*c,mtl2*c  ,zero    ,qdelztl)
      call deltazfl(qd*c,gdm*c,gdp*c,xx*md2*c,xx*mu2*c,qdelzd )
      call deltazfl(qu*c,gum*c,gup*c,xx*mu2*c,xx*md2*c,qdelzu )
      call deltazfl(qd*c,gdm*c,gdp*c,xx*ms2*c,xx*mc2*c,qdelzs )
      call deltazfl(qu*c,gum*c,gup*c,xx*mc2*c,xx*ms2*c,qdelzc )
      call deltazfl(qd*c,gdm*c,gdp*c,   mb2*c,   mt2*c,qdelzb )
      call deltazfl(qu*c,gum*c,gup*c,   mt2*c,   mb2*c,qdelzt )

      call deltazfr(ql*c,glm*c,glp*c,   me2*c,zero    ,qderze )
      call deltazfr(ql*c,glm*c,glp*c,   mm2*c,zero    ,qderzm )
      call deltazfr(ql*c,glm*c,glp*c,  mtl2*c,zero    ,qderztl)
      call deltazfr(qd*c,gdm*c,gdp*c,xx*md2*c,xx*mu2*c,qderzd )
      call deltazfr(qu*c,gum*c,gup*c,xx*mu2*c,xx*md2*c,qderzu )
      call deltazfr(qd*c,gdm*c,gdp*c,xx*ms2*c,xx*mc2*c,qderzs )
      call deltazfr(qu*c,gum*c,gup*c,xx*mc2*c,xx*ms2*c,qderzc )
      call deltazfr(qd*c,gdm*c,gdp*c,   mb2*c,   mt2*c,qderzb )
      call deltazfr(qu*c,gum*c,gup*c,   mt2*c,   mb2*c,qderzt )
! for fermion masses
      call sigmafl(ql*c,glm*c,glp*c,  me2*c ,     zero,  me2*c ,sel)
      call sigmafr(ql*c,glm*c,glp*c,  me2*c ,     zero,  me2*c ,ser)
      call sigmafs(ql*c,glm*c,glp*c,  me2*c ,     zero,  me2*c ,ses)
      call sigmafl(ql*c,glm*c,glp*c,  mm2*c ,     zero,  mm2*c ,sml)
      call sigmafr(ql*c,glm*c,glp*c,  mm2*c ,     zero,  mm2*c ,smr)
      call sigmafs(ql*c,glm*c,glp*c,  mm2*c ,     zero,  mm2*c ,sms)
      call sigmafl(ql*c,glm*c,glp*c,  mtl2*c,     zero,  mtl2*c,stll)
      call sigmafr(ql*c,glm*c,glp*c,  mtl2*c,     zero,  mtl2*c,stlr)
      call sigmafs(ql*c,glm*c,glp*c,  mtl2*c,     zero,  mtl2*c,stls)
      call sigmafl(qu*c,gum*c,gup*c,xx*mu2*c, xx*md2*c,xx*mu2*c,sul)
      call sigmafr(qu*c,gum*c,gup*c,xx*mu2*c, xx*md2*c,xx*mu2*c,sur)
      call sigmafs(qu*c,gum*c,gup*c,xx*mu2*c, xx*md2*c,xx*mu2*c,sus)
      call sigmafl(qd*c,gdm*c,gdp*c,xx*md2*c, xx*mu2*c,xx*md2*c,sdl)
      call sigmafr(qd*c,gdm*c,gdp*c,xx*md2*c, xx*mu2*c,xx*md2*c,sdr)
      call sigmafs(qd*c,gdm*c,gdp*c,xx*md2*c, xx*mu2*c,xx*md2*c,sds)
      call sigmafl(qu*c,gum*c,gup*c,xx*mc2*c, xx*ms2*c,xx*mc2*c,scl)
      call sigmafr(qu*c,gum*c,gup*c,xx*mc2*c, xx*ms2*c,xx*mc2*c,scr)
      call sigmafs(qu*c,gum*c,gup*c,xx*mc2*c, xx*ms2*c,xx*mc2*c,scs)
      call sigmafl(qd*c,gdm*c,gdp*c,xx*ms2*c, xx*mc2*c,xx*ms2*c,ssl)
      call sigmafr(qd*c,gdm*c,gdp*c,xx*ms2*c, xx*mc2*c,xx*ms2*c,ssr)
      call sigmafs(qd*c,gdm*c,gdp*c,xx*ms2*c, xx*mc2*c,xx*ms2*c,sss)
      call sigmafl(qu*c,gum*c,gup*c,   mt2*c,    mb2*c, dble(mt2)*c,stl)
      call sigmafr(qu*c,gum*c,gup*c,   mt2*c,    mb2*c, dble(mt2)*c,str)
      call sigmafs(qu*c,gum*c,gup*c,   mt2*c,    mb2*c, dble(mt2)*c,sts)
      call sigmafl(qd*c,gdm*c,gdp*c,   mb2*c,    mt2*c,   mb2*c,sbl)
      call sigmafr(qd*c,gdm*c,gdp*c,   mb2*c,    mt2*c,   mb2*c,sbr)
      call sigmafs(qd*c,gdm*c,gdp*c,   mb2*c,    mt2*c,   mb2*c,sbs)

      call sigmaflp(qu*c,gum*c,gup*c,  mt2*c,   mb2*c, dble(mt2)*c,stpl)
      call sigmafrp(qu*c,gum*c,gup*c,  mt2*c,   mb2*c, dble(mt2)*c,stpr)
      call sigmafsp(qu*c,gum*c,gup*c,  mt2*c,   mb2*c, dble(mt2)*c,stps)

      ! switch off the imaginary parts if not in the complex mass-scheme
      ! only for debug
      if(.not.cmpxmasses) then
         do i1=0,2
            swt0    (i1) =dble(  swt0    (i1) )
            swtmw2  (i1) =dble(  swtmw2  (i1) )
            swtpmw2 (i1) =dble(  swtpmw2 (i1) )
            sazt0   (i1) =dble(  sazt0   (i1) )
            saztmz2 (i1) =dble(  saztmz2 (i1) )
            sztmz2  (i1) =dble(  sztmz2  (i1) )
            szt0    (i1) =dble(  szt0    (i1) )
            sztpmz2 (i1) =dble(  sztpmz2 (i1) )
            shh     (i1) =dble(  shh     (i1) )
            shhp    (i1) =dble(  shhp    (i1) )
            sat0    (i1) =dble(  sat0    (i1) )
            satp0   (i1) =dble(  satp0   (i1) )
            sel     (i1) =dble(  sel     (i1) )
            ser     (i1) =dble(  ser     (i1) )
            ses     (i1) =dble(  ses     (i1) )
            sml     (i1) =dble(  sml     (i1) )
            smr     (i1) =dble(  smr     (i1) )
            sms     (i1) =dble(  sms     (i1) )
            stll    (i1) =dble(  stll    (i1) )
            stlr    (i1) =dble(  stlr    (i1) )
            stls    (i1) =dble(  stls    (i1) )
            sul     (i1) =dble(  sul     (i1) )
            sur     (i1) =dble(  sur     (i1) )
            sus     (i1) =dble(  sus     (i1) )
            sdl     (i1) =dble(  sdl     (i1) )
            sdr     (i1) =dble(  sdr     (i1) )
            sds     (i1) =dble(  sds     (i1) )
            scl     (i1) =dble(  scl     (i1) )
            scr     (i1) =dble(  scr     (i1) )
            scs     (i1) =dble(  scs     (i1) )
            ssl     (i1) =dble(  ssl     (i1) )
            ssr     (i1) =dble(  ssr     (i1) )
            sss     (i1) =dble(  sss     (i1) )
            stl     (i1) =dble(  stl     (i1) )
            str     (i1) =dble(  str     (i1) )
            sts     (i1) =dble(  sts     (i1) )
            sbl     (i1) =dble(  sbl     (i1) )
            sbr     (i1) =dble(  sbr     (i1) )
            sbs     (i1) =dble(  sbs     (i1) )
            stpl    (i1) =dble(  stpl    (i1) )
            stpr    (i1) =dble(  stpr    (i1) )
            stps    (i1) =dble(  stps    (i1) )
         end do
      end if
! vec-bos masses
      ddmw2(1)=swtmw2(0)
      ddmw2(2)=swtmw2(1)
      ddmz2(1)=sztmz2(0)
      ddmz2(2)=sztmz2(1)
      ddmh2(1)=shh(0)
      ddmh2(2)=shh(1)
! vec bos wf
      ddzw(1)=-swtpmw2(0)
      ddzw(2)=-swtpmw2(1)
      ddzz(1)=-sztpmz2(0)
      ddzz(2)=-sztpmz2(1)
      ddzh(1)=-shhp(0)
      ddzh(2)=-shhp(1)
      ddza(1)=-satp0(0)
      ddza(2)=-satp0(1)
      ddz_za(1)=2d0*sazt0(0)/mz2
      ddz_za(2)=2d0*sazt0(1)/mz2
      ddz_az(1)=-2d0*saztmz2(0)/dble(mz2)  &
         + (mz2/dble(mz2) - cone)*ddz_za(1)
      ddz_az(2)=-2d0*saztmz2(1)/dble(mz2)  &
         + (mz2/dble(mz2) - cone)*ddz_za(2)
! tadpole
      dtad(1)=ttt(0)
      dtad(2)=ttt(1)
!  fermion masses
      ddme2(1)=0.5d0*me*(sel(0) + ser(0) + 2d0*ses(0))
      ddme2(2)=0.5d0*me*(sel(1) + ser(1) + 2d0*ses(1))
      ddmm2(1)=0.5d0*mm*(sml(0) + smr(0) + 2d0*sms(0))
      ddmm2(2)=0.5d0*mm*(sml(1) + smr(1) + 2d0*sms(1))
      ddmtl2(1)=0.5d0*mtl*(stll(0) + stlr(0) + 2d0*stls(0))
      ddmtl2(2)=0.5d0*mtl*(stll(1) + stlr(1) + 2d0*stls(1))
      ddmu2(1)=0.5d0*mu*(sul(0) + sur(0) + 2d0*sus(0))
      ddmu2(2)=0.5d0*mu*(sul(1) + sur(1) + 2d0*sus(1))
      ddmd2(1)=0.5d0*md*(sdl(0) + sdr(0) + 2d0*sds(0))
      ddmd2(2)=0.5d0*md*(sdl(1) + sdr(1) + 2d0*sds(1))
      ddmc2(1)=0.5d0*mc*(scl(0) + scr(0) + 2d0*scs(0))
      ddmc2(2)=0.5d0*mc*(scl(1) + scr(1) + 2d0*scs(1))
      ddms2(1)=0.5d0*ms*(ssl(0) + ssr(0) + 2d0*sss(0))
      ddms2(2)=0.5d0*ms*(ssl(1) + ssr(1) + 2d0*sss(1))
      ddmt2(1)=0.5d0*sqrt(dble(mt2))*(stl(0) + str(0) + 2d0*sts(0)) ! eq 4.38 hep-ph 0505042
      ddmt2(2)=0.5d0*sqrt(dble(mt2))*(stl(1) + str(1) + 2d0*sts(1)) ! eq 4.38 hep-ph 0505042
!
      ddme2ome(1)=0.5d0*(sel(0) + ser(0) + 2d0*ses(0))
      ddme2ome(2)=0.5d0*(sel(1) + ser(1) + 2d0*ses(1))
      ddmm2omm(1)=0.5d0*(sml(0) + smr(0) + 2d0*sms(0))
      ddmm2omm(2)=0.5d0*(sml(1) + smr(1) + 2d0*sms(1))
      ddmtl2omtl(1)=0.5d0*(stll(0) + stlr(0) + 2d0*stls(0))
      ddmtl2omtl(2)=0.5d0*(stll(1) + stlr(1) + 2d0*stls(1))
      ddmu2omu(1)=0.5d0*(sul(0) + sur(0) + 2d0*sus(0))
      ddmu2omu(2)=0.5d0*(sul(1) + sur(1) + 2d0*sus(1))
      ddmd2omd(1)=0.5d0*(sdl(0) + sdr(0) + 2d0*sds(0))
      ddmd2omd(2)=0.5d0*(sdl(1) + sdr(1) + 2d0*sds(1))
      ddmc2omc(1)=0.5d0*(scl(0) + scr(0) + 2d0*scs(0))
      ddmc2omc(2)=0.5d0*(scl(1) + scr(1) + 2d0*scs(1))
      ddms2oms(1)=0.5d0*(ssl(0) + ssr(0) + 2d0*sss(0))
      ddms2oms(2)=0.5d0*(ssl(1) + ssr(1) + 2d0*sss(1))
      ddmt2omt(1)=0.5d0*(stl(0) + str(0) + 2d0*sts(0)) ! eq 4.38 hep-ph 0505042
      ddmt2omt(2)=0.5d0*(stl(1) + str(1) + 2d0*sts(1)) ! eq 4.38 hep-ph 0505042
   
      ddmb2(1)=0.5d0*mb*(sbl(0) + sbr(0) + 2d0*sbs(0))
      ddmb2(2)=0.5d0*mb*(sbl(1) + sbr(1) + 2d0*sbs(1))
      ddmb2omb(1)=0.5d0*(sbl(0) + sbr(0) + 2d0*sbs(0))
      ddmb2omb(2)=0.5d0*(sbl(1) + sbr(1) + 2d0*sbs(1))
! sermion wf renorm NEUTRINI
      ddznel(1)=qdelzne(0)
      ddznel(2)=qdelzne(1)
      ddznml(1)=qdelznm(0)
      ddznml(2)=qdelznm(1)
      ddzntl(1)=qdelznt(0)
      ddzntl(2)=qdelznt(1)
! altri L
      ddzel(1) = qdelze(0)
      ddzel(2) = qdelze(1)
      ddzml(1) = qdelzm(0)
      ddzml(2) = qdelzm(1)
      ddztll(1) = qdelztl(0)
      ddztll(2) = qdelztl(1)
      ddzul(1) = qdelzu(0)
      ddzul(2) = qdelzu(1)
      ddzdl(1) = qdelzd(0)
      ddzdl(2) = qdelzd(1)
      ddzcl(1) = qdelzc(0)
      ddzcl(2) = qdelzc(1)
      ddzsl(1) = qdelzs(0)
      ddzsl(2) = qdelzs(1)
      ddztl(1) = qdelzt(0)
      ddztl(2) = qdelzt(1)
      ddzbl(1) = qdelzb(0)
      ddzbl(2) = qdelzb(1)
! altri R
      ddzer(1) = qderze(0)
      ddzer(2) = qderze(1)
      ddzmr(1) = qderzm(0)
      ddzmr(2) = qderzm(1)
      ddztlr(1) = qderztl(0)
      ddztlr(2) = qderztl(1)
      ddzur(1) = qderzu(0)
      ddzur(2) = qderzu(1)
      ddzdr(1) = qderzd(0)
      ddzdr(2) = qderzd(1)
      ddzcr(1) = qderzc(0)
      ddzcr(2) = qderzc(1)
      ddzsr(1) = qderzs(0)
      ddzsr(2) = qderzs(1)
      ddztr(1) = qderzt(0)
      ddztr(2) = qderzt(1)
      ddzbr(1) = qderzb(0)
      ddzbr(2) = qderzb(1)
! parameters
! szztmz2 + ii*dimag(mz2)*szztpmz2
! they do not change for real masses
      ddmw2(1)=ddmw2(1)+swtpmw2(0)*(0d0,1d0)*dimag(mw2)  &
                         -(0d0,1d0)*dimag(mw2)*alpha/pi      
      ddmw2(2)=ddmw2(2)+swtpmw2(1)*(0d0,1d0)*dimag(mw2)

      ddmz2(1)=ddmz2(1)+sztpmz2(0)*(0d0,1d0)*dimag(mz2) 
      ddmz2(2)=ddmz2(2)+sztpmz2(1)*(0d0,1d0)*dimag(mz2)

      ! ADDED 29/08 begin
      ddmh2(1)=ddmh2(1)+shhp(0)*(0d0,1d0)*dimag(mh2) 
      ddmh2(2)=ddmh2(2)+shhp(1)*(0d0,1d0)*dimag(mh2)
      ! ADDED 29/08 end

      ddmt2omt(1)=ddmt2omt(1)+(0d0,1d0)*dimag(mt2)*( &
           0.5d0*stpl(1) +0.5d0*stpr(1) +stps(1)   )  &
                         -(0d0,1d0)*qu*qu*alpha*dimag(mt2)/dble(mt2)/pi      
      ddmt2omt(2)=ddmt2omt(2)+(0d0,1d0)*dimag(mt2)*( &
           0.5d0*stpl(2) +0.5d0*stpr(2) +stps(2)   )
      ddmt2(1)=ddmt2(1) + sqrt(dble(mt2))*( &
            (0d0,1d0)*dimag(mt2)*(0.5d0*stpl(1) +0.5d0*stpr(1) +stps(1))  &
                         -(0d0,1d0)*qu*qu*alpha*dimag(mt2)/dble(mt2)/pi)
      ddmt2(2)=ddmt2(2) + sqrt(dble(mt2))*( &
            (0d0,1d0)*dimag(mt2)*(0.5d0*stpl(2) +0.5d0*stpr(2) +stps(2))  &
                                           )

      ddee(1)= -0.5d0*(ddza(1)+sw/cw*ddz_za(1)) ! de/e
      ddee(2)= -0.5d0*(ddza(2)+sw/cw*ddz_za(2)) ! de/e
      ddcwcw(1)=0.5d0*( ddmw2(1)/mw2 - ddmz2(1)/mz2 )       ! dcw/cw
      ddcwcw(2)=0.5d0*( ddmw2(2)/mw2 - ddmz2(2)/mz2 )       ! dcw/cw
      ddswsw(1)=-cw2/sw2*ddcwcw(1)  ! dsw/sw
      ddswsw(2)=-cw2/sw2*ddcwcw(2)  ! dsw/sw

      ddrr(1)=+satp0(0)-(cw2/sw2)*(ddmz2(1)/mz2-ddmw2(1)/mw2) &
           +(swt0(0)- ddmw2(1) )/mw2 &
           +2d0*(cw/sw)*sazt0(0)/mz2 &
           +(alsu4pi/sw2)*(6d0*c+log(cw2)*(7d0*c-4d0*sw2)/2d0/sw2)

      ddrr(2)=+satp0(1)-(cw2/sw2)*(ddmz2(2)/mz2-ddmw2(2)/mw2) &
           +(swt0(1)- ddmw2(2) )/mw2 &
           +2d0*(cw/sw)*sazt0(1)/mz2


! per cdr --> dred      
      if(dred) then
         ddza(1) = ddza(1) - 2d0/3d0*alsu4pi
         ddee(1) = ddee(1)  + 1d0/3d0*alsu4pi
!         dZZA1 = dZZA1        --> ddz_za(1)
         ddz_az(1)=ddz_az(1)+4d0/3d0*cw/sw*alsu4pi
         ddZZ(1) = ddzz(1) - 2d0/3d0*cw2/sw2*alsu4pi
         ddzw(1) = ddzw(1) - 2d0/3d0/sw2*alsu4pi
!         dZH1 = dZH1
! it is equivalent to keep dm(re) and dz separately !       
         ddMW2(1)=ddMW2(1) + 2d0/3d0*MW2/SW2*alsu4pi
         ddMZ2(1)=ddMZ2(1) + 2d0/3d0*cw2*MZ2/sw2*alsu4pi
         ddMH2(1)=ddMH2(1) + 3d0*(2d0*cw2*MW2+MZ2)/2d0/cw2/sw2*alsu4pi

         dtad(1) =dtad(1) - convt ! this already includes alsu4pi

         ddcwcw(1)=0.5d0*(ddmw2(1)/mw2-ddmz2(1)/mz2) ! dcw/cw
         ddswsw(1)=-cw2/sw2*ddcwcw(1) ! dsw/sw
! effectively only if are massive
         ddmu2(1) = ddmu2(1) + MU*((3d0-4d0*sw2)**2 &
                        +2d0*cw2*(9d0+8d0*sw2))/72d0/cw2/sw2*alsu4pi
         ddmd2(1) = ddmd2(1) + MD*(9d0+4d0*sw2**2 &
                        +2d0*cw2*(9d0+2d0*sw2))/72d0/cw2/sw2*alsu4pi
         ddme2(1) = ddme2(1) + ME*(1d0+4d0*(-2d0+sw2)*sw2 &
                        +cw2*(2d0+4d0*sw2))/8d0/cw2/sw2*alsu4pi
         ddmc2(1) = ddmc2(1) + Mc*((3d0-4d0*sw2)**2 &
                        +2d0*cw2*(9d0+8d0*sw2))/72d0/cw2/sw2*alsu4pi
         ddms2(1) = ddms2(1) + Ms*(9d0+4d0*sw2**2 &
                        +2d0*cw2*(9d0+2d0*sw2))/72d0/cw2/sw2*alsu4pi
         ddmm2(1) = ddmm2(1) + MM*(1d0+4d0*(-2d0+sw2)*sw2 &
                        +cw2*(2d0+4d0*sw2))/8d0/cw2/sw2*alsu4pi
! scheme change on sigma:: not sigma' :: mass multiplied afterwards
! same scheme conversion for RE and CMPLX top mass  
         ddmt2(1) = ddmt2(1) + sqrt(dble(mt2))*((3d0-4d0*sw2)**2 &
                        +2d0*cw2*(9d0+8d0*sw2))/72d0/cw2/sw2*alsu4pi


         ddmb2(1) = ddmb2(1) + mb*(9d0+4d0*sw2**2 &
                        +2d0*cw2*(9d0+2d0*sw2))/72d0/cw2/sw2*alsu4pi
         ddmtl2(1) = ddmtl2(1) + mtl*(1d0+4d0*(-2d0+sw2)*sw2 &
                        +cw2*(2d0+4d0*sw2))/8d0/cw2/sw2*alsu4pi

         ddmu2omu(1) = ddmu2omu(1) + ((3d0-4d0*sw2)**2 &
                        +2d0*cw2*(9d0+8d0*sw2))/72d0/cw2/sw2*alsu4pi
         ddmd2omd(1) = ddmd2omd(1) + (9d0+4d0*sw2**2 &
                        +2d0*cw2*(9d0+2d0*sw2))/72d0/cw2/sw2*alsu4pi
         ddme2ome(1) = ddme2ome(1) + (1d0+4d0*(-2d0+sw2)*sw2 &
                        +cw2*(2d0+4d0*sw2))/8d0/cw2/sw2*alsu4pi
         ddmc2omc(1) = ddmc2omc(1) + ((3d0-4d0*sw2)**2 &
                        +2d0*cw2*(9d0+8d0*sw2))/72d0/cw2/sw2*alsu4pi
         ddms2oms(1) = ddms2oms(1) + (9d0+4d0*sw2**2 &
                        +2d0*cw2*(9d0+2d0*sw2))/72d0/cw2/sw2*alsu4pi
         ddmm2omm(1) = ddmm2omm(1) + (1d0+4d0*(-2d0+sw2)*sw2 &
                        +cw2*(2d0+4d0*sw2))/8d0/cw2/sw2*alsu4pi
         ddmt2omt(1) = ddmt2omt(1) +          ((3d0-4d0*sw2)**2 &
                        +2d0*cw2*(9d0+8d0*sw2))/72d0/cw2/sw2*alsu4pi
         ddmb2omb(1) = ddmb2omb(1) + (9d0+4d0*sw2**2 &
                        +2d0*cw2*(9d0+2d0*sw2))/72d0/cw2/sw2*alsu4pi
         ddmtl2omtl(1) = ddmtl2omtl(1) + (1d0+4d0*(-2d0+sw2)*sw2 &
                        +cw2*(2d0+4d0*sw2))/8d0/cw2/sw2*alsu4pi


         ddzel(1)=ddzel(1) -(1d0+2d0*CW2)/4d0/CW2/SW2*alsu4pi
         ddzer(1)=ddzer(1) -1d0/CW2*alsu4pi
         ddznel(1)=ddznel(1) -(1d0+2d0*CW2)/4d0/CW2/SW2*alsu4pi

         ddzml(1)=ddzml(1) -(1d0+2d0*CW2)/4d0/CW2/SW2*alsu4pi
         ddzmr(1)=ddzmr(1) -1d0/CW2*alsu4pi
         ddznml(1)=ddznml(1) -(1d0+2d0*CW2)/4d0/CW2/SW2*alsu4pi

         ddztll(1)=ddztll(1) -(1d0+2d0*CW2)/4d0/CW2/SW2*alsu4pi
         ddztlr(1)=ddztlr(1) -1d0/CW2*alsu4pi
         ddzntl(1)=ddzntl(1) -(1d0+2d0*CW2)/4d0/CW2/SW2*alsu4pi

         ddzul(1)=ddzul(1) -((3d0-4d0*SW2)**2 + 2d0*CW2*(9d0+8d0*SW2)) &
                   /36d0/CW2/SW2*alsu4pi
         ddzcl(1)=ddzcl(1) -((3d0-4d0*SW2)**2 + 2d0*CW2*(9d0+8d0*SW2)) &
                   /36d0/CW2/SW2*alsu4pi
         ddztl(1)=ddztl(1) -((3d0-4d0*SW2)**2 + 2d0*CW2*(9d0+8d0*SW2)) &
                   /36d0/CW2/SW2*alsu4pi

         ddzur(1)=ddzur(1) -4d0/9d0/CW2*alsu4pi
         ddzcr(1)=ddzcr(1) -4d0/9d0/CW2*alsu4pi
         ddztr(1)=ddztr(1) -4d0/9d0/CW2*alsu4pi

         ddzdl(1)=ddzdl(1) -((3d0-2d0*SW2)**2 + 2d0*CW2*(9d0+2d0*SW2)) &
                   /36d0/CW2/SW2*alsu4pi
         ddzsl(1)=ddzsl(1) -((3d0-2d0*SW2)**2 + 2d0*CW2*(9d0+2d0*SW2)) &
                   /36d0/CW2/SW2*alsu4pi
         ddzbl(1)=ddzbl(1) -((3d0-2d0*SW2)**2 + 2d0*CW2*(9d0+2d0*SW2)) &
                   /36d0/CW2/SW2*alsu4pi

         ddzdr(1)=ddzdr(1) -1d0/9d0/CW2*alsu4pi
         ddzsr(1)=ddzsr(1) -1d0/9d0/CW2*alsu4pi
         ddzbr(1)=ddzbr(1) -1d0/9d0/CW2*alsu4pi

         if(abs(me2).lt.epsilon*10d3)then
            ddzel(1)=ddzel(1) + alsu4pi
            ddzer(1)=ddzer(1) + alsu4pi
         endif
         if(abs(mm2).lt.epsilon*10d3)then
            ddzml(1)=ddzml(1) + alsu4pi
            ddzmr(1)=ddzmr(1) + alsu4pi
         endif
         if(abs(mtl2).lt.epsilon*10d3)then
            ddztll(1)=ddztll(1) + alsu4pi
            ddztlr(1)=ddztlr(1) + alsu4pi
         endif
         if(abs(mu2).lt.epsilon*10d3.or.masslesswf)then
            ddzul(1)=ddzul(1) + alsu4pi*4d0/9d0
            ddzur(1)=ddzur(1) + alsu4pi*4d0/9d0
         endif
         if(abs(mc2).lt.epsilon*10d3.or.masslesswf)then
            ddzcl(1)=ddzcl(1) + alsu4pi*4d0/9d0
            ddzcr(1)=ddzcr(1) + alsu4pi*4d0/9d0
         endif
         if(abs(md2).lt.epsilon*10d3.or.masslesswf)then
            ddzdl(1)=ddzdl(1) + alsu4pi*1d0/9d0
            ddzdr(1)=ddzdr(1) + alsu4pi*1d0/9d0
         endif
         if(abs(ms2).lt.epsilon*10d3.or.masslesswf)then
            ddzsl(1)=ddzsl(1) + alsu4pi*1d0/9d0
            ddzsr(1)=ddzsr(1) + alsu4pi*1d0/9d0
         endif
         if(abs(mb2).lt.epsilon*10d3.or.masslesswf)then
            ddzbl(1)=ddzbl(1) + alsu4pi*1d0/9d0
            ddzbr(1)=ddzbr(1) + alsu4pi*1d0/9d0
         endif

         if(noqed) then
            write(*,*)'ANCORA DA IMPLEMENTARE :: MA CI INTERESSA?'
            stop
         endif
      endif
      if(debug) call printoutct
      end subroutine delta_z

      subroutine computectcoeff
      implicit none
      include 'dzdecl.h'
      include 'declmasses.h'
!      include 'ddrrdecl.h'
! options 
      real*8 epsilon
      common/epsi/epsilon
      logical masslesswf,dred
      common/ewoptions/masslesswf,dred
      real*8 xx
! auxiliary parameters
      real*8 pi,pis
      common/pigreco/pi,pis      
      complex*16 gnm,gnp,glm,glp,gum,gup,gdm,gdp
      common/vectorassial/gnm,gnp,glm,glp,gum,gup,gdm,gdp
      real*8 qu,qd,ql,qnu
      common/charges/qu,qd,qnu,ql
      complex*16 sw,cw,sw2,cw2,sw4,cw4,alpha,el2,alsu4pi
      common/couplings/sw,sw2,sw4,cw,cw2,cw4,alpha,el2,alsu4pi
      real*8 unite
      common/unitcharge/unite
      complex*16 cone,zero,ii
      common/complexunit/cone,zero,ii
! not in common
      complex*16 swtmw2(0:2)
      complex*16 swt0(0:2)
      complex*16 swtpmw2(0:2)
      complex*16 sazt0(0:2)
      complex*16 saztmz2(0:2)
      complex*16 sztmz2(0:2)
      complex*16 szt0(0:2)
      complex*16 sztpmz2(0:2)
      complex*16 sat0(0:2),satp0(0:2)
      complex*16 shh(0:2),shhp(0:2)
      complex*16 qdelzne(0:2),qdelznm(0:2),qdelznt(0:2)
      complex*16 qdelze(0:2) ,qdelzm(0:2) ,qdelztl(0:2)
      complex*16 qdelzu(0:2) ,qdelzd(0:2)
      complex*16 qdelzc(0:2) ,qdelzs(0:2)
      complex*16 qdelzt(0:2) ,qdelzb(0:2)
!
      complex*16 qderze(0:2) ,qderzm(0:2) ,qderztl(0:2)
      complex*16 qderzu(0:2) ,qderzd(0:2)
      complex*16 qderzc(0:2) ,qderzs(0:2)
      complex*16 qderzt(0:2) ,qderzb(0:2)
!
      complex*16 sel(0:2) ,ser(0:2), ses(0:2)
      complex*16 sml(0:2) ,smr(0:2), sms(0:2)
      complex*16 stll(0:2),stlr(0:2),stls(0:2)
      complex*16 sul(0:2) ,sur(0:2), sus(0:2)
      complex*16 sdl(0:2) ,sdr(0:2), sds(0:2)
      complex*16 scl(0:2) ,scr(0:2), scs(0:2)
      complex*16 ssl(0:2) ,ssr(0:2), sss(0:2)
      complex*16 stl(0:2) ,str(0:2), sts(0:2)
      complex*16 sbl(0:2) ,sbr(0:2), sbs(0:2)
      complex*16 stpl(0:2) ,stpr(0:2), stps(0:2)
!
! auxiliary and local only
     complex*16  cdznel(1:2),cdznml(1:2),cdzntl(1:2) ! wf renorm
     complex*16  cdzel(1:2),cdzml(1:2),cdztll(1:2) ! wf renorm
     complex*16  cdzul(1:2),cdzcl(1:2),cdztl(1:2)
     complex*16  cdzdl(1:2),cdzsl(1:2),cdzbl(1:2)
     complex*16  cdzer(1:2),cdzmr(1:2),cdztlr(1:2)
     complex*16  cdzur(1:2),cdzcr(1:2),cdztr(1:2)
     complex*16  cdzdr(1:2),cdzsr(1:2),cdzbr(1:2)
      complex*16 ccgp(0:2),ccgm(0:2)
!
      integer i1
      real*8 i3l,i3n,i3d,i3u
      common/ctisospin/i3l,i3n,i3d,i3u
!
      complex*16 coeff,coeff2
      logical gmuscheme
      common/schemeewcorr/gmuscheme
      logical cmpxmasses
      common/ccomplexmasses/cmpxmasses

      logical heavydbg
      parameter(heavydbg=.false.)

      if(cmpxmasses) then
         do i1=1,2
            cdznel(i1)=cone*(ddznel(i1))
            cdznml(i1)=cone*(ddznml(i1))
            cdzntl(i1)=cone*(ddzntl(i1))
            cdzel(i1) =cone*(ddzel(i1) )
            cdzml(i1) =cone*(ddzml(i1) )
            cdztll(i1)=cone*(ddztll(i1))
            cdzul(i1) =cone*(ddzul(i1) )
            cdzcl(i1) =cone*(ddzcl(i1) )
            cdztl(i1) =cone*(ddztl(i1) )
            cdzdl(i1) =cone*(ddzdl(i1) )
            cdzsl(i1) =cone*(ddzsl(i1) )
            cdzbl(i1) =cone*(ddzbl(i1) )
            cdzer(i1) =cone*(ddzer(i1) )
            cdzmr(i1) =cone*(ddzmr(i1) )
            cdztlr(i1)=cone*(ddztlr(i1))
            cdzur(i1) =cone*(ddzur(i1) )
            cdzcr(i1) =cone*(ddzcr(i1) )
            cdztr(i1) =cone*(ddztr(i1) )
            cdzdr(i1) =cone*(ddzdr(i1) )
            cdzsr(i1) =cone*(ddzsr(i1) )
            cdzbr(i1) =cone*(ddzbr(i1) )
         end do 
      else
         do i1=1,2
            cdznel(i1)=conjg(ddznel(i1))
            cdznml(i1)=conjg(ddznml(i1))
            cdzntl(i1)=conjg(ddzntl(i1))
            cdzel(i1) =conjg(ddzel(i1) )
            cdzml(i1) =conjg(ddzml(i1) )
            cdztll(i1)=conjg(ddztll(i1))
            cdzul(i1) =conjg(ddzul(i1) )
            cdzcl(i1) =conjg(ddzcl(i1) )
            cdztl(i1) =conjg(ddztl(i1) )
            cdzdl(i1) =conjg(ddzdl(i1) )
            cdzsl(i1) =conjg(ddzsl(i1) )
            cdzbl(i1) =conjg(ddzbl(i1) )
            cdzer(i1) =conjg(ddzer(i1) )
            cdzmr(i1) =conjg(ddzmr(i1) )
            cdztlr(i1)=conjg(ddztlr(i1))
            cdzur(i1) =conjg(ddzur(i1) )
            cdzcr(i1) =conjg(ddzcr(i1) )
            cdztr(i1) =conjg(ddztr(i1) )
            cdzdr(i1) =conjg(ddzdr(i1) )
            cdzsr(i1) =conjg(ddzsr(i1) )
            cdzbr(i1) =conjg(ddzbr(i1) )
         end do
      end if
      if(masslesswf) then
         xx=0d0
      else
         xx=1d0
      endif
! aux for zff
      do i1=1,2
         ccgp(i1)=-(ddee(i1)+ddswsw(i1)/cw2)*sw/cw
         ccgm(i1)=+(ddee(i1)+ddswsw(i1)*(sw2-cw2)/cw2)/sw/cw
      enddo
! 1 = finite part, 2 = pole part
      do i1=1,2
! vector bosons PROPAGATORS A.3
         gctW1(i1 )=ddzw(i1)
         gctW2(i1 )=mw2*ddzw(i1)+ddmw2(i1)
         gctZ1(i1 )=ddzz(i1)
         gctZ2(i1 )=mz2*ddzz(i1)+ddmz2(i1)
         gctA(i1  )=ddza(i1)
         gctAZ1(i1)=0.5d0*(ddz_az(i1)+ddz_za(i1))
         gctAZ2(i1)=0.5d0*mz2*ddz_za(i1)
! scalar propagators A.4
         gctH1(i1 )=ddzh(i1)
         gctH2(i1 )=mh2*ddzh(i1)+ddmh2(i1)
         gctchi(i1)=ddmz2(i1)-unite*dtad(i1)/2d0/sw/mw
         gctphi(i1)=ddmw2(i1)-unite*dtad(i1)/2d0/sw/mw
! fermion propagator A.5
         gctCLU(i1)=0.5d0*(ddzul(i1)+cone*(cdzul(i1)))
         gctCRU(i1)=0.5d0*(ddzur(i1)+cone*(cdzur(i1)))
         gctCPU(i1)=xx*(mu*cone*(cdzul(i1)/2d0)+mu*ddzur(i1)/2d0+ddmu2(i1))
         gctCMU(i1)=xx*(mu*cone*(cdzur(i1)/2d0)+mu*ddzul(i1)/2d0+ddmu2(i1))
!
         gctCLC(i1)=0.5d0*(ddzcl(i1)+cone*(cdzcl(i1)))
         gctCRC(i1)=0.5d0*(ddzcr(i1)+cone*(cdzcr(i1)))
         gctCPC(i1)=xx*(mc*cone*(cdzcl(i1)/2d0)+mc*ddzcr(i1)/2d0+ddmc2(i1))
         gctCMC(i1)=xx*(mc*cone*(cdzcr(i1)/2d0)+mc*ddzcl(i1)/2d0+ddmc2(i1))
! 
         gctCLT(i1)=0.5d0*(ddztl(i1)+cone*(cdztl(i1)))
         gctCRT(i1)=0.5d0*(ddztr(i1)+cone*(cdztr(i1)))
         gctCPT(i1)=mt*(cone*(cdztl(i1)/2d0)+ddztr(i1)/2d0+ddmt2omt(i1))
         gctCMT(i1)=mt*(cone*(cdztr(i1)/2d0)+ddztl(i1)/2d0+ddmt2omt(i1))
!
         gctCLD(i1)=0.5d0*(ddzdl(i1)+cone*(cdzdl(i1)))
         gctCRD(i1)=0.5d0*(ddzdr(i1)+cone*(cdzdr(i1)))
         gctCPD(i1)=xx*(md*cone*(cdzdl(i1)/2d0)+md*ddzdr(i1)/2d0+ddmd2(i1))
         gctCMD(i1)=xx*(md*cone*(cdzdr(i1)/2d0)+md*ddzdl(i1)/2d0+ddmd2(i1))
!
         gctCLS(i1)=0.5d0*(ddzsl(i1)+cone*(cdzsl(i1)))
         gctCRS(i1)=0.5d0*(ddzsr(i1)+cone*(cdzsr(i1)))
         gctCPS(i1)=xx*(ms*cone*(cdzsl(i1)/2d0)+ms*ddzsr(i1)/2d0+ddms2(i1))
         gctCMS(i1)=xx*(ms*cone*(cdzsr(i1)/2d0)+ms*ddzsl(i1)/2d0+ddms2(i1))
!
         gctCLB(i1)=0.5d0*(ddzbl(i1)+cone*(cdzbl(i1)))
         gctCRB(i1)=0.5d0*(ddzbr(i1)+cone*(cdzbr(i1)))
         gctCPB(i1)=xx*(mb*cone*(cdzbl(i1)/2d0)+mb*ddzbr(i1)/2d0+ddmb2(i1))
         gctCMB(i1)=xx*(mb*cone*(cdzbr(i1)/2d0)+mb*ddzbl(i1)/2d0+ddmb2(i1))
!
         gctCLne(i1)=0.5d0*(ddznel(i1)+cone*(cdznel(i1)))
         gctCRne(i1)=0d0!0.5d0*(ddzner(i1)+cone*(cdzner(i1)))
!
         gctCLnmu(i1)=0.5d0*(ddznml(i1)+cone*(cdznml(i1)))
         gctCRnmu(i1)=0d0!0.5d0*(ddznmr(i1)+cone*(cdznmr(i1)))
!
         gctCLntau(i1)=0.5d0*(ddzntl(i1)+cone*(cdzntl(i1)))
         gctCRntau(i1)=0d0!0.5d0*(ddzntr(i1)+cone*(cdzntr(i1)))
!
         gctCLe(i1)=0.5d0*(ddzel(i1)+cone*(cdzel(i1)))
         gctCRe(i1)=0.5d0*(ddzer(i1)+cone*(cdzer(i1)))
         gctCPe(i1)=xx*(me*cone*(cdzel(i1)/2d0)+me*ddzer(i1)/2d0+ddme2(i1))
         gctCMe(i1)=xx*(me*cone*(cdzer(i1)/2d0)+me*ddzel(i1)/2d0+ddme2(i1))
!
         gctCLmu(i1)=0.5d0*(ddzml(i1)+cone*(cdzml(i1)))
         gctCRmu(i1)=0.5d0*(ddzmr(i1)+cone*(cdzmr(i1)))
         gctCPmu(i1)=xx*(mm*cone*(cdzml(i1)/2d0)+mm*ddzmr(i1)/2d0+ddmm2(i1))
         gctCMmu(i1)=xx*(mm*cone*(cdzmr(i1)/2d0)+mm*ddzml(i1)/2d0+ddmm2(i1))
!
         gctCLtau(i1)=0.5d0*(ddztll(i1)+cone*(cdztll(i1)))
         gctCRtau(i1)=0.5d0*(ddztlr(i1)+cone*(cdztlr(i1)))
         gctCPtau(i1)=xx*(mtl*cone*(cdztll(i1)/2d0)+mtl*ddztlr(i1)/2d0 &
              +ddmtl2(i1))
         gctCMtau(i1)=xx*(mtl*cone*(cdztlr(i1)/2d0)+mtl*ddztll(i1)/2d0 &
              +ddmtl2(i1))
!c quartic gauge boson interaction A.6
         gctWWZZ(i1) = -(cw2/sw2)*( 2d0*ddee(i1) &
              -2d0*ddswsw(i1)/cw2 + ddzw(i1) + ddzz(i1) ) &
              +(cw/sw)*ddz_az(i1)
         gctWWAZ(i1) = +(cw/sw)*( 2d0*ddee(i1) - ddswsw(i1)/cw2 &
              +ddzw(i1) + 0.5d0*ddzz(i1) + 0.5d0*ddza(i1) ) &
              -0.5d0*ddz_az(i1)-0.5d0*(cw2/sw2)*ddz_za(i1)
         gctWWAA(i1) = -( 2d0*ddee(i1) + ddzw(i1) + ddza(i1) ) &
              +(cw/sw)*ddz_za(i1)
         gctWWWW(i1)=(2d0*ddee(i1) -2d0*ddswsw(i1) +2d0*ddzw(i1) )/sw2
! 3 vector A.7
         gctWWA(i1) = ddee(i1)+ddzw(i1)+0.5d0*ddza(i1) &
              -0.5d0*(cw/sw)*ddz_za(i1)
         gctWWZ(i1) = -(cw/sw)*( ddee(i1)-ddswsw(i1)/cw2 + ddzw(i1) &
              +0.5d0*ddzz(i1) ) + 0.5d0*ddz_az(i1)
! 4 scalars A.8
         coeff =mh2/4d0/sw2/mw2
         coeff2=unite/2d0/sw/mw/mh2
         gctHHHH(i1)=-3d0*coeff*(2d0*ddee(i1) - 2d0*ddswsw(i1) &
              + ddmh2(i1)/mh2 + coeff2*dtad(i1) -ddmw2(i1)/mw2  &
              +2d0*ddzh(i1))
         gctHHXX(i1)=    -coeff*(2d0*ddee(i1) - 2d0*ddswsw(i1) &
              + ddmh2(i1)/mh2 + coeff2*dtad(i1) - ddmw2(i1)/mw2  &
              + ddzh(i1))
         gctHHPP(i1)=    -coeff*(2d0*ddee(i1) - 2d0*ddswsw(i1) &
              + ddmh2(i1)/mh2 + coeff2*dtad(i1) - ddmw2(i1)/mw2 &
              + ddzh(i1))
         gctXXXX(i1)=-3d0*coeff*(2d0*ddee(i1) - 2d0*ddswsw(i1) &
              + ddmh2(i1)/mh2 + coeff2*dtad(i1) - ddmw2(i1)/mw2 )
         gctXXPP(i1)=-1d0*coeff*(2d0*ddee(i1) - 2d0*ddswsw(i1) &
              + ddmh2(i1)/mh2 + coeff2*dtad(i1) - ddmw2(i1)/mw2 )
         gctPPPP(i1)=-2d0*coeff*(2d0*ddee(i1) - 2d0*ddswsw(i1) &
              + ddmh2(i1)/mh2 + coeff2*dtad(i1) - ddmw2(i1)/mw2 )
! 3 scalars A.9
         coeff =mh2/2d0/sw/mw
         gctHHH(i1)=-3d0*coeff*(ddee(i1) - ddswsw(i1) &
              + ddmh2(i1)/mh2 + coeff2*dtad(i1) - 0.5d0*ddmw2(i1)/mw2 &
              + 1.5d0*ddzh(i1))
         gctHPP(i1)=-coeff*(ddee(i1) - ddswsw(i1) &
              + ddmh2(i1)/mh2 + coeff2*dtad(i1) - 0.5d0*ddmw2(i1)/mw2 &
              + 0.5d0*ddzh(i1))
         gctHXX(i1)=-coeff*(ddee(i1) - ddswsw(i1) &
              + ddmh2(i1)/mh2 + coeff2*dtad(i1) - 0.5d0*ddmw2(i1)/mw2 &
              + 0.5d0*ddzh(i1))
! 2 vectors 2 scalars A.10
         gctWWHH(i1)=(1d0/2d0/sw2)*(2d0*ddee(i1) - 2d0*ddswsw(i1) + ddzw(i1) &
              + ddzh(i1))
         gctWWXX(i1)=(1d0/2d0/sw2)*(2d0*ddee(i1) - 2d0*ddswsw(i1) +ddzw(i1))
         gctWWPP(i1)=(1d0/2d0/sw2)*(2d0*ddee(i1) - 2d0*ddswsw(i1) +ddzw(i1))
         gctZZPP(i1)=(sw2-cw2)**2/2d0/sw2/cw2*( 2d0*ddee(i1) &
              +2d0*ddswsw(i1)/cw2/(sw2-cw2)+ddzz(i1) )  &
              +(sw2-cw2)/sw/cw*ddz_az(i1)
         gctAZPP(i1)=(sw2-cw2)/sw/cw*(2d0*ddee(i1) &
              +ddswsw(i1)/cw2/(sw2-cw2)+0.5d0*ddzz(i1)+0.5d0*ddza(i1)) & 
              +(sw2-cw2)**2/2d0/sw2/cw2*0.5d0*ddz_za(i1)+ddz_az(i1)
         gctAAPP(i1)=2d0*(2d0*ddee(i1)+ddza(i1)) &
              +(sw2-cw2)/sw/cw*ddz_za(i1)
         gctZZHH(i1)=1d0/2d0/sw2/cw2*(2d0*ddee(i1) &
              +2d0*(sw2-cw2)/cw2*ddswsw(i1)+ddzz(i1)+ddzh(i1))
         gctZZXX(i1)=1d0/2d0/sw2/cw2*(2d0*ddee(i1) &
              +2d0*(sw2-cw2)/cw2*ddswsw(i1)+ddzz(i1))
         gctZAHH(i1)=1d0/2d0/sw2/cw2*(0.5d0*ddz_za(i1))
         gctZAXX(i1)=1d0/2d0/sw2/cw2*(0.5d0*ddz_za(i1))
         gctWZPH(i1)=-1d0/2d0/cw*(2d0*ddee(i1)-ddcwcw(i1) &
              +0.5d0*ddzw(i1)+0.5d0*ddzh(i1)+0.5d0*ddzz(i1)) &
              -ddz_az(i1)/4d0/sw
         gctWAPH(i1)=-1d0/2d0/sw*(2d0*ddee(i1)-ddswsw(i1) &
              +0.5d0*ddzw(i1)+0.5d0*ddzh(i1)+0.5d0*ddza(i1)) &
              -ddz_za(i1)/4d0/cw
         gctWZPX(i1)=-ii/2d0/cw*(2d0*ddee(i1)-ddcwcw(i1) &
              +0.5d0*ddzw(i1)+0.5d0*ddzz(i1)) &
              -ii/4d0/sw*ddz_az(i1)
         gctWAPX(i1)=-ii/2d0/sw*(2d0*ddee(i1)-ddswsw(i1) &
              +0.5d0*ddzw(i1)+0.5d0*ddza(i1)) &
              -ii/4d0/cw*ddz_za(i1)
! vector scalar scalar A.11
         gctAXH(i1)=-ii*ddz_za(i1)/4d0/cw/sw
         gctZXH(i1)=-ii/2d0/cw/sw*(ddee(i1)+(sw2-cw2)/cw2*ddswsw(i1) &
              +0.5d0*ddzh(i1)+0.5d0*ddzz(i1))
         gctAPP(i1)=-(ddee(i1)+0.5d0*ddza(i1) &
              +(sw2-cw2)/4d0/cw/sw*ddz_za(i1))
         gctZPP(i1)=-(sw2-cw2)/2d0/cw/sw*(ddee(i1) &
              +ddswsw(i1)/cw2/(sw2-cw2)+0.5d0*ddzz(i1)) &
              -0.5d0*ddz_az(i1)
         gctWPH(i1)=-1d0/2d0/sw*(ddee(i1)-ddswsw(i1) &
              +0.5d0*ddzw(i1)+0.5d0*ddzh(i1))
         gctWPX(i1)=-ii/2d0/sw*(ddee(i1)-ddswsw(i1) &
              +0.5d0*ddzw(i1))
! vector vector scalar A.12
         gctHWW(i1)=mw/sw*(ddee(i1)-ddswsw(i1)+0.5d0*ddmw2(i1)/mw2 &
              +0.5d0*ddzh(i1)+ddzw(i1))
         gctHZZ(i1)=mw/sw/cw2*(ddee(i1)+(2d0*sw2-cw2)/cw2*ddswsw(i1) &
              +0.5d0*ddmw2(i1)/mw2 &
              +0.5d0*ddzh(i1)+ddzz(i1))
         gctHZA(i1)=mw/2d0/sw/cw2*ddz_za(i1)
         gctPWZ(i1)=-mw*sw/cw*(ddee(i1)+1d0/cw2*ddswsw(i1) &
              +0.5d0*ddmw2(i1)/mw2 &
              +0.5d0*ddzz(i1)+0.5d0*ddzw(i1) ) - 0.5d0*mw*ddz_az(i1)
         gctPWA(i1)=-mw*(ddee(i1)+0.5d0*ddmw2(i1)/mw2 &
              +0.5d0*ddza(i1)+0.5d0*ddzw(i1) )-0.5d0*mw*sw/cw*ddz_za(i1)
! vecor fermion fermion A.15
         gctWpud(i1)=1d0/sqrt(2d0)/sw*(ddee(i1)-ddswsw(i1) &
              +0.5d0*ddzw(i1) &
              +0.5d0*cone*(cdzul(i1)) + 0.5d0*ddzdl(i1) )
         gctWpcs(i1)=1d0/sqrt(2d0)/sw*(ddee(i1)-ddswsw(i1) &
              +0.5d0*ddzw(i1) &
              +0.5d0*cone*(cdzcl(i1)) + 0.5d0*ddzsl(i1) )
         gctWptb(i1)=1d0/sqrt(2d0)/sw*(ddee(i1)-ddswsw(i1) &
              +0.5d0*ddzw(i1) &
              +0.5d0*cone*(cdztl(i1)) + 0.5d0*ddzbl(i1) )
         gctWmud(i1)=1d0/sqrt(2d0)/sw*(ddee(i1)-ddswsw(i1) &
              +0.5d0*ddzw(i1) &
              +0.5d0*cone*(cdzdl(i1)) + 0.5d0*ddzul(i1) )
         gctWmcs(i1)=1d0/sqrt(2d0)/sw*(ddee(i1)-ddswsw(i1) &
              +0.5d0*ddzw(i1) &
              +0.5d0*cone*(cdzsl(i1)) + 0.5d0*ddzcl(i1) )
         gctWmtb(i1)=1d0/sqrt(2d0)/sw*(ddee(i1)-ddswsw(i1) &
              +0.5d0*ddzw(i1) &
              +0.5d0*cone*(cdzbl(i1)) + 0.5d0*ddztl(i1) )
!
         gctWpe(i1)=1d0/sqrt(2d0)/sw*(ddee(i1)-ddswsw(i1) &
              +0.5d0*ddzw(i1) &
              +0.5d0*cone*(cdznel(i1)) + 0.5d0*ddzel(i1) )
         gctWme(i1)=1d0/sqrt(2d0)/sw*(ddee(i1)-ddswsw(i1) &
              +0.5d0*ddzw(i1) &
              +0.5d0*cone*(cdzel(i1)) + 0.5d0*ddznel(i1) )
         gctWpmu(i1)=1d0/sqrt(2d0)/sw*(ddee(i1)-ddswsw(i1) &
              +0.5d0*ddzw(i1) &
              +0.5d0*cone*(cdznml(i1)) + 0.5d0*ddzml(i1) )
         gctWmmu(i1)=1d0/sqrt(2d0)/sw*(ddee(i1)-ddswsw(i1) &
              +0.5d0*ddzw(i1) &
              +0.5d0*cone*(cdzml(i1)) + 0.5d0*ddznml(i1) )
         gctWptau(i1)=1d0/sqrt(2d0)/sw*(ddee(i1)-ddswsw(i1) &
              +0.5d0*ddzw(i1) &
              +0.5d0*cone*(cdzntl(i1)) + 0.5d0*ddztll(i1) )
         gctWmtau(i1)=1d0/sqrt(2d0)/sw*(ddee(i1)-ddswsw(i1) &
              +0.5d0*ddzw(i1) &
              +0.5d0*cone*(cdztll(i1)) + 0.5d0*ddzntl(i1) )
         !
         ! added
         gctArne(i1)=0d0 ! gnp=0d0 ! q=0
         gctAlne(i1)=gnm*0.5d0*ddz_za(i1)
         gctArnmu(i1)=0d0 ! gnp=0d0 ! q=0
         gctAlnmu(i1)=gnm*0.5d0*ddz_za(i1)
         gctArntau(i1)=0d0 ! gnp=0d0 ! q=0
         gctAlntau(i1)=gnm*0.5d0*ddz_za(i1)
         ! added
         gctAre(i1)=-ql*(ddee(i1)+0.5d0*ddza(i1) &
              +0.5d0*(cone*(cdzer(i1))+ddzer(i1)) ) &
              +glp*0.5d0*ddz_za(i1)
         gctAle(i1)=-ql*(ddee(i1)+0.5d0*ddza(i1) &
              +0.5d0*(cone*(cdzel(i1))+ddzel(i1)) ) &
              +glm*0.5d0*ddz_za(i1)
         gctArmu(i1)=-ql*(ddee(i1)+0.5d0*ddza(i1) &
              +0.5d0*(cone*(cdzmr(i1))+ddzmr(i1)) ) &
              +glp*0.5d0*ddz_za(i1)
         gctAlmu(i1)=-ql*(ddee(i1)+0.5d0*ddza(i1) &
              +0.5d0*(cone*(cdzml(i1))+ddzml(i1)) ) &
              +glm*0.5d0*ddz_za(i1)
         gctArtau(i1)=-ql*(ddee(i1)+0.5d0*ddza(i1) &
              +0.5d0*(cone*(cdztlr(i1))+ddztlr(i1)) ) &
              +glp*0.5d0*ddz_za(i1)
         gctAltau(i1)=-ql*(ddee(i1)+0.5d0*ddza(i1) &
              +0.5d0*(cone*(cdztll(i1))+ddztll(i1)) ) &
              +glm*0.5d0*ddz_za(i1)
 
         gctArU(i1)=-qu*(ddee(i1)+0.5d0*ddza(i1) &
              +0.5d0*(cone*(cdzur(i1))+ddzur(i1)) ) &
              +gup*0.5d0*ddz_za(i1)
         gctAlU(i1)=-qu*(ddee(i1)+0.5d0*ddza(i1) &
              +0.5d0*(cone*(cdzul(i1))+ddzul(i1)) ) &
              +gum*0.5d0*ddz_za(i1)
         gctArC(i1)=-qu*(ddee(i1)+0.5d0*ddza(i1) &
              +0.5d0*(cone*(cdzcr(i1))+ddzcr(i1)) ) &
              +gup*0.5d0*ddz_za(i1)
         gctAlC(i1)=-qu*(ddee(i1)+0.5d0*ddza(i1) &
              +0.5d0*(cone*(cdzcl(i1))+ddzcl(i1)) ) &
              +gum*0.5d0*ddz_za(i1)
         gctArT(i1)=-qu*(ddee(i1)+0.5d0*ddza(i1) &
              +0.5d0*(cone*(cdztr(i1))+ddztr(i1)) ) &
              +gup*0.5d0*ddz_za(i1)
         gctAlT(i1)=-qu*(ddee(i1)+0.5d0*ddza(i1) &
              +0.5d0*(cone*(cdztl(i1))+ddztl(i1)) ) &
              +gum*0.5d0*ddz_za(i1)
 
         gctArD(i1)=-qd*(ddee(i1)+0.5d0*ddza(i1) &
              +0.5d0*(cone*(cdzdr(i1))+ddzdr(i1)) ) &
              +gdp*0.5d0*ddz_za(i1)
         gctAlD(i1)=-qd*(ddee(i1)+0.5d0*ddza(i1) &
              +0.5d0*(cone*(cdzdl(i1))+ddzdl(i1)) ) &
              +gdm*0.5d0*ddz_za(i1)
         gctArS(i1)=-qd*(ddee(i1)+0.5d0*ddza(i1) &
              +0.5d0*(cone*(cdzsr(i1))+ddzsr(i1)) ) &
              +gdp*0.5d0*ddz_za(i1)
         gctAlS(i1)=-qd*(ddee(i1)+0.5d0*ddza(i1) &
              +0.5d0*(cone*(cdzsl(i1))+ddzsl(i1)) ) &
              +gdm*0.5d0*ddz_za(i1)
         gctArB(i1)=-qd*(ddee(i1)+0.5d0*ddza(i1) &
              +0.5d0*(cone*(cdzbr(i1))+ddzbr(i1)) ) &
              +gdp*0.5d0*ddz_za(i1)
         gctAlB(i1)=-qd*(ddee(i1)+0.5d0*ddza(i1) &
              +0.5d0*(cone*(cdzbl(i1))+ddzbl(i1)) ) &
              +gdm*0.5d0*ddz_za(i1)
! glon f fbar :: as in gamma f fbar
         gctGrU(i1)=0.5d0*(ddzur(i1)+cone*(cdzur(i1)))
         gctGlU(i1)=0.5d0*(ddzul(i1)+cone*(cdzul(i1)))
         gctGrD(i1)=0.5d0*(ddzdr(i1)+cone*(cdzdr(i1)))
         gctGlD(i1)=0.5d0*(ddzdl(i1)+cone*(cdzdl(i1)))
         gctGrC(i1)=0.5d0*(ddzcr(i1)+cone*(cdzcr(i1)))
         gctGlC(i1)=0.5d0*(ddzcl(i1)+cone*(cdzcl(i1)))
         gctGrS(i1)=0.5d0*(ddzsr(i1)+cone*(cdzsr(i1)))
         gctGlS(i1)=0.5d0*(ddzsl(i1)+cone*(cdzsl(i1)))
         gctGrT(i1)=0.5d0*(ddztr(i1)+cone*(cdztr(i1)))
         gctGlT(i1)=0.5d0*(ddztl(i1)+cone*(cdztl(i1)))
         gctGrB(i1)=0.5d0*(ddzbr(i1)+cone*(cdzbr(i1)))
         gctGlB(i1)=0.5d0*(ddzbl(i1)+cone*(cdzbl(i1)))
 
         gctZrne(i1)=0d0 ! gnp=0d0 ! q=0
         gctZlne(i1)=gnm*(ccgm(i1)*i3n/gnm+0.5d0*ddzz(i1) &
              +0.5d0*(cone*(cdznel(i1))+ ddznel(i1) ))
         gctZrnmu(i1)=0d0 ! gnp=0d0 ! q=0
         gctZlnmu(i1)=gnm*(ccgm(i1)*i3n/gnm+0.5d0*ddzz(i1) &
              +0.5d0*(cone*(cdznml(i1))+ ddznml(i1) ))
         gctZrntau(i1)=0d0 ! gnp=0d0 ! q=0
         gctZlntau(i1)=gnm*(ccgm(i1)*i3n/gnm+0.5d0*ddzz(i1) &
              +0.5d0*(cone*(cdzntl(i1))+ ddzntl(i1) ))
 
         gctZre(i1)=glp*(ccgp(i1)*ql/glp +0.5d0*ddzz(i1) &
              +0.5d0*(cone*(cdzer(i1))+ ddzer(i1) )) &
              -0.5d0*ql*ddz_az(i1)
         gctZle(i1)=glm*(ccgp(i1)*ql/glm + ccgm(i1)*i3l/glm &
              +0.5d0*ddzz(i1) &
              +0.5d0*(cone*(cdzel(i1))+ ddzel(i1) )) &
              -0.5d0*ql*ddz_az(i1)
         gctZrmu(i1)=glp*(ccgp(i1)*ql/glp +0.5d0*ddzz(i1) &
              +0.5d0*(cone*(cdzmr(i1))+ ddzmr(i1) )) &
              -0.5d0*ql*ddz_az(i1)
         gctZlmu(i1)=glm*(ccgp(i1)*ql/glm + ccgm(i1)*i3l/glm &
              +0.5d0*ddzz(i1) &
              +0.5d0*(cone*(cdzml(i1))+ ddzml(i1) )) &
              -0.5d0*ql*ddz_az(i1)
         gctZrtau(i1)=glp*(ccgp(i1)*ql/glp +0.5d0*ddzz(i1) &
              +0.5d0*(cone*(cdztlr(i1))+ ddztlr(i1) )) &
              -0.5d0*ql*ddz_az(i1)
         gctZltau(i1)=glm*(ccgp(i1)*ql/glm + ccgm(i1)*i3l/glm &
              +0.5d0*ddzz(i1) &
              +0.5d0*(cone*(cdztll(i1))+ ddztll(i1) )) &
              -0.5d0*ql*ddz_az(i1)
 
         gctZrU(i1)=gup*(ccgp(i1)*qu/gup +0.5d0*ddzz(i1) &
              +0.5d0*(cone*(cdzur(i1))+ ddzur(i1) )) &
              -0.5d0*qu*ddz_az(i1)
         gctZlU(i1)=gum*(ccgp(i1)*qu/gum + ccgm(i1)*i3u/gum &
              +0.5d0*ddzz(i1) &
              +0.5d0*(cone*(cdzul(i1))+ ddzul(i1) )) &
              -0.5d0*qu*ddz_az(i1)
         gctZrC(i1)=gup*(ccgp(i1)*qu/gup +0.5d0*ddzz(i1) &
              +0.5d0*(cone*(cdzcr(i1))+ ddzcr(i1) )) &
              -0.5d0*qu*ddz_az(i1)
         gctZlC(i1)=gum*(ccgp(i1)*qu/gum + ccgm(i1)*i3u/gum &
              +0.5d0*ddzz(i1) &
              +0.5d0*(cone*(cdzcl(i1))+ ddzcl(i1) )) &
              -0.5d0*qu*ddz_az(i1)
         gctZrT(i1)=gup*(ccgp(i1)*qu/gup +0.5d0*ddzz(i1) &
              +0.5d0*(cone*(cdztr(i1))+ ddztr(i1) )) &
              -0.5d0*qu*ddz_az(i1)
         gctZlT(i1)=gum*(ccgp(i1)*qu/gum + ccgm(i1)*i3u/gum &
              +0.5d0*ddzz(i1) &
              +0.5d0*(cone*(cdztl(i1))+ ddztl(i1) )) &
              -0.5d0*qu*ddz_az(i1)
 
         gctZrD(i1)=gdp*(ccgp(i1)*qd/gdp +0.5d0*ddzz(i1) &
              +0.5d0*(cone*(cdzdr(i1))+ ddzdr(i1) )) &
              -0.5d0*qd*ddz_az(i1)
         gctZlD(i1)=gdm*(ccgp(i1)*qd/gdm + ccgm(i1)*i3d/gdm &
              +0.5d0*ddzz(i1) &
              +0.5d0*(cone*(cdzdl(i1))+ ddzdl(i1) )) &
              -0.5d0*qd*ddz_az(i1)
         gctZrS(i1)=gdp*(ccgp(i1)*qd/gdp +0.5d0*ddzz(i1) &
              +0.5d0*(cone*(cdzsr(i1))+ ddzsr(i1) )) &
              -0.5d0*qd*ddz_az(i1)
         gctZlS(i1)=gdm*(ccgp(i1)*qd/gdm + ccgm(i1)*i3d/gdm &
              +0.5d0*ddzz(i1) &
              +0.5d0*(cone*(cdzsl(i1))+ ddzsl(i1) )) &
              -0.5d0*qd*ddz_az(i1)
         gctZrB(i1)=gdp*(ccgp(i1)*qd/gdp +0.5d0*ddzz(i1) &
              +0.5d0*(cone*(cdzbr(i1))+ ddzbr(i1) )) &
              -0.5d0*qd*ddz_az(i1)
         gctZlB(i1)=gdm*(ccgp(i1)*qd/gdm + ccgm(i1)*i3d/gdm &
              +0.5d0*ddzz(i1) &
              +0.5d0*(cone*(cdzbl(i1))+ ddzbl(i1) )) &
              -0.5d0*qd*ddz_az(i1)
! scalar fermion fermion A.16
         coeff=-1d0/2d0/sw/mw
         gctHre(i1)=coeff*me*( ddee(i1)-ddswsw(i1)+ddme2ome(i1)  &
              -0.5d0*ddmw2(i1)/mw2 +0.5d0*ddzh(i1)  &
              +0.5d0*( ddzer(i1)+cone*(cdzel(i1)) ) )
         gctHle(i1)=coeff*me*( ddee(i1)-ddswsw(i1)+ddme2ome(i1)  &
              -0.5d0*ddmw2(i1)/mw2 +0.5d0*ddzh(i1)  &
              +0.5d0*( ddzel(i1)+cone*(cdzer(i1)) ) )
         gctHrmu (i1)=coeff*mm*(ddee(i1)-ddswsw(i1)+ddmm2omm(i1)  &
              -0.5d0*ddmw2(i1)/mw2 +0.5d0*ddzh(i1) &
              +0.5d0*( ddzmr(i1)+cone*(cdzml(i1)) ) )
         gctHlmu(i1)=mm*coeff*(ddee(i1)-ddswsw(i1)+ddmm2omm(i1)  &
              -0.5d0*ddmw2(i1)/mw2 +0.5d0*ddzh(i1) &
              +0.5d0*( ddzml(i1)+cone*(cdzmr(i1)) ) )
         gctHrtau(i1)=coeff*mtl*(ddee(i1)-ddswsw(i1)+ddmtl2omtl(i1) & 
              -0.5d0*ddmw2(i1)/mw2 +0.5d0*ddzh(i1) &
              +0.5d0*( ddztlr(i1)+cone*(cdztll(i1)) ) )
         gctHltau(i1)=mtl*coeff*(ddee(i1)-ddswsw(i1)+ddmtl2omtl(i1)  &
              -0.5d0*ddmw2(i1)/mw2 +0.5d0*ddzh(i1) &
              +0.5d0*( ddztll(i1)+cone*(cdztlr(i1)) ) )
         gctHrU(i1)=coeff*mu*( ddee(i1)-ddswsw(i1)+ddmu2omu(i1)  &
              -0.5d0*ddmw2(i1)/mw2 +0.5d0*ddzh(i1)  &
              +0.5d0*( ddzur(i1)+cone*(cdzul(i1)) ) )
         gctHlU(i1)=coeff*mu*( ddee(i1)-ddswsw(i1)+ddmu2omu(i1)  &
              -0.5d0*ddmw2(i1)/mw2 +0.5d0*ddzh(i1)  &
              +0.5d0*( ddzul(i1)+cone*(cdzur(i1)) ) )
         gctHrD(i1)=coeff*md*( ddee(i1)-ddswsw(i1)+ddmd2omd(i1)  &
              -0.5d0*ddmw2(i1)/mw2 +0.5d0*ddzh(i1)  &
              +0.5d0*( ddzdr(i1)+cone*(cdzdl(i1)) ) )
         gctHlD(i1)=coeff*md*( ddee(i1)-ddswsw(i1)+ddmd2omd(i1)  &
              -0.5d0*ddmw2(i1)/mw2 +0.5d0*ddzh(i1)  &
              +0.5d0*( ddzdl(i1)+cone*(cdzdr(i1)) ) )
         gctHrC(i1)=coeff*mc*( ddee(i1)-ddswsw(i1)+ddmc2omc(i1)  &
              -0.5d0*ddmw2(i1)/mw2 +0.5d0*ddzh(i1)  &
              +0.5d0*( ddzcr(i1)+cone*(cdzcl(i1)) ) )
         gctHlC(i1)=coeff*mc*( ddee(i1)-ddswsw(i1)+ddmc2omc(i1)  &
              -0.5d0*ddmw2(i1)/mw2 +0.5d0*ddzh(i1)  &
              +0.5d0*( ddzcl(i1)+cone*(cdzcr(i1)) ) )
         gctHrS(i1)=coeff*ms*( ddee(i1)-ddswsw(i1)+ddms2oms(i1)  &
              -0.5d0*ddmw2(i1)/mw2 +0.5d0*ddzh(i1)  &
              +0.5d0*( ddzsr(i1)+cone*(cdzsl(i1)) ) )
         gctHlS(i1)=coeff*ms*( ddee(i1)-ddswsw(i1)+ddms2oms(i1)  &
              -0.5d0*ddmw2(i1)/mw2 +0.5d0*ddzh(i1)  &
              +0.5d0*( ddzsl(i1)+cone*(cdzsr(i1)) ) )
         gctHrT(i1)=coeff*mt*( ddee(i1)-ddswsw(i1)+ddmt2omt(i1) &
              -0.5d0*ddmw2(i1)/mw2 +0.5d0*ddzh(i1)  &
              +0.5d0*( ddztr(i1)+cone*(cdztl(i1)) ) )
         gctHlT(i1)=coeff*mt*( ddee(i1)-ddswsw(i1)+ddmt2omt(i1)  &
              -0.5d0*ddmw2(i1)/mw2 +0.5d0*ddzh(i1)  &
              +0.5d0*( ddztl(i1)+cone*(cdztr(i1)) ) )
         gctHrB(i1)=coeff*mb*( ddee(i1)-ddswsw(i1)+ddmb2omb(i1)  &
              -0.5d0*ddmw2(i1)/mw2 +0.5d0*ddzh(i1)  &
              +0.5d0*( ddzbr(i1)+cone*(cdzbl(i1)) ) )
         gctHlB(i1)=coeff*mb*( ddee(i1)-ddswsw(i1)+ddmb2omb(i1)  &
              -0.5d0*ddmw2(i1)/mw2 +0.5d0*ddzh(i1)  &
              +0.5d0*( ddzbl(i1)+cone*(cdzbr(i1)) ) )
! NB
         coeff=-1d0/sw/mw
         gctXre(i1)=+coeff*me*i3l*( ddee(i1)-ddswsw(i1)  &
              +ddme2ome(i1) - 0.5d0*ddmw2(i1)/mw2  &
              +0.5d0*( ddzer(i1)+cone*(cdzel(i1)) ) )
         gctXle(i1)=+coeff*me*i3l*( ddee(i1)-ddswsw(i1)  &
              +ddme2ome(i1) - 0.5d0*ddmw2(i1)/mw2  &
              +0.5d0*( ddzel(i1)+cone*(cdzer(i1)) ) )         
         gctXrmu(i1)=+coeff*mm*i3l*( ddee(i1)-ddswsw(i1)  &
              +ddmm2omm(i1) - 0.5d0*ddmw2(i1)/mw2  &
              +0.5d0*( ddzmr(i1)+cone*(cdzml(i1)) ) )
         gctXlmu(i1)=+coeff*mm*i3l*( ddee(i1)-ddswsw(i1)  &
              +ddmm2omm(i1) - 0.5d0*ddmw2(i1)/mw2  &
              +0.5d0*( ddzml(i1)+cone*(cdzmr(i1)) ) )         
         gctXrtau(i1)=+coeff*mtl*i3l*( ddee(i1)-ddswsw(i1)  &
              +ddmtl2omtl(i1) - 0.5d0*ddmw2(i1)/mw2  &
              +0.5d0*( ddztlr(i1)+cone*(cdztll(i1)) ) )
         gctXltau(i1)=+coeff*mtl*i3l*( ddee(i1)-ddswsw(i1)  &
              +ddmtl2omtl(i1) - 0.5d0*ddmw2(i1)/mw2  &
              +0.5d0*( ddztll(i1)+cone*(cdztlr(i1)) ) )         
!
         gctXrU(i1)=+coeff*mu*i3u*( ddee(i1)-ddswsw(i1)  &
              +ddmu2omu(i1) - 0.5d0*ddmw2(i1)/mw2  &
              +0.5d0*( ddzur(i1)+cone*(cdzul(i1)) ) )
         gctXlU(i1)=+coeff*mu*i3u*( ddee(i1)-ddswsw(i1)  &
              +ddmu2omu(i1) - 0.5d0*ddmw2(i1)/mw2  &
              +0.5d0*( ddzul(i1)+cone*(cdzur(i1)) ) )         
         gctXrC(i1)=+coeff*mc*i3u*( ddee(i1)-ddswsw(i1)  &
              +ddmc2omc(i1) - 0.5d0*ddmw2(i1)/mw2  &
              +0.5d0*( ddzcr(i1)+cone*(cdzcl(i1)) ) )
         gctXlC(i1)=+coeff*mc*i3u*( ddee(i1)-ddswsw(i1)  &
              +ddmc2omc(i1) - 0.5d0*ddmw2(i1)/mw2  &
              +0.5d0*( ddzcl(i1)+cone*(cdzcr(i1)) ) )         
         gctXrT(i1)=+coeff*mt*i3u*( ddee(i1)-ddswsw(i1)  &
              +ddmt2omt(i1)    - 0.5d0*ddmw2(i1)/mw2  &
              +0.5d0*( ddztr(i1)+cone*(cdztl(i1)) ) )
         gctXlT(i1)=+coeff*mt*i3u*( ddee(i1)-ddswsw(i1)  &
              +ddmt2omt(i1)    - 0.5d0*ddmw2(i1)/mw2  &
              +0.5d0*( ddztl(i1)+cone*(cdztr(i1)) ) )         
         gctXrD(i1)=+coeff*md*i3d*( ddee(i1)-ddswsw(i1)  &
              +ddmd2omd(i1) - 0.5d0*ddmw2(i1)/mw2  &
              +0.5d0*( ddzdr(i1)+cone*(cdzdl(i1)) ) )
         gctXlD(i1)=+coeff*md*i3d*( ddee(i1)-ddswsw(i1)  &
              +ddmd2omd(i1) - 0.5d0*ddmw2(i1)/mw2  &
              +0.5d0*( ddzdl(i1)+cone*(cdzdr(i1)) ) )         
         gctXrS(i1)=+coeff*ms*i3d*( ddee(i1)-ddswsw(i1)  &
              +ddms2oms(i1) - 0.5d0*ddmw2(i1)/mw2  &
              +0.5d0*( ddzsr(i1)+cone*(cdzsl(i1)) ) )
         gctXlS(i1)=+coeff*ms*i3d*( ddee(i1)-ddswsw(i1)  &
              +ddms2oms(i1) - 0.5d0*ddmw2(i1)/mw2  &
              +0.5d0*( ddzsl(i1)+cone*(cdzsr(i1)) ) )         
         gctXrB(i1)=+coeff*mb*i3d*( ddee(i1)-ddswsw(i1)  &
              +ddmb2omb(i1) - 0.5d0*ddmw2(i1)/mw2  &
              +0.5d0*( ddzbr(i1)+cone*(cdzbl(i1)) ) )
         gctXlB(i1)=+coeff*mb*i3d*( ddee(i1)-ddswsw(i1)  &
              +ddmb2omb(i1) - 0.5d0*ddmw2(i1)/mw2  &
              +0.5d0*( ddzbl(i1)+cone*(cdzbr(i1)) ) ) 
! 
         coeff=+1d0/sqrt(2d0)/sw/mw
         gctPpre(i1)=-coeff*me*(ddee(i1)-ddswsw(i1) &
              +ddme2ome(i1) - 0.5d0*ddmw2(i1)/mw2 &
              +0.5d0*(cone*(cdznel(i1)) + ddzer(i1)) )
         gctPple(i1)=0d0! mnu*
         gctPprmu(i1)=-coeff*mm*(ddee(i1)-ddswsw(i1) &
              +ddmm2omm(i1) - 0.5d0*ddmw2(i1)/mw2 &
              +0.5d0*(cone*(cdznml(i1)) + ddzmr(i1)) )
         gctPplmu(i1)=0d0! mnu*
         gctPprtau(i1)=-coeff*mtl*(ddee(i1)-ddswsw(i1) &
              +ddmtl2omtl(i1) - 0.5d0*ddmw2(i1)/mw2 &
              +0.5d0*(cone*(cdzntl(i1)) + ddztlr(i1)) )
         gctPpltau(i1)=0d0! mnu*
!
         gctPprud(i1)=-coeff*md*(ddee(i1)-ddswsw(i1) &
              +ddmd2omd(i1) - 0.5d0*ddmw2(i1)/mw2 &
              +0.5d0*(cone*(cdzul(i1)) + ddzdr(i1)) )
         gctPplud(i1)=+coeff*mu*(ddee(i1)-ddswsw(i1) &
              +ddmu2omu(i1) - 0.5d0*ddmw2(i1)/mw2 &
              +0.5d0*(cone*(cdzur(i1)) + ddzdl(i1)) )
         gctPprcs(i1)=-coeff*ms*(ddee(i1)-ddswsw(i1) &
              +ddms2oms(i1) - 0.5d0*ddmw2(i1)/mw2 &
              +0.5d0*(cone*(cdzcl(i1)) + ddzsr(i1)) )
         gctPplcs(i1)=+coeff*mc*(ddee(i1)-ddswsw(i1) &
              +ddmc2omc(i1) - 0.5d0*ddmw2(i1)/mw2 &
              +0.5d0*(cone*(cdzcr(i1)) + ddzsl(i1)) )
         gctPprtb(i1)=-coeff*mb*(ddee(i1)-ddswsw(i1) &
              +ddmb2omb(i1) - 0.5d0*ddmw2(i1)/mw2 &
              +0.5d0*(cone*(cdztl(i1)) + ddzbr(i1)) )
         gctPpltb(i1)=+coeff*mt*(ddee(i1)-ddswsw(i1) &
              +ddmt2omt(i1) - 0.5d0*ddmw2(i1)/mw2 &
              +0.5d0*(cone*(cdztr(i1)) + ddzbl(i1)) )
 
         gctPmre(i1)=0d0!mnu
         gctPmle(i1)=-coeff*me*(ddee(i1)-ddswsw(i1) &
              +ddme2ome(i1) - 0.5d0*ddmw2(i1)/mw2 &
              +0.5d0*(cone*(cdzer(i1)) + ddznel(i1)) )
         gctPmrmu(i1)=0d0!mnu
         gctPmlmu(i1)=-coeff*mm*(ddee(i1)-ddswsw(i1) &
              +ddmm2omm(i1) - 0.5d0*ddmw2(i1)/mw2 &
              +0.5d0*(cone*(cdzmr(i1)) + ddznml(i1)) )
         gctPmrtau(i1)=0d0!mnu
         gctPmltau(i1)=-coeff*mtl*(ddee(i1)-ddswsw(i1) &
              +ddmtl2omtl(i1) - 0.5d0*ddmw2(i1)/mw2 &
              +0.5d0*(cone*(cdztlr(i1)) + ddzntl(i1)) )
 
         gctPmrud(i1)=+coeff*mu*(ddee(i1)-ddswsw(i1) &
              +ddmu2omu(i1) - 0.5d0*ddmw2(i1)/mw2 &
              +0.5d0*(cone*(cdzdl(i1)) + ddzur(i1)) )
         gctPmlud(i1)=-coeff*md*(ddee(i1)-ddswsw(i1) &
              +ddmd2omd(i1) - 0.5d0*ddmw2(i1)/mw2 &
              +0.5d0*(cone*(cdzdr(i1)) + ddzul(i1)) )
         gctPmrcs(i1)=+coeff*mc*(ddee(i1)-ddswsw(i1) &
              +ddmc2omc(i1) - 0.5d0*ddmw2(i1)/mw2 &
              +0.5d0*(cone*(cdzsl(i1)) + ddzcr(i1)) )
         gctPmlcs(i1)=-coeff*ms*(ddee(i1)-ddswsw(i1) &
              +ddms2oms(i1) - 0.5d0*ddmw2(i1)/mw2 &
              +0.5d0*(cone*(cdzsr(i1)) + ddzcl(i1)) )
         gctPmrtb(i1)=+coeff*mt*(ddee(i1)-ddswsw(i1) &
              +ddmt2omt(i1) - 0.5d0*ddmw2(i1)/mw2 &
              +0.5d0*(cone*(cdzbl(i1)) + ddztr(i1)) )
         gctPmltb(i1)=-coeff*mb*(ddee(i1)-ddswsw(i1) &
              +ddmb2omb(i1) - 0.5d0*ddmw2(i1)/mw2 &
              +0.5d0*(cone*(cdzbr(i1)) + ddztl(i1)) ) 
      enddo 
      if(heavydbg) call printallgct
      end subroutine computectcoeff

      subroutine init_scalars
      use avh_olo
      implicit none
      include 'declscalars.h'
      include 'declmasses.h'
      complex*16 b11(0:2),b00(0:2),b0(0:2),s,t,v,zeroout(0:2)
      complex*16 cone,zero,ii
      common/complexunit/cone,zero,ii
      real*8 scale
      common/scalale/scale
      real*8 epsilon
      common/epsi/epsilon

      complex*16 mtprova(0:2)

      call olo_onshell( 1d-10 )
      call olo_scale( scale )
!
!      write(*,*)'>----------------------------------------------<'
!      write(*,*)'>-- WITH COMPLEXMASSES MW2, MZ2 and MH2 MUST be '
!      write(*,*)'>-- converted to real numbers whenever appearing'
!      write(*,*)'>-- as energy scales inside the scalar functions'
! b0d(smm)
      s=zero
      call olo(b0d0meme,s,cone*abs(me2) ,cone*abs(me2) )
      call olo(b0d0mmmm,s,cone*abs(mm2) ,cone*abs(mm2) )
      call olo(b0d0mlml,s,cone*abs(mtl2),cone*abs(mtl2))
      call olo(b0d0mumu,s,cone*abs(mu2) ,cone*abs(mu2) )
      call olo(b0d0mdmd,s,cone*abs(md2) ,cone*abs(md2) )
      call olo(b0d0mcmc,s,cone*abs(mc2) ,cone*abs(mc2) )
      call olo(b0d0msms,s,cone*abs(ms2) ,cone*abs(ms2) )
      call olo(b0d0mtmt,s,         mt2  ,         mt2  )
      call olo(b0d0mbmb,s,cone*abs(mb2) ,cone*abs(mb2)  )
      call olo(b0d0mwmw,s,         mw2  ,         mw2  )
      call olo(b0d0mzmz,s,         mz2  ,         mz2  )
      call olo(b0d0mhmh,s,         mh2  ,         mh2  )
      call olo(b0d0mzmh,s,         mz2  ,         mh2  )
      call olo(b0d0mwmh,s,         mw2  ,         mh2  )
      call olo(b0d0mwmz,s,         mw2  ,         mz2  )
      call olo(b0d0memw,s,cone*abs(me2) ,         mw2  )
      call olo(b0d0mmmw,s,cone*abs(mm2) ,         mw2  )
      call olo(b0d0mlmw,s,cone*abs(mtl2),         mw2  )
      call olo(b0d0mumd,s,cone*abs(mu2) ,cone*abs(md2) )
      call olo(b0d0mcms,s,cone*abs(mc2) ,cone*abs(ms2) )
      call olo(b0d0mtmb,s,         mt2  ,cone*abs(mb2) )
      call olo(b0dmw0me,dble(mw2)*cone ,s, cone*abs(me2)  )
      call olo(b0dmw0mm,dble(mw2)*cone ,s, cone*abs(mm2)  )
      call olo(b0dmw0ml,dble(mw2)*cone ,s, cone*abs(mtl2) )
      call olo(b0dme0mw,cone*abs(me2) ,s ,mw2 )
      call olo(b0dmm0mw,cone*abs(mm2) ,s ,mw2 )
      call olo(b0dml0mw,cone*abs(mtl2),s ,mw2 )
      t=zero
      call olo(b0d00me,s,t ,cone*abs(me2) )
      call olo(b0d00mm,s,t ,cone*abs(mm2) )
      call olo(b0d00ml,s,t ,cone*abs(mtl2))
      call olo(b0d00mz,s,t ,         mz2  )
      call olo(b0dmz00,dble(mz2)*cone,s,t)
      s=dble(mz2)*cone
      call olo(b0dmzmeme,s,cone*abs(me2) ,cone*abs(me2) )
      call olo(b0dmzmmmm,s,cone*abs(mm2) ,cone*abs(mm2) )
      call olo(b0dmzmlml,s,cone*abs(mtl2),cone*abs(mtl2))
      call olo(b0dmzmumu,s,cone*abs(mu2) ,cone*abs(mu2) )
      call olo(b0dmzmdmd,s,cone*abs(md2) ,cone*abs(md2) )
      call olo(b0dmzmcmc,s,cone*abs(mc2) ,cone*abs(mc2) )
      call olo(b0dmzmsms,s,cone*abs(ms2) ,cone*abs(ms2) )
      call olo(b0dmzmtmt,s,         mt2  ,         mt2  )
      call olo(b0dmzmbmb,s,cone*abs(mb2) ,cone*abs(mb2) )
      call olo(b0dmzmwmw,s,         mw2  ,         mw2  )
  
      call olo(b0dmememz,cone*abs(me2) ,cone*abs(me2) ,mz2 )
      call olo(b0dmmmmmz,cone*abs(mm2) ,cone*abs(mm2) ,mz2 )
      call olo(b0dmlmlmz,cone*abs(mtl2),cone*abs(mtl2),mz2 )
      call olo(b0dmumumz,cone*abs(mu2) ,cone*abs(mu2) ,mz2 )
      call olo(b0dmdmdmz,cone*abs(md2) ,cone*abs(md2) ,mz2 )
      call olo(b0dmcmcmz,cone*abs(mc2) ,cone*abs(mc2) ,mz2 )
      call olo(b0dmsmsmz,cone*abs(ms2) ,cone*abs(ms2) ,mz2 )
      call olo(b0dmtmtmz,cone*dble(mt2),         mt2  ,mz2 )
      call olo(b0dmbmbmz,cone*abs(mb2) ,cone*abs(mb2) ,mz2 )
      s=dble(mh2)*cone
      call olo(b0dmhmeme,s,cone*abs(me2) ,cone*abs(me2) )
      call olo(b0dmhmmmm,s,cone*abs(mm2) ,cone*abs(mm2) )
      call olo(b0dmhmlml,s,cone*abs(mtl2),cone*abs(mtl2))
      call olo(b0dmhmumu,s,cone*abs(mu2) ,cone*abs(mu2) )
      call olo(b0dmhmdmd,s,cone*abs(md2) ,cone*abs(md2) )
      call olo(b0dmhmcmc,s,cone*abs(mc2) ,cone*abs(mc2) )
      call olo(b0dmhmsms,s,cone*abs(ms2) ,cone*abs(ms2) )
      call olo(b0dmhmtmt,s,         mt2  ,         mt2  )
      call olo(b0dmhmbmb,s,cone*abs(mb2) ,cone*abs(mb2) )
      call olo(b0dmhmwmw,s,         mw2  ,         mw2  )
      call olo(b0dmhmzmz,s,         mz2  ,         mz2  )
      call olo(b0dmhmhmh,s,         mh2  ,         mh2  )
  
      call olo(b0dmememh,cone*abs(me2) ,cone*abs(me2) ,mh2 )
      call olo(b0dmmmmmh,cone*abs(mm2) ,cone*abs(mm2) ,mh2 )
      call olo(b0dmlmlmh,cone*abs(mtl2),cone*abs(mtl2),mh2 )
      call olo(b0dmumumh,cone*abs(mu2) ,cone*abs(mu2) ,mh2 )
      call olo(b0dmdmdmh,cone*abs(md2) ,cone*abs(md2) ,mh2 )
      call olo(b0dmcmcmh,cone*abs(mc2) ,cone*abs(mc2) ,mh2 )
      call olo(b0dmsmsmh,cone*abs(ms2) ,cone*abs(ms2) ,mh2 )
      call olo(b0dmtmtmh,cone*dble(mt2),         mt2  ,mh2 )
      call olo(b0dmbmbmh,cone*abs(mb2) ,cone*abs(mb2) ,mh2 )

      call olo(b0dmwmwmh, dble(mw2)*cone ,  mw2 ,  mh2 )
      call olo(b0dmwmwmz, dble(mw2)*cone ,  mw2 ,  mz2 )
      call olo(b0dmzmzmh, dble(mz2)*cone ,  mz2 ,  mh2 )
  
      s=dble(mw2)*cone
      call olo(b0dmwmumd,s,cone*abs(mu2) ,cone*abs(md2) )
      call olo(b0dmwmcms,s,cone*abs(mc2) ,cone*abs(ms2) )
      call olo(b0dmwmtmb,s,         mt2  ,cone*abs(mb2) )
      call olo(b0dmumdmw,cone*abs(mu2) ,cone*abs(md2) ,mw2)
      call olo(b0dmcmsmw,cone*abs(mc2) ,cone*abs(ms2) ,mw2)
      call olo(b0dmtmbmw,cone*dble(mt2),cone*abs(mb2) ,mw2)
      call olo(b0dmdmumw,cone*abs(md2) ,cone*abs(mu2) ,mw2)
      call olo(b0dmsmcmw,cone*abs(ms2) ,cone*abs(mc2) ,mw2)
      call olo(b0dmbmtmw,cone*abs(mb2) ,         mt2  ,mw2)
! a0
      call olo( a0dme ,cone*abs(me2) )
      call olo( a0dmm ,cone*abs(mm2) )
      call olo( a0dml ,cone*abs(mtl2))
      call olo( a0dmu ,cone*abs(mu2) )
      call olo( a0dmd ,cone*abs(md2) )
      call olo( a0dmc ,cone*abs(mc2) )
      call olo( a0dms ,cone*abs(ms2) )
      call olo( a0dmt ,         mt2  )
      call olo( a0dmb ,cone*abs(mb2) )
      call olo( a0dmw ,         mw2  )
      call olo( a0dmz ,         mz2  )
      call olo( a0dmh ,         mh2  )
! derivatives b0
      s=zero
      call b0preg(s,cone*abs(me2) ,cone*abs(me2) , b0pd0meme)
      call b0preg(s,cone*abs(mm2) ,cone*abs(mm2) , b0pd0mmmm)
      call b0preg(s,cone*abs(mtl2),cone*abs(mtl2), b0pd0mlml)
      call b0preg(s,cone*abs(mu2) ,cone*abs(mu2) , b0pd0mumu)
      call b0preg(s,cone*abs(md2) ,cone*abs(md2) , b0pd0mdmd)
      call b0preg(s,cone*abs(mc2) ,cone*abs(mc2) , b0pd0mcmc)
      call b0preg(s,cone*abs(ms2) ,cone*abs(ms2) , b0pd0msms)
      call b0preg(s,         mt2  ,         mt2  , b0pd0mtmt)
      call b0preg(s,cone*abs(mb2) ,cone*abs(mb2) , b0pd0mbmb)
      call b0preg(s,         mw2  ,         mw2  , b0pd0mwmw)
      call b0preg(s,         mz2  ,         mz2  , b0pd0mzmz)
      call b0preg(s,         mh2  ,         mh2  , b0pd0mhmh)
      call b0preg(s,s,cone*abs(me2) , b0pd00me)
      call b0preg(s,s,cone*abs(mm2) , b0pd00mm)
      call b0preg(s,s,cone*abs(mtl2), b0pd00ml)
      call b0preg(s,s,         mz2  , b0pd00mz)
      call b0preg(dble(mz2)*cone,s,s,            b0pdmz00)
      call b0preg(dble(mh2)*cone, mh2, mh2,      b0pdmhmhmh)
 
      if(abs(mu2).gt.epsilon*1d3.and.abs(md2).gt.epsilon*1d3) then
         call olo_db0(b0pd0mumd,s,cone*abs(mu2), cone*abs(md2) )
      else
         call b0preg(s,cone*abs(mu2), cone*abs(md2), b0pd0mumd )
      endif
      if(abs(mc2).gt.epsilon*1d3.and.abs(ms2).gt.epsilon*1d3) then
         call olo_db0(b0pd0mcms,s,cone*abs(mc2), cone*abs(ms2) )
      else
         call b0preg(s,cone*abs(mc2), cone*abs(ms2), b0pd0mcms )
      endif
      if(abs(mb2).gt.epsilon*1d3) then
         call olo_db0(b0pd0mtmb,s,         mt2 , cone*abs(mb2) )
      else
         call b0preg(s,         mt2 , cone*abs(mb2), b0pd0mtmb )
      endif
      call olo_db0(b0pd0mzmh,s,         mz2 ,          mh2  )
      call olo_db0(b0pd0mwmh,s,         mw2 ,          mh2  )
      call olo_db0(b0pd0mwmz,s,         mw2 ,          mz2  )
      s=dble(mz2)*cone
      call olo_db0(b0pdmzmeme,s,cone*abs(me2), cone*abs(me2) )
      call olo_db0(b0pdmzmmmm,s,cone*abs(mm2), cone*abs(mm2) )
      call olo_db0(b0pdmzmlml,s,cone*abs(mtl2),cone*abs(mtl2))
      call olo_db0(b0pdmzmumu,s,cone*abs(mu2), cone*abs(mu2) )
      call olo_db0(b0pdmzmdmd,s,cone*abs(md2), cone*abs(md2) )
      call olo_db0(b0pdmzmcmc,s,cone*abs(mc2), cone*abs(mc2) )
      call olo_db0(b0pdmzmsms,s,cone*abs(ms2), cone*abs(ms2) )
      call olo_db0(b0pdmzmtmt,s,         mt2 ,          mt2  )
      call olo_db0(b0pdmzmbmb,s,cone*abs(mb2), cone*abs(mb2) )
      call olo_db0(b0pdmzmwmw,s,         mw2 ,          mw2  )
 
      if(abs(me2).gt.epsilon*1d3) then
         call olo_db0(b0pdmememz,cone*abs(me2), cone*abs(me2) ,mz2)
      else
         call b0preg(cone*abs(me2), cone*abs(me2) ,mz2, b0pdmememz)
      endif
      if(abs(mm2).gt.epsilon*1d3) then
         call olo_db0(b0pdmmmmmz,cone*abs(mm2), cone*abs(mm2) ,mz2)
      else
         call b0preg(cone*abs(mm2), cone*abs(mm2) ,mz2, b0pdmmmmmz)
      endif
      if(abs(mtl2).gt.epsilon*1d3) then
         call olo_db0(b0pdmlmlmz,cone*abs(mtl2), cone*abs(mtl2) ,mz2)
      else
         call b0preg(cone*abs(mtl2), cone*abs(mtl2) ,mz2, b0pdmlmlmz)
      endif
      if(abs(mu2).gt.epsilon*1d3) then
         call olo_db0(b0pdmumumz,cone*abs(mu2), cone*abs(mu2) ,mz2)
      else
         call b0preg(cone*abs(mu2), cone*abs(mu2) ,mz2, b0pdmumumz)
      endif
      if(abs(md2).gt.epsilon*1d3) then
         call olo_db0(b0pdmdmdmz,cone*abs(md2), cone*abs(md2) ,mz2)
      else
         call b0preg(cone*abs(md2), cone*abs(md2) ,mz2, b0pdmdmdmz)
      endif
      if(abs(mc2).gt.epsilon*1d3) then
         call olo_db0(b0pdmcmcmz,cone*abs(mc2), cone*abs(mc2) ,mz2)
      else
         call b0preg(cone*abs(mc2), cone*abs(mc2) ,mz2, b0pdmcmcmz)
      endif
      if(abs(ms2).gt.epsilon*1d3) then
         call olo_db0(b0pdmsmsmz,cone*abs(ms2), cone*abs(ms2) ,mz2)
      else
         call b0preg(cone*abs(ms2), cone*abs(ms2) ,mz2, b0pdmsmsmz)
      endif
      if(abs(mb2).gt.epsilon*1d3) then
         call olo_db0(b0pdmbmbmz,cone*abs(mb2), cone*abs(mb2) ,mz2)
      else
         call b0preg(cone*abs(mb2), cone*abs(mb2) ,mz2, b0pdmbmbmz)
      endif
      call olo_db0(b0pdmtmtmz,cone*dble(mt2),         mt2  ,mz2)
  
      call olo_db0(b0pdmzmzmh, dble(mz2)*cone , mz2 ,mh2 )
      call olo_db0(b0pdmwmwmh, dble(mw2)*cone , mw2 ,mh2 )
      call olo_db0(b0pdmwmwmz, dble(mw2)*cone , mw2 ,mz2 )
 
      s=dble(mh2)*cone
      call olo_db0(b0pdmhmeme,s,cone*abs(me2), cone*abs(me2) )
      call olo_db0(b0pdmhmmmm,s,cone*abs(mm2), cone*abs(mm2) )
      call olo_db0(b0pdmhmlml,s,cone*abs(mtl2),cone*abs(mtl2))
      call olo_db0(b0pdmhmumu,s,cone*abs(mu2), cone*abs(mu2) )
      call olo_db0(b0pdmhmdmd,s,cone*abs(md2), cone*abs(md2) )
      call olo_db0(b0pdmhmcmc,s,cone*abs(mc2), cone*abs(mc2) )
      call olo_db0(b0pdmhmsms,s,cone*abs(ms2), cone*abs(ms2) )
      call olo_db0(b0pdmhmtmt,s,         mt2 ,          mt2  )
      call olo_db0(b0pdmhmbmb,s,cone*abs(mb2), cone*abs(mb2) )
      call olo_db0(b0pdmhmwmw,s,         mw2 ,          mw2  )
      call olo_db0(b0pdmhmzmz,s,         mz2 ,          mz2  )
  
      if(abs(me2).gt.epsilon*1d3) then
         call olo_db0(b0pdmememh,cone*abs(me2), cone*abs(me2) ,mh2)
      else
         call b0preg(cone*abs(me2), cone*abs(me2) ,mh2, b0pdmememh)
      endif
      if(abs(mm2).gt.epsilon*1d3) then
         call olo_db0(b0pdmmmmmh,cone*abs(mm2), cone*abs(mm2) ,mh2)
      else
         call b0preg(cone*abs(mm2), cone*abs(mm2) ,mh2, b0pdmmmmmh)
      endif
      if(abs(mtl2).gt.epsilon*1d3) then
         call olo_db0(b0pdmlmlmh,cone*abs(mtl2), cone*abs(mtl2) ,mh2)
      else
         call b0preg(cone*abs(mtl2), cone*abs(mtl2) ,mh2, b0pdmlmlmh)
      endif
      if(abs(mu2).gt.epsilon*1d3) then
         call olo_db0(b0pdmumumh,cone*abs(mu2), cone*abs(mu2) ,mh2)
      else
         call b0preg(cone*abs(mu2), cone*abs(mu2) ,mh2, b0pdmumumh)
      endif
      if(abs(md2).gt.epsilon*1d3) then
         call olo_db0(b0pdmdmdmh,cone*abs(md2), cone*abs(md2) ,mh2)
      else
         call b0preg(cone*abs(md2), cone*abs(md2) ,mh2, b0pdmdmdmh)
      endif
      if(abs(mc2).gt.epsilon*1d3) then
         call olo_db0(b0pdmcmcmh,cone*abs(mc2), cone*abs(mc2) ,mh2)
      else
         call b0preg(cone*abs(mc2), cone*abs(mc2) ,mh2, b0pdmcmcmh)
      endif
      if(abs(ms2).gt.epsilon*1d3) then
         call olo_db0(b0pdmsmsmh,cone*abs(ms2), cone*abs(ms2) ,mh2)
      else
         call b0preg(cone*abs(ms2), cone*abs(ms2) ,mh2, b0pdmsmsmh)
      endif
      if(abs(mb2).gt.epsilon*1d3) then
         call olo_db0(b0pdmbmbmh,cone*abs(mb2), cone*abs(mb2) ,mh2)
      else
         call b0preg(cone*abs(mb2), cone*abs(mb2) ,mh2, b0pdmbmbmh)
      endif
      call olo_db0(b0pdmtmtmh,cone*dble(mt2),         mt2  ,mh2)
  
      s=dble(mw2)*cone
      call olo_db0(b0pdmwmumd,s,cone*abs(mu2) ,cone*abs(md2) )
      call olo_db0(b0pdmwmcms,s,cone*abs(mc2) ,cone*abs(ms2) )
      call olo_db0(b0pdmwmtmb,s,         mt2  ,cone*abs(mb2) )
      if(abs(mu2).gt.epsilon*1d3.or.abs(md2).gt.epsilon*1d3) then ! OR it works for ONE
         call olo_db0(b0pdmumdmw,cone*abs(mu2) ,cone*abs(md2) ,mw2)
      else
         call b0preg(cone*abs(mu2) ,cone*abs(md2) ,mw2, b0pdmumdmw)
      endif
      if(abs(mc2).gt.epsilon*1d3.or.abs(ms2).gt.epsilon*1d3) then ! OR it works for ONE
         call olo_db0(b0pdmcmsmw,cone*abs(mc2) ,cone*abs(ms2) ,mw2)
      else
         call b0preg(cone*abs(mc2) ,cone*abs(ms2) ,mw2, b0pdmcmsmw)
      endif
      call olo_db0(b0pdmtmbmw,cone*dble(mt2),cone*abs(mb2) ,mw2)
      if(abs(mu2).gt.epsilon*1d3.or.abs(md2).gt.epsilon*1d3) then ! OR it works for ONE
         call olo_db0(b0pdmdmumw,cone*abs(md2) ,cone*abs(mu2) ,mw2)
      else
         call b0preg(cone*abs(md2) ,cone*abs(mu2) ,mw2, b0pdmdmumw)
      endif
      if(abs(mc2).gt.epsilon*1d3.or.abs(ms2).gt.epsilon*1d3) then ! OR it works for ONE
         call olo_db0(b0pdmsmcmw,cone*abs(ms2) ,cone*abs(mc2) ,mw2)
      else
         call b0preg(cone*abs(ms2) ,cone*abs(mc2) ,mw2, b0pdmsmcmw)
      endif
      call olo_db0(b0pdmbmtmw,cone*abs(mb2) ,         mt2  ,mw2)
  
      t=zero
      if(abs(me2).gt.epsilon*1d3) then
         call olo_db0(b0pdme0mw,cone*abs(me2) ,t,mw2 )
      else
         call b0preg(cone*abs(me2) ,t,mw2, b0pdme0mw)
      endif
      if(abs(mm2).gt.epsilon*1d3) then
         call olo_db0(b0pdmm0mw,cone*abs(mm2) ,t,mw2 )
      else
         call b0preg(cone*abs(mm2) ,t,mw2, b0pdmm0mw)
      endif
      if(abs(mtl2).gt.epsilon*1d3) then
         call olo_db0(b0pdml0mw,cone*abs(mtl2) ,t,mw2 )
      else
         call b0preg(cone*abs(mtl2) ,t,mw2, b0pdml0mw)
      endif
      call olo_db0(b0pdmw0me,s,t,cone*abs(me2)  )
      call olo_db0(b0pdmw0mm,s,t,cone*abs(mm2)  )
      call olo_db0(b0pdmw0ml,s,t,cone*abs(mtl2) )
! b1
 
      s=mz2
      t=zero
      call olo_b11(b11,b00,b1d00mz,b0, t,t,s )
      t=cone*abs(me2)
      call olo_b11(b11,b00,b1dmememz,b0, t,t,s )
      t=cone*abs(mm2)
      call olo_b11(b11,b00,b1dmmmmmz,b0, t,t,s )
      t=cone*abs(mtl2)
      call olo_b11(b11,b00,b1dmlmlmz,b0, t,t,s )
      t=cone*abs(mu2)
      call olo_b11(b11,b00,b1dmumumz,b0, t,t,s )
      t=cone*abs(md2)
      call olo_b11(b11,b00,b1dmdmdmz,b0, t,t,s )
      t=cone*abs(mc2)
      call olo_b11(b11,b00,b1dmcmcmz,b0, t,t,s )
      t=cone*abs(ms2)
      call olo_b11(b11,b00,b1dmsmsmz,b0, t,t,s )
      t=cone*dble(mt2)
      call olo_b11(b11,b00,b1dmtmtmz,b0, t,mt2,s )
      t=cone*abs(mb2)
      call olo_b11(b11,b00,b1dmbmbmz,b0, t,t,s )
 
      s=mh2
      t=cone*abs(me2)
      call olo_b11(b11,b00,b1dmememh,b0, t,t,s )
      t=cone*abs(mm2)
      call olo_b11(b11,b00,b1dmmmmmh,b0, t,t,s )
      t=cone*abs(mtl2)
      call olo_b11(b11,b00,b1dmlmlmh,b0, t,t,s )
      t=cone*abs(mu2)
      call olo_b11(b11,b00,b1dmumumh,b0, t,t,s )
      t=cone*abs(md2)
      call olo_b11(b11,b00,b1dmdmdmh,b0, t,t,s )
      t=cone*abs(mc2)
      call olo_b11(b11,b00,b1dmcmcmh,b0, t,t,s )
      t=cone*abs(ms2)
      call olo_b11(b11,b00,b1dmsmsmh,b0, t,t,s )
      t=cone*dble(mt2)
      call olo_b11(b11,b00,b1dmtmtmh,b0, t,mt2,s )
      t=cone*abs(mb2)
      call olo_b11(b11,b00,b1dmbmbmh,b0, t,t,s )
 
      s=mw2
      v=zero
      t=cone*abs(me2)
      call olo_b11(b11,b00,b1dme0mw ,b0, t,v,s )
      call olo_b11(b11,b00,b1d0memw ,b0, v,t,s )
      t=cone*abs(mm2)
      call olo_b11(b11,b00,b1dmm0mw ,b0, t,v,s )
      call olo_b11(b11,b00,b1d0mmmw ,b0, v,t,s )
      t=cone*abs(mtl2)
      call olo_b11(b11,b00,b1dml0mw ,b0, t,v,s )
      call olo_b11(b11,b00,b1d0mlmw ,b0, v,t,s )
      t=cone*abs(mu2)
      v=cone*abs(md2)
      call olo_b11(b11,b00,b1dmumdmw,b0, t,v,s )
      call olo_b11(b11,b00,b1dmdmumw,b0, v,t,s )
      t=cone*abs(mc2)
      v=cone*abs(ms2)
      call olo_b11(b11,b00,b1dmcmsmw,b0, t,v,s )
      call olo_b11(b11,b00,b1dmsmcmw,b0, v,t,s )
      t=cone*dble(mt2)
      v=cone*abs(mb2)
      call olo_b11(b11,b00,b1dmtmbmw,b0, t,v,s )
      call olo_b11(b11,b00,b1dmbmtmw,b0, v,mt2,s )
! derivatives of b1
      zeroout(0) = zero
      zeroout(1) = zero
      zeroout(2) = zero
      s=mz2
! b1p(m,x,y) only enter in m*dS/dp --> simply set them to zero
! if the external mass is zero 
!      call b1avo(zero          ,zero          ,s,b1pd00mz  )
      b1pd00mz = zeroout
      if(abs(me2).gt.epsilon*1d3) then
         call b1avo(cone*abs(me2) ,cone*abs(me2) ,s,b1pdmememz)
      else
         b1pdmememz = zeroout
      end if
      if(abs(mm2).gt.epsilon*1d3) then
         call b1avo(cone*abs(mm2) ,cone*abs(mm2) ,s,b1pdmmmmmz)
      else
         b1pdmmmmmz = zeroout
      end if
      if(abs(mtl2).gt.epsilon*1d3) then
         call b1avo(cone*abs(mtl2),cone*abs(mtl2),s,b1pdmlmlmz)
      else
         b1pdmlmlmz = zeroout
      end if
      if(abs(mu2).gt.epsilon*1d3) then
         call b1avo(cone*abs(mu2) ,cone*abs(mu2) ,s,b1pdmumumz)
      else
         b1pdmumumz = zeroout
      end if
      if(abs(md2).gt.epsilon*1d3) then
         call b1avo(cone*abs(md2) ,cone*abs(md2) ,s,b1pdmdmdmz)
      else
         b1pdmdmdmz = zeroout
      end if
      if(abs(mc2).gt.epsilon*1d3) then
         call b1avo(cone*abs(mc2) ,cone*abs(mc2) ,s,b1pdmcmcmz)
      else
         b1pdmcmcmz = zeroout
      end if
      if(abs(ms2).gt.epsilon*1d3) then
         call b1avo(cone*abs(ms2) ,cone*abs(ms2) ,s,b1pdmsmsmz)
      else
         b1pdmsmsmz = zeroout
      end if
      call b1avo(cone*dble(mt2),         mt2  ,s,b1pdmtmtmz)
      if(abs(mb2).gt.epsilon*1d3) then
         call b1avo(cone*abs(mb2) ,cone*abs(mb2) ,s,b1pdmbmbmz)
      else
         b1pdmbmbmz = zeroout
      end if

      s=mh2
      if(abs(me2).gt.epsilon*1d3) then
         call b1avo(cone*abs(me2) ,cone*abs(me2) ,s,b1pdmememh)
      else
         b1pdmememh = zeroout
      end if
      if(abs(mm2).gt.epsilon*1d3) then
         call b1avo(cone*abs(mm2) ,cone*abs(mm2) ,s,b1pdmmmmmh)
      else
         b1pdmmmmmh = zeroout
      end if
      if(abs(mtl2).gt.epsilon*1d3) then
         call b1avo(cone*abs(mtl2),cone*abs(mtl2),s,b1pdmlmlmh)
      else
         b1pdmlmlmh = zeroout
      end if
      if(abs(mu2).gt.epsilon*1d3) then
         call b1avo(cone*abs(mu2) ,cone*abs(mu2) ,s,b1pdmumumh)
      else
         b1pdmumumh = zeroout
      end if
      if(abs(md2).gt.epsilon*1d3) then
         call b1avo(cone*abs(md2) ,cone*abs(md2) ,s,b1pdmdmdmh)
      else
         b1pdmdmdmh = zeroout
      end if
      if(abs(mc2).gt.epsilon*1d3) then
         call b1avo(cone*abs(mc2) ,cone*abs(mc2) ,s,b1pdmcmcmh)
      else
         b1pdmcmcmh = zeroout
      end if
      if(abs(ms2).gt.epsilon*1d3) then
         call b1avo(cone*abs(ms2) ,cone*abs(ms2) ,s,b1pdmsmsmh)
      else
         b1pdmsmsmh = zeroout
      end if
      call b1avo(cone*dble(mt2),         mt2  ,s,b1pdmtmtmh)
      if(abs(mb2).gt.epsilon*1d3) then
         call b1avo(cone*abs(mb2) ,cone*abs(mb2) ,s,b1pdmbmbmh)
      else
         b1pdmbmbmh = zeroout
      end if


      s=mw2
      if(abs(me2).gt.epsilon*1d3) then
         call b1avo(cone*abs(me2) ,zero          ,s,b1pdme0mw )
      else
         b1pdme0mw = zeroout
      end if
      if(abs(mm2).gt.epsilon*1d3) then
         call b1avo(cone*abs(mm2) ,zero          ,s,b1pdmm0mw )
      else
         b1pdmm0mw = zeroout
      end if
      if(abs(mtl2).gt.epsilon*1d3) then
         call b1avo(cone*abs(mtl2),zero          ,s,b1pdml0mw )
      else
         b1pdml0mw = zeroout
      end if

!      call b1avo(zero          ,cone*abs(me2) ,s,b1pd0memw )
      b1pd0memw = zeroout

!      call b1avo(zero          ,cone*abs(mm2) ,s,b1pd0mmmw )
      b1pd0mmmw = zeroout

!      call b1avo(zero          ,cone*abs(mtl2),s,b1pd0mlmw )
      b1pd0mlmw = zeroout

      if(abs(mu2).gt.epsilon*1d3) then
         call b1avo(cone*abs(mu2) ,cone*abs(md2) ,s,b1pdmumdmw)
      else
         b1pdmumdmw = zeroout
      end if
      if(abs(md2).gt.epsilon*1d3) then
         call b1avo(cone*abs(md2) ,cone*abs(mu2) ,s,b1pdmdmumw)
      else
         b1pdmdmumw = zeroout
      end if
      if(abs(mc2).gt.epsilon*1d3) then
         call b1avo(cone*abs(mc2) ,cone*abs(ms2) ,s,b1pdmcmsmw)
      else
         b1pdmcmsmw = zeroout
      end if
      if(abs(ms2).gt.epsilon*1d3) then
         call b1avo(cone*abs(ms2) ,cone*abs(mc2) ,s,b1pdmsmcmw)
      else
         b1pdmsmcmw = zeroout
      end if

      if(abs(mb2).lt.epsilon*1d3)then
         call b1pp0m(cone*dble(mt2), mw2, b1pdmtmbmw)
      else
         call b1avo(cone*dble(mt2),cone*abs(mb2) ,s,b1pdmtmbmw)
      end if
!
      if(abs(mb2).gt.epsilon*1d3) then
         call b1avo(cone*abs(mb2) ,         mt2  ,s,b1pdmbmtmw)
      else
         b1pdmbmtmw = zeroout
      end if
! regular gamma
      s=zero
      call olo(b0dmememg,cone*abs(me2) ,cone*abs(me2) ,s)
      call olo(b0dmmmmmg,cone*abs(mm2) ,cone*abs(mm2) ,s)
      call olo(b0dmlmlmg,cone*abs(mtl2),cone*abs(mtl2),s)
      call olo(b0dmumumg,cone*abs(mu2) ,cone*abs(mu2) ,s)
      call olo(b0dmdmdmg,cone*abs(md2) ,cone*abs(md2) ,s)
      call olo(b0dmcmcmg,cone*abs(mc2) ,cone*abs(mc2) ,s)
      call olo(b0dmsmsmg,cone*abs(ms2) ,cone*abs(ms2) ,s)
      call olo(b0dmtmtmg,cone*dble(mt2),         mt2  ,s)
      call olo(b0dmbmbmg,cone*abs(mb2) ,cone*abs(mb2) ,s)
      call olo(b0d0mwmg,          zero   ,         mw2  ,s)
      call olo(b0dmwmwmg,dble(mw2)*cone  ,         mw2  ,s)
      t=cone*abs(me2)
      call olo_b11(b11,b00,b1dmememg,b0, t,t,s )
      t=cone*abs(mm2)
      call olo_b11(b11,b00,b1dmmmmmg,b0, t,t,s )
      t=cone*abs(mtl2)
      call olo_b11(b11,b00,b1dmlmlmg,b0, t,t,s )
      t=cone*abs(mu2)
      call olo_b11(b11,b00,b1dmumumg,b0, t,t,s )
      t=cone*abs(md2)
      call olo_b11(b11,b00,b1dmdmdmg,b0, t,t,s )
      t=cone*abs(mc2)
      call olo_b11(b11,b00,b1dmcmcmg,b0, t,t,s )
      t=cone*abs(ms2)
      call olo_b11(b11,b00,b1dmsmsmg,b0, t,t,s )
      t=cone*dble(mt2)
      call olo_b11(b11,b00,b1dmtmtmg,b0, t,mt2,s )
      t=cone*abs(mb2)
      call olo_b11(b11,b00,b1dmbmbmg,b0, t,t,s )
! IR gamma
      call b0pir(cone*abs(me2) ,cone*abs(me2) ,b0pdmememg)
      call b0pir(cone*abs(mm2) ,cone*abs(mm2) ,b0pdmmmmmg)
      call b0pir(cone*abs(mtl2),cone*abs(mtl2),b0pdmlmlmg)
      call b0pir(cone*abs(mu2) ,cone*abs(mu2) ,b0pdmumumg)
      call b0pir(cone*abs(md2) ,cone*abs(md2) ,b0pdmdmdmg)
      call b0pir(cone*abs(mc2) ,cone*abs(mc2) ,b0pdmcmcmg)
      call b0pir(cone*abs(ms2) ,cone*abs(ms2) ,b0pdmsmsmg)
      call b0pir(cone*dble(mt2),         mt2  ,b0pdmtmtmg)
      if(abs(dimag(mt2)).gt.epsilon) then
         call b0pcomplexmt(cone*abs(mt2),mt2,b0pdmtmtmg)
      else
         call b0pir(cone*abs(mb2) ,cone*abs(mb2) ,b0pdmbmbmg)
      end if
      call olo_db0(b0pdmwmwmg,dble(mw2),         mw2, zero )

      call b0preg(dble(zero)*cone, mw2,zero, b0pd0mwmg)
 
      call b1pir(cone*abs(me2) ,cone*abs(me2) ,b1pdmememg)
      call b1pir(cone*abs(mm2) ,cone*abs(mm2) ,b1pdmmmmmg)
      call b1pir(cone*abs(mtl2),cone*abs(mtl2),b1pdmlmlmg)
      call b1pir(cone*abs(mu2) ,cone*abs(mu2) ,b1pdmumumg)
      call b1pir(cone*abs(md2) ,cone*abs(md2) ,b1pdmdmdmg)
      call b1pir(cone*abs(mc2) ,cone*abs(mc2) ,b1pdmcmcmg)
      call b1pir(cone*abs(ms2) ,cone*abs(ms2) ,b1pdmsmsmg)

      if(abs(dimag(mt2)).lt.epsilon) then
         call b1pir(cone*dble(mt2),         mt2  ,b1pdmtmtmg)
      else
         call b1pcomplexmt(cone*dble(mt2),  mt2,  b1pdmtmtmg)
      end if

      call b1pir(cone*abs(mb2) ,cone*abs(mb2) ,b1pdmbmbmg)

      end subroutine init_scalars

! routines for scalar integrals (also with olo)
      subroutine b0pcomplexmt(p2in ,m0 ,out)
        implicit none
        complex*16 p2in,m0,out(0:2)
        real*8 mm,gg,aa
        complex*16 cone,zero,ii
        common/complexunit/cone,zero,ii
        if(dimag(p2in).gt.1d-20)then
           write(*,*)'improper call to b0pcomplexmt'
           stop
        endif
        out=zero
        mm=sqrt(dble(m0))
        gg=-dimag(m0)/mm
        aa=gg/mm
        out(0)=(cone-ii*aa)*log((ii*aa-cone)/ii/aa)-cone
        out(0)=out(0)/mm/mm
      end subroutine b0pcomplexmt

      subroutine b1pcomplexmt(p2in ,m0 ,out)
        implicit none
        complex*16 p2in,m0,out(0:2)
        real*8 mm,gg,aa
        complex*16 cone,zero,ii
        common/complexunit/cone,zero,ii
        if(dimag(p2in).gt.1d-20)then
           write(*,*)'improper call to b1pcomplexmt'
           stop
        endif
        out=zero
        mm=sqrt(dble(m0))
        gg=-dimag(m0)/mm
        aa=gg/mm
        out(0)=-1.5d0+ii*aa+(1d0-aa**2-2d0*ii*aa)*log((ii*aa-cone)/ii/aa)
        out(0)=-out(0)/mm/mm
      end subroutine b1pcomplexmt
      subroutine b1pp0m(p2in, m12, out)
        implicit none
        complex*16 p2in,m12,out(0:2),aa,bb
        complex*16 cone,zero,ii
        common/complexunit/cone,zero,ii
        if(dimag(p2in).gt.1d-20)then
           write(*,*)'improper call to b1pp0m'
           stop
        endif
        out=zero
        aa=m12/p2in
        bb=p2in/m12
        out(0)=-aa/p2in+cone/2d0/p2in-(aa-cone)*log(cone-bb)*aa/p2in
      end subroutine b1pp0m
      subroutine b1avo(p2in,m02in,m12in,out)
        implicit none
        complex(kind= 8) p2in,m02in,m12in,out(0:2)
        complex(kind= 8) p2conv,m02conv
        complex(kind=16) p2,m02,m12,outpr
        complex(kind=16) cone
        parameter(cone=(1q0,0q0))
        complex(kind=16) ii
        parameter(ii=(0q0,1q0))
        complex(kind=16) zero
        parameter(zero=(0q0,0q0))
        real(kind=16) eps
        parameter(eps=1q-30)
        complex(kind=16) qda,qdb,qdc,qdr1,qdr2,cquad1,cquad2
        complex(kind=16) x1,x2,y1,y2,f1x1,f1x2,int1,int2,in21,in22,coeff
        
        complex(kind=16) f3x1,f3x2,dd,ss,pp2
        
        complex(kind=16) r8qda,r8qdb,r8qdc,r8qdr1,r8qdr2,r8cquad1,r8cquad2
        
        integer i1
        
        real(kind=16) mprec
        integer :: ini=0
        save ini
        
        complex(kind=16) coeffp2,coeffm02,coeffm12
        
        real(kind=8) oloscale
        parameter(oloscale=1d-10)
        
        if(ini.eq.0) then
           ini=1
           write(*,*)'!-------------------------------------------------------!'
           write(*,*)'! This subroutine computes the derivatives of the B1    !'
           write(*,*)'! functions needed in the wave function renormalization !'
           write(*,*)'! counterterms. NB it is not meant to be general:       !'
           write(*,*)'! p2 , m02 , m12 => Im(p2)=0, m12=mz,mw,mh,0            !'
           write(*,*)'! p2 , p2 , 0 => IR singular                            !'
           write(*,*)'! 0  , m02, m12 IS NOT COMPUTED as we need p2*dB1/dp2   !'
           write(*,*)'!-------------------------------------------------------!'
        end if
        
        
        mprec=1q-5
        do i1=0,2
           out(i1)  =(0d0,0d0)
        end do
        outpr=(0q0,0q0)
        
        ! 0 move the output to 0:2 and init all entries to (0d0,0d0)
        
        ! 1
        ! TO DO : as in olo_on_shell import the parameter AND set to
        ! zero all the smaller entries (a coefficient to multiply in
        ! the lines below
        coeffp2=cone ; coeffm02=cone; coeffm12=cone;
        if(abs(p2in ).lt.oloscale) coeffp2 =zero
        if(abs(m02in).lt.oloscale) coeffm02=zero
        if(abs(m12in).lt.oloscale) coeffm12=zero
        
        
        ! 2 check if p2=0 -> out=0 return
        !   check if Im(p2)=/=0 -> ERROR return
        
        p2 =p2in *coeffp2
        m02=m02in*coeffm02
        m12=m12in*coeffm12
        
        
        !  write(*,*)'p2 ',p2
        !  write(*,*)'m02',m02
        !  write(*,*)'m12',m12
        
        ! 3
        ! before the quadrati LOOK FOR THE SPECIAL CONFIGURATIONS
        ! p2 0 0
        ! p2 p2 0  -> IR (add the POLE PART)
        ! p2 m02 0 -> re(m02)=p2 --> b1complexmt
        ! p2 0 p2 --> special regular case
        
        if(imagpart(p2).ne.0q0) then
           write(*,*)'the p2 value in DB1 must be real, stop'
           stop
        end if
        
        if(realpart(p2).eq.0q0) then
           return ! out is zero
        endif
        
        if(m02.eq.zero.and.m12.eq.zero) then
           out(0)=1d0/2d0/p2
           return
        endif
        
        
        if(realpart(p2).eq.realpart(m02).and.m12.eq.zero) then
           
           if(imagpart(m02).eq.zero) then
              
              p2conv =p2
              m02conv=m02
        
              !        write(*,*)'p2conv ',p2conv
              !        write(*,*)'m02conv',m02conv

              
              call b1pir(p2conv,m02conv,out)
              return
           else
              p2conv =p2
              m02conv=m02
              call b1pcomplexmt(p2conv,m02conv,out)
              return
           end if
        end if
        

        if(realpart(p2).eq.realpart(m12).and.m02.eq.zero) then
           if(imagpart(m12).eq.zero) then
              out(0) = -1d0/2d0/p2
              return
           end if
        end if
        
        ! 4 all the other configurations are handeld below
        
        qda= p2
        qdb=-(p2-m02+m12)
        qdc=+m12 + ii*eps
        
        call q0qcroots(qda,qdb,qdc,qdr1,qdr2,cquad1,cquad2)
        
        
        x1=qdr1
        x2=qdr2
        
        
        !  write(*,*)'x1,x2',x1,x2
        
        if(x1.eq.x2) then
           
           coeff=  - cone/p2
           call expand_deg(x1,outpr)
           outpr=coeff*outpr
           out(0)=outpr
           return
        endif
        
        if(abs(x1-x2)/abs(x1+x2).lt.mprec) then
           
           coeff=   cone/p2
           dd=x1-x2
           ss=x1+x2
           pp2=p2
           
           !     write(*,*)'dd',dd
           !     write(*,*)'ss',ss
           !     write(*,*)'p2',pp2
           
           outpr=-(dd**20q0*((14q0 - ss)/(-2q0 + ss)**19 + 228q0/ss**20             &
                &        + 24q0/ss**19 + ss**(-18)))/(95760.q0*pp2) -                    &
                &        (dd**18*((38q0 - 3q0*ss)/(-2q0 + ss)**17 + 544q0/ss**18         &
                &        + 64q0/ss**17 + 3q0/ss**16))/(186048.q0*pp2) -                  &
                &        (dd**16*((34q0 - 3q0*ss)/(-2q0 + ss)**15 + 420q0/ss**16         &
                &        + 56q0/ss**15 + 3q0/ss**14))/(114240.q0*pp2) -                  &
                &        (dd**14*((10q0 - ss)/(-2q0 + ss)**13 + 104q0/ss**14             &
                &        + 16q0/ss**13 + ss**(-12)))/(21840.q0*pp2) -                    &
                &        (dd**12*((26q0 - 3q0*ss)/(-2q0 + ss)**11 + 220q0/ss**12         &
                &        + 40q0/ss**11 + 3q0/ss**10))/(34320.q0*pp2) +                   &
                &        (dd**4*(6q0 - 5q0*ss))/(15.q0*pp2*(-2q0 + ss)**3*ss**4)         &
                &        + (dd**6*(80q0 - 7q0*ss*(24q0 + ss*(-18q0 + 5*ss))))            &
                &        /(105.q0*pp2*(-2q0 + ss)**5*ss**6) +                            &
                &        (dd**8*(112q0 - 3q0*ss*(120q0 + ss*(-160q0 + 7q0*ss*(16q0       &
                &        + (-6q0 + ss)*ss)))))/(63.q0*pp2*(-2q0 + ss)**7*ss**8) +        &
                &        (dd**10*(2304q0 - 11q0*ss*(896q0 + 3q0*ss*(-560q0               &
                &        + ss*(600q0 + ss*(-400q0 + ss*(168q0                            &
                &        + ss*(-42q0 + 5*ss))))))))/(495.q0*pp2*(-2q0                    &
                &        + ss)**9*ss**10) +                                              &
                &        (dd**2*(4q0 - 6q0*(-1q0 + ss)*ss                                &
                &        - 3q0*(-2q0 + ss)*ss**2*Log((-2q0 + ss)/ss)))                   &
                &        /(12.q0*pp2*(-2q0 + ss)*ss**2) +                                &
                &        (10q0 - 6q0*ss + (-4q0 + (8q0 - 3q0*ss)*ss)*Log((-2q0           &
                &        + ss)/ss))/(4.q0*pp2)                                                   
           
           out(0)=outpr
           
           !     write(*,*)'??????????????????',out
           
           return
        endif
        
        coeff=   cone/p2/(x1-x2)
        
        if(abs(x1).lt.10q0.and.abs(x2).lt.10q0) then
           
           f1x1= - cone - x1*log((x1-cone)/x1)
           f1x2= - cone - x2*log((x2-cone)/x2)
           
           outpr=coeff*((x1-cone)**2*f1x1-(x2-cone)**2*f1x2-(x1-x2)/2q0)
           
        elseif(abs(x1).gt.10q0.and.abs(x2).gt.10q0) then

           !     f1x1= - cone - x1*log((x1-cone)/x1)
           !     f1x2= - cone - x2*log((x2-cone)/x2)
           !
           !     write(*,*)'unstable old', &
           !          &        coeff*((x1-cone)**2*f1x1-(x2-cone)**2*f1x2-(x1-x2)/2q0)
           !
           !     f3x1 = -x1**3* log((x1 - cone)/x1) - x1**2 - x1/2q0 - cone/3q0
           !     f3x2 = -x2**3* log((x2 - cone)/x2) - x2**2 - x2/2q0 - cone/3q0
           !
           !
           !     outpr=coeff*(f3x1 - f3x2 + f3x1/x1**2 - (2q0* f3x1)/x1   &
           !          &              - f3x2/x2**2 + (2q0*f3x2)/x2 )                &
           !          &        + (-((x1 + x2)/(3q0* x1**2 * x2**2))                &
           !          &           + cone/(6q0* x1*x2))*cone/p2                     
           !
           !
           !
           !     write(*,*)'unstable new',outpr
           
           ! with the expansion
           f3x1=(0q0,0q0)
           f3x2=(0q0,0q0)
           call expand(x1,f3x1)
           call expand(x2,f3x2)
           
           
           outpr=coeff*(f3x1 - f3x2 + f3x1/x1**2 - (2q0* f3x1)/x1  &
                &              - f3x2/x2**2 + (2q0*f3x2)/x2 )           &
                &        + (-((x1 + x2)/(3q0* x1**2 * x2**2))           &
                &           + cone/(6q0* x1*x2))*cone/p2                  
           
           
           !     write(*,*)'expanded new',outpr
           
           
        elseif(abs(x1).lt.10q0.and.abs(x2).gt.10q0) then
           
           f1x1= - cone - x1*log((x1-cone)/x1)
           call expand(x2,f3x2)
           outpr=coeff*(                           &
                & (2q0/3q0)*cone + f1x1 - f3x2 - x1/2q0 &
                & - 2q0* f1x1* x1 + f1x1* x1**2         &
                & - cone/( 3q0* x2**2) - f3x2/x2**2 +   &
                & cone/(6q0* x2) + (2q0* f3x2)/x2 )      
           
           
        elseif(abs(x1).gt.10q0.and.abs(x2).lt.10q0) then
           
           f1x2= - cone - x2*log((x2-cone)/x2)
           call expand(x1,f3x1)
           
           outpr=coeff*(                                                 &
                & - (2q0/3q0)*cone - f1x2 + f3x1 + cone/(3q0* x1**2)              &
                & + f3x1/x1**2 - cone/(6q0* x1) - (                               &
                &        2q0*  f3x1)/x1 + x2/2q0 + 2q0* f1x2* x2 - f1x2* x2**2 )  
        endif
        out(0)=outpr
        
        ! write(*,*)'out',out
        
      end subroutine b1avo
      
      subroutine expand_deg(yy,out)
        implicit none
        complex(kind=16) yy,x,out
        x=1q0/yy
        out= x**2/12.q0 + x**3/15.q0 + x**4/20.q0 +          &
             &  (4q0*x**5)/105.q0 + (5q0*x**6)/168.q0 +            &
             &  x**7/42.q0 + (7q0*x**8)/360.q0 +                   &
             &  (8q0*x**9)/495.q0 + (3q0*x**10)/220.q0 +           &
             &  (5q0*x**11)/429.q0 + (11q0*x**12)/1092.q0 +        &
             &  (4q0*x**13)/455.q0 + (13q0*x**14)/1680.q0 +        &
             &  (7q0*x**15)/1020.q0 + (5q0*x**16)/816.q0 +         &
             &  (16q0*x**17)/2907.q0 + (17q0*x**18)/3420.q0 +      &
             &  (3q0*x**19)/665.q0 + (19q0*x**20)/4620.q0 +        &
             &  (20q0*x**21)/5313.q0 + (7q0*x**22)/2024.q0 +       &
             &  (11q0*x**23)/3450.q0 + (23q0*x**24)/7800.q0 +      &
             &  (8q0*x**25)/2925.q0 + (25q0*x**26)/9828.q0 +       &
             &  (13q0*x**27)/5481.q0 + (9q0*x**28)/4060.q0 +       &
             &  (28q0*x**29)/13485.q0 + (29q0*x**30)/14880.q0 +    &
             &  (5q0*x**31)/2728.q0 + (31q0*x**32)/17952.q0 +      &
             &  (32q0*x**33)/19635.q0 + (11q0*x**34)/7140.q0 +     &
             &  (17q0*x**35)/11655.q0 + (35q0*x**36)/25308.q0 +    &
             &  (12q0*x**37)/9139.q0 + (37q0*x**38)/29640.q0 +     &
             &  (19q0*x**39)/15990.q0 + (13q0*x**40)/11480.q0 +    &
             &  (40q0*x**41)/37023.q0 + (41q0*x**42)/39732.q0 +    &
             &  (7q0*x**43)/7095.q0 + (43q0*x**44)/45540.q0 +      &
             &  (44q0*x**45)/48645.q0 + (15q0*x**46)/17296.q0 +    &
             &  (23q0*x**47)/27636.q0 + (47q0*x**48)/58800.q0 +    &
             &  (16q0*x**49)/20825.q0 + (49q0*x**50)/66300.q0 +    &
             &  (25q0*x**51)/35139.q0 + (17q0*x**52)/24804.q0 +    &
             &  (52q0*x**53)/78705.q0 + (53q0*x**54)/83160.q0 +    &
             &  (9q0*x**55)/14630.q0 + (55q0*x**56)/92568.q0 +     &
             &  (56q0*x**57)/97527.q0 + (19q0*x**58)/34220.q0 +    &
             &  (29q0*x**59)/53985.q0 + (59q0*x**60)/113460.q0 +   &
             &  (20q0*x**61)/39711.q0 + (61q0*x**62)/124992.q0 +   &
             &  (31q0*x**63)/65520.q0 + (21q0*x**64)/45760.q0 +    &
             &  (64q0*x**65)/143715.q0 + (65q0*x**66)/150348.q0 +  &
             &  (11q0*x**67)/26197.q0 + (67q0*x**68)/164220.q0 +   &
             &  (68q0*x**69)/171465.q0 + (23q0*x**70)/59640.q0 +   &
             &  (35q0*x**71)/93294.q0 + (71q0*x**72)/194472.q0 +   &
             &  (24q0*x**73)/67525.q0 + (73q0*x**74)/210900.q0 +   &
             &  (37q0*x**75)/109725.q0 + (25q0*x**76)/76076.q0 +   &
             &  (76q0*x**77)/237237.q0 + (77q0*x**78)/246480.q0 +  &
             &  (13q0*x**79)/42660.q0 + (79q0*x**80)/265680.q0 +   &
             &  (80q0*x**81)/275643.q0 + (27q0*x**82)/95284.q0 +   &
             &  (41q0*x**83)/148155.q0 + (83q0*x**84)/307020.q0 +  &
             &  (28q0*x**85)/105995.q0 + (85q0*x**86)/329208.q0 +  &
             &  (43q0*x**87)/170346.q0 + (29q0*x**88)/117480.q0 +  &
             &  (88q0*x**89)/364455.q0 + (89q0*x**90)/376740.q0 +  &
             &  (15q0*x**91)/64883.q0 + (91q0*x**92)/402132.q0 +   &
             &  (92q0*x**93)/415245.q0 + (31q0*x**94)/142880.q0 +  &
             &  (47q0*x**95)/221160.q0 + (95q0*x**96)/456288.q0 +  &
             &  (32q0*x**97)/156849.q0 + (97q0*x**98)/485100.q0 +  &
             &  (49q0*x**99)/249975.q0 + (33q0*x**100)/171700.d0                              
        ! end sub q0*x
      end subroutine expand_deg
      
      subroutine expand(in,out)
        implicit none
        complex(kind=16) in,out
        integer ini
        data ini/0/
        save ini
        integer nmax,i1
        parameter(nmax=200)
        real(kind=16) vecc(nmax)
        integer vece(nmax)
        save vecc,vece
        complex(kind=16) cone
        parameter(cone=(1q0,0q0))
        real(kind=16) check
        
        if(ini.eq.0) then
           ini=1
           do i1=1,nmax
              vece(i1)=i1
              vecc(i1)=i1*1q0 +3q0
           end do
        endif
        
        out=(0q0,0q0)
        do i1=1,nmax
           
           check=realpart(cone/(vecc(i1)*in**vece(i1)))
           if(check.ne.check) return
           check=imagpart(cone/(vecc(i1)*in**vece(i1)))
           if(check.ne.check) return
           
           out= out + cone/(vecc(i1)*in**vece(i1))
        end do
        
      end subroutine expand
      
      subroutine q0qcroots(qda,qdb,qdc,qdr1,qdr2,cquad1,cquad2)
        implicit none
        complex(kind=16) qda,qdb,qdc,qdr1,qdr2,cquad1,cquad2
        complex(kind=16) qa,qb,qc,qr1,qr2
        real(kind=16) si
        complex(kind=16) sqdisc,argsq
        complex(kind=16) qtmp
        complex(kind=16) cone
        parameter(cone=(1q0,0q0))
        complex(kind=16) ii
        parameter(ii=(0q0,1q0))
        !
        qa= qda
        qb= qdb
        qc= qdc
        
        if (abs(qda).gt.0.q0) then
           if (abs(qb).gt.0.q0) then
              argsq=1.q0 * &
                   &      (1.q0-2.q0*sqrt(qa*qc)/qb)*(1.q0+2.q0*sqrt(qa*qc)/qb) 
              argsq =cone*realpart(argsq)+ii*imagpart(- 4.q0*qa*qc/qb/qb)
              sqdisc = qb*sqrt(argsq)
              si = 1.q0
              if (realpart(conjg(qb)*sqdisc).lt.0.q0) si = -1.q0
              
              !      write(*,*)'si',si
              
           else
              argsq=1.q0 * &
                   &           (qb-2.q0*sqrt(qa*qc))*(qb+2.q0*sqrt(qa*qc))
              argsq = realpart(argsq)*cone+ii*imagpart(- 4.q0*qa*qc)
              sqdisc = sqrt(argsq)
              si = 1.q0
              if (realpart(conjg(qb)*sqdisc).lt.0.q0) si = -1.q0
           endif
           
           qtmp = -0.5q0*(qb + si*sqdisc)
           qr1 = qtmp/qa
           qr2 = qc/qr1/qa
        else
           if (abs(qdb).gt.0.q0) then
              qr1 = -qdc/qdb
              qr2 = qr1
           else
              qr1 = (0.q0,0.q0)
              qr2 = (0.q0,0.q0)
           endif
        endif
        cquad1= qa*qr1*qr1 + qb*qr1 + qc
        cquad2= qa*qr2*qr2 + qb*qr2 + qc
        qdr1 = qr1
        qdr2 = qr2
        
        ! write(*,*)'cquad1,cquad2',cquad1,cquad2
        
        return
      end subroutine q0qcroots

      subroutine b0preg(p2i,m02i,m12i,b0peps)
      implicit none
      complex*16 p2i,m02i,m12i
      complex*16 b0peps(0:2)
      complex*16 p2,m02,m12
      real*8 epsilon
      common/epsi/epsilon
      real*8 pi,pis
      common/pigreco/pi,pis
      complex*16 cone,zero,ii
      common/complexunit/cone,zero,ii
      complex*16 m0m1
      complex*16 r1,r2
      complex*16 a,b,c
      complex*16 la
      complex*16 cquad1,cquad2     
      complex*16 tmp1,tmp2
      p2 = dble(p2i)*cone
      if (abs(m02i).lt.abs(m12i)) then
          m02 = m02i
          m12 = m12i
      else
          m02 = m12i
          m12 = m02i
      endif
!
! special cases: 
! p2 = 0
!
      if (abs(p2).lt.1.d-20) then
!
!* p2=m02=m12=0
!
          if (abs(m02).lt.1.d-20.and.abs(m12).lt.1.d-20) then
              b0peps(2) = zero
              b0peps(1) = zero
              b0peps(0) = zero
!
!* p2=m12=0
!
          elseif (abs(m02).lt.1.d-20) then
              b0peps(2) = zero
              b0peps(1) = zero
              b0peps(0) = 1.d0/(2.d0*m12)
!
!* p2=0, m02=m12
!
          elseif (abs(m12-m02).lt.1.d-20) then
              b0peps(2) = zero
              b0peps(1) = zero
              b0peps(0) = 1.d0/(6.d0*m02)

          else
!
!* p2=0, m02 << m12
!
              if (abs(m02/m12).gt.1.d-4) then

                 if (abs(dimag(m02i)).lt.epsilon) then
                    m02 = m02i - ii*epsilon
                 else
                    m02 = m02i
                 endif
                 if (abs(dimag(m12i)).lt.epsilon) then
                    m12 = m12i - ii*epsilon
                 else
                    m12 = m12i
                 endif
                 tmp1=m02
                 tmp2=m12
                 if (abs(m02).lt.abs(m12)) then
                    m02 = tmp1
                    m12 = tmp2
                 else
                    m02 = tmp2
                    m12 = tmp1
                 endif
!                                 
!                                  
                 if (abs(m02/m12).gt.1.d-4) then
!                                                                   
                    b0peps(0)=-(  (2.d0*m12*log(-m02) - m02)*m02 &
                              -(2.d0*m02*log(-m12) - m12)*m12 )/ &
                              ( 2.d0*(m02-m12)**3)
                 endif
!
!* p2=0, m02 << m12
!
              else
                 if (abs(dimag(m02i)).lt.epsilon) then
                    m02 = m02i - ii*epsilon
                 else
                    m02 = m02i
                 endif
                 if (abs(dimag(m12i)).lt.epsilon) then
                    m12 = m12i - ii*epsilon
                 else
                    m12 = m12i
                 endif
                  b0peps(0) = +1.d0/(2.d0*m12) &
     &                - m02*(-3.d0*cone - 2.d0*ii*pi - 2.d0*log(m02) &
     &                  + 2.d0*log(-m12))/(2.d0*m12**2) &
     &                + m02**2*(-5.d0 - 6.d0*ii*pi - 6.d0*log(m02) &
     &                  + 6.d0*log(-m12))/(2.d0*m12**3) &
     &                + m02**3*(-7.d0 - 12.d0*ii*pi - 12.d0*log(m02) &
     &                  + 12.d0*log(-m12))/(2.d0*m12**4) &
     &                + m02**4*(-9.d0 - 20.d0*ii*pi - 20.d0*log(m02) &
     &                  + 20.d0*log(-m12))/(2.d0*m12**5) &
     &                + m02**5*(-11.d0 - 30.d0*ii*pi - 30.d0*log(m02) &
     &                  + 30.d0*log(-m12))/(2.d0*m12**6)

              endif

              b0peps(2) = zero
              b0peps(1) = zero
          endif
!*
!* m02 = 0
!*
      elseif (abs(m02).lt.1.d-20) then
          call b0pm10(p2,m12,b0peps)
!*
!* p2 = m02, p2 << m12
!*
      elseif (abs(p2-m02).lt.1.d-20.and.abs(p2/m12).lt.1.d-4) then

          a  = p2/m12
          la = log(a)
          b0peps(0) = &
     &       (a*(1.d0/2.*cone &
     &      - a*((-11.d0/6.d0    -       la) &
     &      - a*((-89.d0/12.d0   - 5.d0* la) &
     &      - a*((-589.d0/20.d0  - 21.d0*la) &
     &      - a*((-1732.d0/15.d0 - 84.d0*la)  &
     &      - a*(-18899.d0/42.d0 - 330.d0*la) ))))) &
     &      )/p2
          b0peps(2)=zero
          b0peps(1)=zero
!
! general cases
!
      else

          m0m1=sqrt(m02*m12)
         
          a = cone
          b = (m02+m12-p2-ii*epsilon)/m0m1
          c = cone
         
          call qcroots(a,b,c,r1,r2,cquad1,cquad2)
          r1 = -r1
          r2 = -r2
        
          b0peps(0) = -(m02-m12)/p2/p2*log(m12/m02)/2.d0 &
     &           + m0m1/p2/p2*(r2-r1)*log(r1) &
     &           -( cone + (r1**2+cone)/(r1**2-cone)*log(r1) )/p2
          b0peps(2)=zero
          b0peps(1)=zero
      endif
      return
      end subroutine b0preg
! subroutine for the derivative of the b0(p2,m02,m12)
! when m12 = 0
! according to Denner hep-ph/0709.1075 eq. (4.25)
!
      subroutine b0pm10(p2i,m02,b0peps)
      implicit none
      complex*16 p2i,m02
      complex*16 b0peps(0:2)
      complex*16 p2
      real*8 pi,pis
      common/pigreco/pi,pis
      complex*16 cone,zero,ii
      common/complexunit/cone,zero,ii
      real*8 epsilon
      common/epsi/epsilon
      p2 = dble(p2i)*cone
!
! m02 = m12 = 0
!
      if(abs(m02).lt.1.d-20) then
          b0peps(0)= -1.d0/p2
          b0peps(2) = zero
          b0peps(1) = zero
!
! m12 = 0, p2 << m02
!
      elseif (abs(p2/m02).lt.1.d-4) then

          b0peps(0) = &
     &         (  60*p2**5 &
     &           + m02*(70*p2**4 & 
     &           + m02*(84*p2**3  &
     &           + m02*(105.d0*p2**2  &
     &           + m02*(140.d0*p2  &
     &           + 210.d0*m02 ) )))) &
     &           /(420.d0*m02**6)
          b0peps(2) = zero
          b0peps(1) = zero
      else
!
! m12 = 0
!
          if (dble(m02).le.dble(p2)) then
             if (abs(dimag(m02)).lt.epsilon) then
                m02 = m02 - ii*epsilon
             else
                m02 = m02
             endif
              b0peps(0) = conjg(- m02*log(cone-p2/m02)/(p2**2)-cone/p2)
          else
              b0peps(0) = - m02*log(cone-p2/m02)/(p2**2)-cone/p2
          endif
          b0peps(2) = zero
          b0peps(1) = zero
      
      endif

      return
      end subroutine b0pm10
!
! subroutine for precise calculation of the roots of quadratic equations
!
      subroutine qcroots(qda,qdb,qdc,qdr1,qdr2,cquad1,cquad2)
      implicit none
      complex*16 qda,qdb,qdc,qdr1,qdr2,cquad1,cquad2
      complex*16 qa,qb,qc,qr1,qr2
      real*8 si
      complex*16 sqdisc,argsq
      complex*16 qtmp
!
      qa= qda
      qb= qdb
      qc= qdc
      if (abs(qda).gt.0.d0) then
         if (abs(qb).gt.0.d0) then
            argsq=1.d0 * &
                 (1.d0-2.d0*sqrt(qa*qc)/qb)*(1.d0+2.d0*sqrt(qa*qc)/qb) 
            argsq = dcmplx(dble(argsq),dimag(- 4.d0*qa*qc/qb/qb))
            sqdisc = qb*sqrt(argsq)
            si = 1.d0
            if (dble(dconjg(qb)*sqdisc).lt.0.d0) si = -1.d0
         else
            argsq=1.d0 * &
                 (qb-2.d0*sqrt(qa*qc))*(qb+2.d0*sqrt(qa*qc))
            argsq = dcmplx(dble(argsq),dimag(- 4.d0*qa*qc))
            sqdisc = sqrt(argsq)
            si = 1.d0
            if (dble(dconjg(qb)*sqdisc).lt.0.d0) si = -1.d0
         endif

         qtmp = -0.5d0*(qb + si*sqdisc)
         qr1 = qtmp/qa
         qr2 = qc/qr1/qa
      else
         if (abs(qdb).gt.0.d0) then
            qr1 = -qdc/qdb
            qr2 = qr1
         else
            qr1 = (0.d0,0.d0)
            qr2 = (0.d0,0.d0)
         endif
      endif
      cquad1= qa*qr1*qr1 + qb*qr1 + qc
      cquad2= qa*qr2*qr2 + qb*qr2 + qc
      qdr1 = qr1
      qdr2 = qr2
      return
      end subroutine qcroots
!
!* subroutine for the singular b0p (p2,lambda,m12)
!
      subroutine b0pir(p2i,m12,b0peps)
      implicit none
      complex*16 p2i,m12
      complex*16 b0peps(0:2)
      complex*16 p2
      real*8 lambda2
      common/photmass/lambda2
      real*8 pi,pis
      common/pigreco/pi,pis
      real*8 deltauv,mudim,dimf1,dimf2,eulergamma
      common/dimreg/deltauv,mudim,dimf1,dimf2,eulergamma
      complex*16 cone,zero,ii
      common/complexunit/cone,zero,ii
      p2  = dble(p2i)*cone
      if (abs(p2).lt.1.d-20) then
      
          b0peps(2) = zero
          b0peps(1) = zero
          b0peps(0) = zero
          return
       endif
!*
!* eq. 5.51 bardin - passarino
!*
      b0peps(2) = zero
      b0peps(1) = - 0.5d0/m12
      b0peps(0) = - ( ( dimf1 + 2.d0 )*cone &
                         - log(m12/(mudim**2)) )/(2d0*m12)


      return
      end subroutine b0pir
!
!* subroutine for the singular b1p (p2,lambda,m12)
!
      subroutine b1pir(p2i,m12,b1peps)
      implicit none
      complex*16 p2i,m12
      complex*16 b1peps(0:2)
      complex*16 p2
      real*8 lambda2
      common/photmass/lambda2

      real*8 pi,pis
      common/pigreco/pi,pis

      real*8 deltauv,mudim,dimf1,dimf2,eulergamma
      common/dimreg/deltauv,mudim,dimf1,dimf2,eulergamma

      complex*16 cone,zero,ii
      common/complexunit/cone,zero,ii
      p2 = dble(p2i)*cone
      if(abs(p2).lt.1.d-20)then

          b1peps(2) = zero
          b1peps(1) = zero
          b1peps(0) = zero
          return

      else
!
! eq. 5.54 bardin - passarino
!
          b1peps(2) = zero
          b1peps(1) = 1d0/2d0/m12
          b1peps(0) = + ( ( dimf1 + 3.d0 )*cone &
                          - log(m12/(mudim**2)) )/(2.d0*m12)

      endif

      return
      end subroutine b1pir

! tadpole
      subroutine deltatad(out,conv)
      implicit none
      include 'declmasses.h'
      include 'declscalars.h'
      complex*16 cone,zero,ii
      common/complexunit/cone,zero,ii
      complex*16 sw,cw,sw2,cw2,sw4,cw4,alpha,el2,alsu4pi
      common/couplings/sw,sw2,sw4,cw,cw2,cw4,alpha,el2,alsu4pi
      complex*16 out(0:2),conv,coeff
      real*8 pi,pis
      common/pigreco/pi,pis           
      complex*16 chzz,chww,chhh,chxx,chff,chuz,chpm,chee,chmm
      complex*16  chll,chuu,chdd,chcc,chss,chbb,chtt
      real*8 nc
      integer i1
! setting the parameters
      coeff= -alsu4pi/sqrt(4*pi*alpha)
      nc   = 3d0
      chzz = mw/sw/cw2
      chww = mw/sw
      chhh = - 3d0*mh2/mw/2d0/sw
      chxx = -     mh2/mw/2d0/sw
      chff = -     mh2/mw/2d0/sw
      chuz = - mw /2d0/sw/cw2
      chpm = - mw /2d0/sw
      chee = - me /2d0/sw/mw
      chmm = - mm /2d0/sw/mw
      chll = - mtl/2d0/sw/mw
      chuu = - mu /2d0/sw/mw
      chcc = - mc /2d0/sw/mw
      chtt = - mt /2d0/sw/mw
      chdd = - md /2d0/sw/mw
      chss = - ms /2d0/sw/mw
      chbb = - mb /2d0/sw/mw
 
      do i1=0,2
         out(i1)= coeff*( &
     &         2d0*chzz*a0dmz(i1)    +4d0*chww*a0dmw(i1) &
     &        +4d0*me*chee*a0dme(i1) +4d0*mm*chmm*a0dmm(i1) & 
     &                               +4d0*mtl*chll*a0dml(i1) &
     &        + nc*( &
     &         4d0*mu*chuu*a0dmu(i1) +4d0*md*chdd*a0dmd(i1) & 
     &        +4d0*mc*chcc*a0dmc(i1) +4d0*ms*chss*a0dms(i1)  &
     &        +4d0*mt*chtt*a0dmt(i1) +4d0*mb*chbb*a0dmb(i1) ) &
     &        -chhh*a0dmh(i1)/2d0 -chff*a0dmw(i1) -chxx*a0dmz(i1)/2d0 &
     &        +chuz*a0dmz(i1) + chpm*a0dmw(i1)*2d0 )
      enddo
      conv= coeff*(   -chzz*mz2    -2d0*chww*mw2  )
      out(0)=out(0) + conv ! CDR result
      end subroutine deltatad

! self energies
      subroutine sigmafs(qf,gfm,gfp,mf2,mfp2,s,sfseps)
      use avh_olo
      implicit none
      include 'declmasses.h'
      complex*16 s,qf,gfm,gfp,mf2,mfp2,sfseps(0:2)
      complex*16 cone,zero,ii
      common/complexunit/cone,zero,ii

      complex*16 sw,cw,sw2,cw2,sw4,cw4,alpha,el2,alsu4pi
      common/couplings/sw,sw2,sw4,cw,cw2,cw4,alpha,el2,alsu4pi
      complex*16 b0dsmfmg(0:2),b0dsmfmz(0:2)
      complex*16 b0dsmfmh(0:2),b0dsmfpmw(0:2)
      integer i1
      real*8 scale
      common/scalale/scale
      logical noqed
      common/qedswitch/noqed
      logical masslesswf,dred
      common/ewoptions/masslesswf,dred
      complex*16 xx,yy,sch
      xx=cone
      if(noqed) then
         xx=zero
         if(dred) then 
            yy=cone
         else
            yy=zero
         endif
      endif
      call olo_onshell( 1d-10 )
      call olo_scale( scale )
      if(abs(qf).lt.1.d-20) then
         do i1=0,2
            b0dsmfmg(i1)   = zero
         enddo
      else
         call olo(b0dsmfmg, s ,mf2 ,zero)
      endif
      call olo(b0dsmfmz , s ,mf2 ,mz2 )
      call olo(b0dsmfmh , s ,mf2 ,mh2 )
      call olo(b0dsmfpmw, s ,mfp2,mw2 )

      sfseps(2)= zero

      sfseps(1)= - alsu4pi * ( xx* qf**2 * (4.d0*b0dsmfmg(1)) &! -2d0*cone)
                             + gfm*gfp * (4.d0*b0dsmfmz(1) ) &!- 2d0*cone)
                   + 0.5d0/sw2*mf2/2.d0/mw2*(b0dsmfmz(1) - b0dsmfmh(1)) &
                   + 0.5d0/sw2*mfp2/mw2*b0dsmfpmw(1)   )      

      sch=(1d0,0d0)
      if(abs(mf2).lt.1d-20) sch=(0d0,0d0)

      sfseps(0)= - alsu4pi * ( xx*qf**2 *(4.d0*b0dsmfmg(0))  &
                                 +qf**2 *(-2d0*xx*cone*sch    ) &
                   + gfm*gfp * (4.d0*b0dsmfmz(0) - 2d0*cone) &
                   + 0.5d0/sw2*mf2/2.d0/mw2*(b0dsmfmz(0) - b0dsmfmh(0)) &
                   + 0.5d0/sw2*mfp2/mw2*b0dsmfpmw(0)   )      
      
      return
      end subroutine sigmafs
      subroutine sigmafl(qf,gfm,gfp,mf2,mfp2,s,sfleps)
      use avh_olo
      implicit none
      include 'declmasses.h'
      complex*16 s,qf,gfm,gfp,mf2,mfp2,sfleps(0:2)
      complex*16 cone,zero,ii
      common/complexunit/cone,zero,ii

      complex*16 sw,cw,sw2,cw2,sw4,cw4,alpha,el2,alsu4pi
      common/couplings/sw,sw2,sw4,cw,cw2,cw4,alpha,el2,alsu4pi
      complex*16 b1dsmfmg(0:2),b1dsmfmz(0:2),b11(0:2),b0(0:2)
      complex*16 b1dsmfmh(0:2),b1dsmfpmw(0:2),b00(0:2)
      integer i1
      real*8 scale
      common/scalale/scale
      logical noqed
      common/qedswitch/noqed
      logical masslesswf,dred
      common/ewoptions/masslesswf,dred
      complex*16 xx,yy,sch
      xx=cone
      if(noqed) then
         xx=zero
         if(dred) then 
            yy=cone
         else
            yy=zero
         endif
      endif
      call olo_onshell( 1d-10 )
      call olo_scale( scale )
      if(abs(qf).lt.1.d-20) then
         do i1=0,2
            b1dsmfmg(i1)   = zero
         enddo
      else
         call olo_b11( b11,b00,b1dsmfmg,b0,  s ,mf2 ,zero)
      endif
      call olo_b11( b11,b00,b1dsmfmz ,b0,  s ,mf2 ,mz2)
      call olo_b11( b11,b00,b1dsmfmh ,b0,  s ,mf2 ,mh2)
      call olo_b11( b11,b00,b1dsmfpmw,b0,  s ,mfp2,mw2)
      
      sfleps(2)= zero
      
      sch=(1d0,0d0)
      if(abs(mf2).lt.1d-20) sch=(0d0,0d0)

      sfleps(1)= - alsu4pi * (xx*qf**2 * (2.d0*b1dsmfmg(1)) &
                   +            gfm**2 * (2.d0*b1dsmfmz(1)) &
                   + 0.5d0/sw2*mf2/2.d0/mw2*(b1dsmfmz(1) + b1dsmfmh(1)) &
                   + 0.5d0/sw2*(2.d0*cone+mfp2/mw2)*b1dsmfpmw(1)   )

      sfleps(0)= - alsu4pi * ( xx*qf**2 *(2.d0*b1dsmfmg(0)) &
                                 +qf**2 *(xx*cone*sch         ) &         
                  +            gfm**2 * (2.d0*b1dsmfmz(0) +cone) &
                  + 0.5d0/sw2*mf2/2.d0/mw2*(b1dsmfmz(0) + b1dsmfmh(0)) &
                  + 0.5d0/sw2*((2.d0*cone+mfp2/mw2)*b1dsmfpmw(0) +cone))
 

      return
      end subroutine sigmafl
      subroutine sigmafr(qf,gfm,gfp,mf2,mfp2,s,sfreps)
      use avh_olo
      implicit none
      include 'declmasses.h'
      complex*16 s,qf,gfm,gfp,mf2,mfp2,sfreps(0:2)
      complex*16 cone,zero,ii
      common/complexunit/cone,zero,ii

      complex*16 sw,cw,sw2,cw2,sw4,cw4,alpha,el2,alsu4pi
      common/couplings/sw,sw2,sw4,cw,cw2,cw4,alpha,el2,alsu4pi
      complex*16 b1dsmfmg(0:2),b1dsmfmz(0:2),b11(0:2),b0(0:2)
      complex*16 b1dsmfmh(0:2),b1dsmfpmw(0:2),b00(0:2)
      integer i1
      real*8 scale
      common/scalale/scale
      logical noqed
      common/qedswitch/noqed
      logical masslesswf,dred
      common/ewoptions/masslesswf,dred
      complex*16 xx,yy,sch
      xx=cone
      if(noqed) then
         xx=zero
         if(dred) then 
            yy=cone
         else
            yy=zero
         endif
      endif
      call olo_onshell( 1d-10 )
      call olo_scale( scale )

      if(abs(qf).lt.1.d-20) then
         do i1=0,2
            b1dsmfmg(i1)   = zero
         enddo
      else
         call olo_b11( b11,b00,b1dsmfmg,b0,  s ,mf2 ,zero)
      endif
      call olo_b11( b11,b00,b1dsmfmz ,b0,  s ,mf2 ,mz2)
      call olo_b11( b11,b00,b1dsmfmh ,b0,  s ,mf2 ,mh2)
      call olo_b11( b11,b00,b1dsmfpmw,b0,  s ,mfp2,mw2)
      
      sfreps(2)= zero

      sfreps(1)= - alsu4pi * ( xx*qf**2 * (2.d0*b1dsmfmg(1)) &
                   +            gfp**2 * (2.d0*b1dsmfmz(1)) &
                   + 0.5d0/sw2*mf2/2.d0/mw2*(b1dsmfmz(1) + b1dsmfmh(1)) &
                   + 0.5d0/sw2*mf2/mw2*b1dsmfpmw(1)   )

      sch=(1d0,0d0)
      if(abs(mf2).lt.1d-20) sch=(0d0,0d0)

      sfreps(0)= - alsu4pi * ( xx*qf**2 * (2.d0*b1dsmfmg(0)) &
                                 +qf**2 * (xx*cone*sch     ) &
                   +            gfp**2 * (2.d0*b1dsmfmz(0)+cone) &
                   + 0.5d0/sw2*mf2/2.d0/mw2*(b1dsmfmz(0) + b1dsmfmh(0)) &
                   + 0.5d0/sw2*mf2/mw2*b1dsmfpmw(0)   )

      end subroutine sigmafr

      subroutine sigmafsp(qf,gfm,gfp,mf2,mfp2,s,sfspeps)
      use avh_olo
      implicit none
      include 'declmasses.h'
      complex*16 s,qf,gfm,gfp,mf2,mfp2,sfspeps(0:2)
      complex*16 cone,zero,ii
      common/complexunit/cone,zero,ii

      complex*16 sw,cw,sw2,cw2,sw4,cw4,alpha,el2,alsu4pi
      common/couplings/sw,sw2,sw4,cw,cw2,cw4,alpha,el2,alsu4pi
      complex*16 b0pdsmfmg(0:2),b0pdsmfmz(0:2)
      complex*16 b0pdsmfmh(0:2),b0pdsmfpmw(0:2)
      integer i1
      real*8 scale
      common/scalale/scale
      logical noqed
      common/qedswitch/noqed
      complex*16 xx
      xx=cone
      if(noqed) xx=zero
      call olo_onshell( 1d-10 )
      call olo_scale( scale )

      if(abs(qf).lt.1.d-20) then
         do i1=0,2
            b0pdsmfmg(i1)   = zero
         enddo
      else
         if(abs(dimag(mf2)).lt.1d-20) then
            call b0pir( s ,mf2 ,b0pdsmfmg)
         else
            call b0pcomplexmt( s ,mf2 ,b0pdsmfmg)
         end if
      endif
      if(abs(mf2).lt.1d-20 .and. abs(mfp2).lt.1d-20) then
         call b0preg(s,mf2,mz2  , b0pdsmfmz)
         call b0preg(s,mf2,mh2  , b0pdsmfmh)
      else
         call olo_db0(b0pdsmfmz , s ,mf2 ,mz2 )
         call olo_db0(b0pdsmfmh , s ,mf2 ,mh2 )
      endif
      if(abs(mf2).lt.1d-20 .and. abs(mfp2).lt.1d-20) then
         call b0preg(s,mfp2,mw2 , b0pdsmfpmw)
      else
         call olo_db0(b0pdsmfpmw, s ,mfp2,mw2 )
      endif

      sfspeps(2)= zero

      sfspeps(1)= - alsu4pi * ( xx*qf**2 * (4.d0*b0pdsmfmg(1)) &! -2d0*cone)
                             + gfm*gfp *  (4.d0*b0pdsmfmz(1)) &!- 2d0*cone)
                   + 0.5d0/sw2*mf2/2.d0/mw2*(b0pdsmfmz(1) -b0pdsmfmh(1)) &
                   + 0.5d0/sw2*mfp2/mw2*b0pdsmfpmw(1)   )      

      sfspeps(0)= - alsu4pi * ( xx*qf**2 * 4.d0*b0pdsmfmg(0) &
                           + gfp*gfm * (4.d0*b0pdsmfmz(0)) &
              + 0.5d0/sw2*mf2/2.d0/mw2*(b0pdsmfmz(0) - b0pdsmfmh(0)) &
              + 0.5d0/sw2*mfp2/mw2*     b0pdsmfpmw(0) )
      
      return
      end subroutine sigmafsp

      subroutine sigmaflp(qf,gfm,gfp,mf2,mfp2,s,sflpeps)
      use avh_olo
      implicit none
      include 'declmasses.h'
      complex*16 s,qf,gfm,gfp,mf2,mfp2,sflpeps(0:2)
      complex*16 cone,zero,ii
      common/complexunit/cone,zero,ii

      complex*16 sw,cw,sw2,cw2,sw4,cw4,alpha,el2,alsu4pi
      common/couplings/sw,sw2,sw4,cw,cw2,cw4,alpha,el2,alsu4pi
      complex*16 b1pdsmfmg(0:2),b1pdsmfmz(0:2)
      complex*16 b1pdsmfmh(0:2),b1pdsmfpmw(0:2)
      integer i1
      real*8 scale
      common/scalale/scale
      logical noqed
      common/qedswitch/noqed
      complex*16 xx

      xx=cone
      if(noqed) xx=zero                                                 
      call olo_onshell( 1d-10 )
      call olo_scale( scale )
      if(abs(qf).lt.1.d-20) then
         do i1=0,2
            b1pdsmfmg(i1)   = zero
         enddo
      else
         if(abs(dimag(mf2)).lt.1d-20) then
            call b1pir( s ,mf2 ,b1pdsmfmg)
         else
            call b1pcomplexmt( s ,mf2 ,b1pdsmfmg)
         endif
      endif
      call b1avo( s ,mf2 ,mz2,b1pdsmfmz )
      call b1avo( s ,mf2 ,mh2,b1pdsmfmh )
      if(abs(mfp2).lt.10d-20.and.abs(s).gt.abs(mw2)) then
         call b1pp0m(s, mw2, b1pdsmfpmw)
      else
         call b1avo( s ,mfp2,mw2,b1pdsmfpmw)
      end if

      sflpeps(2)= zero
      
      sflpeps(1)= - alsu4pi * (xx*qf**2 * (2.d0*b1pdsmfmg(1)) &
                   +            gfm**2 * (2.d0*b1pdsmfmz(1)) &
                   + 0.5d0/sw2*mf2/2.d0/mw2*(b1pdsmfmz(1) +b1pdsmfmh(1)) &
                   + 0.5d0/sw2*(2.d0*cone+mfp2/mw2)*b1pdsmfpmw(1)   )

      sflpeps(0)= - alsu4pi * ( xx*qf**2 * (2.d0*b1pdsmfmg(0)) &
                   +            gfm**2 * (2.d0*b1pdsmfmz(0)) &
                   + 0.5d0/sw2*mf2/2.d0/mw2*(b1pdsmfmz(0) +b1pdsmfmh(0)) &
                   + 0.5d0/sw2*(2.d0*cone+mfp2/mw2)*b1pdsmfpmw(0)   )

      return
      end subroutine sigmaflp

      subroutine sigmafrp(qf,gfm,gfp,mf2,mfp2,s,sfrpeps)
      use avh_olo
      implicit none
      include 'declmasses.h'
      complex*16 s,qf,gfm,gfp,mf2,mfp2,sfrpeps(0:2)
      complex*16 cone,zero,ii
      common/complexunit/cone,zero,ii

      complex*16 sw,cw,sw2,cw2,sw4,cw4,alpha,el2,alsu4pi
      common/couplings/sw,sw2,sw4,cw,cw2,cw4,alpha,el2,alsu4pi
      complex*16 b1pdsmfmg(0:2),b1pdsmfmz(0:2)
      complex*16 b1pdsmfmh(0:2),b1pdsmfpmw(0:2)
      integer i1
      real*8 scale
      common/scalale/scale
      logical noqed
      common/qedswitch/noqed
      complex*16 xx
      xx=cone
      if(noqed) xx=zero
      call olo_onshell( 1d-10 )
      call olo_scale( scale )

      if(abs(qf).lt.1.d-20) then
         do i1=0,2
            b1pdsmfmg(i1)   = zero
         enddo
      else
         if(abs(dimag(mf2)).lt.1d-20) then
            call b1pir( s ,mf2 ,b1pdsmfmg)
         else
            call b1pcomplexmt( s ,mf2 ,b1pdsmfmg)
         endif
      endif

      call b1avo( s ,mf2 ,mz2,b1pdsmfmz )
      call b1avo( s ,mf2 ,mh2,b1pdsmfmh )
      if(abs(mfp2).lt.10d-20.and.abs(s).gt.abs(mw2)) then
         call b1pp0m(s, mw2, b1pdsmfpmw)
      else
         call b1avo( s ,mfp2,mw2,b1pdsmfpmw)
      end if

      
      sfrpeps(2)= zero
      
      sfrpeps(1)= - alsu4pi * ( xx*qf**2 * (2.d0*b1pdsmfmg(1)) &
                 +           gfp**2 *   (2.d0*b1pdsmfmz(1)) &
                 + 0.5d0/sw2*mf2/2.d0/mw2*(b1pdsmfmz(1) + b1pdsmfmh(1)) &
                 + 0.5d0/sw2*mf2/mw2*b1pdsmfpmw(1)   )

      sfrpeps(0)= - alsu4pi * ( xx*qf**2 * (2.d0*b1pdsmfmg(0)) &
                 +           gfp**2 *   (2.d0*b1pdsmfmz(0)) &
                 + 0.5d0/sw2*mf2/2.d0/mw2*(b1pdsmfmz(0) + b1pdsmfmh(0)) &
                 + 0.5d0/sw2*mf2/mw2*b1pdsmfpmw(0)   )

      return
      end subroutine sigmafrp

      subroutine deltazfl(qf,gfm,gfp,mf2,mfp2,dzfleps)
! only flavour diagonal terms are considered since ckm=1 always
      implicit none
      complex*16 s,qf,gfm,gfp,mf2,mfp2,dzfleps(0:2)
 
      complex*16 cone,zero,ii
      common/complexunit/cone,zero,ii
 
      complex*16 sfl(0:2),sflp(0:2),sfrp(0:2),sfsp(0:2)
 
      real*8 epsilon
      common/epsi/epsilon

      integer i1
      logical cmpxmasses
      common/ccomplexmasses/cmpxmasses
 
      call sigmafl (qf,gfm,gfp,mf2,mfp2,dble(mf2)*cone,sfl  )

      if(abs(mf2).lt.epsilon) then
         sflp(1)=zero
         sflp(0)=zero
         sfrp(1)=zero
         sfrp(0)=zero
         sfsp(1)=zero
         sfsp(0)=zero
      else
         call sigmaflp(qf,gfm,gfp,mf2,mfp2,dble(mf2)*cone,sflp)
         call sigmafrp(qf,gfm,gfp,mf2,mfp2,dble(mf2)*cone,sfrp)
         call sigmafsp(qf,gfm,gfp,mf2,mfp2,dble(mf2)*cone,sfsp)
      endif

      if(.not.cmpxmasses) then
         do i1=0,2
            sfl (i1)=dble(sfl (i1))
            sflp(i1)=dble(sflp(i1))
            sfrp(i1)=dble(sfrp(i1))
            sfsp(i1)=dble(sfsp(i1))
         end do
      endif

      dzfleps(2) = zero
      dzfleps(1) = - sfl(1) - mf2*( sflp(1) + sfrp(1) + 2.d0*sfsp(1) )
      dzfleps(0) = - sfl(0) - mf2*( sflp(0) + sfrp(0) + 2.d0*sfsp(0) )      


      return
      end subroutine deltazfl

      subroutine deltazfr(qf,gfm,gfp,mf2,mfp2,dzfreps)
! only flavour diagonal terms are considered since ckm=1 always
      implicit none
      complex*16 s,qf,gfm,gfp,mf2,mfp2,dzfreps(0:2)
      complex*16 cone,zero,ii
      common/complexunit/cone,zero,ii
      complex*16 sfr(0:2),sflp(0:2),sfrp(0:2),sfsp(0:2)
      real*8 epsilon
      common/epsi/epsilon

      integer i1
      logical cmpxmasses
      common/ccomplexmasses/cmpxmasses


      call sigmafr (qf,gfm,gfp,mf2,mfp2,dble(mf2)*cone,sfr )

      if(abs(mf2).lt.epsilon) then
         sflp(1)=zero
         sflp(0)=zero
         sfrp(1)=zero
         sfrp(0)=zero
         sfsp(1)=zero
         sfsp(0)=zero
      else
         call sigmaflp(qf,gfm,gfp,mf2,mfp2,dble(mf2)*cone,sflp)
         call sigmafrp(qf,gfm,gfp,mf2,mfp2,dble(mf2)*cone,sfrp)
         call sigmafsp(qf,gfm,gfp,mf2,mfp2,dble(mf2)*cone,sfsp)
      endif


      if(.not.cmpxmasses) then
         do i1=0,2
            sfr (i1)=dble(sfr (i1))
            sflp(i1)=dble(sflp(i1))
            sfrp(i1)=dble(sfrp(i1))
            sfsp(i1)=dble(sfsp(i1))
         end do
      endif

      dzfreps(2) = zero
      dzfreps(1) = - sfr(1) - mf2*( sflp(1) + sfrp(1) + 2.d0*sfsp(1) )
      dzfreps(0) = - sfr(0) - mf2*( sflp(0) + sfrp(0) + 2.d0*sfsp(0) )      

      return
      end subroutine deltazfr

      subroutine sigmaaat(s,saateps)
      implicit none
      include 'declmasses.h'
      include 'declscalars.h'
      complex*16 s,saateps(0:2)
      complex*16 cone,zero,ii
      common/complexunit/cone,zero,ii

      real*8 qu,qd,ql,qnu
      common/charges/qu,qd,qnu,ql

      complex*16 sw,cw,sw2,cw2,sw4,cw4,alpha,el2,alsu4pi
      common/couplings/sw,sw2,sw4,cw,cw2,cw4,alpha,el2,alsu4pi

      saateps(2)= zero
!                 s=0
      saateps(1)= 2.d0/3.d0*( &
! sum over three charged leptons
     &      2.d0*ql*ql*(-(s+2.d0*me2*cone)*b0d0meme(1) &
     &                  +2.d0*me2*b0d0meme(1)) &! +s/3d0)
     &     +2.d0*ql*ql*(-(s+2.d0*mm2*cone)*b0d0mmmm(1) &
     &                  +2.d0*mm2*b0d0mmmm(1)) &! +s/3d0)
     &     +2.d0*ql*ql*(-(s+2.d0*mtl2*cone)*b0d0mlml(1) &
     &                  +2.d0*mtl2*b0d0mlml(1)) &! +s/3d0)
! sum over quarks
     &     +3.d0* 2.d0*qu*qu*(-(s+2.d0*mu2*cone)*b0d0mumu(1) &
     &                           +2.d0*mu2*b0d0mumu(1)) &!+ s/3.d0 )
     &     +3.d0* 2.d0*qd*qd*(-(s+2.d0*md2*cone)*b0d0mdmd(1) &
     &                           +2.d0*md2*b0d0mdmd(1)) &!+ s/3.d0 )
     &     +3.d0* 2.d0*qu*qu*(-(s+2.d0*mc2*cone)*b0d0mcmc(1) &
     &                           +2.d0*mc2*b0d0mcmc(1)) &!+ s/3.d0 )
     &     +3.d0* 2.d0*qd*qd*(-(s+2.d0*ms2*cone)*b0d0msms(1) &
     &                           +2.d0*ms2*b0d0msms(1)) &!+ s/3.d0 )
     &     +3.d0* 2.d0*qu*qu*(-(s+2.d0*mt2*cone)*b0d0mtmt(1) &
     &                           +2.d0*mt2*b0d0mtmt(1)) &!+ s/3.d0 )
     &     +3.d0* 2.d0*qd*qd*(-(s+2.d0*mb2*cone)*b0d0mbmb(1) &
     &                           +2.d0*mb2*b0d0mbmb(1)) &!+ s/3.d0 ) 
     &     ) &!+ s/3.d0 )
! bosonic part
     &    -4.d0*mw2*b0d0mwmw(1) + (3.d0*s + 4.d0*mw2) * b0d0mwmw(1) 
      saateps(1)= - alsu4pi * saateps(1)
!**
      saateps(0)= 2.d0/3.d0*( &
! sum over three charged leptons
     &      2.d0*ql*ql*(-(s+2.d0*me2*cone)*b0d0meme(0) &
     &                  +2.d0*me2*b0d0meme(0) +s/3d0) &
     &     +2.d0*ql*ql*(-(s+2.d0*mm2*cone)*b0d0mmmm(0) &
     &                  +2.d0*mm2*b0d0mmmm(0) +s/3d0) &
     &     +2.d0*ql*ql*(-(s+2.d0*mtl2*cone)*b0d0mlml(0) &
     &                  +2.d0*mtl2*b0d0mlml(0) +s/3d0) &
! sum over quarks
     &     +3.d0* 2.d0*qu*qu*(-(s+2.d0*mu2*cone)*b0d0mumu(0) &
     &                           +2.d0*mu2*b0d0mumu(0)+ s/3.d0 ) &
     &     +3.d0* 2.d0*qd*qd*(-(s+2.d0*md2*cone)*b0d0mdmd(0) &
     &                           +2.d0*md2*b0d0mdmd(0)+ s/3.d0 ) &
     &     +3.d0* 2.d0*qu*qu*(-(s+2.d0*mc2*cone)*b0d0mcmc(0) &
     &                           +2.d0*mc2*b0d0mcmc(0)+ s/3.d0 ) &
     &     +3.d0* 2.d0*qd*qd*(-(s+2.d0*ms2*cone)*b0d0msms(0) &
     &                           +2.d0*ms2*b0d0msms(0)+ s/3.d0 ) &
     &     +3.d0* 2.d0*qu*qu*(-(s+2.d0*mt2*cone)*b0d0mtmt(0) &
     &                           +2.d0*mt2*b0d0mtmt(0)+ s/3.d0 ) &
     &     +3.d0* 2.d0*qd*qd*(-(s+2.d0*mb2*cone)*b0d0mbmb(0) &
     &                           +2.d0*mb2*b0d0mbmb(0)+ s/3.d0 ) &
     &     ) &
! bosonic part
     &    -4.d0*mw2*b0d0mwmw(0) + (3.d0*s + 4.d0*mw2) * b0d0mwmw(0)
      saateps(0) = - alsu4pi * saateps(0)

      return
      end subroutine sigmaaat      
   
      subroutine sigmaaatp(s,saatpeps)
      implicit none
      include 'declmasses.h'
      include 'declscalars.h'
      complex*16 s,saatpeps(0:2)
      complex*16 cone,zero,ii
      common/complexunit/cone,zero,ii

      real*8 qu,qd,ql,qnu
      common/charges/qu,qd,qnu,ql

      complex*16 sw,cw,sw2,cw2,sw4,cw4,alpha,el2,alsu4pi
      common/couplings/sw,sw2,sw4,cw,cw2,cw4,alpha,el2,alsu4pi

      real*8 xxme,xxmm,xxmtl,xxmu,xxmd,xxmc,xxms,xxmt,xxmb
      
      saatpeps(2)= zero
! in s=0
      saatpeps(1)= 2.d0/3.d0*( &
!* sum over three charged leptons
     &      2.d0*ql*ql*( (-1.d0)*b0d0meme(1) ) &
     &     +2.d0*ql*ql*( (-1.d0)*b0d0mmmm(1) )  &
     &     +2.d0*ql*ql*( (-1.d0)*b0d0mlml(1) ) &
!* sum over quarks
     &     +3.d0* 2.d0*qu*qu*( (-1.d0)*b0d0mumu(1) ) &
     &     +3.d0* 2.d0*qd*qd*( (-1.d0)*b0d0mdmd(1) ) &
     &     +3.d0* 2.d0*qu*qu*( (-1.d0)*b0d0mcmc(1) ) &
     &     +3.d0* 2.d0*qd*qd*( (-1.d0)*b0d0msms(1) ) &
     &     +3.d0* 2.d0*qu*qu*( (-1.d0)*b0d0mtmt(1) ) &
     &     +3.d0* 2.d0*qd*qd*( (-1.d0)*b0d0mbmb(1) ) ) &
!* bosonic part
     &     +3.d0 * b0d0mwmw(1) 
      saatpeps(1)= - alsu4pi * saatpeps(1)

      ! if fermions are massive -2*m2*b0p+1/3 =0d0
      ! if they are massless put -2*m2*b0p+1/3 =0d0 rather than 1/3
      ! that wouldn't be smooth
      ! in practice always avoided in the mixed agf-a0 scheme
      xxme =1d0
      xxmm =1d0
      xxmtl=1d0
      xxmu =1d0
      xxmd =1d0
      xxmc =1d0
      xxms =1d0
      xxmt =1d0
      xxmb =1d0
      if(dble(me2).lt.1d-20) xxme=0d0
      if(dble(mm2).lt.1d-20) xxmm=0d0
      if(dble(mtl2).lt.1d-20) xxmtl=0d0
      if(dble(mu2).lt.1d-20) xxmu=0d0
      if(dble(md2).lt.1d-20) xxmd=0d0
      if(dble(mc2).lt.1d-20) xxmc=0d0
      if(dble(ms2).lt.1d-20) xxms=0d0
      if(dble(mt2).lt.1d-20) xxmt=0d0
      if(dble(mb2).lt.1d-20) xxmb=0d0

      
      saatpeps(0)= 2.d0/3.d0*( &
!* sum over three charged leptons
     &      2.d0*ql*ql*( (-1.d0)*b0d0meme(0)  &
     &                    - (s+2.d0*me2*cone)*b0pd0meme(0) &
     &                    + 1.d0/3.d0*cone*xxme ) &
     &     +2.d0*ql*ql*( (-1.d0)*b0d0mmmm(0)  &
     &                    - (s+2.d0*mm2*cone)*b0pd0mmmm(0) &
     &                    + 1.d0/3.d0*cone*xxmm ) &
     &     +2.d0*ql*ql*( (-1.d0)*b0d0mlml(0) &
     &                    -(s+2.d0*mtl2*cone)*b0pd0mlml(0) &
     &                    + 1.d0/3.d0*cone*xxmtl ) &
!* sum over quarks
     &     +3.d0* 2.d0*qu*qu*( (-1.d0)*b0d0mumu(0) &
     &                          - (s+2.d0*mu2*cone)*b0pd0mumu(0) &
     &                        + 1.d0/3.d0*cone*xxmu ) &
     &     +3.d0* 2.d0*qd*qd*( (-1.d0)*b0d0mdmd(0) &
     &                          - (s+2.d0*md2*cone)*b0pd0mdmd(0) &
     &                        + 1.d0/3.d0*cone*xxmd ) &
     &     +3.d0* 2.d0*qu*qu*( (-1.d0)*b0d0mcmc(0) &
     &                          - (s+2.d0*mc2*cone)*b0pd0mcmc(0) &
     &                        + 1.d0/3.d0*cone*xxmc ) &
     &     +3.d0* 2.d0*qd*qd*( (-1.d0)*b0d0msms(0) &
     &                          - (s+2.d0*ms2*cone)*b0pd0msms(0) &
     &                        + 1.d0/3.d0*cone*xxms ) &
     &     +3.d0* 2.d0*qu*qu*( (-1.d0)*b0d0mtmt(0) &
     &                          - (s+2.d0*mt2*cone)*b0pd0mtmt(0) &
     &                        + 1.d0/3.d0*cone*xxmt ) &
     &     +3.d0* 2.d0*qd*qd*( (-1.d0)*b0d0mbmb(0) &
     &                          - (s+2.d0*mb2*cone)*b0pd0mbmb(0) &
     &                        + 1.d0/3.d0*cone*xxmb ) ) &
!* bosonic part
     &    +3.d0 * b0d0mwmw(0) + (3.d0*s + 4.d0*mw2) * b0pd0mwmw(0)
      saatpeps(0) = - alsu4pi * saatpeps(0)

      return
      end subroutine sigmaaatp

      subroutine sigmazzt(s,szzteps)
      use avh_olo
      implicit none
      include 'declscalars.h'
      include 'declmasses.h'
      complex*16 s,szzteps(0:2)
      complex*16 cone,zero,ii
      common/complexunit/cone,zero,ii

      complex*16 sw,cw,sw2,cw2,sw4,cw4,alpha,el2,alsu4pi
      common/couplings/sw,sw2,sw4,cw,cw2,cw4,alpha,el2,alsu4pi

      complex*16 gnm,gnp,glm,glp,gum,gup,gdm,gdp
      common/vectorassial/gnm,gnp,glm,glp,gum,gup,gdm,gdp
      szzteps(2)= zero
      szzteps(1)= 2.d0/3.d0*( &
! sum over three neutrino families
     &      3.d0*(gnp**2+gnm**2)*( - (s)*b0dmz00(1)) &! + 1.d0/3.d0*s)
! sum over three lepton families
     &     +(glp**2+glm**2)*(- (s+2.d0*me2*cone)*b0dmzmeme(1) &
     &                  +2.d0*me2*b0d0meme(1)) &! + 1.d0/3.d0*s)
     &                  +3.d0/4.d0/sw2/cw2*me2*b0dmzmeme(1) &
     &     +(glp**2+glm**2)*(- (s+2.d0*mm2*cone)*b0dmzmmmm(1) &
     &                  +2.d0*mm2*b0d0mmmm(1)) &! + 1.d0/3.d0*s)
     &                  +3.d0/4.d0/sw2/cw2*mm2*b0dmzmmmm(1) &
     &     +(glp**2+glm**2)*(- (s+2.d0*mtl2*cone)*b0dmzmlml(1) &
     &                  +2.d0*mtl2*b0d0mlml(1)) &! + 1.d0/3.d0*s)
     &                  +3.d0/4.d0/sw2/cw2*mtl2*b0dmzmlml(1) &
! sum over quarks
     &     +3.d0*( (gup**2+gum**2)*(- (s+2.d0*mu2*cone)*b0dmzmumu(1) &
     &                  +2.d0*mu2*b0d0mumu(1)) &! + 1.d0/3.d0*s) 
     &                  +3.d0/4.d0/sw2/cw2*mu2*b0dmzmumu(1) & 
     &           + (gdp**2+gdm**2)*(- (s+2.d0*md2*cone)*b0dmzmdmd(1) &
     &                  +2.d0*md2*b0d0mdmd(1)) &! + 1.d0/3.d0*s) 
     &                  +3.d0/4.d0/sw2/cw2*md2*b0dmzmdmd(1) & 
     &           + (gup**2+gum**2)*(- (s+2.d0*mc2*cone)*b0dmzmcmc(1) &
     &                  +2.d0*mc2*b0d0mcmc(1)) &! + 1.d0/3.d0*s) 
     &                  +3.d0/4.d0/sw2/cw2*mc2*b0dmzmcmc(1) & 
     &           + (gdp**2+gdm**2)*(- (s+2.d0*ms2*cone)*b0dmzmsms(1) &
     &                  +2.d0*ms2*b0d0msms(1)) &! + 1.d0/3.d0*s)
     &                  +3.d0/4.d0/sw2/cw2*ms2*b0dmzmsms(1) & 
     &           + (gup**2+gum**2)*(- (s+2.d0*mt2*cone)*b0dmzmtmt(1) &
     &                  +2.d0*mt2*b0d0mtmt(1)) &! + 1.d0/3.d0*s)
     &                  +3.d0/4.d0/sw2/cw2*mt2*b0dmzmtmt(1) & 
     &           + (gdp**2+gdm**2)*(- (s+2.d0*mb2*cone)*b0dmzmbmb(1) &
     &                  +2.d0*mb2*b0d0mbmb(1)) &! + 1.d0/3.d0*s)
     &                  +3.d0/4.d0/sw2/cw2*mb2*b0dmzmbmb(1)  )  ) & 
! bosonic part
     &    + 1.d0/6.d0/sw2/cw2 * ( &
     &           ( (18.d0*cw4+ 2.d0*cw2-0.5d0*cone)*s &
     &            +(24.d0*cw4+16.d0*cw2-10.d0*cone)*mw2 )*b0dmzmwmw(1) &
     &            -(24.d0*cw4-8.d0*cw2+2.d0*cone)*mw2*b0d0mwmw(1)) &
! higgs
     &   + 1.d0/12.d0/sw2/cw2 * ( &
     &        (2.d0*mh2-10.d0*mz2-s)*b0dmzmzmh(1) &
     &        -2.d0*mz2*b0d0mzmz(1) - 2.d0*mh2*b0d0mhmh(1) ) 
      szzteps(1)= - alsu4pi * szzteps(1)

      szzteps(0)= 2.d0/3.d0*( &
!* sum over three neutrino families
     &      3.d0*(gnp**2+gnm**2)*( - (s)*b0dmz00(0) + 1.d0/3.d0*s) &
!* sum over three lepton families
     &     +(glp**2+glm**2)*(- (s+2.d0*me2*cone)*b0dmzmeme(0) &
     &                  +2.d0*me2*b0d0meme(0) + 1.d0/3.d0*s) &
     &                  +3.d0/4.d0/sw2/cw2*me2*b0dmzmeme(0) &
     &     +(glp**2+glm**2)*(- (s+2.d0*mm2*cone)*b0dmzmmmm(0) &
     &                  +2.d0*mm2*b0d0mmmm(0) + 1.d0/3.d0*s) &
     &                  +3.d0/4.d0/sw2/cw2*mm2*b0dmzmmmm(0) &
     &     +(glp**2+glm**2)*(- (s+2.d0*mtl2*cone)*b0dmzmlml(0) &
     &                  +2.d0*mtl2*b0d0mlml(0) + 1.d0/3.d0*s) &
     &                  +3.d0/4.d0/sw2/cw2*mtl2*b0dmzmlml(0) &
!* sum over quarks
     &     +3.d0*( (gup**2+gum**2)*(- (s+2.d0*mu2*cone)*b0dmzmumu(0) &
     &                  +2.d0*mu2*b0d0mumu(0) + 1.d0/3.d0*s)  &
     &                  +3.d0/4.d0/sw2/cw2*mu2*b0dmzmumu(0)  &
     &           + (gdp**2+gdm**2)*(- (s+2.d0*md2*cone)*b0dmzmdmd(0) &
     &                  +2.d0*md2*b0d0mdmd(0) + 1.d0/3.d0*s)  &
     &                  +3.d0/4.d0/sw2/cw2*md2*b0dmzmdmd(0)  &
     &           + (gup**2+gum**2)*(- (s+2.d0*mc2*cone)*b0dmzmcmc(0) &
     &                  +2.d0*mc2*b0d0mcmc(0) + 1.d0/3.d0*s)  &
     &                  +3.d0/4.d0/sw2/cw2*mc2*b0dmzmcmc(0)  &
     &           + (gdp**2+gdm**2)*(- (s+2.d0*ms2*cone)*b0dmzmsms(0) &
     &                  +2.d0*ms2*b0d0msms(0) + 1.d0/3.d0*s) &
     &                  +3.d0/4.d0/sw2/cw2*ms2*b0dmzmsms(0)  &
     &           + (gup**2+gum**2)*(- (s+2.d0*mt2*cone)*b0dmzmtmt(0) &
     &                  +2.d0*mt2*b0d0mtmt(0) + 1.d0/3.d0*s) &
     &                  +3.d0/4.d0/sw2/cw2*mt2*b0dmzmtmt(0)  &
     &           + (gdp**2+gdm**2)*(- (s+2.d0*mb2*cone)*b0dmzmbmb(0) &
     &                        +2.d0*mb2*b0d0mbmb(0) + 1.d0/3.d0*s) &
     &                        +3.d0/4.d0/sw2/cw2*mb2*b0dmzmbmb(0)  )  ) & 
!* bosonic part
     &    + 1.d0/6.d0/sw2/cw2 * ( &
     &           ( (18.d0*cw4+ 2.d0*cw2-0.5d0*cone)*s &
     &            +(24.d0*cw4+16.d0*cw2-10.d0*cone)*mw2 )*b0dmzmwmw(0) &
     &            -(24.d0*cw4-8.d0*cw2+2.d0*cone)*mw2*b0d0mwmw(0) &
     &            +(4.d0*cw2-cone)/3.d0*s ) &
!* higgs
     &   + 1.d0/12.d0/sw2/cw2 * ( &
     &        (2.d0*mh2-10.d0*mz2-s)*b0dmzmzmh(0) &
     &        -2.d0*mz2*b0d0mzmz(0) - 2.d0*mh2*b0d0mhmh(0) &
     &        -(mz2-mh2)**2 *(b0dmzmzmh(0)-b0d0mzmh(0))/s &
     &        -2.d0/3.d0*s ) 
      szzteps(0)= - alsu4pi * szzteps(0)


      return
      end subroutine sigmazzt

      subroutine sigmazztp(s,szztpeps)
      use avh_olo
      implicit none
      include 'declscalars.h'
      include 'declmasses.h'
      complex*16 s,szztpeps(0:2)
      complex*16 cone,zero,ii
      common/complexunit/cone,zero,ii

      complex*16 sw,cw,sw2,cw2,sw4,cw4,alpha,el2,alsu4pi
      common/couplings/sw,sw2,sw4,cw,cw2,cw4,alpha,el2,alsu4pi

      complex*16 gnm,gnp,glm,glp,gum,gup,gdm,gdp
      common/vectorassial/gnm,gnp,glm,glp,gum,gup,gdm,gdp
      szztpeps(2)= zero

      szztpeps(1)= 2.d0/3.d0*( &
!* sum over three neutrino families
     &      3.d0*(gnp**2+gnm**2)*( -b0dmz00(1) -s*b0pdmz00(1)) &!+1/3
!* sum over three lepton families
     &     +(glp**2+glm**2)*(- (s+2.d0*me2*cone)*b0pdmzmeme(1) &!+1/3
     &         -b0dmzmeme(1)) +3.d0/4.d0/sw2/cw2*me2*b0pdmzmeme(1) &
     &     +(glp**2+glm**2)*(- (s+2.d0*mm2*cone)*b0pdmzmmmm(1) &!+1/3
     &         -b0dmzmmmm(1)) +3.d0/4.d0/sw2/cw2*mm2*b0pdmzmmmm(1) &
     &     +(glp**2+glm**2)*(- (s+2.d0*mtl2*cone)*b0pdmzmlml(1) &!+1/3
     &         -b0dmzmlml(1)) +3.d0/4.d0/sw2/cw2*mtl2*b0pdmzmlml(1) &
!* sum over quarks
     & +3.d0*( (gup**2+gum**2)*(- (s+2.d0*mu2*cone)*b0pdmzmumu(1) &!+1/3
     &            -b0dmzmumu(1)) +3.d0/4.d0/sw2/cw2*mu2*b0pdmzmumu(1) &
     &        +(gup**2+gum**2)*(- (s+2.d0*mc2*cone)*b0pdmzmcmc(1) &!+1/3
     &            -b0dmzmcmc(1)) +3.d0/4.d0/sw2/cw2*mc2*b0pdmzmcmc(1) &
     &        +(gup**2+gum**2)*(- (s+2.d0*mt2*cone)*b0pdmzmtmt(1)  &!+1/3
     &            -b0dmzmtmt(1)) +3.d0/4.d0/sw2/cw2*mt2*b0pdmzmtmt(1)  &
     &        +(gdp**2+gdm**2)*(- (s+2.d0*md2*cone)*b0pdmzmdmd(1) &!+1/3
     &            -b0dmzmdmd(1)) +3.d0/4.d0/sw2/cw2*md2*b0pdmzmdmd(1) &
     &        +(gdp**2+gdm**2)*(- (s+2.d0*ms2*cone)*b0pdmzmsms(1) &!+1/3
     &            -b0dmzmsms(1)) +3.d0/4.d0/sw2/cw2*ms2*b0pdmzmsms(1) &
     &        +(gdp**2+gdm**2)*(- (s+2.d0*mb2*cone)*b0pdmzmbmb(1) &!+1/3
     &            -b0dmzmbmb(1)) +3.d0/4.d0/sw2/cw2*mb2*b0pdmzmbmb(1) )) & 
!* bosonic part
     & + 1.d0/6.d0/sw2/cw2 * ( &
     &           (  18.d0*cw4+ 2.d0*cw2-0.5d0*cone)*b0dmzmwmw(1)  &
     &          +( (18.d0*cw4+ 2.d0*cw2-0.5d0*cone)*s &
     &            +(24.d0*cw4+16.d0*cw2-10.d0*cone)*mw2 )*b0pdmzmwmw(1)) &
! higgs
     &   + 1.d0/12.d0/sw2/cw2 * ( - b0dmzmzmh(1) &
     &       + (2.d0*mh2-10.d0*mz2-s)*b0pdmzmzmh(1))

      szztpeps(1)= - alsu4pi * szztpeps(1)

      szztpeps(0)= 2.d0/3.d0*( &
!* sum over three neutrino families
     &      3.d0*(gnp**2+gnm**2)*( -b0dmz00(0) -s*b0pdmz00(0) +1d0/3d0) &
!* sum over three lepton families
     &     +(glp**2+glm**2)*(- (s+2.d0*me2*cone)*b0pdmzmeme(0)+1d0/3d0 &
     &         -b0dmzmeme(0)) +3.d0/4.d0/sw2/cw2*me2*b0pdmzmeme(0) &
     &     +(glp**2+glm**2)*(- (s+2.d0*mm2*cone)*b0pdmzmmmm(0)+1d0/3d0 &
     &         -b0dmzmmmm(0)) +3.d0/4.d0/sw2/cw2*mm2*b0pdmzmmmm(0) &
     &     +(glp**2+glm**2)*(- (s+2.d0*mtl2*cone)*b0pdmzmlml(0)+1d0/3d0 &
     &         -b0dmzmlml(0)) +3.d0/4.d0/sw2/cw2*mtl2*b0pdmzmlml(0) &
!* sum over quarks
     & +3.d0*( (gup**2+gum**2)*(-(s+2.d0*mu2*cone)*b0pdmzmumu(0)+1d0/3d0 &
     &            -b0dmzmumu(0)) +3.d0/4.d0/sw2/cw2*mu2*b0pdmzmumu(0) &
     &        +(gup**2+gum**2)*(-(s+2.d0*mc2*cone)*b0pdmzmcmc(0)+1d0/3d0 &
     &            -b0dmzmcmc(0)) +3.d0/4.d0/sw2/cw2*mc2*b0pdmzmcmc(0) &
     &        +(gup**2+gum**2)*(-(s+2.d0*mt2*cone)*b0pdmzmtmt(0)+1d0/3d0 &
     &            -b0dmzmtmt(0)) +3.d0/4.d0/sw2/cw2*mt2*b0pdmzmtmt(0)  &
     &        +(gdp**2+gdm**2)*(-(s+2.d0*md2*cone)*b0pdmzmdmd(0)+1d0/3d0 &
     &            -b0dmzmdmd(0)) +3.d0/4.d0/sw2/cw2*md2*b0pdmzmdmd(0) &
     &        +(gdp**2+gdm**2)*(-(s+2.d0*ms2*cone)*b0pdmzmsms(0)+1d0/3d0 &
     &            -b0dmzmsms(0)) +3.d0/4.d0/sw2/cw2*ms2*b0pdmzmsms(0) &
     &        +(gdp**2+gdm**2)*(-(s+2.d0*mb2*cone)*b0pdmzmbmb(0)+1d0/3d0 &
     &            -b0dmzmbmb(0)) +3.d0/4.d0/sw2/cw2*mb2*b0pdmzmbmb(0) ))  &
!* bosonic part
     & + 1.d0/6.d0/sw2/cw2 * ( &
     &           (  18.d0*cw4+ 2.d0*cw2-0.5d0*cone)*b0dmzmwmw(0)  &
     &          +( (18.d0*cw4+ 2.d0*cw2-0.5d0*cone)*s &
     &            +(24.d0*cw4+16.d0*cw2-10.d0*cone)*mw2 )*b0pdmzmwmw(0) &
     &          +(4.d0*cw2-cone)/3.d0 ) &
!* higgs
     &   + 1.d0/12.d0/sw2/cw2 * ( - b0dmzmzmh(0) &
     &       + (2.d0*mh2-10.d0*mz2-s)*b0pdmzmzmh(0) &
     &        +(mz2-mh2)**2 *(b0dmzmzmh(0)-b0d0mzmh(0))/s/s &
     &        -(mz2-mh2)**2 *b0pdmzmzmh(0)/s  &
     &        -2.d0/3.d0 )
      szztpeps(0)= - alsu4pi * szztpeps(0)

      return
      end subroutine sigmazztp
      
      subroutine sigmaazt(s,sazteps)
      implicit none
      include 'declmasses.h'
      include 'declscalars.h'
      complex*16 s,sazteps(0:2)
      complex*16 cone,zero,ii
      common/complexunit/cone,zero,ii

      real*8 qu,qd,ql,qnu
      common/charges/qu,qd,qnu,ql

      complex*16 sw,cw,sw2,cw2,sw4,cw4,alpha,el2,alsu4pi
      common/couplings/sw,sw2,sw4,cw,cw2,cw4,alpha,el2,alsu4pi

      complex*16 gnm,gnp,glm,glp,gum,gup,gdm,gdp
      common/vectorassial/gnm,gnp,glm,glp,gum,gup,gdm,gdp

      sazteps(2)= zero

      if(abs(s).lt.1d-20) then
         sazteps(1)=  2.d0/3.d0*s*( &
!*     sum over three charged leptons
     &        -ql*(glp+glm)*( - b0d0meme(1) &
     &                        - b0d0mmmm(1) &
     &                        - b0d0mlml(1) ) &
!*     sum over quarks
     &        -3.d0*qu*(gup+gum)*(- b0d0mumu(1)  &
     &                            - b0d0mcmc(1)  &
     &                            - b0d0mtmt(1) ) &
     &        -3.d0*qd*(gdp+gdm)*(- b0d0mdmd(1)  &
     &                            - b0d0msms(1)  &
     &                            - b0d0mbmb(1) ) &
     &        ) &
!* bosonic part
     &    -1.d0/3.d0/sw/cw*( ( (9.d0*cw2+0.5d0*cone)*s &
     &                         +(12.d0*cw2+4.d0*cone)*mw2 )*b0d0mwmw(1) &
     &                        - (12.d0*cw2-2.d0*cone)*mw2*b0d0mwmw(1) &
     &                      )
         sazteps(1)  = - alsu4pi * sazteps(1)
      
         sazteps(0)=  2.d0/3.d0*s*( &
!*     sum over three charged leptons
     &        -ql*(glp+glm)*( - b0d0meme(0) &
     &                        - b0d0mmmm(0) &
     &                        - b0d0mlml(0) ) &
!*     sum over quarks
     &        -3.d0*qu*(gup+gum)*(- b0d0mumu(0)  &
     &                            - b0d0mcmc(0)  &
     &                            - b0d0mtmt(0) ) &
     &        -3.d0*qd*(gdp+gdm)*(- b0d0mdmd(0)  &
     &                            - b0d0msms(0)  &
     &                            - b0d0mbmb(0) ) &
     &        ) &
!* bosonic part
     &    -1.d0/3.d0/sw/cw*( ( (9.d0*cw2+0.5d0*cone)*s &
     &                         +(12.d0*cw2+4.d0*cone)*mw2 )*b0d0mwmw(0) &
     &                        - (12.d0*cw2-2.d0*cone)*mw2  *b0d0mwmw(0) &
     &                      )
         sazteps(0)  = - alsu4pi * sazteps(0)
      else ! Saz(mz2)
         sazteps(1)=  2.d0/3.d0*( &
!* sum over three charged leptons
     &     -ql*(glp+glm)*( - (s+2.d0*me2*cone)*b0dmzmeme(1) &
     &                       + 2.d0*me2*b0d0meme(1) & !+ 1.d0/3.d0*s 
     &                     - (s+2.d0*mm2*cone)*b0dmzmmmm(1) &
     &                       + 2.d0*mm2*b0d0mmmm(1) & !+ 1.d0/3.d0*s 
     &                     - (s+2.d0*mtl2*cone)*b0dmzmlml(1) &
     &                       + 2.d0*mtl2*b0d0mlml(1)                ) &
!* sum over quarks
     &    -3.d0*( qu*(gup+gum)*(- (s+2.d0*mu2*cone)*b0dmzmumu(1) &
     &                         +2.d0*mu2*b0d0mumu(1)) &! + 1.d0/3.d0*s )
     &           +qd*(gdp+gdm)*(- (s+2.d0*md2*cone)*b0dmzmdmd(1) &
     &                         +2.d0*md2*b0d0mdmd(1)) &! + 1.d0/3.d0*s )
     &           +qu*(gup+gum)*(- (s+2.d0*mc2*cone)*b0dmzmcmc(1) &
     &                         +2.d0*mc2*b0d0mcmc(1)) &! + 1.d0/3.d0*s )
     &           +qd*(gdp+gdm)*(- (s+2.d0*ms2*cone)*b0dmzmsms(1) &
     &                         +2.d0*ms2*b0d0msms(1) ) &!+ 1.d0/3.d0*s )
     &           +qu*(gup+gum)*(- (s+2.d0*mt2*cone)*b0dmzmtmt(1) &
     &                         +2.d0*mt2*b0d0mtmt(1) ) &!+ 1.d0/3.d0*s )
     &           +qd*(gdp+gdm)*(- (s+2.d0*mb2*cone)*b0dmzmbmb(1) &
     &                         +2.d0*mb2*b0d0mbmb(1)               ) ) ) &
!* bosonic part
     &    -1.d0/3.d0/sw/cw*(  ( (9.d0*cw2+0.5d0*cone)*s &
     &                         +(12.d0*cw2+4.d0*cone)*mw2 )*b0dmzmwmw(1) &
     &                       - (12.d0*cw2-2.d0*cone)*mw2*b0d0mwmw(1))
         sazteps(1)  = - alsu4pi * sazteps(1)
     
         sazteps(0)=  2.d0/3.d0*( &
!* sum over three charged leptons
     &     -ql*(glp+glm)*( - (s+2.d0*me2*cone)*b0dmzmeme(0) &
     &                       + 2.d0*me2*b0d0meme(0) + 1.d0/3.d0*s  &
     &                     - (s+2.d0*mm2*cone)*b0dmzmmmm(0) &
     &                       + 2.d0*mm2*b0d0mmmm(0) + 1.d0/3.d0*s  &
     &                     - (s+2.d0*mtl2*cone)*b0dmzmlml(0) &
     &                       + 2.d0*mtl2*b0d0mlml(0) + 1.d0/3.d0*s  ) &
!* sum over quarks
     &    -3.d0*( qu*(gup+gum)*(- (s+2.d0*mu2*cone)*b0dmzmumu(0) &
     &                         +2.d0*mu2*b0d0mumu(0) + 1.d0/3.d0*s ) &
     &           +qd*(gdp+gdm)*(- (s+2.d0*md2*cone)*b0dmzmdmd(0) &
     &                         +2.d0*md2*b0d0mdmd(0) + 1.d0/3.d0*s ) &
     &           +qu*(gup+gum)*(- (s+2.d0*mc2*cone)*b0dmzmcmc(0) &
     &                         +2.d0*mc2*b0d0mcmc(0) + 1.d0/3.d0*s ) &
     &           +qd*(gdp+gdm)*(- (s+2.d0*ms2*cone)*b0dmzmsms(0) &
     &                         +2.d0*ms2*b0d0msms(0) + 1.d0/3.d0*s ) &
     &           +qu*(gup+gum)*(- (s+2.d0*mt2*cone)*b0dmzmtmt(0) &
     &                         +2.d0*mt2*b0d0mtmt(0) + 1.d0/3.d0*s ) &
     &           +qd*(gdp+gdm)*(- (s+2.d0*mb2*cone)*b0dmzmbmb(0) &
     &                         +2.d0*mb2*b0d0mbmb(0) + 1.d0/3.d0*s ) ) ) &
!* bosonic part
     &    -1.d0/3.d0/sw/cw*(  ( (9.d0*cw2+0.5d0*cone)*s &
     &                         +(12.d0*cw2+4.d0*cone)*mw2 )*b0dmzmwmw(0) &
     &                       - (12.d0*cw2-2.d0*cone)*mw2*b0d0mwmw(0) &
     &                       + 1.d0/3.d0*s   )
         sazteps(0)  = - alsu4pi * sazteps(0)
      endif

      return
      end subroutine sigmaazt

      subroutine sigmawt(s,swteps)
      implicit none
      include 'declmasses.h'
      include 'declscalars.h'
      complex*16 s,swteps(0:2)

      complex*16 cone,zero,ii
      common/complexunit/cone,zero,ii

      complex*16 sw,cw,sw2,cw2,sw4,cw4,alpha,el2,alsu4pi
      common/couplings/sw,sw2,sw4,cw,cw2,cw4,alpha,el2,alsu4pi

      if (abs(s).gt.1.d-20) then ! in mw2

          swteps(2)= zero

          swteps(1)= 2.d0/3.d0/2.d0/sw2*( &
!* sum over three charged leptons
     &                - (s-me2/2.d0*cone)*b0dmw0me(1) &
     &                + me2*b0d0meme(1) &
     &                - (s-mm2/2.d0*cone)*b0dmw0mm(1) &
     &                + mm2*b0d0mmmm(1)  &
     &                - (s-mtl2/2.d0*cone)*b0dmw0ml(1) &
     &                + mtl2*b0d0mlml(1)   &
     &             ) &
!* sum over three quark families
     &            + 2.d0/3.d0/2.d0/sw2 * 3.d0 * ( &
     &                - (s-(mu2+md2)*cone/2.d0)*b0dmwmumd(1) &
     &                + mu2*b0d0mumu(1) + md2*b0d0mdmd(1)  &
     &                - (s-(mc2+ms2)*cone/2.d0)*b0dmwmcms(1) &
     &                + mc2*b0d0mcmc(1) + ms2*b0d0msms(1) &
     &                - (s-(mt2+mb2)*cone/2.d0)*b0dmwmtmb(1) &
     &                + mt2*b0d0mtmt(1) + mb2*b0d0mbmb(1)  &
     &             ) &
!* bosonic part
     &       + 2.d0/3.d0*( &
     &           (2.d0*mw2 + 5.d0*s)*b0dmwmwmg(1)-2.d0*mw2*b0d0mwmw(1) ) &
     &       + 1.d0/12.d0/sw2*( ((40.d0*cw2-cone)*s  &
     &           +(16.d0*cw2+54.d0*cone-10.d0/cw2)*mw2)*b0dmwmwmz(1) &
     &           -(16.d0*cw2+2.d0*cone)*(mw2*b0d0mwmw(1) &
     &                                  +mz2*b0d0mzmz(1)) ) &
     &       + 1.d0/12.d0/sw2*( (-10.d0*mw2-s)*b0dmwmwmh(1) &
     &                            -2.d0*mw2*b0d0mwmw(1) )
          swteps(1)  = - alsu4pi * swteps(1)
      
          swteps(0)= 2.d0/3.d0/2.d0/sw2*( &
!* sum over three charged leptons
     &         -(s-me2/2.d0*cone)*b0dmw0me(0) + 1.d0/3.d0*s &
     &         +me2*b0d0meme(0) + me2**2/2.d0/s*(b0dmw0me(0)-b0d00me(0)) &
     &         -(s-mm2/2.d0*cone)*b0dmw0mm(0) + 1.d0/3.d0*s &
     &         +mm2*b0d0mmmm(0) + mm2**2/2.d0/s*(b0dmw0mm(0)-b0d00mm(0)) &
     &         -(s-mtl2/2.d0*cone)*b0dmw0ml(0) + 1.d0/3.d0*s &
     &         +mtl2*b0d0mlml(0)  &
     &                      + mtl2**2/2.d0/s*(b0dmw0ml(0)-b0d00ml(0)) ) &
!* sum over three quark families
     &          + 2.d0/3.d0/2.d0/sw2 * 3.d0 * ( &
     &         -(s-(mu2+md2)*cone/2.d0)*b0dmwmumd(0) + 1.d0/3.d0*s &
     &         +mu2*b0d0mumu(0) + md2*b0d0mdmd(0) &
     &         + (mu2-md2)**2/2.d0/s * (b0dmwmumd(0) - b0d0mumd(0)) &
     &         -(s-(mc2+ms2)*cone/2.d0)*b0dmwmcms(0) + 1.d0/3.d0*s &
     &         +mc2*b0d0mcmc(0) + ms2*b0d0msms(0) &
     &         + (mc2-ms2)**2/2.d0/s * (b0dmwmcms(0) - b0d0mcms(0)) &
     &         -(s-(mt2+mb2)*cone/2.d0)*b0dmwmtmb(0) + 1.d0/3.d0*s &
     &         +mt2*b0d0mtmt(0) + mb2*b0d0mbmb(0) &
     &         + (mt2-mb2)**2/2.d0/s * (b0dmwmtmb(0) - b0d0mtmb(0)) ) &
!* bosonic part
     &         + 2.d0/3.d0*( &
     &            (2.d0*mw2 + 5.d0*s)*b0dmwmwmg(0) -2.d0*mw2*b0d0mwmw(0) &
     &             -mw2**2/s*(b0dmwmwmg(0)-b0d0mwmg(0)) + 1.d0/3.d0*s ) &
     &          + 1.d0/12.d0/sw2*( ((40.d0*cw2-cone)*s  &
     &               +(16.d0*cw2+54.d0*cone-10.d0/cw2)*mw2)*b0dmwmwmz(0) &
     &               -(16.d0*cw2+2.d0*cone)*(mw2*b0d0mwmw(0) &
     &                                      +mz2*b0d0mzmz(0)) &
     &                 +(4.d0*cw2-cone)*2.d0/3.d0*s &
     &                 -(8.d0*cw2+cone)*(mw2-mz2)**2/s &
     &                              *(b0dmwmwmz(0) - b0d0mwmz(0)) ) &
     &          + 1.d0/12.d0/sw2*( (2.d0*mh2-10.d0*mw2-s)*b0dmwmwmh(0) &
     &                   -2.d0*mw2*b0d0mwmw(0) - 2.d0*mh2*b0d0mhmh(0) &
     &                   -(mw2-mh2)**2/s*(b0dmwmwmh(0)-b0d0mwmh(0)) &
     &                   -2.d0/3.d0*s )
          swteps(0)  = - alsu4pi * swteps(0)
      
       else 
          swteps(2)= zero
!* sum over three charged leptons
          swteps(1)= 2.d0/3.d0/2.d0/sw2*( &
     &             -(-me2/2.d0)*b0d00me(1) &
     &             +me2*b0d0meme(1) + me2*me2/2.d0*b0pd00me(1) &
     &             -(-mm2/2.d0)*b0d00mm(1) &
     &             +mm2*b0d0mmmm(1) + mm2*mm2/2.d0*b0pd00mm(1) &
     &             -(-mtl2/2.d0)*b0d00ml(1) &
     &             +mtl2*b0d0mlml(1) + mtl2*mtl2/2.d0*b0pd00ml(1) ) &
!* sum over three quark families
     &          + 2.d0/3.d0/2.d0/sw2 * 3.d0 * ( &
     &             -(-(mu2+md2)/2.d0)*b0d0mumd(1) &
     &             +mu2*b0d0mumu(1) + md2*b0d0mdmd(1) &
     &             + (mu2-md2)**2/2.d0*b0pd0mumd(1) &
     &             -(-(mc2+ms2)/2.d0)*b0d0mcms(1) &
     &             +mc2*b0d0mcmc(1) + ms2*b0d0msms(1) &
     &             + (mc2-ms2)**2/2.d0*b0pd0mcms(1) &
     &             -(-(mt2+mb2)/2.d0)*b0d0mtmb(1) &
     &             +mt2*b0d0mtmt(1) + mb2*b0d0mbmb(1) &
     &             + (mt2-mb2)**2/2.d0*b0pd0mtmb(1) ) &
!* bosonic part
     &          + 2.d0/3.d0*( &
     &            (2.d0*mw2)*b0d0mwmg(1) - 2.d0*mw2*b0d0mwmw(1) &
     &           -mw2**2*b0pd0mwmg(1) ) &
     &          + 1.d0/12.d0/sw2*( (  &
     &               +(16.d0*cw2+54.d0*cone-10.d0/cw2)*mw2)*b0d0mwmz(1) &
     &               -(16.d0*cw2+2.d0*cone)*(mw2*b0d0mwmw(1) &
     &                                      +mz2*b0d0mzmz(1)) &
     &               -(8.d0*cw2+cone)*(mw2-mz2)**2*b0pd0mwmz(1) ) &
     &          + 1.d0/12.d0/sw2*( (2.d0*mh2-10.d0*mw2)*b0d0mwmh(1) &
     &                 -2.d0*mw2*b0d0mwmw(1) - 2.d0*mh2*b0d0mhmh(1) &
     &                 -(mw2-mh2)**2*b0pd0mwmh(1) )
          swteps(1)= - alsu4pi * swteps(1)
!* sum over three charged leptons
          swteps(0)= 2.d0/3.d0/2.d0/sw2*( &
     &             -(-me2/2.d0)*b0d00me(0) &
     &             +me2*b0d0meme(0) + me2*me2/2.d0*b0pd00me(0) &
     &             -(-mm2/2.d0)*b0d00mm(0) &
     &             +mm2*b0d0mmmm(0) + mm2*mm2/2.d0*b0pd00mm(0) &
     &             -(-mtl2/2.d0)*b0d00ml(0) &
     &             +mtl2*b0d0mlml(0) + mtl2*mtl2/2.d0*b0pd00ml(0) ) &
!* sum over three quark families
     &          + 2.d0/3.d0/2.d0/sw2 * 3.d0 * ( &
     &             -(-(mu2+md2)/2.d0)*b0d0mumd(0) &
     &             +mu2*b0d0mumu(0) + md2*b0d0mdmd(0) &
     &             + (mu2-md2)**2/2.d0*b0pd0mumd(0) &
     &             -(-(mc2+ms2)/2.d0)*b0d0mcms(0) &
     &             +mc2*b0d0mcmc(0) + ms2*b0d0msms(0) &
     &             + (mc2-ms2)**2/2.d0*b0pd0mcms(0) &
     &             -(-(mt2+mb2)/2.d0)*b0d0mtmb(0) &
     &             +mt2*b0d0mtmt(0) + mb2*b0d0mbmb(0) &
     &             + (mt2-mb2)**2/2.d0*b0pd0mtmb(0) ) &
!* bosonic part
     &          + 2.d0/3.d0*( &
     &            (2.d0*mw2)*b0d0mwmg(0) - 2.d0*mw2*b0d0mwmw(0) &
     &           -mw2**2*b0pd0mwmg(0) ) &
     &          + 1.d0/12.d0/sw2*( (  &
     &               +(16.d0*cw2+54.d0*cone-10.d0/cw2)*mw2)*b0d0mwmz(0) &
     &               -(16.d0*cw2+2.d0*cone)*(mw2*b0d0mwmw(0) &
     &                                      +mz2*b0d0mzmz(0)) &
     &               -(8.d0*cw2+cone)*(mw2-mz2)**2*b0pd0mwmz(0) ) &
     &          + 1.d0/12.d0/sw2*( (2.d0*mh2-10.d0*mw2)*b0d0mwmh(0) &
     &                 -2.d0*mw2*b0d0mwmw(0) - 2.d0*mh2*b0d0mhmh(0) &
     &                 -(mw2-mh2)**2*b0pd0mwmh(0) )
          swteps(0) = - alsu4pi * swteps(0)

      endif
      return
      end subroutine sigmawt

      subroutine sigmawtp(s,swtpeps)
      implicit none
      include 'declscalars.h'
      include 'declmasses.h'
      complex*16 s,swtpeps(0:2)

      complex*16 cone,zero,ii
      common/complexunit/cone,zero,ii

      complex*16 sw,cw,sw2,cw2,sw4,cw4,alpha,el2,alsu4pi
      common/couplings/sw,sw2,sw4,cw,cw2,cw4,alpha,el2,alsu4pi


      swtpeps(2)= zero

      swtpeps(1)= 2.d0/3.d0/2.d0/sw2*( &
!* sum over three charged leptons
     &           - b0dmw0me(1) -(s-me2/2.d0*cone)*b0pdmw0me(1) &
     &           + me2*me2/2.d0/s*   b0pdmw0me(1) &
     &           - me2*me2/2.d0/s/s*(b0dmw0me(1)-b0d00me(1)) &
     &           - b0dmw0mm(1) -(s-mm2/2.d0*cone)*b0pdmw0mm(1) &
     &           + mm2*mm2/2.d0/s*   b0pdmw0mm(1) &
     &           - mm2*mm2/2.d0/s/s*(b0dmw0mm(1)-b0d00mm(1)) &
     &           - b0dmw0ml(1) -(s-mtl2/2.d0*cone)*b0pdmw0ml(1) &
     &           + mtl2*mtl2/2.d0/s*   b0pdmw0ml(1) &
     &           - mtl2*mtl2/2.d0/s/s*(b0dmw0ml(1)-b0d00ml(1)) ) &
!* sum over three quark families
     &      + 2.d0/3.d0/2.d0/sw2 * 3.d0 * ( &
     &           - b0dmwmumd(1) -(s-(mu2+md2)*cone/2.d0)*b0pdmwmumd(1) &
     &           + (mu2-md2)**2/2.d0/s   *  b0pdmwmumd(1) &
     &           - (mu2-md2)**2/2.d0/s/s * (b0dmwmumd(1) - b0d0mumd(1)) &
     &           - b0dmwmcms(1) -(s-(mc2+ms2)*cone/2.d0)*b0pdmwmcms(1) &
     &           + (mc2-ms2)**2/2.d0/s   *  b0pdmwmcms(1) &
     &           - (mc2-ms2)**2/2.d0/s/s * (b0dmwmcms(1) - b0d0mcms(1)) &
     &           - b0dmwmtmb(1) -(s-(mt2+mb2)*cone/2.d0)*b0pdmwmtmb(1) &
     &           + (mt2-mb2)**2/2.d0/s   *  b0pdmwmtmb(1)  &
     &           - (mt2-mb2)**2/2.d0/s/s * (b0dmwmtmb(1) - b0d0mtmb(1))) &
!* bosonic part
     &      + 2.d0/3.d0*( &
     &             (5.d0)*b0dmwmwmg(1) &
     &           + (2.d0*mw2 + 5.d0*s)*b0pdmwmwmg(1) &
     &           -mw2*mw2/s*   b0pdmwmwmg(1) &
     &           +mw2*mw2/s/s*(b0dmwmwmg(1) -b0d0mwmg(1)) ) &
     &      +1.d0/12.d0/sw2*( ((40.d0*cw2-cone)*s  &
     &           +(16.d0*cw2+54.d0*cone-10.d0/cw2)*mw2)*b0pdmwmwmz(1) &
     &             +(40.d0*cw2- cone)*b0dmwmwmz(1) &
     &             -(8.d0*cw2 + cone)*(mw2-mz2)**2/s &
     &                               *b0pdmwmwmz(1) &
     &             +(8.d0*cw2 + cone)*(mw2-mz2)**2/s/s &
     &                         *(b0dmwmwmz(1) - b0d0mwmz(1)) ) &
     &      +1.d0/12.d0/sw2*( (2.d0*mh2-10.d0*mw2-s)*b0pdmwmwmh(1) &
     &                   +(-1.d0)*b0dmwmwmh(1) &
     &                   -(mw2-mh2)**2/s*   b0pdmwmwmh(1) &
     &                   +(mw2-mh2)**2/s/s*(b0dmwmwmh(1)-b0d0mwmh(1)  ))
      swtpeps(1)= - alsu4pi * swtpeps(1)
      
      
      swtpeps(0)= 2.d0/3.d0/2.d0/sw2*( &
!* sum over three charged leptons
     &           - b0dmw0me(0) -(s-me2/2.d0*cone)*b0pdmw0me(0) &
     &                         + 1.d0/3.d0*cone &
     &           + me2*me2/2.d0/s*   b0pdmw0me(0) &
     &           - me2*me2/2.d0/s/s*(b0dmw0me(0)-b0d00me(0)) &
     &           - b0dmw0mm(0) -(s-mm2/2.d0*cone)*b0pdmw0mm(0) &
     &                         + 1.d0/3.d0*cone &
     &           + mm2*mm2/2.d0/s*   b0pdmw0mm(0) &
     &           - mm2*mm2/2.d0/s/s*(b0dmw0mm(0)-b0d00mm(0)) &
     &           - b0dmw0ml(0) -(s-mtl2/2.d0*cone)*b0pdmw0ml(0) &
     &                         + 1.d0/3.d0*cone &
     &           + mtl2*mtl2/2.d0/s*   b0pdmw0ml(0) &
     &           - mtl2*mtl2/2.d0/s/s*(b0dmw0ml(0)-b0d00ml(0)) ) &
!* sum over three quark families
     &      + 2.d0/3.d0/2.d0/sw2 * 3.d0 * ( &
     &           - b0dmwmumd(0) -(s-(mu2+md2)*cone/2.d0)*b0pdmwmumd(0) &
     &                         + 1.d0/3.d0*cone &
     &           + (mu2-md2)**2/2.d0/s   *  b0pdmwmumd(0) &
     &           - (mu2-md2)**2/2.d0/s/s * (b0dmwmumd(0) - b0d0mumd(0)) &
     &           - b0dmwmcms(0) -(s-(mc2+ms2)*cone/2.d0)*b0pdmwmcms(0) &
     &                         + 1.d0/3.d0*cone &
     &           + (mc2-ms2)**2/2.d0/s   *  b0pdmwmcms(0) &
     &           - (mc2-ms2)**2/2.d0/s/s * (b0dmwmcms(0) - b0d0mcms(0)) &
     &           - b0dmwmtmb(0) - (s-(mt2+mb2)*cone/2.d0)*b0pdmwmtmb(0) &
     &                         + 1.d0/3.d0*cone &
     &           + (mt2-mb2)**2/2.d0/s   *  b0pdmwmtmb(0)  &
     &           - (mt2-mb2)**2/2.d0/s/s * (b0dmwmtmb(0) - b0d0mtmb(0))) &
!* bosonic part
     &      + 2.d0/3.d0*( &
     &             (5.d0)*b0dmwmwmg(0) &
     &           + (2.d0*mw2 + 5.d0*s)*b0pdmwmwmg(0) &
     &           -mw2*mw2/s*   b0pdmwmwmg(0) &
     &           +mw2*mw2/s/s*(b0dmwmwmg(0) -b0d0mwmg(0)) &
     &           + 1.d0/3.d0*cone) &
     &      +1.d0/12.d0/sw2*( ((40.d0*cw2-cone)*s  &
     &           +(16.d0*cw2+54.d0*cone-10.d0/cw2)*mw2)*b0pdmwmwmz(0) &
     &             +(40.d0*cw2- cone)*b0dmwmwmz(0) &
     &             +(4.d0*cw2 - cone)*2.d0/3.d0*cone &
     &             -(8.d0*cw2 + cone)*(mw2-mz2)**2/s &
     &                               *b0pdmwmwmz(0) &
     &             +(8.d0*cw2 + cone)*(mw2-mz2)**2/s/s &
     &                         *(b0dmwmwmz(0) - b0d0mwmz(0)) ) &
     &      +1.d0/12.d0/sw2*( (2.d0*mh2-10.d0*mw2-s)*b0pdmwmwmh(0) &
     &                      +(-1.d0)*b0dmwmwmh(0) &
     &                      -(mw2-mh2)**2/s*   b0pdmwmwmh(0) &
     &                      +(mw2-mh2)**2/s/s*(b0dmwmwmh(0)-b0d0mwmh(0)) &
     &                      -2.d0/3.d0*cone )
      swtpeps(0)= - alsu4pi * swtpeps(0)

      return
      end subroutine sigmawtp

      subroutine sigmahh(s,shheps)
      implicit none
      include 'declmasses.h'
      include 'declscalars.h'
      complex*16 s,shheps(0:2)

      complex*16 cone,zero,ii
      common/complexunit/cone,zero,ii

      complex*16 sw,cw,sw2,cw2,sw4,cw4,alpha,el2,alsu4pi
      common/couplings/sw,sw2,sw4,cw,cw2,cw4,alpha,el2,alsu4pi

      complex*16 gnm,gnp,glm,glp,gum,gup,gdm,gdp
      common/vectorassial/gnm,gnp,glm,glp,gum,gup,gdm,gdp

      shheps(2)= zero

      shheps(1)=0.5d0/sw2/mw2*( &
     &              me2*(2d0*a0dme(1)+(4d0*me2-s)*b0dmhmeme(1) ) &
     &         +    mm2*(2d0*a0dmm(1)+(4d0*mm2-s)*b0dmhmmmm(1) ) &
     &         +   mtl2*(2d0*a0dml(1)+(4d0*mtl2-s)*b0dmhmlml(1)) &
     &         +3d0*mu2*(2d0*a0dmu(1)+(4d0*mu2-s)*b0dmhmumu(1) ) &
     &         +3d0*mc2*(2d0*a0dmc(1)+(4d0*mc2-s)*b0dmhmcmc(1) ) &
     &         +3d0*mt2*(2d0*a0dmt(1)+(4d0*mt2-s)*b0dmhmtmt(1) ) &
     &         +3d0*md2*(2d0*a0dmd(1)+(4d0*md2-s)*b0dmhmdmd(1) ) &
     &         +3d0*ms2*(2d0*a0dms(1)+(4d0*ms2-s)*b0dmhmsms(1) ) &
     &         +3d0*mb2*(2d0*a0dmb(1)+(4d0*mb2-s)*b0dmhmbmb(1) )) &
     &         -0.5d0/sw2*( (3d0+0.5d0*mh2/mw2)*a0dmw(1) & !-6d0*mw2
     &               + (6d0*mw2 -2d0*s +0.5d0*mh2*mh2/mw2)*b0dmhmwmw(1)) &
     &         -0.25d0/sw2/cw2*( (3d0+0.5d0*mh2/mz2)*a0dmz(1) &! -6d0*mz2
     &               + (6d0*mz2 -2d0*s +0.5d0*mh2*mh2/mz2)*b0dmhmzmz(1)) &
     &         -3d0/sw2/8d0*(3d0*mh2*mh2/mw2*b0dmhmhmh(1) &
     &                      +mh2/mw2*a0dmh(1))             
      shheps(1)= - alsu4pi * shheps(1)
      
      shheps(0)=0.5d0/sw2/mw2*( &
     &              me2*(2d0*a0dme(0)+(4d0*me2-s)*b0dmhmeme(0) ) &
     &         +    mm2*(2d0*a0dmm(0)+(4d0*mm2-s)*b0dmhmmmm(0) ) &
     &         +   mtl2*(2d0*a0dml(0)+(4d0*mtl2-s)*b0dmhmlml(0)) &
     &         +3d0*mu2*(2d0*a0dmu(0)+(4d0*mu2-s)*b0dmhmumu(0) ) &
     &         +3d0*mc2*(2d0*a0dmc(0)+(4d0*mc2-s)*b0dmhmcmc(0) ) &
     &         +3d0*mt2*(2d0*a0dmt(0)+(4d0*mt2-s)*b0dmhmtmt(0) ) &
     &         +3d0*md2*(2d0*a0dmd(0)+(4d0*md2-s)*b0dmhmdmd(0) ) &
     &         +3d0*ms2*(2d0*a0dms(0)+(4d0*ms2-s)*b0dmhmsms(0) ) &
     &         +3d0*mb2*(2d0*a0dmb(0)+(4d0*mb2-s)*b0dmhmbmb(0) )) &
     &         -0.5d0/sw2*( (3d0+0.5d0*mh2/mw2)*a0dmw(0) -6d0*mw2 &
     &               + (6d0*mw2 -2d0*s +0.5d0*mh2*mh2/mw2)*b0dmhmwmw(0)) &
     &         -0.25d0/sw2/cw2*( (3d0+0.5d0*mh2/mz2)*a0dmz(0) -6d0*mz2 &
     &               + (6d0*mz2 -2d0*s +0.5d0*mh2*mh2/mz2)*b0dmhmzmz(0)) &
     &         -3d0/sw2/8d0*(3d0*mh2*mh2/mw2*b0dmhmhmh(0) &
     &                      +mh2/mw2*a0dmh(0))             
      shheps(0)= - alsu4pi * shheps(0)
      return
      end subroutine sigmahh

      subroutine sigmahhp(s,shhpeps)
      implicit none
      include 'declmasses.h'
      include 'declscalars.h'
      complex*16 s,shhpeps(0:2)

      complex*16 cone,zero,ii
      common/complexunit/cone,zero,ii

      complex*16 sw,cw,sw2,cw2,sw4,cw4,alpha,el2,alsu4pi
      common/couplings/sw,sw2,sw4,cw,cw2,cw4,alpha,el2,alsu4pi

      complex*16 gnm,gnp,glm,glp,gum,gup,gdm,gdp
      common/vectorassial/gnm,gnp,glm,glp,gum,gup,gdm,gdp

      shhpeps(2)= zero

      shhpeps(1)=0.5d0/sw2/mw2*( &
     &        +      me2 *( -b0dmhmeme(1)+(4d0*me2-s)*b0pdmhmeme(1)) &
     &        +      mm2 *( -b0dmhmmmm(1)+(4d0*mm2-s)*b0pdmhmmmm(1)) &
     &        +      mtl2*( -b0dmhmlml(1)+(4d0*mtl2-s)*b0pdmhmlml(1))) &
     &          +1.5d0/sw2/mw2*( &
     &        +      mu2 *( -b0dmhmumu(1)+(4d0*mu2-s)*b0pdmhmumu(1)) &
     &        +      mc2 *( -b0dmhmcmc(1)+(4d0*mc2-s)*b0pdmhmcmc(1)) &
     &        +      mt2 *( -b0dmhmtmt(1)+(4d0*mt2-s)*b0pdmhmtmt(1)) &
     &        +      md2 *( -b0dmhmdmd(1)+(4d0*md2-s)*b0pdmhmdmd(1)) &
     &        +      ms2 *( -b0dmhmsms(1)+(4d0*ms2-s)*b0pdmhmsms(1)) &
     &        +      mb2 *( -b0dmhmbmb(1)+(4d0*mb2-s)*b0pdmhmbmb(1))) &
     &         -0.5d0/sw2*( -2d0*b0dmhmwmw(1) &
     &                  +(6d0*mw2-2d0*s+mh2*mh2/mw2/2d0)*b0pdmhmwmw(1)) &
     &         -0.25d0/sw2/cw2*( -2d0*b0dmhmzmz(1) &
     &                  +(6d0*mz2-2d0*s+mh2*mh2/mz2/2d0)*b0pdmhmzmz(1)) &
     &         -3d0/sw2/8d0*(3d0*mh2*mh2/mw2*b0pdmhmhmh(1) )             
      shhpeps(1)= - alsu4pi * shhpeps(1)
      
      shhpeps(0)=0.5d0/sw2/mw2*( &
     &               me2 *( -b0dmhmeme(0)+(4d0*me2-s)*b0pdmhmeme(0)) &
     &             + mm2 *( -b0dmhmmmm(0)+(4d0*mm2-s)*b0pdmhmmmm(0)) &
     &             + mtl2*( -b0dmhmlml(0)+(4d0*mtl2-s)*b0pdmhmlml(0))) &
     &          +1.5d0/sw2/mw2*( &
     &             + mu2 *( -b0dmhmumu(0)+(4d0*mu2-s)*b0pdmhmumu(0)) &
     &             + mc2 *( -b0dmhmcmc(0)+(4d0*mc2-s)*b0pdmhmcmc(0)) &
     &             + mt2 *( -b0dmhmtmt(0)+(4d0*mt2-s)*b0pdmhmtmt(0)) &
     &             + md2 *( -b0dmhmdmd(0)+(4d0*md2-s)*b0pdmhmdmd(0)) &
     &             + ms2 *( -b0dmhmsms(0)+(4d0*ms2-s)*b0pdmhmsms(0)) &
     &             + mb2 *( -b0dmhmbmb(0)+(4d0*mb2-s)*b0pdmhmbmb(0))) &
     &         -0.5d0/sw2*( -2d0*b0dmhmwmw(0) &
     &                  +(6d0*mw2-2d0*s+mh2*mh2/mw2/2d0)*b0pdmhmwmw(0)) &
     &         -0.25d0/sw2/cw2*( -2d0*b0dmhmzmz(0) &
     &                  +(6d0*mz2-2d0*s+mh2*mh2/mz2/2d0)*b0pdmhmzmz(0)) &
     &         -3d0/sw2/8d0*(3d0*mh2*mh2/mw2*b0pdmhmhmh(0) )             
      shhpeps(0)= - alsu4pi * shhpeps(0)
      return
      end subroutine sigmahhp


      subroutine printoutct
      implicit none
      include 'dzdecl.h'
      include 'declmasses.h'
!      include 'ddrrdecl.h'
      write(*,*)'FINITE PART'
      write(*,*)'dmw ',ddmw2(1)
      write(*,*)'dmz ',ddmz2(1)
      write(*,*)'dmh ',ddmh2(1)               !mass renorm
      write(*,*)'dme ',ddme2(1)
      write(*,*)'dmm ',ddmm2(1)
      write(*,*)'dml ',ddmtl2(1)
      write(*,*)'dmu ',ddmu2(1)
      write(*,*)'dmd ',ddmd2(1)
      write(*,*)'dmc ',ddmc2(1)
      write(*,*)'dms ',ddms2(1)
      write(*,*)'dmt ',ddmt2(1)
      write(*,*)'dmb ',ddmb2(1)
      write(*,*)'dzne',ddznel(1)
      write(*,*)'dznm',ddznml(1)
      write(*,*)'dznl',ddzntl(1)              ! wf renorm
      write(*,*)'dzel',ddzel(1)
      write(*,*)'dzml',ddzml(1)
      write(*,*)'dzll',ddztll(1)         ! wf renorm
      write(*,*)'dzul',ddzul(1)
      write(*,*)'dzcl',ddzcl(1)
      write(*,*)'dztl',ddztl(1)     
      write(*,*)'dzdl',ddzdl(1)
      write(*,*)'dzsl',ddzsl(1)
      write(*,*)'dzbl',ddzbl(1)     
      write(*,*)'dzer',ddzer(1)
      write(*,*)'dzmr',ddzmr(1)
      write(*,*)'dzlr',ddztlr(1)
      write(*,*)'dzur',ddzur(1)
      write(*,*)'dzcr',ddzcr(1)
      write(*,*)'dztr',ddztr(1)     
      write(*,*)'dzdr',ddzdr(1)
      write(*,*)'dzsr',ddzsr(1)
      write(*,*)'dzbr',ddzbr(1)
      write(*,*)'dzw ',ddzw(1)
      write(*,*)'dzz ',ddzz(1)
      write(*,*)'dzh ',ddzh(1)
      write(*,*)'dza ',ddza(1)
      write(*,*)'d_za',ddz_za(1)
      write(*,*)'d_az',ddz_az(1) 
      write(*,*)'dee ',ddee(1)
      write(*,*)'dss ',ddswsw(1)
      write(*,*)'dcc ',ddcwcw(1)        !coupling renorm
      write(*,*)'dtad',dtad(1)
      write(*,*)'dtot',ddmt2omt(1)
      write(*,*)'drr ',ddrr(1)

      write(*,*)'SINGOLE POLE PART'
      write(*,*)'dmw ',ddmw2(2)
      write(*,*)'dmz ',ddmz2(2)
      write(*,*)'dmh ',ddmh2(2)               !mass renorm
      write(*,*)'dme ',ddme2(2)
      write(*,*)'dmm ',ddmm2(2)
      write(*,*)'dml ',ddmtl2(2)
      write(*,*)'dmu ',ddmu2(2)
      write(*,*)'dmd ',ddmd2(2)
      write(*,*)'dmc ',ddmc2(2)
      write(*,*)'dms ',ddms2(2)
      write(*,*)'dmt ',ddmt2(2)
      write(*,*)'dmb ',ddmb2(2)
      write(*,*)'dzne',ddznel(2)
      write(*,*)'dznm',ddznml(2)
      write(*,*)'dznl',ddzntl(2)              ! wf renorm
      write(*,*)'dzel',ddzel(2)
      write(*,*)'dzml',ddzml(2)
      write(*,*)'dzll',ddztll(2)         ! wf renorm
      write(*,*)'dzul',ddzul(2)
      write(*,*)'dzcl',ddzcl(2)
      write(*,*)'dztl',ddztl(2)     
      write(*,*)'dzdl',ddzdl(2)
      write(*,*)'dzsl',ddzsl(2)
      write(*,*)'dzbl',ddzbl(2)     
      write(*,*)'dzer',ddzer(2)
      write(*,*)'dzmr',ddzmr(2)
      write(*,*)'dzlr',ddztlr(2)
      write(*,*)'dzur',ddzur(2)
      write(*,*)'dzcr',ddzcr(2)
      write(*,*)'dztr',ddztr(2)     
      write(*,*)'dzdr',ddzdr(2)
      write(*,*)'dzsr',ddzsr(2)
      write(*,*)'dzbr',ddzbr(2)
      write(*,*)'dzw ',ddzw(2)
      write(*,*)'dzz ',ddzz(2)
      write(*,*)'dzh ',ddzh(2)
      write(*,*)'dza ',ddza(2)
      write(*,*)'d_za',ddz_za(2)
      write(*,*)'d_az',ddz_az(2) 
      write(*,*)'dee ',ddee(2)
      write(*,*)'dss ',ddswsw(2)
      write(*,*)'dcc ',ddcwcw(2)        !coupling renorm
      write(*,*)'dtad',dtad(2)
      write(*,*)'dtot',ddmt2omt(2)
      write(*,*)'drr ',ddrr(2)
      end subroutine printoutct

      subroutine printallgct
        implicit none
        include 'dzdecl.h'
        integer i1
        real*8 unite
        common/unitcharge/unite                            
        do i1=1,2       !1,2
           write(*,*)'----------------------i1',i1
           write(*,*)'gctW1(i1 )    ',  gctW1(i1 )     !ddzw(i1)
           write(*,*)'gctW2(i1 )    ',  gctW2(i1 )     !mw2*ddzw(i1)+ddmw2(i1)
           write(*,*)'gctZ1(i1 )    ',  gctZ1(i1 )     !ddzz(i1)
           write(*,*)'gctZ2(i1 )    ',  gctZ2(i1 )     !mz2*ddzz(i1)+ddmz2(i1)
           write(*,*)'gctA(i1  )    ',  gctA(i1  )     !ddza(i1)
           write(*,*)'gctAZ1(i1)    ',  gctAZ1(i1)     !0.5d0*(ddz_az(i1)+ddz_za(i1))
           write(*,*)'gctAZ2(i1)    ',  gctAZ2(i1)     !0.5d0*mz2*ddz_za(i1)
           write(*,*)'gctH1(i1 )    ',  gctH1(i1 )     !ddzh(i1)
           write(*,*)'gctH2(i1 )    ',  gctH2(i1 )     !mh2*ddzh(i1)+ddmh2(i1)
           write(*,*)'gctchi(i1)    ',  gctchi(i1)     !ddmz2(i1)-unite*dtad(i1)/2d0/sw/mw
           write(*,*)'gctphi(i1)    ',  gctphi(i1)     !ddmw2(i1)-unite*dtad(i1)/2d0/sw/mw
           write(*,*)'gctCLU(i1)    ',  gctCLU(i1)     !0.5d0*(ddzul(i1)+conjg(ddzul(i1)))
           write(*,*)'gctCRU(i1)    ',  gctCRU(i1)     !0.5d0*(ddzur(i1)+conjg(ddzur(i1)))
           write(*,*)'gctCPU(i1)    ',  gctCPU(i1)     !xx*(mu*conjg(ddzul(i1)/2d0)+mu*ddzur(i1)/2d0+ddmu2(i1))
           write(*,*)'gctCMU(i1)    ',  gctCMU(i1)     !xx*(mu*conjg(ddzur(i1)/2d0)+mu*ddzul(i1)/2d0+ddmu2(i1))
           write(*,*)'gctCLC(i1)    ',  gctCLC(i1)     !0.5d0*(ddzcl(i1)+conjg(ddzcl(i1)))
           write(*,*)'gctCRC(i1)    ',  gctCRC(i1)     !0.5d0*(ddzcr(i1)+conjg(ddzcr(i1)))
           write(*,*)'gctCPC(i1)    ',  gctCPC(i1)     !xx*(mc*conjg(ddzcl(i1)/2d0)+mc*ddzcr(i1)/2d0+ddmc2(i1))
           write(*,*)'gctCMC(i1)    ',  gctCMC(i1)     !xx*(mc*conjg(ddzcr(i1)/2d0)+mc*ddzcl(i1)/2d0+ddmc2(i1))
           write(*,*)'gctCLT(i1)    ',  gctCLT(i1)     !0.5d0*(ddztl(i1)+conjg(ddztl(i1)))
           write(*,*)'gctCRT(i1)    ',  gctCRT(i1)     !0.5d0*(ddztr(i1)+conjg(ddztr(i1)))
           write(*,*)'gctCPT(i1)    ',  gctCPT(i1)     !mt*(conjg(ddztl(i1)/2d0)+ddztr(i1)/2d0+ddmt2omt(i1))
           write(*,*)'gctCMT(i1)    ',  gctCMT(i1)     !mt*(conjg(ddztr(i1)/2d0)+ddztl(i1)/2d0+ddmt2omt(i1))
           write(*,*)'gctCLD(i1)    ',  gctCLD(i1)     !0.5d0*(ddzdl(i1)+conjg(ddzdl(i1)))
           write(*,*)'gctCRD(i1)    ',  gctCRD(i1)     !0.5d0*(ddzdr(i1)+conjg(ddzdr(i1)))
           write(*,*)'gctCPD(i1)    ',  gctCPD(i1)     !xx*(md*conjg(ddzdl(i1)/2d0)+md*ddzdr(i1)/2d0+ddmd2(i1))
           write(*,*)'gctCMD(i1)    ',  gctCMD(i1)     !xx*(md*conjg(ddzdr(i1)/2d0)+md*ddzdl(i1)/2d0+ddmd2(i1))
           write(*,*)'gctCLS(i1)    ',  gctCLS(i1)     !0.5d0*(ddzsl(i1)+conjg(ddzsl(i1)))
           write(*,*)'gctCRS(i1)    ',  gctCRS(i1)     !0.5d0*(ddzsr(i1)+conjg(ddzsr(i1)))
           write(*,*)'gctCPS(i1)    ',  gctCPS(i1)     !xx*(ms*conjg(ddzsl(i1)/2d0)+ms*ddzsr(i1)/2d0+ddms2(i1))
           write(*,*)'gctCMS(i1)    ',  gctCMS(i1)     !xx*(ms*conjg(ddzsr(i1)/2d0)+ms*ddzsl(i1)/2d0+ddms2(i1))
           write(*,*)'gctCLB(i1)    ',  gctCLB(i1)     !0.5d0*(ddzbl(i1)+conjg(ddzbl(i1)))
           write(*,*)'gctCRB(i1)    ',  gctCRB(i1)     !0.5d0*(ddzbr(i1)+conjg(ddzbr(i1)))
           write(*,*)'gctCPB(i1)    ',  gctCPB(i1)     !xx*(mb*conjg(ddzbl(i1)/2d0)+mc*ddzbr(i1)/2d0+ddmb2(i1))
           write(*,*)'gctCMB(i1)    ',  gctCMB(i1)     !xx*(mb*conjg(ddzbr(i1)/2d0)+mc*ddzbl(i1)/2d0+ddmb2(i1))
           write(*,*)'gctCLne(i1)   ',  gctCLne(i1)     !0.5d0*(ddznel(i1)+conjg(ddznel(i1)))
           write(*,*)'gctCRne(i1)   ',  gctCRne(i1)     !0d0!0.5d0*(ddzner(i1)+conjg(ddzner(i1)))
           write(*,*)'gctCLnmu(i1)  ',  gctCLnmu(i1)     !0.5d0*(ddznml(i1)+conjg(ddznml(i1)))
           write(*,*)'gctCRnmu(i1)  ',  gctCRnmu(i1)     !0d0!0.5d0*(ddznmr(i1)+conjg(ddznmr(i1)))
           write(*,*)'gctCLntau(i1) ',  gctCLntau(i1)     !0.5d0*(ddzntl(i1)+conjg(ddzntl(i1)))
           write(*,*)'gctCRntau(i1) ',  gctCRntau(i1)     !0d0!0.5d0*(ddzntr(i1)+conjg(ddzntr(i1)))
           write(*,*)'gctCLe(i1)    ',  gctCLe(i1)     !0.5d0*(ddzel(i1)+conjg(ddzel(i1)))
           write(*,*)'gctCRe(i1)    ',  gctCRe(i1)     !0.5d0*(ddzer(i1)+conjg(ddzer(i1)))
           write(*,*)'gctCPe(i1)    ',  gctCPe(i1)     !xx*(me*conjg(ddzel(i1))+me*ddzer(i1)+ddme2(i1))
           write(*,*)'gctCMe(i1)    ',  gctCMe(i1)     !xx*(me*conjg(ddzer(i1))+me*ddzel(i1)+ddme2(i1))
           write(*,*)'gctCLmu(i1)   ',  gctCLmu(i1)     !0.5d0*(ddzml(i1)+conjg(ddzml(i1)))
           write(*,*)'gctCRmu(i1)   ',  gctCRmu(i1)     !0.5d0*(ddzmr(i1)+conjg(ddzmr(i1)))
           write(*,*)'gctCPmu(i1)   ',  gctCPmu(i1)     !xx*(mm*conjg(ddzml(i1))+mm*ddzmr(i1)+ddmm2(i1))
           write(*,*)'gctCMmu(i1)   ',  gctCMmu(i1)     !xx*(mm*conjg(ddzmr(i1))+mm*ddzml(i1)+ddmm2(i1))
           write(*,*)'gctCLtau(i1)  ',  gctCLtau(i1)     !0.5d0*(ddztll(i1)+conjg(ddztll(i1)))
           write(*,*)'gctCRtau(i1)  ',  gctCRtau(i1)     !0.5d0*(ddztlr(i1)+conjg(ddztlr(i1)))
           write(*,*)'gctCPtau(i1)  ',  gctCPtau(i1)     !xx*(mtl*conjg(ddztll(i1))+mtl*ddztlr(i1) &
           write(*,*)'gctCMtau(i1)  ',  gctCMtau(i1)     !xx*(mtl*conjg(ddztlr(i1))+mtl*ddztll(i1) &
           write(*,*)'gctWWZZ(i1)   ',  gctWWZZ(i1)*unite**2      ! -(cw2/sw2)*( 2d0*ddee(i1) &
           write(*,*)'gctWWAZ(i1)   ',  gctWWAZ(i1)*unite**2      ! +(cw/sw)*( 2d0*ddee(i1) - ddswsw(i1)/cw2 &
           write(*,*)'gctWWAA(i1)   ',  gctWWAA(i1)*unite**2      ! -( 2d0*ddee(i1) + ddzw(i1) + ddza(i1) ) &
           write(*,*)'gctWWWW(i1)   ',  gctWWWW(i1)*unite**2     !(2d0*ddee(i1) -2d0*ddswsw(i1) +2d0*ddzw(i1) )/sw2
           write(*,*)'gctWWA(i1)    ',  gctWWA(i1)*unite      ! ddee(i1)+ddzw(i1)+0.5d0*ddza(i1) &
           write(*,*)'gctWWZ(i1)    ',  gctWWZ(i1)*unite      ! -(cw/sw)*( ddee(i1)-ddswsw(i1)/cw2 + ddzw(i1) &
           write(*,*)'gctHHHH(i1)   ',  gctHHHH(i1)*unite**2     !-3d0*coeff*(2d0*ddee(i1) - 2d0*ddswsw(i1) &
           write(*,*)'gctHHXX(i1)   ',  gctHHXX(i1)*unite**2     !    -coeff*(2d0*ddee(i1) - 2d0*ddswsw(i1) &
           write(*,*)'gctHHPP(i1)   ',  gctHHPP(i1)*unite**2     !    -coeff*(2d0*ddee(i1) - 2d0*ddswsw(i1) &
           write(*,*)'gctXXXX(i1)   ',  gctXXXX(i1)*unite**2     !-3d0*coeff*(2d0*ddee(i1) - 2d0*ddswsw(i1) &
           write(*,*)'gctXXPP(i1)   ',  gctXXPP(i1)*unite**2     !-1d0*coeff*(2d0*ddee(i1) - 2d0*ddswsw(i1) &
           write(*,*)'gctPPPP(i1)   ',  gctPPPP(i1)*unite**2     !-2d0*coeff*(2d0*ddee(i1) - 2d0*ddswsw(i1) &
           write(*,*)'gctHHH(i1)    ',  gctHHH(i1)*unite     !-3d0*coeff*(ddee(i1) - ddswsw(i1) &
           write(*,*)'gctHPP(i1)    ',  gctHPP(i1)*unite     !-coeff*(ddee(i1) - ddswsw(i1) &
           write(*,*)'gctHXX(i1)    ',  gctHXX(i1)*unite     !-coeff*(ddee(i1) - ddswsw(i1) &
           write(*,*)'gctWWHH(i1)   ',  gctWWHH(i1)*unite**2     !(1d0/sw2)*(2d0*ddee(i1) - 2d0*ddswsw(i1) + ddzw(i1) &
           write(*,*)'gctWWXX(i1)   ',  gctWWXX(i1)*unite**2     !(1d0/sw2)*(2d0*ddee(i1) - 2d0*ddswsw(i1) +ddzw(i1))
           write(*,*)'gctWWPP(i1)   ',  gctWWPP(i1)*unite**2     !(1d0/sw2)*(2d0*ddee(i1) - 2d0*ddswsw(i1) +ddzw(i1))
           write(*,*)'gctZZPP(i1)   ',  gctZZPP(i1)*unite**2     !(sw2-cw2)**2/2d0/sw2/cw2*( 2d0*ddee(i1) &
           write(*,*)'gctAZPP(i1)   ',  gctAZPP(i1)*unite**2     !(sw2-cw2)/sw/cw*(2d0*ddee(i1) &
           write(*,*)'gctAAPP(i1)   ',  gctAAPP(i1)*unite**2     !2d0*(2d0*ddee(i1)+ddza(i1)) &
           write(*,*)'gctZZHH(i1)   ',  gctZZHH(i1)*unite**2     !1d0/2d0/sw2/cw2*(2d0*ddee(i1) &
           write(*,*)'gctZZXX(i1)   ',  gctZZXX(i1)*unite**2     !1d0/2d0/sw2/cw2*(2d0*ddee(i1) &
           write(*,*)'gctZAHH(i1)   ',  gctZAHH(i1)*unite**2     !1d0/2d0/sw2/cw2*(0.5d0*ddz_za(i1))
           write(*,*)'gctZAXX(i1)   ',  gctZAXX(i1)*unite**2     !1d0/2d0/sw2/cw2*(0.5d0*ddz_za(i1))
           write(*,*)'gctWZPH(i1)   ',  gctWZPH(i1)*unite**2     !-1d0/2d0/cw*(2d0*ddee(i1)-ddcwcw(i1) &
           write(*,*)'gctWAPH(i1)   ',  gctWAPH(i1)*unite**2     !-1d0/2d0/sw*(2d0*ddee(i1)-ddswsw(i1) &
           write(*,*)'gctWZPX(i1)   ',  gctWZPX(i1)*unite**2     !-ii/2d0/cw*(2d0*ddee(i1)-ddcwcw(i1) &
           write(*,*)'gctWAPX(i1)   ',  gctWAPX(i1)*unite**2     !-ii/2d0/sw*(2d0*ddee(i1)-ddswsw(i1) &
           write(*,*)'gctAXH(i1)    ',  gctAXH(i1)*unite     !-ii*ddz_za(i1)/4d0/cw/sw
           write(*,*)'gctZXH(i1)    ',  gctZXH(i1)*unite     !-ii/2d0/cw/sw*(ddee(i1)+(sw2-cw2)/cw2*ddswsw(i1) &
           write(*,*)'gctAPP(i1)    ',  gctAPP(i1)*unite     !-(ddee(i1)+0.5d0*ddza(i1) &
           write(*,*)'gctZPP(i1)    ',  gctZPP(i1)*unite     !-(sw2-cw2)/2d0/cw/sw*(ddee(i1) &
           write(*,*)'gctWPH(i1)    ',  gctWPH(i1)*unite     !-1d0/2d0/sw*(ddee(i1)-ddswsw(i1) &
           write(*,*)'gctWPX(i1)    ',  gctWPX(i1)*unite     !-ii/2d0/sw*(ddee(i1)-ddswsw(i1) &
           write(*,*)'gctHWW(i1)    ',  gctHWW(i1)*unite     !mw/sw*(ddee(i1)-ddswsw(i1)+0.5d0*ddmw2(i1)/mw2 &
           write(*,*)'gctHZZ(i1)    ',  gctHZZ(i1)*unite     !mw/sw/cw2*(ddee(i1)+(2d0*sw2-cw2)/cw2*ddswsw(i1) &
           write(*,*)'gctHZA(i1)    ',  gctHZA(i1)*unite     !mw/2d0/sw/cw2*ddz_za(i1)
           write(*,*)'gctPWZ(i1)    ',  gctPWZ(i1)*unite     !-mw*sw/cw*(ddee(i1)+1d0/cw2*ddswsw(i1) &
           write(*,*)'gctPWA(i1)    ',  gctPWA(i1)*unite     !-mw*(ddee(i1)+0.5d0*ddmw2(i1)/mw2 &
           write(*,*)'gctWpud(i1)   ',  gctWpud(i1) *unite    !1d0/sqrt(2d0)/sw*(ddee(i1)-ddswsw(i1) &
           write(*,*)'gctWpcs(i1)   ',  gctWpcs(i1) *unite    !1d0/sqrt(2d0)/sw*(ddee(i1)-ddswsw(i1) &
           write(*,*)'gctWptb(i1)   ',  gctWptb(i1) *unite    !1d0/sqrt(2d0)/sw*(ddee(i1)-ddswsw(i1) &
           write(*,*)'gctWmud(i1)   ',  gctWmud(i1) *unite    !1d0/sqrt(2d0)/sw*(ddee(i1)-ddswsw(i1) &
           write(*,*)'gctWmcs(i1)   ',  gctWmcs(i1) *unite    !1d0/sqrt(2d0)/sw*(ddee(i1)-ddswsw(i1) &
           write(*,*)'gctWmtb(i1)   ',  gctWmtb(i1) *unite    !1d0/sqrt(2d0)/sw*(ddee(i1)-ddswsw(i1) &
           write(*,*)'gctWpe(i1)    ',  gctWpe(i1)  *unite   !1d0/sqrt(2d0)/sw*(ddee(i1)-ddswsw(i1) &
           write(*,*)'gctWme(i1)    ',  gctWme(i1)  *unite   !1d0/sqrt(2d0)/sw*(ddee(i1)-ddswsw(i1) &
           write(*,*)'gctWpmu(i1)   ',  gctWpmu(i1) *unite    !1d0/sqrt(2d0)/sw*(ddee(i1)-ddswsw(i1) &
           write(*,*)'gctWmmu(i1)   ',  gctWmmu(i1) *unite    !1d0/sqrt(2d0)/sw*(ddee(i1)-ddswsw(i1) &
           write(*,*)'gctWptau(i1)  ',  gctWptau(i1)*unite     !1d0/sqrt(2d0)/sw*(ddee(i1)-ddswsw(i1) &
           write(*,*)'gctWmtau(i1)  ',  gctWmtau(i1)*unite     !1d0/sqrt(2d0)/sw*(ddee(i1)-ddswsw(i1) &
           
           write(*,*)'gctArne(i1)      ',  gctArne(i1)  *unite   !-ql*(ddee(i1)+0.5d0*ddza(i1) &
           write(*,*)'gctAlne(i1)      ',  gctAlne(i1)  *unite   !-ql*(ddee(i1)+0.5d0*ddza(i1) &
           write(*,*)'gctArnmu(i1)     ',  gctArnmu(i1)  *unite   !-ql*(ddee(i1)+0.5d0*ddza(i1) &
           write(*,*)'gctAlnmu(i1)     ',  gctAlnmu(i1)  *unite   !-ql*(ddee(i1)+0.5d0*ddza(i1) &
           write(*,*)'gctArntau(i1)    ',  gctArntau(i1)  *unite   !-ql*(ddee(i1)+0.5d0*ddza(i1) &
           write(*,*)'gctAlntau(i1)    ',  gctAlntau(i1)  *unite   !-ql*(ddee(i1)+0.5d0*ddza(i1) &
           
           write(*,*)'gctAre(i1)    ',  gctAre(i1)  *unite   !-ql*(ddee(i1)+0.5d0*ddza(i1) &
           write(*,*)'gctAle(i1)    ',  gctAle(i1)  *unite   !-ql*(ddee(i1)+0.5d0*ddza(i1) &
           write(*,*)'gctArmu(i1)   ',  gctArmu(i1) *unite    !-ql*(ddee(i1)+0.5d0*ddza(i1) &
           write(*,*)'gctAlmu(i1)   ',  gctAlmu(i1) *unite    !-ql*(ddee(i1)+0.5d0*ddza(i1) &
           write(*,*)'gctArtau(i1)  ',  gctArtau(i1)*unite     !-ql*(ddee(i1)+0.5d0*ddza(i1) &
           write(*,*)'gctAltau(i1)  ',  gctAltau(i1)*unite     !-ql*(ddee(i1)+0.5d0*ddza(i1) &
           write(*,*)'gctArU(i1)    ',  gctArU(i1)  *unite   !-qu*(ddee(i1)+0.5d0*ddza(i1) &
           write(*,*)'gctAlU(i1)    ',  gctAlU(i1)  *unite   !-qu*(ddee(i1)+0.5d0*ddza(i1) &
           write(*,*)'gctArC(i1)    ',  gctArC(i1)  *unite   !-qu*(ddee(i1)+0.5d0*ddza(i1) &
           write(*,*)'gctAlC(i1)    ',  gctAlC(i1)  *unite   !-qu*(ddee(i1)+0.5d0*ddza(i1) &
           write(*,*)'gctArT(i1)    ',  gctArT(i1)  *unite   !-qu*(ddee(i1)+0.5d0*ddza(i1) &
           write(*,*)'gctAlT(i1)    ',  gctAlT(i1)  *unite   !-qu*(ddee(i1)+0.5d0*ddza(i1) &
           write(*,*)'gctArD(i1)    ',  gctArD(i1)  *unite   !-qd*(ddee(i1)+0.5d0*ddza(i1) &
           write(*,*)'gctAlD(i1)    ',  gctAlD(i1)  *unite   !-qd*(ddee(i1)+0.5d0*ddza(i1) &
           write(*,*)'gctArS(i1)    ',  gctArS(i1)  *unite   !-qd*(ddee(i1)+0.5d0*ddza(i1) &
           write(*,*)'gctAlS(i1)    ',  gctAlS(i1)  *unite   !-qd*(ddee(i1)+0.5d0*ddza(i1) &
           write(*,*)'gctArB(i1)    ',  gctArB(i1)  *unite   !-qd*(ddee(i1)+0.5d0*ddza(i1) &
           write(*,*)'gctAlB(i1)    ',  gctAlB(i1)  *unite   !-qd*(ddee(i1)+0.5d0*ddza(i1) &
           write(*,*)'gctGrU(i1)    ',  gctGrU(i1)     !0.5d0*(ddzur(i1)+conjg(ddzur(i1)))
           write(*,*)'gctGlU(i1)    ',  gctGlU(i1)     !0.5d0*(ddzul(i1)+conjg(ddzul(i1)))
           write(*,*)'gctGrD(i1)    ',  gctGrD(i1)     !0.5d0*(ddzdr(i1)+conjg(ddzdr(i1)))
           write(*,*)'gctGlD(i1)    ',  gctGlD(i1)     !0.5d0*(ddzdl(i1)+conjg(ddzdl(i1)))
           write(*,*)'gctGrC(i1)    ',  gctGrC(i1)     !0.5d0*(ddzcr(i1)+conjg(ddzcr(i1)))
           write(*,*)'gctGlC(i1)    ',  gctGlC(i1)     !0.5d0*(ddzcl(i1)+conjg(ddzcl(i1)))
           write(*,*)'gctGrS(i1)    ',  gctGrS(i1)     !0.5d0*(ddzsr(i1)+conjg(ddzsr(i1)))
           write(*,*)'gctGlS(i1)    ',  gctGlS(i1)     !0.5d0*(ddzsl(i1)+conjg(ddzsl(i1)))
           write(*,*)'gctGrT(i1)    ',  gctGrT(i1)     !0.5d0*(ddztr(i1)+conjg(ddztr(i1)))
           write(*,*)'gctGlT(i1)    ',  gctGlT(i1)     !0.5d0*(ddztl(i1)+conjg(ddztl(i1)))
           write(*,*)'gctGrB(i1)    ',  gctGrB(i1)     !0.5d0*(ddzbr(i1)+conjg(ddzbr(i1)))
           write(*,*)'gctGlB(i1)    ',  gctGlB(i1)     !0.5d0*(ddzbl(i1)+conjg(ddzbl(i1)))
           write(*,*)'gctZrne(i1)   ',  gctZrne(i1)  *unite   !0d0 ! gnp       !0d0 ! q       !0
           write(*,*)'gctZlne(i1)   ',  gctZlne(i1)  *unite   !gnm*(ccgm(i1)*i3n/gnm+0.5d0*ddzz(i1) &
           write(*,*)'gctZrnmu(i1)  ',  gctZrnmu(i1) *unite    !0d0 ! gnp       !0d0 ! q       !0
           write(*,*)'gctZlnmu(i1)  ',  gctZlnmu(i1) *unite    !gnm*(ccgm(i1)*i3n/gnm+0.5d0*ddzz(i1) &
           write(*,*)'gctZrntau(i1) ',  gctZrntau(i1)*unite     !0d0 ! gnp       !0d0 ! q       !0
           write(*,*)'gctZlntau(i1) ',  gctZlntau(i1)*unite     !gnm*(ccgm(i1)*i3n/gnm+0.5d0*ddzz(i1) &
           write(*,*)'gctZre(i1)    ',  gctZre(i1)   *unite  !glp*(ccgp(i1)*ql/glp +0.5d0*ddzz(i1) &
           write(*,*)'gctZle(i1)    ',  gctZle(i1)   *unite  !glm*(ccgp(i1)*ql/glm + ccgm(i1)*i3l/glm &
           write(*,*)'gctZrmu(i1)   ',  gctZrmu(i1)  *unite   !glp*(ccgp(i1)*ql/glp +0.5d0*ddzz(i1) &
           write(*,*)'gctZlmu(i1)   ',  gctZlmu(i1)  *unite   !glm*(ccgp(i1)*ql/glm + ccgm(i1)*i3l/glm &
           write(*,*)'gctZrtau(i1)  ',  gctZrtau(i1) *unite    !glp*(ccgp(i1)*ql/glp +0.5d0*ddzz(i1) &
           write(*,*)'gctZltau(i1)  ',  gctZltau(i1) *unite    !glm*(ccgp(i1)*ql/glm + ccgm(i1)*i3l/glm &
           write(*,*)'gctZrU(i1)    ',  gctZrU(i1)   *unite  !gup*(ccgp(i1)*qu/gup +0.5d0*ddzz(i1) &
           write(*,*)'gctZlU(i1)    ',  gctZlU(i1)   *unite  !gum*(ccgp(i1)*qu/gum + ccgm(i1)*i3u/gum &
           write(*,*)'gctZrC(i1)    ',  gctZrC(i1)   *unite  !gup*(ccgp(i1)*qu/gup +0.5d0*ddzz(i1) &
           write(*,*)'gctZlC(i1)    ',  gctZlC(i1)   *unite  !gum*(ccgp(i1)*qu/gum + ccgm(i1)*i3u/gum &
           write(*,*)'gctZrT(i1)    ',  gctZrT(i1)   *unite  !gup*(ccgp(i1)*qu/gup +0.5d0*ddzz(i1) &
           write(*,*)'gctZlT(i1)    ',  gctZlT(i1)   *unite  !gum*(ccgp(i1)*qu/gum + ccgm(i1)*i3u/gum &
           write(*,*)'gctZrD(i1)    ',  gctZrD(i1)   *unite  !gdp*(ccgp(i1)*qd/gdp +0.5d0*ddzz(i1) &
           write(*,*)'gctZlD(i1)    ',  gctZlD(i1)   *unite  !gdm*(ccgp(i1)*qd/gdm + ccgm(i1)*i3d/gdm &
           write(*,*)'gctZrS(i1)    ',  gctZrS(i1)   *unite  !gdp*(ccgp(i1)*qd/gdp +0.5d0*ddzz(i1) &
           write(*,*)'gctZlS(i1)    ',  gctZlS(i1)   *unite  !gdm*(ccgp(i1)*qd/gdm + ccgm(i1)*i3d/gdm &
           write(*,*)'gctZrB(i1)    ',  gctZrB(i1)   *unite  !gdp*(ccgp(i1)*qd/gdp +0.5d0*ddzz(i1) &
           write(*,*)'gctZlB(i1)    ',  gctZlB(i1)   *unite  !gdm*(ccgp(i1)*qd/gdm + ccgm(i1)*i3d/gdm &
           write(*,*)'gctHre(i1)    ',  gctHre(i1)   *unite  !coeff*me*( ddee(i1)-ddswsw(i1)+ddme2ome(i1)  &
           write(*,*)'gctHle(i1)    ',  gctHle(i1)   *unite  !coeff*me*( ddee(i1)-ddswsw(i1)+ddme2ome(i1)  &
           write(*,*)'gctHrmu (i1)  ',  gctHrmu (i1) *unite    !coeff*mm*(ddee(i1)-ddswsw(i1)+ddmm2omm(i1)  &
           write(*,*)'gctHlmu(i1)   ',  gctHlmu(i1)  *unite   !mm*coeff*(ddee(i1)-ddswsw(i1)+ddmm2omm(i1)  &
           write(*,*)'gctHrtau(i1)  ',  gctHrtau(i1) *unite    !coeff*mtl*(ddee(i1)-ddswsw(i1)+ddmtl2omtl(i1) & 
           write(*,*)'gctHltau(i1)  ',  gctHltau(i1) *unite    !mtl*coeff*(ddee(i1)-ddswsw(i1)+ddmtl2omtl(i1)  &
           write(*,*)'gctHrU(i1)    ',  gctHrU(i1)   *unite  !coeff*mu*( ddee(i1)-ddswsw(i1)+ddmu2omu(i1)  &
           write(*,*)'gctHlU(i1)    ',  gctHlU(i1)   *unite  !coeff*mu*( ddee(i1)-ddswsw(i1)+ddmu2omu(i1)  &
           write(*,*)'gctHrD(i1)    ',  gctHrD(i1)   *unite  !coeff*md*( ddee(i1)-ddswsw(i1)+ddmd2omd(i1)  &
           write(*,*)'gctHlD(i1)    ',  gctHlD(i1)   *unite  !coeff*md*( ddee(i1)-ddswsw(i1)+ddmd2omd(i1)  &
           write(*,*)'gctHrC(i1)    ',  gctHrC(i1)   *unite  !coeff*mc*( ddee(i1)-ddswsw(i1)+ddmc2omc(i1)  &
           write(*,*)'gctHlC(i1)    ',  gctHlC(i1)   *unite  !coeff*mc*( ddee(i1)-ddswsw(i1)+ddmc2omc(i1)  &
           write(*,*)'gctHrS(i1)    ',  gctHrS(i1)   *unite  !coeff*ms*( ddee(i1)-ddswsw(i1)+ddms2oms(i1)  &
           write(*,*)'gctHlS(i1)    ',  gctHlS(i1)   *unite  !coeff*ms*( ddee(i1)-ddswsw(i1)+ddms2oms(i1)  &
           write(*,*)'gctHrT(i1)    ',  gctHrT(i1)   *unite  !coeff*mt*( ddee(i1)-ddswsw(i1)+ddmt2omt(i1) &
           write(*,*)'gctHlT(i1)    ',  gctHlT(i1)   *unite  !coeff*mt*( ddee(i1)-ddswsw(i1)+ddmt2omt(i1)  &
           write(*,*)'gctHrB(i1)    ',  gctHrB(i1)   *unite  !coeff*mb*( ddee(i1)-ddswsw(i1)+ddmb2omb(i1)  &
           write(*,*)'gctHlB(i1)    ',  gctHlB(i1)   *unite  !coeff*mb*( ddee(i1)-ddswsw(i1)+ddmb2omb(i1)  &
           write(*,*)'gctXre(i1)    ',  gctXre(i1)   *unite  !+coeff*me*i3l*( ddee(i1)-ddswsw(i1)  &
           write(*,*)'gctXle(i1)    ',  gctXle(i1)   *unite  !+coeff*me*i3l*( ddee(i1)-ddswsw(i1)  &
           write(*,*)'gctXrmu(i1)   ',  gctXrmu(i1)  *unite   !+coeff*mm*i3l*( ddee(i1)-ddswsw(i1)  &
           write(*,*)'gctXlmu(i1)   ',  gctXlmu(i1)  *unite   !+coeff*mm*i3l*( ddee(i1)-ddswsw(i1)  &
           write(*,*)'gctXrtau(i1)  ',  gctXrtau(i1) *unite    !+coeff*mtl*i3l*( ddee(i1)-ddswsw(i1)  &
           write(*,*)'gctXltau(i1)  ',  gctXltau(i1) *unite    !+coeff*mtl*i3l*( ddee(i1)-ddswsw(i1)  &
           write(*,*)'gctXrU(i1)    ',  gctXrU(i1)   *unite  !+coeff*mu*i3u*( ddee(i1)-ddswsw(i1)  &
           write(*,*)'gctXlU(i1)    ',  gctXlU(i1)   *unite  !+coeff*mu*i3u*( ddee(i1)-ddswsw(i1)  &
           write(*,*)'gctXrC(i1)    ',  gctXrC(i1)   *unite  !+coeff*mc*i3u*( ddee(i1)-ddswsw(i1)  &
           write(*,*)'gctXlC(i1)    ',  gctXlC(i1)   *unite  !+coeff*mc*i3u*( ddee(i1)-ddswsw(i1)  &
           write(*,*)'gctXrT(i1)    ',  gctXrT(i1)   *unite  !+coeff*mt*i3u*( ddee(i1)-ddswsw(i1)  &
           write(*,*)'gctXlT(i1)    ',  gctXlT(i1)   *unite  !+coeff*mt*i3u*( ddee(i1)-ddswsw(i1)  &
           write(*,*)'gctXrD(i1)    ',  gctXrD(i1)   *unite  !+coeff*md*i3d*( ddee(i1)-ddswsw(i1)  &
           write(*,*)'gctXlD(i1)    ',  gctXlD(i1)   *unite  !+coeff*md*i3d*( ddee(i1)-ddswsw(i1)  &
           write(*,*)'gctXrS(i1)    ',  gctXrS(i1)   *unite  !+coeff*ms*i3d*( ddee(i1)-ddswsw(i1)  &
           write(*,*)'gctXlS(i1)    ',  gctXlS(i1)   *unite  !+coeff*ms*i3d*( ddee(i1)-ddswsw(i1)  &
           write(*,*)'gctXrB(i1)    ',  gctXrB(i1)   *unite  !+coeff*mb*i3d*( ddee(i1)-ddswsw(i1)  &
           write(*,*)'gctXlB(i1)    ',  gctXlB(i1)   *unite  !+coeff*mb*i3d*( ddee(i1)-ddswsw(i1)  &
           write(*,*)'gctPpre(i1)   ',  gctPpre(i1)  *unite   !-coeff*me*(ddee(i1)-ddswsw(i1) &
           write(*,*)'gctPple(i1)   ',  gctPple(i1)  *unite   !0d0! mnu*
           write(*,*)'gctPprmu(i1)  ',  gctPprmu(i1) *unite    !-coeff*mm*(ddee(i1)-ddswsw(i1) &
           write(*,*)'gctPplmu(i1)  ',  gctPplmu(i1) *unite    !0d0! mnu*
           write(*,*)'gctPprtau(i1) ',  gctPprtau(i1)*unite     !-coeff*mtl*(ddee(i1)-ddswsw(i1) &
           write(*,*)'gctPpltau(i1) ',  gctPpltau(i1)*unite     !0d0! mnu*
           write(*,*)'gctPprud(i1)  ',  gctPprud(i1) *unite    !-coeff*md*(ddee(i1)-ddswsw(i1) &
           write(*,*)'gctPplud(i1)  ',  gctPplud(i1) *unite    !+coeff*mu*(ddee(i1)-ddswsw(i1) &
           write(*,*)'gctPprcs(i1)  ',  gctPprcs(i1) *unite    !-coeff*ms*(ddee(i1)-ddswsw(i1) &
           write(*,*)'gctPplcs(i1)  ',  gctPplcs(i1) *unite    !+coeff*mc*(ddee(i1)-ddswsw(i1) &
           write(*,*)'gctPprtb(i1)  ',  gctPprtb(i1) *unite    !-coeff*mb*(ddee(i1)-ddswsw(i1) &
           write(*,*)'gctPpltb(i1)  ',  gctPpltb(i1) *unite    !+coeff*mt*(ddee(i1)-ddswsw(i1) &
           write(*,*)'gctPmre(i1)   ',  gctPmre(i1)  *unite   !0d0!mnu
           write(*,*)'gctPmle(i1)   ',  gctPmle(i1)  *unite   !-coeff*me*(ddee(i1)-ddswsw(i1) &
           write(*,*)'gctPmrmu(i1)  ',  gctPmrmu(i1) *unite    !0d0!mnu
           write(*,*)'gctPmlmu(i1)  ',  gctPmlmu(i1) *unite    !-coeff*mm*(ddee(i1)-ddswsw(i1) &
           write(*,*)'gctPmrtau(i1) ',  gctPmrtau(i1)*unite     !0d0!mnu
           write(*,*)'gctPmltau(i1) ',  gctPmltau(i1)*unite     !-coeff*mtl*(ddee(i1)-ddswsw(i1) &
           write(*,*)'gctPmrud(i1)  ',  gctPmrud(i1) *unite    !+coeff*mu*(ddee(i1)-ddswsw(i1) &
           write(*,*)'gctPmlud(i1)  ',  gctPmlud(i1) *unite    !-coeff*md*(ddee(i1)-ddswsw(i1) &
           write(*,*)'gctPmrcs(i1)  ',  gctPmrcs(i1) *unite    !+coeff*mc*(ddee(i1)-ddswsw(i1) &
           write(*,*)'gctPmlcs(i1)  ',  gctPmlcs(i1) *unite    !-coeff*ms*(ddee(i1)-ddswsw(i1) &
           write(*,*)'gctPmrtb(i1)  ',  gctPmrtb(i1) *unite    !+coeff*mt*(ddee(i1)-ddswsw(i1) &
           write(*,*)'gctPmltb(i1)  ',  gctPmltb(i1) *unite    !-coeff*mb*(ddee(i1)-ddswsw(i1) &
        end do
      end subroutine printallgct
      
end module [% process_name asprefix=\_ %]_ew_ct