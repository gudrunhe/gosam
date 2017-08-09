#include <iostream>
#include <cassert>
#include <vector>
#include <quadmath.h>

#define SQMASS_THRESHOLD  1e-13
#define MAX_ITERATIONS    16


template <typename T, typename U>
static T truncate(const T val, const T acc, int numscales, const U* scales)
{
  T ans = val;
  bool known = false;
  for (int i=0; i<numscales; i++) {
    if (fabsq(val - T(scales[i])) < acc) {
      ans = T(scales[i]);
      known = true;
      break;
    }
  }
  //  if (not known) {
  //    std::cout<<"unknown scale " << val<<std::endl;
  //  }
  return ans;
}


std::ostream& operator<<(std::ostream& out, const __float128& value)
{
  char* str = new char[50];
  quadmath_snprintf(str, 50, "%Qf", value);
  out<<str;
  return out;
}


template <typename SRC, typename DST, typename SCT>
void refineMomenta(const int NN, const SRC* pin, DST* pout, int numscales2, const SCT* scales2)
{
/*
F = {
  s0 + q0 + p0 == 0,
  s3 + q3 + p3 == 0,
  q0^2 - q12sq - q3^2 - qM^2,
  p0^2 - p12sq - p3^2 - pM^2}
  X = {q0, q3, p0, p3}
J = {{1, 0, 1, 0},
     {0, 1, 0, 1},
     {2 q0, -2 q3, 0, 0},
     {0, 0, 2 p0, -2 p3}}
J(X_n) (X_n+1 - X_n) = -F(X_n)
*/
//  SRC* pin;
//  DST* pout;

// Find the two particles to be modified last
  int np = NN-2;
  int nq = NN-1;

  SRC x1x2maxp = 0;
  SRC x1x2maxq = 0;

  DST scale = 0.;
  for (int n=0; n<NN; n++) {
    const DST x0abs = fabsq(pin[0+4*n]);
    if (x0abs > scale) {
      scale = x0abs;
    }
    const SRC x1x2abs = fabsq(pin[1+4*n]*pin[2+4*n]);
    if (x1x2abs > x1x2maxq) {
      if (nq != n) {
        x1x2maxp = x1x2maxq;
        np = nq;
      }
      if (np != n) {
        x1x2maxq = x1x2abs;
        nq = n;
      }
    } else if (x1x2abs > x1x2maxp) {
      if (nq != n) {
        x1x2maxp = x1x2abs;
        np = n;
      }
    }
  }
  assert(nq != np);

// Fix all the other particles
  const DST M2acc = (scale*scale)*SQMASS_THRESHOLD;

  DST s0 = DST();
  DST s1 = DST();
  DST s2 = DST();
  DST s3 = DST();

  for (int n=0; n<NN; n++) {
    if (n == np or n == nq) continue;

    const DST nP2 = DST(pin[1+4*n])*pin[1+4*n]
                  + DST(pin[2+4*n])*pin[2+4*n]
                  + DST(pin[3+4*n])*pin[3+4*n];
    DST nM2 = DST(pin[0+4*n])*pin[0+4*n] - nP2;

    // if we are close enough to a known scale, assume it is equal to it
    nM2 = truncate(nM2, M2acc, numscales2, scales2);


    // fix on-shellness of particles other than np or nq
    DST energy = sqrtq(nP2 + nM2);
    if (pin[0+4*n] < 0.) {
      energy = -energy;
    }
    pout[0+4*n] = energy;
    pout[1+4*n] = pin[1+4*n];
    pout[2+4*n] = pin[2+4*n];
    pout[3+4*n] = pin[3+4*n];

    DST sign = 1.;
    if (n<2)
      sign=-1.;

    s0 += sign*pout[0+4*n];
    s1 += sign*pout[1+4*n];
    s2 += sign*pout[2+4*n];
    s3 += sign*pout[3+4*n];
  }

  //Now do the last 2 particles
  const DST p1 = pout[1+4*np] = pin[1+4*np];
  const DST p2 = pout[2+4*np] = pin[2+4*np];
  const DST q1 = pout[1+4*nq] = -(pin[1+4*np] + s1);
  const DST q2 = pout[2+4*nq] = -(pin[2+4*np] + s2);

  DST p0 = pin[0+4*np];
  DST p3 = pin[3+4*np];
  DST q0 = pin[0+4*nq];
  DST q3 = pin[3+4*nq];

  const DST p12sq = p1*p1 + p2*p2;
  const DST q12sq = q1*q1 + q2*q2;

  DST pM2 = p0*p0 - (p12sq + p3*p3);
  DST qM2 = q0*q0 - (q12sq + q3*q3);

  pM2 = truncate(pM2, M2acc, numscales2, scales2);
  qM2 = truncate(qM2, M2acc, numscales2, scales2);

  DST dist = 1e30;
  DST prevdist = 1e31;
  int count = 0;

  DST newq0 = q0;
  DST newq3 = q3;
  DST newp0 = p0;
  DST newp3 = p3;

  do {
    q0 = newq0;
    q3 = newq3;
    p0 = newp0;
    p3 = newp3;

    const DST detJ = 4.*(q0*p3 - q3*p0);
    if (detJ == 0.) {
      std::cout<<"det(J) == " << detJ << " expect nan"<<std::endl;
    }

    const DST ex1 = 2.*p12sq - 2.*p3*p3 + 2.*pM2 + 4.*p0*s0 - 4.*p3*s3;
    const DST exq12 = 2.*q12sq + 2.*qM2;
    const DST exr12 = 2.*p12sq + 2.*pM2;
    const DST dq0 = (p3*(-2.*q0*q0 + exq12) + q3*(2.*p0*p0 - 2.*q3*p3 + 4.*q0*p0 + ex1))/detJ;
    const DST dq3 = (p0*( 2.*q3*q3 + exq12) + q0*(2.*p0*p0 + 2.*p0*q0 - 4.*q3*p3 + ex1))/detJ;
    const DST dp0 = (p3*(-2.*q0*q0 - exq12 - 4.*q0*p0 + 2.*q3*q3 - 4.*q0*s0)
                   + q3*(-exr12 + 2.*p0*p0 + 2.*p3*p3 + 4.*p3*s3))/detJ;
    const DST dp3 = (q0*(-2.*p0*p0 - exr12 - 2.*q0*p0 - 2.*p3*p3 - 4.*p0*s0)
                   + p0*(-exq12 + 2.*q3*q3 + 4.*q3*p3 + 4.*q3*s3))/detJ;
    newq0 = q0 + dq0;
    newq3 = q3 + dq3;
    newp0 = p0 + dp0;
    newp3 = p3 + dp3;
    prevdist = dist;
    dist = fabsq(s0 + newp0 + newq0) + fabsq(newp0*newp0 - (p12sq + newp3*newp3 + pM2))
         + fabsq(s3 + newp3 + newq3) + fabsq(newq0*newq0 - (q12sq + newq3*newq3 + qM2));
  } while (prevdist > dist and ++count < MAX_ITERATIONS);

  if (prevdist > dist and count == MAX_ITERATIONS) {
    std::cout<<"failed to converge after " << count << " iterations"<<std::endl;
  }

  pout[0+4*np] = p0;
  pout[3+4*np] = p3;
  pout[0+4*nq] = q0;
  pout[3+4*nq] = q3;

}


template void refineMomenta(const int NN, const double* pin, double* pout, int numscales2, const double* scales2);

template void refineMomenta(const int NN, const double* pin, __float128* pout, int numscales2, const double* scales2);



extern "C" {

  void refine_momenta_to_dp_(const int& nn, const double* in, double* out, const int& nsc, const double* sc2)
  {
    refineMomenta(nn,in,out,nsc,sc2);
  }

  void refine_momenta_to_qp_(const int& nn, const double* in_gs, __float128* out_gs, const int& nsc, const double* sc2)
  {
    double in[4*nn];
    __float128 out[4*nn];

    for(int i=0; i<nn*4; i++){
      in[i] = in_gs[i/4+nn*(i%4)];
    }

    refineMomenta(nn,in,out,nsc,sc2);

    for(int i=0; i<nn*4; i++){
      out_gs[i] = out[i/nn+4*(i%nn)];
    }
  }
}
