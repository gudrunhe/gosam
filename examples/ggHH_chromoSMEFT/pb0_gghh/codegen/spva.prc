#procedure spva
* vim: syntax=form


   Id Spab3(k1, Q, k2) = Qspvak1k2;
   Id Spab3(k1, Q, l3) = Qspvak1l3;
   Id Spab3(k1, Q, l4) = Qspvak1l4;
   Id Spab3(k2, Q, k1) = Qspvak2k1;
   Id Spab3(k2, Q, l3) = Qspvak2l3;
   Id Spab3(k2, Q, l4) = Qspvak2l4;
   Id Spab3(l3, Q, k1) = Qspval3k1;
   Id Spab3(l3, Q, k2) = Qspval3k2;
   Id Spab3(l3, Q, l4) = Qspval3l4;
   Id Spab3(l4, Q, k1) = Qspval4k1;
   Id Spab3(l4, Q, k2) = Qspval4k2;
   Id Spab3(l4, Q, l3) = Qspval4l3;
   Id Spab3(k1, Q, e1) = Qspvak1e1;
   Id Spab3(e1, Q, k1) = Qspvae1k1;
   Id Spab3(k1, Q, e2) = Qspvak1e2;
   Id Spab3(e2, Q, k1) = Qspvae2k1;
   Id Spab3(k2, Q, e1) = Qspvak2e1;
   Id Spab3(e1, Q, k2) = Qspvae1k2;
   Id Spab3(k2, Q, e2) = Qspvak2e2;
   Id Spab3(e2, Q, k2) = Qspvae2k2;
   Id Spab3(l3, Q, e1) = Qspval3e1;
   Id Spab3(e1, Q, l3) = Qspvae1l3;
   Id Spab3(l3, Q, e2) = Qspval3e2;
   Id Spab3(e2, Q, l3) = Qspvae2l3;
   Id Spab3(l4, Q, e1) = Qspval4e1;
   Id Spab3(e1, Q, l4) = Qspvae1l4;
   Id Spab3(l4, Q, e2) = Qspval4e2;
   Id Spab3(e2, Q, l4) = Qspvae2l4;
   Id Spab3(e1, Q, e2) = Qspvae1e2;
   Id Spab3(e2, Q, e1) = Qspvae2e1;



   Id Spab3(k1, Q?, k2) = spvak1k2.Q;
   Id Spab3(k1, Q?, l3) = spvak1l3.Q;
   Id Spab3(k1, Q?, l4) = spvak1l4.Q;
   Id Spab3(k2, Q?, k1) = spvak2k1.Q;
   Id Spab3(k2, Q?, l3) = spvak2l3.Q;
   Id Spab3(k2, Q?, l4) = spvak2l4.Q;
   Id Spab3(l3, Q?, k1) = spval3k1.Q;
   Id Spab3(l3, Q?, k2) = spval3k2.Q;
   Id Spab3(l3, Q?, l4) = spval3l4.Q;
   Id Spab3(l4, Q?, k1) = spval4k1.Q;
   Id Spab3(l4, Q?, k2) = spval4k2.Q;
   Id Spab3(l4, Q?, l3) = spval4l3.Q;
   Id Spab3(k1, Q?, e1) = spvak1e1.Q;
   Id Spab3(e1, Q?, k1) = spvae1k1.Q;
   Id Spab3(k1, Q?, e2) = spvak1e2.Q;
   Id Spab3(e2, Q?, k1) = spvae2k1.Q;
   Id Spab3(k2, Q?, e1) = spvak2e1.Q;
   Id Spab3(e1, Q?, k2) = spvae1k2.Q;
   Id Spab3(k2, Q?, e2) = spvak2e2.Q;
   Id Spab3(e2, Q?, k2) = spvae2k2.Q;
   Id Spab3(l3, Q?, e1) = spval3e1.Q;
   Id Spab3(e1, Q?, l3) = spvae1l3.Q;
   Id Spab3(l3, Q?, e2) = spval3e2.Q;
   Id Spab3(e2, Q?, l3) = spvae2l3.Q;
   Id Spab3(l4, Q?, e1) = spval4e1.Q;
   Id Spab3(e1, Q?, l4) = spvae1l4.Q;
   Id Spab3(l4, Q?, e2) = spval4e2.Q;
   Id Spab3(e2, Q?, l4) = spvae2l4.Q;
   Id Spab3(e1, Q?, e2) = spvae1e2.Q;
   Id Spab3(e2, Q?, e1) = spvae2e1.Q;

#EndProcedure
