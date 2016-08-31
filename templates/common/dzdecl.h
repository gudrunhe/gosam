      complex*16 ddmw2,ddmz2,ddmh2, & !mass renorm
     & ddme2,ddmm2,ddmtl2, &
     & ddmu2,ddmd2,ddmc2,ddms2, &
     & ddmt2,ddmb2, &
     & ddznel,ddznml,ddzntl, & ! wf renorm
     & ddzel,ddzml,ddztll, & ! wf renorm
     & ddzul,ddzcl,ddztl,      &
     & ddzdl,ddzsl,ddzbl,      &
     & ddzer,ddzmr,ddztlr, &
     & ddzur,ddzcr,ddztr,      &
     & ddzdr,ddzsr,ddzbr, &
     & ddzw,ddzz,ddzh,ddza,ddz_za,ddz_az,  &
     & ddee,ddswsw,ddcwcw, & !coupling renorm
     & dtad,ddmt2omt, &
     & ddme2ome,ddmm2omm,ddmtl2omtl, &
     & ddmu2omu,ddmd2omd,ddmc2omc,ddms2oms, &
     & ddmb2omb
      common/deltas/ddmw2(1:2),ddmz2(1:2),ddmh2(1:2), & !mass renorm
     & ddme2(1:2),ddmm2(1:2),ddmtl2(1:2), &
     & ddmu2(1:2),ddmd2(1:2),ddmc2(1:2),ddms2(1:2), &
     & ddmt2(1:2),ddmb2(1:2), &
     & ddznel(1:2),ddznml(1:2),ddzntl(1:2), & ! wf renorm
     & ddzel(1:2),ddzml(1:2),ddztll(1:2), & ! wf renorm
     & ddzul(1:2),ddzcl(1:2),ddztl(1:2),      &
     & ddzdl(1:2),ddzsl(1:2),ddzbl(1:2),      &
     & ddzer(1:2),ddzmr(1:2),ddztlr(1:2), &
     & ddzur(1:2),ddzcr(1:2),ddztr(1:2),      &
     & ddzdr(1:2),ddzsr(1:2),ddzbr(1:2), &
     & ddzw(1:2),ddzz(1:2),ddzh(1:2),ddza(1:2),ddz_za(1:2),ddz_az(1:2),  &
     & ddee(1:2),ddswsw(1:2),ddcwcw(1:2), & !coupling renorm
     & dtad(1:2),ddmt2omt(1:2), &
     & ddme2ome(1:2),ddmm2omm(1:2),ddmtl2omtl(1:2), &
     & ddmu2omu(1:2),ddmd2omd(1:2),ddmc2omc(1:2),ddms2oms(1:2), &
     & ddmb2omb(1:2)
       complex*16 gctWWZZ, gctWWAZ, gctWWAA, gctWWWW, gctWWZ, &
     & gctHHHH, gctHHXX, gctHHPP, gctXXPP, gctPPPP, gctXXXX, &
     & gctHHH, gctHXX, gctHPP, &
     & gctZZHH, gctZZXX, gctWWHH, gctWWXX, gctWWPP, gctAAPP,  &
     & gctAZPP, gctZZPP, &
     & gctWAPH, gctWZPH, gctWZPX, gctWAPX, &
     & gctZXH, gctAPP, gctZPP, gctWPH, gctWPX, &
     & gctHZZ, gctHWW, gctPWA, gctPWZ, &
     & gctWpud, gctWpcs, gctWptb, &
     & gctWmud, gctWmcs, gctWmtb, &
     & gctPplud, gctPplcs, gctPpltb, gctPprud, gctPprcs, gctPprtb, &
     & gctPmlud, gctPmlcs, gctPmltb, gctPmrud, gctPmrcs, gctPmrtb, &
     & gctPple, gctPplmu, gctPpltau, gctPpre, gctPprmu, gctPprtau, &
     & gctPmle, gctPmlmu, gctPmltau, gctPmre, gctPmrmu, gctPmrtau, &
     & gctWpe, gctWpmu, gctWptau, &
     & gctWme, gctWmmu, gctWmtau, &
     & gctW1, gctW2, gctZ1, gctZ2, gctAZ1, gctAZ2, gctH1, gctH2, &
     & gctA,  &
     & gctZAXX, gctZAHH, gctHZA, gctAXH, &
     & gctWWA, gctchi, gctphi, &
     & gctGlU, gctGrU,  &
     & gctGlD, gctGrD,  &
     & gctGlC, gctGrC,  &
     & gctGlS, gctGrS,  &
     & gctGlT, gctGrT,  &
     & gctGlB, gctGrB, &
     & gctHlU, gctHrU, gctXlU, gctXrU,  &
     & gctHlD, gctHrD, gctXlD, gctXrD,  &
     & gctHlC, gctHrC, gctXlC, gctXrC,  &
     & gctHlS, gctHrS, gctXlS, gctXrS,  &
     & gctHlT, gctHrT, gctXlT, gctXrT,  &
     & gctHlB, gctHrB, gctXlB, gctXrB,  &
     & gctHle, gctHre, gctXle, gctXre,  &
     & gctHlmu, gctHrmu, gctXlmu, gctXrmu,  &
     & gctHltau, gctHrtau, gctXltau, gctXrtau,  &
     & gctAlU, gctArU, gctZlU, gctZrU,  &
     & gctAlD, gctArD, gctZlD, gctZrD,  &
     & gctAlC, gctArC, gctZlC, gctZrC,  &
     & gctAlS, gctArS, gctZlS, gctZrS,  &
     & gctAlT, gctArT, gctZlT, gctZrT,  &
     & gctAlB, gctArB, gctZlB, gctZrB,  &
     & gctAle, gctAre, gctZle, gctZre,  &	
     & gctAlne, gctArne,  &
     & gctAlnmu, gctArnmu,  &
     & gctAlntau, gctArntau,  &
     & gctAlmu, gctArmu, gctZlmu, gctZrmu,  &
     & gctAltau, gctArtau, gctZltau, gctZrtau,  &
     & gctZlne, gctZrne, gctCLne, gctCRne,  &
     & gctZlnmu, gctZrnmu, gctCLnmu, gctCRnmu,  &
     & gctZlntau, gctZrntau, gctCLntau, gctCRntau, &
     & gctCLU, gctCRU, gctCPU, gctCMU,  &
     & gctCLD, gctCRD, gctCPD, gctCMD,  &
     & gctCLC, gctCRC, gctCPC, gctCMC,  &
     & gctCLS, gctCRS, gctCPS, gctCMS,  &
     & gctCLT, gctCRT, gctCPT, gctCMT,  &
     & gctCLB, gctCRB, gctCPB, gctCMB,  &
     & gctCLe, gctCRe, gctCPe, gctCMe,  &
     & gctCLmu, gctCRmu, gctCPmu, gctCMmu,  &
     & gctCLtau, gctCRtau, gctCPtau, gctCMtau   
       common/gctvalues/gctWWZZ(1:2), gctWWAZ(1:2), gctWWAA(1:2),  &
     &                                 gctWWWW(1:2), gctWWZ(1:2), &
     & gctHHHH(1:2), gctHHXX(1:2), gctHHPP(1:2), gctXXPP(1:2),  &
     &                             gctPPPP(1:2), gctXXXX(1:2), &
     & gctHHH(1:2), gctHXX(1:2), gctHPP(1:2), &
     & gctZZHH(1:2), gctZZXX(1:2), gctWWHH(1:2), gctWWXX(1:2),  &
     & gctWWPP(1:2), gctAAPP(1:2), gctAZPP(1:2), gctZZPP(1:2), &
     & gctWAPH(1:2), gctWZPH(1:2), gctWZPX(1:2), gctWAPX(1:2), &
     & gctZXH(1:2), gctAPP(1:2), gctZPP(1:2), gctWPH(1:2),  &
     &                                        gctWPX(1:2), &
     & gctHZZ(1:2), gctHWW(1:2), gctPWA(1:2), gctPWZ(1:2), &
     & gctWpud(1:2), gctWpcs(1:2), gctWptb(1:2), &
     & gctWmud(1:2), gctWmcs(1:2), gctWmtb(1:2), &
     & gctPplud(1:2), gctPplcs(1:2), gctPpltb(1:2),  &
     & gctPprud(1:2), gctPprcs(1:2), gctPprtb(1:2), &
     & gctPmlud(1:2), gctPmlcs(1:2), gctPmltb(1:2),  &
     & gctPmrud(1:2), gctPmrcs(1:2), gctPmrtb(1:2), &
     & gctPple(1:2), gctPplmu(1:2), gctPpltau(1:2), &
     & gctPpre(1:2), gctPprmu(1:2), gctPprtau(1:2), &
     & gctPmle(1:2), gctPmlmu(1:2), gctPmltau(1:2), &
     & gctPmre(1:2), gctPmrmu(1:2), gctPmrtau(1:2), &
     & gctWpe(1:2), gctWpmu(1:2), gctWptau(1:2), &
     & gctWme(1:2), gctWmmu(1:2), gctWmtau(1:2), &
     & gctW1(1:2), gctW2(1:2), gctZ1(1:2), gctZ2(1:2), &
     & gctAZ1(1:2), gctAZ2(1:2), gctH1(1:2), gctH2(1:2), &
     & gctA(1:2),  &
     & gctZAXX(1:2), gctZAHH(1:2), gctHZA(1:2), gctAXH(1:2), &
     & gctWWA(1:2), gctchi(1:2), gctphi(1:2), &
     & gctGlU(1:2), gctGrU(1:2),  &
     & gctGlD(1:2), gctGrD(1:2),  &
     & gctGlC(1:2), gctGrC(1:2),  &
     & gctGlS(1:2), gctGrS(1:2),  &
     & gctGlT(1:2), gctGrT(1:2),  &
     & gctGlB(1:2), gctGrB(1:2), &
     & gctHlU(1:2), gctHrU(1:2), gctXlU(1:2), gctXrU(1:2),  &
     & gctHlD(1:2), gctHrD(1:2), gctXlD(1:2), gctXrD(1:2),  &
     & gctHlC(1:2), gctHrC(1:2), gctXlC(1:2), gctXrC(1:2),  &
     & gctHlS(1:2), gctHrS(1:2), gctXlS(1:2), gctXrS(1:2),  &
     & gctHlT(1:2), gctHrT(1:2), gctXlT(1:2), gctXrT(1:2),  &
     & gctHlB(1:2), gctHrB(1:2), gctXlB(1:2), gctXrB(1:2),  &
     & gctHle(1:2), gctHre(1:2), gctXle(1:2), gctXre(1:2),  &
     & gctHlmu(1:2), gctHrmu(1:2), gctXlmu(1:2), gctXrmu(1:2),  &
     & gctHltau(1:2), gctHrtau(1:2), gctXltau(1:2), gctXrtau(1:2),  &
     & gctAlU(1:2), gctArU(1:2), gctZlU(1:2), gctZrU(1:2),  &
     & gctAlD(1:2), gctArD(1:2), gctZlD(1:2), gctZrD(1:2),  &
     & gctAlC(1:2), gctArC(1:2), gctZlC(1:2), gctZrC(1:2),  &
     & gctAlS(1:2), gctArS(1:2), gctZlS(1:2), gctZrS(1:2),  &
     & gctAlT(1:2), gctArT(1:2), gctZlT(1:2), gctZrT(1:2),  &
     & gctAlB(1:2), gctArB(1:2), gctZlB(1:2), gctZrB(1:2),  &
     & gctAle(1:2), gctAre(1:2), gctZle(1:2), gctZre(1:2),  &
     & gctAlne(1:2), gctArne(1:2),  &
     & gctAlnmu(1:2), gctArnmu(1:2),  &
     & gctAlntau(1:2), gctArntau(1:2),  &
     & gctAlmu(1:2), gctArmu(1:2), gctZlmu(1:2), gctZrmu(1:2),  &
     & gctAltau(1:2), gctArtau(1:2), gctZltau(1:2), gctZrtau(1:2),  &
     & gctZlne(1:2), gctZrne(1:2), gctCLne(1:2), gctCRne(1:2),  &
     & gctZlnmu(1:2), gctZrnmu(1:2), gctCLnmu(1:2), gctCRnmu(1:2),  &
     & gctZlntau(1:2), gctZrntau(1:2), gctCLntau(1:2), gctCRntau(1:2), &
     & gctCLU(1:2), gctCRU(1:2), gctCPU(1:2), gctCMU(1:2),  &
     & gctCLD(1:2), gctCRD(1:2), gctCPD(1:2), gctCMD(1:2),  &
     & gctCLC(1:2), gctCRC(1:2), gctCPC(1:2), gctCMC(1:2),  &
     & gctCLS(1:2), gctCRS(1:2), gctCPS(1:2), gctCMS(1:2),  &
     & gctCLT(1:2), gctCRT(1:2), gctCPT(1:2), gctCMT(1:2),  &
     & gctCLB(1:2), gctCRB(1:2), gctCPB(1:2), gctCMB(1:2),  &
     & gctCLe(1:2), gctCRe(1:2), gctCPe(1:2), gctCMe(1:2),  &
     & gctCLmu(1:2), gctCRmu(1:2), gctCPmu(1:2), gctCMmu(1:2),  &
     & gctCLtau(1:2), gctCRtau(1:2), gctCPtau(1:2), gctCMtau(1:2)   