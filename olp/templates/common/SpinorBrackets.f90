module SpinorBrackets
    use config, only: ki
    implicit none

    type SpinorBracket
        real(ki), dimension(0:3) :: k1, k2
        complex(ki) :: value = (0.0, 0.0)
        logical :: needs_evaluation = .true.
    contains
        procedure :: get => Sp_get
        procedure :: evaluate => Sp_evaluate
    end type

    type, extends(SpinorBracket) :: Spaa
    contains
        procedure :: evaluate => Spaa_evaluate
    end type

    type, extends(SpinorBracket) :: Spbb
    contains
        procedure :: evaluate => Spbb_evaluate
    end type

    type Spab3_vec
        real(ki), dimension(0:3) :: k1, k2
        complex(ki), dimension(0:3) :: value = 0.0d0
        logical :: needs_evaluation = .true.
    contains
        procedure :: get => Spab3_vec_get
        procedure :: evaluate => Spab3_vec_evaluate
    end type Spab3_vec

    public operator (*)
    interface operator(*)
        module procedure mult_Sp_real
        module procedure mult_real_Sp
        module procedure mult_Sp_complex
        module procedure mult_complex_Sp
        module procedure mult_Sp_Sp
        module procedure mult_Sp3vec_real
        module procedure mult_real_Sp3vec
        module procedure mult_Sp3vec_complex
        module procedure mult_complex_Sp3vec
    end interface

    public operator (/)
    interface operator(/)
        module procedure div_Sp_real
        module procedure div_real_Sp
        module procedure div_Sp_complex
        module procedure div_complex_Sp
        module procedure div_Sp_Sp
        module procedure div_Sp3vec_real
        module procedure div_Sp3vec_complex
    end interface

    public operator (+)
    interface operator(+)
        module procedure add_Sp_real
        module procedure add_real_Sp
        module procedure add_Sp_complex
        module procedure add_complex_Sp
        module procedure add_Sp_Sp
    end interface

    public operator (-)
    interface operator(-)
        module procedure sub_Sp
        module procedure sub_Sp_real
        module procedure sub_real_Sp
        module procedure sub_Sp_complex
        module procedure sub_complex_Sp
        module procedure sub_Sp_Sp
    end interface

    public operator (**)
    interface operator(**)
        module procedure pow_Sp_real
        module procedure pow_Sp_int
    end interface

    interface conjg
        module procedure Sp_conjg
    end interface

    interface dotproduct
        module procedure dotproduct_Sp_r
        module procedure dotproduct_r_Sp
        module procedure dotproduct_Sp_c
        module procedure dotproduct_c_Sp
        module procedure dotproduct_Sp_Sp
     end interface dotproduct

contains

    function Sp_get(self) result(res)
        implicit none
        class(SpinorBracket) :: self
        complex(ki) :: res
        if (self%needs_evaluation) then
            call self%evaluate()
            self%needs_evaluation = .false.
        end if
        res = self%value
    end function Sp_get

    subroutine Sp_evaluate(self)
        implicit none
        class(SpinorBracket), intent(inout) :: self
    end subroutine

    function mult_Sp_real(sp, r)
        implicit none
        class(SpinorBracket), intent(in) :: sp
        real(ki), intent(in) :: r
        complex(ki):: mult_Sp_real
        mult_Sp_real = sp%get() * r
    end function

    function mult_real_Sp(r, sp)
        implicit none
        class(SpinorBracket), intent(in) :: sp
        real(ki), intent(in) :: r
        complex(ki):: mult_real_Sp
        mult_real_Sp = sp%get() * r
    end function

    function mult_Sp_complex(sp, r)
        implicit none
        class(SpinorBracket), intent(in) :: sp
        complex(ki), intent(in) :: r
        complex(ki):: mult_Sp_complex
        mult_Sp_complex = sp%get() * r
    end function

    function mult_complex_Sp(r, sp)
        implicit none
        class(SpinorBracket), intent(in) :: sp
        complex(ki), intent(in) :: r
        complex(ki):: mult_complex_Sp
        mult_complex_Sp = sp%get() * r
    end function

    function mult_Sp_Sp(sp1, sp2)
      implicit none
      class(SpinorBracket), intent(in) :: sp1, sp2
      complex(ki):: mult_Sp_Sp
      mult_Sp_Sp = sp1%get() * sp2%get()
    end function

    function div_Sp_real(sp, r)
        implicit none
        class(SpinorBracket), intent(in) :: sp
        real(ki), intent(in) :: r
        complex(ki):: div_Sp_real
        div_Sp_real = sp%get() / r
    end function

    function div_real_Sp(r, sp)
        implicit none
        class(SpinorBracket), intent(in) :: sp
        real(ki), intent(in) :: r
        complex(ki):: div_real_Sp
        div_real_Sp = r / sp%get()
    end function

    function div_Sp_complex(sp, r)
        implicit none
        class(SpinorBracket), intent(in) :: sp
        complex(ki), intent(in) :: r
        complex(ki):: div_Sp_complex
        div_Sp_complex = sp%get() / r
    end function

    function div_complex_Sp(r, sp)
        implicit none
        class(SpinorBracket), intent(in) :: sp
        complex(ki), intent(in) :: r
        complex(ki):: div_complex_Sp
        div_complex_Sp = r / sp%get()
    end function

    function div_Sp_Sp(sp1, sp2)
         implicit none
         class(SpinorBracket), intent(in) :: sp1, sp2
         complex(ki):: div_Sp_Sp
         div_Sp_Sp = sp1%get() / sp2%get()
    end function

    function add_Sp_real(sp, r)
        implicit none
        class(SpinorBracket), intent(in) :: sp
        real(ki), intent(in) :: r
        complex(ki):: add_Sp_real
        add_Sp_real = sp%get() + r
    end function

    function add_real_Sp(r, sp)
        implicit none
        class(SpinorBracket), intent(in) :: sp
        real(ki), intent(in) :: r
        complex(ki):: add_real_Sp
        add_real_Sp = r + sp%get()
    end function

    function add_Sp_complex(sp, r)
        implicit none
        class(SpinorBracket), intent(in) :: sp
        complex(ki), intent(in) :: r
        complex(ki):: add_Sp_complex
        add_Sp_complex = sp%get() + r
    end function

    function add_complex_Sp(r, sp)
        implicit none
        class(SpinorBracket), intent(in) :: sp
        complex(ki), intent(in) :: r
        complex(ki):: add_complex_Sp
        add_complex_Sp = r + sp%get()
    end function

    function add_Sp_Sp(sp1, sp2)
      implicit none
      class(SpinorBracket), intent(in) :: sp1, sp2
      complex(ki):: add_Sp_Sp
      add_Sp_Sp = sp1%get() + sp2%get()
    end function

    function sub_Sp(sp)
        implicit none
        class(SpinorBracket), intent(in) :: sp
        complex(ki):: sub_Sp
        sub_Sp = -sp%get()
    end function

    function sub_Sp_real(sp, r)
        implicit none
        class(SpinorBracket), intent(in) :: sp
        real(ki), intent(in) :: r
        complex(ki):: sub_Sp_real
        sub_Sp_real = sp%get() - r
    end function

    function sub_real_Sp(r, sp)
        implicit none
        class(SpinorBracket), intent(in) :: sp
        real(ki), intent(in) :: r
        complex(ki):: sub_real_Sp
        sub_real_Sp = r - sp%get()
    end function

    function sub_Sp_complex(sp, r)
        implicit none
        class(SpinorBracket), intent(in) :: sp
        complex(ki), intent(in) :: r
        complex(ki):: sub_Sp_complex
        sub_Sp_complex = sp%get() - r
    end function

    function sub_complex_Sp(r, sp)
        implicit none
        class(SpinorBracket), intent(in) :: sp
        complex(ki), intent(in) :: r
        complex(ki):: sub_complex_Sp
        sub_complex_Sp = r - sp%get()
    end function

    function sub_Sp_Sp(sp1, sp2)
      implicit none
      class(SpinorBracket), intent(in) :: sp1, sp2
      complex(ki):: sub_Sp_Sp
      sub_Sp_Sp = sp1%get() - sp2%get()
    end function

    function pow_Sp_real(sp, r)
        implicit none
        class(SpinorBracket), intent(in) :: sp
        real(ki), intent(in) :: r
        complex(ki):: pow_Sp_real
        pow_Sp_real = sp%get()**(r)
    end function

    function pow_Sp_int(sp, r)
        implicit none
        class(SpinorBracket), intent(in) :: sp
        integer, intent(in) :: r
        complex(ki):: pow_Sp_int
        pow_Sp_int = sp%get()**(r)
    end function

    function Sp_conjg(sp) result(res)
        implicit none
        class(SpinorBracket), intent(in) :: sp
        complex(ki) :: res
        res = conjg(sp%get())
    end function

    subroutine Spaa_evaluate(self)
        implicit none
        class(Spaa), intent(inout) :: self

        real(ki) :: rt1, rt2
        complex(ki) :: c231, c232, f1, f2
    !---if one of the vectors happens to be zero this routine fails.
    !-----positive energy case
        if (self%k1(0) .gt. 0.0_ki) then
            rt1=sqrt(self%k1(0)+self%k1(1))
            c231=cmplx(self%k1(3),-self%k1(2), ki)
            f1=1.0_ki
        else
    !-----negative energy case
            rt1=sqrt(-self%k1(0)-self%k1(1))
            c231=cmplx(-self%k1(3),self%k1(2), ki)
            f1=(0.0_ki, 1.0_ki)
        endif
    !-----positive energy case
        if (self%k2(0) .gt. 0.0_ki) then
            rt2=sqrt(self%k2(0)+self%k2(1))
            c232=cmplx(self%k2(3),-self%k2(2), ki)
            f2=1.0_ki
        else
    !-----negative energy case
            rt2=sqrt(-self%k2(0)-self%k2(1))
            c232=cmplx(-self%k2(3),self%k2(2), ki)
            f2=(0.0_ki, 1.0_ki)
        endif
        self%value = -f2*f1*(c232*rt1/rt2-c231*rt2/rt1)
    end subroutine Spaa_evaluate

    subroutine Spbb_evaluate(self)
    implicit none
    class(Spbb), intent(inout) :: self

    real(ki) :: rt1, rt2
    complex(ki) :: c231, c232, f1, f2
    !---if one of the vectors happens to be zero this routine fails.
    !-----positive energy case
        if (self%k1(0) .gt. 0.0_ki) then
            rt1=sqrt(self%k1(0)+self%k1(1))
            c231=cmplx(self%k1(3),-self%k1(2), ki)
            f1=1.0_ki
        else
    !-----negative energy case
            rt1=sqrt(-self%k1(0)-self%k1(1))
            c231=cmplx(-self%k1(3),self%k1(2), ki)
            f1=(0.0_ki, 1.0_ki)
        endif
    !-----positive energy case
        if (self%k2(0) .gt. 0.0_ki) then
            rt2=sqrt(self%k2(0)+self%k2(1))
            c232=cmplx(self%k2(3),-self%k2(2), ki)
            f2=1.0_ki
        else
    !-----negative energy case
            rt2=sqrt(-self%k2(0)-self%k2(1))
            c232=cmplx(-self%k2(3),self%k2(2), ki)
            f2=(0.0_ki, 1.0_ki)
        endif
        self%value = sign(1.0_ki, self%k1(0)*self%k2(0) - self%k1(1)*self%k2(1) - self%k1(2)*self%k2(2) &
                & - self%k1(2)*self%k2(2)) * conjg(-f2*f1*(c231*rt2/rt1-c232*rt1/rt2))
    end subroutine Spbb_evaluate

    function Spab3_vec_get(self) result(res)
        implicit none
        class(Spab3_vec) :: self
        complex(ki), dimension(4) :: res
        if (self%needs_evaluation) then
            call self%evaluate()
            self%needs_evaluation = .true.
        end if
        res = self%value
    end function Spab3_vec_get

    subroutine Spab3_vec_evaluate(self)
        implicit none
        complex(ki), parameter :: i_ = (0.0_ki, 1.0_ki)

        class(Spab3_vec), intent(inout) :: self

        complex(ki) :: pr1, pr2, pl1, pl2
        complex(ki) :: f1, f2
        real(ki) :: flip1, flip2, rt1, rt2

        !-----positive energy case
        if (self%k1(0) .gt. 0.0_ki) then
            flip1=1.0_ki
            f1=1.0_ki
        else
            flip1=-1.0_ki
            f1=(0.0_ki, 1.0_ki)
        endif
        rt1=sqrt(flip1*(self%k1(0)+self%k1(1)))
        pr1=cmplx(flip1*self%k1(3),-flip1*self%k1(2), ki)
        pl1=conjg(pr1)

        if (self%k2(0) .gt. 0.0_ki) then
            flip2=1.0_ki
            f2=1.0_ki
        else
            flip2=-1.0_ki
            f2=(0.0_ki, 1.0_ki)
        endif
        rt2=sqrt(flip2*(self%k2(0)+self%k2(1)))
        pr2=cmplx(flip2*self%k2(3),-flip2*self%k2(2), ki)
        pl2=conjg(pr2)

        self%value(0) = f1*f2*(pr1*pl2/rt1/rt2 + rt1*rt2)
        self%value(1) = f1*f2*(rt1*rt2 - pr1*pl2/rt1/rt2)
        self%value(2) = i_*f1*f2*(pr1*rt2/rt1 - rt1*pl2/rt2)
        self%value(3) = f1*f2*(pr1*rt2/rt1 + rt1*pl2/rt2)
    end subroutine Spab3_vec_evaluate

    function mult_Sp3vec_real(sp, r)
        implicit none
        class(Spab3_vec), intent(in) :: sp
        real(ki), intent(in) :: r
        complex(ki), dimension(4) :: mult_Sp3vec_real
        mult_Sp3vec_real = sp%get() * r
    end function

    function mult_real_Sp3vec(r, sp)
        implicit none
        class(Spab3_vec), intent(in) :: sp
        real(ki), intent(in) :: r
        complex(ki), dimension(4) :: mult_real_Sp3vec
        mult_real_Sp3vec = sp%get() * r
    end function

    function mult_Sp3vec_complex(sp, r)
        implicit none
        class(Spab3_vec), intent(in) :: sp
        complex(ki), intent(in) :: r
        complex(ki), dimension(4) :: mult_Sp3vec_complex
        mult_Sp3vec_complex = sp%get() * r
    end function

    function mult_complex_Sp3vec(r, sp)
        implicit none
        class(Spab3_vec), intent(in) :: sp
        complex(ki), intent(in) :: r
        complex(ki), dimension(4) :: mult_complex_Sp3vec
        mult_complex_Sp3vec = sp%get() * r
    end function

    function div_Sp3vec_real(sp, r)
        implicit none
        class(Spab3_vec), intent(in) :: sp
        real(ki), intent(in) :: r
        complex(ki), dimension(4) :: div_Sp3vec_real
        div_Sp3vec_real = sp%get() / r
    end function

    function div_Sp3vec_complex(sp, r)
        implicit none
        class(Spab3_vec), intent(in) :: sp
        complex(ki), intent(in) :: r
        complex(ki), dimension(4) :: div_Sp3vec_complex
        div_Sp3vec_complex = sp%get() / r
    end function

    function dotproduct_Sp_r(Sp, q)
       implicit none
       class(Spab3_vec), intent(in) :: Sp
       complex(ki), dimension(0:3) :: p
       real(ki), dimension(4), intent(in) :: q
       complex(ki) :: dotproduct_Sp_r
       p = Sp%get()
       dotproduct_Sp_r = p(0)*q(1) - p(1)*q(2) - p(2)*q(3) - p(3)*q(4)
    end  function dotproduct_Sp_r

    function dotproduct_r_Sp(p, Sp)
        implicit none
        class(Spab3_vec), intent(in) :: Sp
        complex(ki), dimension(0:3) :: q
        real(ki), dimension(4), intent(in) :: p
        complex(ki) :: dotproduct_r_Sp
        q = Sp%get()
        dotproduct_r_Sp = p(1)*q(0) - p(2)*q(1) - p(3)*q(2) - p(4)*q(3)
    end  function dotproduct_r_Sp

    function dotproduct_Sp_c(Sp, q)
        implicit none
        class(Spab3_vec), intent(in) :: Sp
        complex(ki), dimension(0:3) :: p
        complex(ki), dimension(4), intent(in) :: q
        complex(ki) :: dotproduct_Sp_c
        p = Sp%get()
        dotproduct_Sp_c = p(0)*q(1) - p(1)*q(2) - p(2)*q(3) - p(3)*q(4)
    end  function dotproduct_Sp_c

    function dotproduct_c_Sp(p, Sp)
        implicit none
        class(Spab3_vec), intent(in) :: Sp
        complex(ki), dimension(0:3) :: q
        complex(ki), dimension(4), intent(in) :: p
        complex(ki) :: dotproduct_c_Sp
        q = Sp%get()
        dotproduct_c_Sp = p(1)*q(0) - p(2)*q(1) - p(3)*q(2) - p(4)*q(3)
    end  function dotproduct_c_Sp

    function dotproduct_Sp_Sp(Sp1, Sp2)
        implicit none
        class(Spab3_vec), intent(in) :: Sp1, Sp2
        complex(ki), dimension(0:3) :: p, q
        complex(ki) :: dotproduct_Sp_Sp
        p = Sp1%get()
        q = Sp2%get()
        dotproduct_Sp_Sp = p(0)*q(0) - p(1)*q(1) - p(2)*q(2) - p(3)*q(3)
    end  function dotproduct_Sp_Sp
end module