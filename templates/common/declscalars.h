!ccccccccccccccccccccccccccccccccccccccccccccccccccc
!c     in order to fill and store all the olo output 
!ccccccccccccccccccccccccccccccccccccccccccccccccccc
      complex*16 b0d0meme,b0d0mmmm,b0d0mlml, &
     &     b0d0mumu ,b0d0mcmc ,b0d0mtmt , &
     &     b0d0mdmd ,b0d0msms ,b0d0mbmb , &
     &     b0dmz00  , & ! 3 neutrinos
     &     b0dmzmeme,b0dmzmmmm,b0dmzmlml, &
     &     b0dmzmumu,b0dmzmcmc,b0dmzmtmt, &
     &     b0dmzmdmd,b0dmzmsms,b0dmzmbmb, &
     &     b0dmhmeme,b0dmhmmmm,b0dmhmlml, &
     &     b0dmhmumu,b0dmhmcmc,b0dmhmtmt, &
     &     b0dmhmdmd,b0dmhmsms,b0dmhmbmb, &
     &     b0dmw0me ,b0dmw0mm ,b0dmw0ml , &
     &     b0dmwmumd,b0dmwmcms,b0dmwmtmb, &
     &     b0d00me  ,b0d00mm  ,b0d00ml  , &
     &     b0d0mumd ,b0d0mcms ,b0d0mtmb , &
     &     b0d0mwmw ,b0dmzmwmw,b0dmhmwmw, &
     &     b0dmzmzmh,b0d0mzmh ,b0d0mzmz , &
     &     b0d0mhmh ,b0dmwmwmz,b0d0mwmz , &
     &     b0dmwmwmh,b0d0mwmh , &
     &               b0dmhmzmz,b0dmhmhmh, &
     &     a0dmw,a0dmh,a0dmz, &
     &     a0dme,a0dmm,a0dml,a0dmu,a0dmd, &
     &     a0dmc,a0dms,a0dmt,a0dmb, &
     &     b1d00mz  ,b1d0memw ,b1d0mmmw,b1d0mlmw, &
     &     b1dmememz,b1dmememh,b1dme0mw , &
     &     b1dmmmmmz,b1dmmmmmh,b1dmm0mw , &
     &     b1dmlmlmz,b1dmlmlmh,b1dml0mw , &
     &     b1dmumumz,b1dmumumh,b1dmumdmw , &
     &     b1dmdmdmz,b1dmdmdmh,b1dmdmumw , &
     &     b1dmcmcmz,b1dmcmcmh,b1dmcmsmw , &
     &     b1dmsmsmz,b1dmsmsmh,b1dmsmcmw , &
     &     b1dmtmtmz,b1dmtmtmh,b1dmtmbmw , &
     &     b1dmbmbmz,b1dmbmbmh,b1dmbmtmw , &
     &     b0d00mz  ,b0d0memw ,b0d0mmmw,b0d0mlmw, &
     &     b0dmememz,b0dmememh,b0dme0mw , &
     &     b0dmmmmmz,b0dmmmmmh,b0dmm0mw , &
     &     b0dmlmlmz,b0dmlmlmh,b0dml0mw , &
     &     b0dmumumz,b0dmumumh,b0dmumdmw, &
     &     b0dmcmcmz,b0dmcmcmh,b0dmcmsmw, &
     &     b0dmtmtmz,b0dmtmtmh,b0dmtmbmw, &
     &     b0dmdmdmz,b0dmdmdmh,b0dmdmumw, &
     &     b0dmsmsmz,b0dmsmsmh,b0dmsmcmw, &
     &     b0dmbmbmz,b0dmbmbmh,b0dmbmtmw, &
!c photon part --> take with care SIGMAW(0) for DELTAR => dedicated expression
     &     b0dmwmwmg,b0d0mwmg, &
     &     b0dmememg,b0dmmmmmg,b0dmlmlmg, &
     &     b0dmumumg,b0dmcmcmg,b0dmtmtmg, &
     &     b0dmdmdmg,b0dmsmsmg,b0dmbmbmg, &
     &     b1dmememg,b1dmmmmmg,b1dmlmlmg, &
     &     b1dmumumg,b1dmcmcmg,b1dmtmtmg, &
     &     b1dmdmdmg,b1dmsmsmg,b1dmbmbmg
      common/fixedscalar/b0d0meme(0:2),b0d0mmmm(0:2),b0d0mlml(0:2), &
     &     b0d0mumu(0:2) ,b0d0mcmc(0:2) ,b0d0mtmt(0:2) , &
     &     b0d0mdmd(0:2) ,b0d0msms(0:2) ,b0d0mbmb(0:2) , &
     &     b0dmz00(0:2)  , & ! 3 neutrinos
     &     b0dmzmeme(0:2),b0dmzmmmm(0:2),b0dmzmlml(0:2), &
     &     b0dmzmumu(0:2),b0dmzmcmc(0:2),b0dmzmtmt(0:2), &
     &     b0dmzmdmd(0:2),b0dmzmsms(0:2),b0dmzmbmb(0:2), &
     &     b0dmhmeme(0:2),b0dmhmmmm(0:2),b0dmhmlml(0:2), &
     &     b0dmhmumu(0:2),b0dmhmcmc(0:2),b0dmhmtmt(0:2), &
     &     b0dmhmdmd(0:2),b0dmhmsms(0:2),b0dmhmbmb(0:2), &
     &     b0dmw0me(0:2) ,b0dmw0mm(0:2) ,b0dmw0ml(0:2) , &
     &     b0dmwmumd(0:2),b0dmwmcms(0:2),b0dmwmtmb(0:2), &
     &     b0d00me(0:2)  ,b0d00mm(0:2)  ,b0d00ml(0:2)  , &
     &     b0d0mumd(0:2) ,b0d0mcms(0:2) ,b0d0mtmb(0:2) , &
     &     b0d0mwmw(0:2) ,b0dmzmwmw(0:2),b0dmhmwmw(0:2), &
     &     b0dmzmzmh(0:2),b0d0mzmh(0:2) ,b0d0mzmz(0:2) , &
     &     b0d0mhmh(0:2) ,b0dmwmwmz(0:2),b0d0mwmz(0:2) , &
     &     b0dmwmwmh(0:2),b0d0mwmh(0:2) , &
     &                    b0dmhmzmz(0:2),b0dmhmhmh(0:2), &
     &     a0dmw(0:2),a0dmh(0:2),a0dmz(0:2), &
     &     a0dme(0:2),a0dmm(0:2),a0dml(0:2),a0dmu(0:2),a0dmd(0:2), &
     &     a0dmc(0:2),a0dms(0:2),a0dmt(0:2),a0dmb(0:2), &
     &     b1d00mz(0:2)  ,b1d0memw(0:2) ,b1d0mmmw(0:2),b1d0mlmw(0:2), &
     &     b1dmememz(0:2),b1dmememh(0:2),b1dme0mw(0:2) , &
     &     b1dmmmmmz(0:2),b1dmmmmmh(0:2),b1dmm0mw(0:2) , &
     &     b1dmlmlmz(0:2),b1dmlmlmh(0:2),b1dml0mw(0:2) , &
     &     b1dmumumz(0:2),b1dmumumh(0:2),b1dmumdmw(0:2) , &
     &     b1dmdmdmz(0:2),b1dmdmdmh(0:2),b1dmdmumw(0:2) , &
     &     b1dmcmcmz(0:2),b1dmcmcmh(0:2),b1dmcmsmw(0:2) , &
     &     b1dmsmsmz(0:2),b1dmsmsmh(0:2),b1dmsmcmw(0:2) , &
     &     b1dmtmtmz(0:2),b1dmtmtmh(0:2),b1dmtmbmw(0:2) , &
     &     b1dmbmbmz(0:2),b1dmbmbmh(0:2),b1dmbmtmw(0:2) , &
     &     b0d00mz(0:2)  ,b0d0memw(0:2) ,b0d0mmmw(0:2),b0d0mlmw(0:2), &
     &     b0dmememz(0:2),b0dmememh(0:2),b0dme0mw(0:2) , &
     &     b0dmmmmmz(0:2),b0dmmmmmh(0:2),b0dmm0mw(0:2) , &
     &     b0dmlmlmz(0:2),b0dmlmlmh(0:2),b0dml0mw(0:2) , &
     &     b0dmumumz(0:2),b0dmumumh(0:2),b0dmumdmw(0:2), &
     &     b0dmcmcmz(0:2),b0dmcmcmh(0:2),b0dmcmsmw(0:2), &
     &     b0dmtmtmz(0:2),b0dmtmtmh(0:2),b0dmtmbmw(0:2), &
     &     b0dmdmdmz(0:2),b0dmdmdmh(0:2),b0dmdmumw(0:2), &
     &     b0dmsmsmz(0:2),b0dmsmsmh(0:2),b0dmsmcmw(0:2), &
     &     b0dmbmbmz(0:2),b0dmbmbmh(0:2),b0dmbmtmw(0:2), &
!c photon part --> take with care SIGMAW(0) for DELTAR => dedicated expression
     &     b0dmwmwmg(0:2),b0d0mwmg(0:2), &
     &     b0dmememg(0:2),b0dmmmmmg(0:2),b0dmlmlmg(0:2), &
     &     b0dmumumg(0:2),b0dmcmcmg(0:2),b0dmtmtmg(0:2), &
     &     b0dmdmdmg(0:2),b0dmsmsmg(0:2),b0dmbmbmg(0:2), &
     &     b1dmememg(0:2),b1dmmmmmg(0:2),b1dmlmlmg(0:2), &
     &     b1dmumumg(0:2),b1dmcmcmg(0:2),b1dmtmtmg(0:2), &
     &     b1dmdmdmg(0:2),b1dmsmsmg(0:2),b1dmbmbmg(0:2)

      complex*16 b0pd0meme,b0pd0mmmm,b0pd0mlml, &
     &     b0pd0mumu ,b0pd0mcmc ,b0pd0mtmt , &
     &     b0pd0mdmd ,b0pd0msms ,b0pd0mbmb , &
     &     b0pdmz00  ,  & ! 3 neutrinos
     &     b0pdmzmeme,b0pdmzmmmm,b0pdmzmlml, &
     &     b0pdmzmumu,b0pdmzmcmc,b0pdmzmtmt, &
     &     b0pdmzmdmd,b0pdmzmsms,b0pdmzmbmb, &
     &     b0pdmhmeme,b0pdmhmmmm,b0pdmhmlml, &
     &     b0pdmhmumu,b0pdmhmcmc,b0pdmhmtmt, &
     &     b0pdmhmdmd,b0pdmhmsms,b0pdmhmbmb, &
     &     b0pdmw0me ,b0pdmw0mm ,b0pdmw0ml , &
     &     b0pdmwmumd,b0pdmwmcms,b0pdmwmtmb, &
     &     b0pd00me  ,b0pd00mm  ,b0pd00ml  , &
     &     b0pd0mumd ,b0pd0mcms ,b0pd0mtmb , &
     &     b0pd0mwmw ,b0pdmzmwmw,b0pdmhmwmw, &
     &     b0pdmzmzmh,b0pd0mzmh ,b0pd0mzmz , &
     &     b0pd0mhmh ,b0pdmwmwmz,b0pd0mwmz , &
     &     b0pdmwmwmh,b0pd0mwmh , &
     &                b0pdmhmzmz,b0pdmhmhmh, &
     &     b1pd00mz  ,b1pd0memw ,b1pd0mmmw,b1pd0mlmw, &
     &     b1pdmememz,b1pdmememh,b1pdme0mw , &
     &     b1pdmmmmmz,b1pdmmmmmh,b1pdmm0mw , &
     &     b1pdmlmlmz,b1pdmlmlmh,b1pdml0mw , &
     &     b1pdmumumz,b1pdmumumh,b1pdmumdmw, &
     &     b1pdmcmcmz,b1pdmcmcmh,b1pdmcmsmw, &
     &     b1pdmtmtmz,b1pdmtmtmh,b1pdmtmbmw, &
     &     b1pdmdmdmz,b1pdmdmdmh,b1pdmdmumw, &
     &     b1pdmsmsmz,b1pdmsmsmh,b1pdmsmcmw, &
     &     b1pdmbmbmz,b1pdmbmbmh,b1pdmbmtmw, &
     &     b0pd00mz, &
     &     b0pdmememz,b0pdmememh,b0pdme0mw , &
     &     b0pdmmmmmz,b0pdmmmmmh,b0pdmm0mw , &
     &     b0pdmlmlmz,b0pdmlmlmh,b0pdml0mw , &
     &     b0pdmumumz,b0pdmumumh,b0pdmumdmw, &
     &     b0pdmcmcmz,b0pdmcmcmh,b0pdmcmsmw, &
     &     b0pdmtmtmz,b0pdmtmtmh,b0pdmtmbmw, &
     &     b0pdmdmdmz,b0pdmdmdmh,b0pdmdmumw, &
     &     b0pdmsmsmz,b0pdmsmsmh,b0pdmsmcmw, &
     &     b0pdmbmbmz,b0pdmbmbmh,b0pdmbmtmw, &
!c photon part --> take with care SIGMAW(0) for DELTAR => dedicated expression
     &     b0pdmwmwmg,b0pd0mwmg, &
     &     b0pdmememg,b0pdmmmmmg,b0pdmlmlmg, &
     &     b0pdmumumg,b0pdmcmcmg,b0pdmtmtmg, &
     &     b0pdmdmdmg,b0pdmsmsmg,b0pdmbmbmg, &
     &     b1pdmememg,b1pdmmmmmg,b1pdmlmlmg, &
     &     b1pdmumumg,b1pdmcmcmg,b1pdmtmtmg, &
     &     b1pdmdmdmg,b1pdmsmsmg,b1pdmbmbmg
      common/fixedscalarp/b0pd0meme(0:2),b0pd0mmmm(0:2),b0pd0mlml(0:2), &
     &     b0pd0mumu(0:2) ,b0pd0mcmc(0:2) ,b0pd0mtmt(0:2) , &
     &     b0pd0mdmd(0:2) ,b0pd0msms(0:2) ,b0pd0mbmb(0:2) , &
     &     b0pdmz00(0:2)  , & ! 3 neutrinos
     &     b0pdmzmeme(0:2),b0pdmzmmmm(0:2),b0pdmzmlml(0:2), &
     &     b0pdmzmumu(0:2),b0pdmzmcmc(0:2),b0pdmzmtmt(0:2), &
     &     b0pdmzmdmd(0:2),b0pdmzmsms(0:2),b0pdmzmbmb(0:2), &
     &     b0pdmhmeme(0:2),b0pdmhmmmm(0:2),b0pdmhmlml(0:2), &
     &     b0pdmhmumu(0:2),b0pdmhmcmc(0:2),b0pdmhmtmt(0:2), &
     &     b0pdmhmdmd(0:2),b0pdmhmsms(0:2),b0pdmhmbmb(0:2), &
     &     b0pdmw0me(0:2) ,b0pdmw0mm(0:2) ,b0pdmw0ml(0:2) , &
     &     b0pdmwmumd(0:2),b0pdmwmcms(0:2),b0pdmwmtmb(0:2), &
     &     b0pd00me(0:2)  ,b0pd00mm(0:2)  ,b0pd00ml(0:2)  , &
     &     b0pd0mumd(0:2) ,b0pd0mcms(0:2) ,b0pd0mtmb(0:2) , &
     &     b0pd0mwmw(0:2) ,b0pdmzmwmw(0:2),b0pdmhmwmw(0:2), &
     &     b0pdmzmzmh(0:2),b0pd0mzmh(0:2) ,b0pd0mzmz(0:2) , &
     &     b0pd0mhmh(0:2) ,b0pdmwmwmz(0:2),b0pd0mwmz(0:2) , &
     &     b0pdmwmwmh(0:2),b0pd0mwmh(0:2) , &
     &                     b0pdmhmzmz(0:2),b0pdmhmhmh(0:2), &
     &     b1pd00mz(0:2)  ,b1pd0memw(0:2),b1pd0mmmw(0:2),b1pd0mlmw(0:2), &
     &     b1pdmememz(0:2),b1pdmememh(0:2),b1pdme0mw(0:2) , &
     &     b1pdmmmmmz(0:2),b1pdmmmmmh(0:2),b1pdmm0mw(0:2) , &
     &     b1pdmlmlmz(0:2),b1pdmlmlmh(0:2),b1pdml0mw(0:2) , &
     &     b1pdmumumz(0:2),b1pdmumumh(0:2),b1pdmumdmw(0:2), &
     &     b1pdmcmcmz(0:2),b1pdmcmcmh(0:2),b1pdmcmsmw(0:2), &
     &     b1pdmtmtmz(0:2),b1pdmtmtmh(0:2),b1pdmtmbmw(0:2), &
     &     b1pdmdmdmz(0:2),b1pdmdmdmh(0:2),b1pdmdmumw(0:2), &
     &     b1pdmsmsmz(0:2),b1pdmsmsmh(0:2),b1pdmsmcmw(0:2), &
     &     b1pdmbmbmz(0:2),b1pdmbmbmh(0:2),b1pdmbmtmw(0:2), &
     &     b0pd00mz(0:2), &
     &     b0pdmememz(0:2),b0pdmememh(0:2),b0pdme0mw(0:2) , &
     &     b0pdmmmmmz(0:2),b0pdmmmmmh(0:2),b0pdmm0mw(0:2) , &
     &     b0pdmlmlmz(0:2),b0pdmlmlmh(0:2),b0pdml0mw(0:2) , &
     &     b0pdmumumz(0:2),b0pdmumumh(0:2),b0pdmumdmw(0:2), &
     &     b0pdmcmcmz(0:2),b0pdmcmcmh(0:2),b0pdmcmsmw(0:2), &
     &     b0pdmtmtmz(0:2),b0pdmtmtmh(0:2),b0pdmtmbmw(0:2), &
     &     b0pdmdmdmz(0:2),b0pdmdmdmh(0:2),b0pdmdmumw(0:2), &
     &     b0pdmsmsmz(0:2),b0pdmsmsmh(0:2),b0pdmsmcmw(0:2), &
     &     b0pdmbmbmz(0:2),b0pdmbmbmh(0:2),b0pdmbmtmw(0:2), &
!c photon part --> take with care SIGMAW(0) for DELTAR => dedicated expression
     &     b0pdmwmwmg(0:2),b0pd0mwmg(0:2), &
     &     b0pdmememg(0:2),b0pdmmmmmg(0:2),b0pdmlmlmg(0:2), &
     &     b0pdmumumg(0:2),b0pdmcmcmg(0:2),b0pdmtmtmg(0:2), &
     &     b0pdmdmdmg(0:2),b0pdmsmsmg(0:2),b0pdmbmbmg(0:2), &
     &     b1pdmememg(0:2),b1pdmmmmmg(0:2),b1pdmlmlmg(0:2), &
     &     b1pdmumumg(0:2),b1pdmcmcmg(0:2),b1pdmtmtmg(0:2), &
     &     b1pdmdmdmg(0:2),b1pdmsmsmg(0:2),b1pdmbmbmg(0:2)