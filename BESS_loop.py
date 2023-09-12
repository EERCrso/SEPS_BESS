from matplotlib import pyplot as plt
import pandas as pd
import numpy as np
import baterry
import functions

#inicializacia data SEPS
#df=pd.read_csv("FVE_2021_1MIN_FULL_NO_DIFF.csv",sep=";")
#data=df["SR"].tolist() # oprions SR  SSD  ZSD  VSD

#den_od=140
#den_do=141
#FVE_production=data[den_od*1441:den_do*1441] # vybrane interevali dni
#FVE_production=data[den_od*1441+500:den_od*1441+800] # vybrane interevali dni
#FVE_production=data[:] #ROK


#inicializacia dataharmonia

df=pd.read_csv("data_LVN_20.csv",sep=";")
data=df["P_[kW]"].tolist() # oprions SR  SSD  ZSD  VSD

den_od=3
den_do=4
#FVE_production=data[den_od*28820:den_do*28820] # vybrane interevali dni
#FVE_production=data[den_od*1441+500:den_od*1441+800] # vybrane interevali dni
FVE_production=data[:] #ROK

#cum_times=[3,3,5,5,10,10,15,15]
#MWinstal=[5.5,18,6.5,20,9.5,25,12.5,30]
#cum_times=[3,3,3,3,3,3,3,3,5,5,5,5,5,5,5,5,10,10,10,10,10,10,10,10,15,15,15,15,15,15,15,15]
#MWinstal=[5,7.5,10,12.5,15,20,25,30,5,7.5,10,12.5,15,20,25,30,5,7.5,10,12.5,15,20,25,30,5,7.5,10,12.5,15,20,25,30]
#MWHrated=[150,140,130,125,120,115,110,105,100,95,90,85,80,75,70,65,60,55,50,45,40,35,30,25,20]

cum_times=[10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,10,40,40,40,40,40,40,40,40,40,40,40,40,40,40,40,40,40,40,40,40,40,40,40,20*5,20*5,20*5,20*5,20*5,20*5,20*5,20*5,20*5,20*5,20*5,20*5,20*5,20*5,20*5,20*5,20*5,20*5,20*5,20*5,20*5,20*5,20*5,20*10,20*10,20*10,20*10,20*10,20*10,20*10,20*10,20*10,20*10,20*10,20*10,20*10,20*10,20*10,20*10,20*10,20*10,20*10,20*10,20*10,20*10,20*10]
MWinstal=[1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23]
MWHrated=[40,35,30,25,20,15,10,5]


results_cumMW=list()
results_cumMWh=list()
results_cumMWcykly=list()


for cum_index, cum_item in enumerate(cum_times):
    parcial_results_cumMW = list()
    parcial_results_cumMWh = list()
    parcial_results_cumcyklov = list()

    for MWh_index, MWh_item in enumerate(MWHrated):

        baterka1= baterry.baterry(Name="TEST",
                                  MWhrated=MWh_item,
                                  MWinstalled_power=MWinstal[cum_index],
                                  status=None,
                                  charge_losses=0.5,
                                  discharge_losses=0.5,
                                  idling_losses=1.25e-3,
                                  limit_capacity=True)

        #settings
        trieda="A"
        static_window=False # static or floating window
        average_method=True
        graphs=False

        cum_time=cum_item
        baterry_limit_nabijania=True
        deadband=0.01* baterka1._MWinstalled_power # deadband  5% z inštalovane vykonu

        slope_for_classB=1
        regulate_at_MW_max_ratio = 0.5
        start_time_for_B_in_h=4 # not functional
        end_time_for_B_in_h=21 # not functional
        #inicializačne konštanty

        list_of_values=list()
        Smooth_production = list()
        proposed_baterry_operations = list()
        real_baterry_operations = list()
        regulated_FVE_operations = list()
        baterry_percentage_capacity = list()
        checker_list_enought_power = list()
        checker_list_enought_capacity = list()

        average=0
        sub_slope_time=0
        B1=0
        B1_past=0
        B0_past=0
        B0=0
        vaha=0
        expectation_past=0
        expectation=0
        hold = False
        charge=True
        discharge=False
        den=0
        ####################
        # hlavny casovy loop
        ####################
        for t, val_FVE in enumerate(FVE_production):

            ##############################
            # BMS CLASS A smooth
            ##############################
            if trieda=="A":

                if static_window ==True:

                    # urci hodnotu na ktoru mam regulovat v danej minute
                    list_of_values, release = functions.cumval(val_FVE, list_of_values, cum_time - 1)

                    if release ==True:
                        B1_past=B1
                        B0_past = B0
                        average_past=average
                        average,B0,B1 = functions.analyze_FVE(list_of_values,average_past=average_past)
                        sub_slope_time=0

                    if average_method == True: # average method
                        expectation=average

                    if average_method==False: # slope method
                        expectation =sub_slope_time*(B1+B1_past*vaha) + (B0+B0_past*vaha)
                        sub_slope_time = sub_slope_time + 1
                else: # dnymic window

                    B1_past = B1
                    B0_past = B0
                    average_past = average
                    average, B0, B1 = functions.analyze_FVE(FVE_production[t-cum_time:t], average_past=average_past)
                    sub_slope_time = 0

                    if average_method == True: # average method
                        expectation = average

                    if average_method == False: # slope method
                        expectation = sub_slope_time * (B1 + B1_past * vaha) + (B0 + B0_past * vaha)
                        sub_slope_time = sub_slope_time + 1


                status, value_baterry,release_energy,regulated_FVE = functions.BMS_class_A_smooth_core(FVE=val_FVE,
                                                                            expectations=expectation,
                                                                            baterry=baterka1,
                                                                            deadband=deadband)

            ##############################
            # BMS CLASS B time_shift
            ##############################
            if trieda=="B":

                if t>1440*(den+1):
                    den=den+1

                daylist=FVE_production[den*1441:(den+1)*1441]


                if len(daylist)>0:
                    regulate_at_MW = max(daylist)*regulate_at_MW_max_ratio

                #nabeh faza
                if expectation < regulate_at_MW and hold == False and charge==True:

                    if static_window ==True:

                        # urci hodnotu na ktoru mam regulovat v danej minute
                        list_of_values, release = functions.cumval(val_FVE, list_of_values, cum_time - 1)

                        if release ==True:
                            B1_past=B1
                            B0_past = B0
                            average_past=average
                            average,B0,B1 = functions.analyze_FVE(list_of_values,average_past=average_past)
                            sub_slope_time=0

                        if average_method == True: # average method
                            expectation=average

                        if average_method==False: # slope method
                            expectation =sub_slope_time*(B1+B1_past*vaha) + (B0+B0_past*vaha)
                            sub_slope_time = sub_slope_time + 1
                    else: # dnymic window

                        B1_past = B1
                        B0_past = B0
                        average_past = average
                        average, B0, B1 = functions.analyze_FVE(FVE_production[t-cum_time:t], average_past=average_past)
                        sub_slope_time = 0

                        if average_method == True: # average method
                            expectation = average

                        if average_method == False: # slope method
                            expectation = sub_slope_time * (B1 + B1_past * vaha) + (B0 + B0_past * vaha)
                            sub_slope_time = sub_slope_time + 1


                    if expectation>= regulate_at_MW:
                        hold=True



                # nabeh Hold
                if  hold == True:
                    expectation=regulate_at_MW

                    if baterka1.get_percented_stored()*100>90 or baterka1.get_percented_stored()*100<20:
                        hold =False
                        discharge=True

                    if val_FVE > regulate_at_MW :
                        hold = True
                        discharge = False


                #discharge faza
                if discharge == True:
                    expectation = expectation_past - slope_for_classB

                    if baterka1.get_percented_stored()*100<15 or expectation < 0:
                        hold =False
                        discharge=False
                        expectation=0

                expectation_past = expectation

                # if functions.calc_time_of_day(t) >= start_time_for_B_in_h*60 and functions.calc_time_of_day(t) <= end_time_for_B_in_h*60:
                #
                #     if expectation_past <= regulate_at_MW:
                #         expectation = expectation_past +slope_for_classB
                #         if expectation >= regulate_at_MW :expectation=regulate_at_MW
                #     else:
                #         expectationr=regulate_at_MW
                #
                #     expectation_past=expectation
                #
                # else: expectation=0

            status, value_baterry,release_energy,regulated_FVE = functions.BMS_class_A_smooth_core(FVE=val_FVE,
                                                                                expectations=expectation,
                                                                                baterry=baterka1,
                                                                                deadband=deadband)


            ##############################
            #lists
            ##############################

            checker_list_enought_capacity.append(baterka1.get_enougth_capacity())
            checker_list_enought_power.append(baterka1.get_enougth_power())
            baterry_percentage_capacity.append( baterka1.get_percented_stored()*100)


            proposed_baterry_operations.append(value_baterry)
            real_baterry_operations.append(release_energy)
            regulated_FVE_operations.append(regulated_FVE)
            Smooth_production.append(expectation)



        ####################
        # charts
        ####################
        if graphs == True:
            neregulacia = functions.list_substraction( Smooth_production, regulated_FVE_operations )
            fig, axs = plt.subplots(3,figsize=(15, 15))
            axs[0].plot(neregulacia,lw=0.3)
            axs[0].set_ylabel("P [MW]")
            axs[0].legend(['Unregulated'])
            axs[0].set_xlabel("čas t [min]")

            axs[1].plot(checker_list_enought_power,lw=1)
            axs[1].set_ylim(-1, 2)
            axs[1].set_ylabel("logicka hodnota [%]")
            axs[1].legend(['Dostatočny vykon BESS 1 == TRUE'])
            axs[1].set_xlabel("čas t [min]")

            axs[2].plot(checker_list_enought_capacity,lw=1)
            axs[2].set_ylim(-1, 2)
            axs[2].set_ylabel("logicka hodnota [%]")
            axs[2].legend(['Dostatočna kapacita BESS 1 == TRUE '])
            axs[2].set_xlabel("čas t [min]")
            plt.show()


            fig, axs = plt.subplots(2,figsize=(15, 15))
            axs[0].plot(FVE_production,lw=0.3)
            #axs[0].plot(Smooth_production,lw=0.3)
            axs[0].plot(regulated_FVE_operations,lw=1)
            axs[0].plot(real_baterry_operations,lw=1)
            axs[0].set_ylabel("P [MW]")
            axs[0].legend(['$P_{FVE}$','$P_{REG}$','$P_{saldo}$ (+vybíjanie | -nabíjanie )'])
            axs[0].set_xlabel("čas t [min]")

            axs[1].plot(baterry_percentage_capacity,lw=1)
            axs[1].set_ylim(0, 100)
            axs[1].set_title('% kapacita baterie')
            axs[1].set_ylabel("aktualna kapacita [%]")
            axs[1].set_xlabel("čas t [min]")
            axs[1].axhline(y = 10, color = 'r', linestyle = 'dashed')
            axs[1].axhline(y = 90, color = 'r', linestyle = 'dashed')
            plt.show()

            # male okno
            # fig, axs = plt.subplots(1,figsize=(5, 10))
            # axs.plot(FVE_production[50:],lw=0.5)
            # #axs[0].plot(Smooth_production,lw=0.3)
            # axs.plot(regulated_FVE_operations[50:],lw=1.2)
            # axs.plot(real_baterry_operations[50:],lw=1.2)
            # axs.set_ylabel("P [MW]", fontsize=20)
            # axs.legend(['$P_{FVE}$','$P_{REG}$','$P_{saldo}$ (+vybíjanie | -nabíjanie )'], fontsize=14,loc="center")
            # axs.set_xlabel("t [min]" ,fontsize=20)
            # axs.tick_params(axis="x", labelsize=20)
            # axs.tick_params(axis="y", labelsize=20)
            # plt.text(10, 115, 'n='+ str(cum_time) + ' min', fontsize = 20)
            # plt.show()


            # fig, axs = plt.subplots(1,figsize=(22, 13))
            # x = np.arange(0, 1441, 1)
            # axs.plot(FVE_production,lw=3, color="red")
            # axs.fill_between( x,0 ,FVE_production,facecolor='blue',alpha=0.3)
            # #axs[0].plot(Smooth_production,lw=0.3)
            # axs.set_ylabel("P [MW]",fontsize=20)
            # axs.legend(['FVE_production'], fontsize=20)
            # axs.set_xlabel("čas t [min]", fontsize=20)
            # axs.tick_params(axis="x", labelsize=20)
            # axs.tick_params(axis="y", labelsize=20)
            # plt.show()

        #STATISTA
        print("******INFO*******")
        print("CLASS                   = " + trieda )
        if static_window ==True:
            print("Window                   = STATIC ")
        else:
            print("Window                  = DINAMIC ")

        print("Interval                = " + str(cum_time) + ' min')
        print("Necitlivosť             = " + str(deadband) + ' MW')
        print("Inštalovany výkon       = " + str(baterka1._MWinstalled_power) + ' MWh')
        print("No. nedostatok vykonu   = " + str(checker_list_enought_power.count(0)) + ' min')
        print("Kapacita                = " + str(baterka1._MWhrated) + ' MWh')
        print("No. nedostatok kapacity = " + str(checker_list_enought_capacity.count(0)) + ' min')
        print("No. charging cyklov     = " + str(baterka1.number_of_charging_cycles()) + ' -')
        print("No. discharging cyklov  = " + str(baterka1.number_of_discharging_cycles()) + ' -')

        # todo count fails
        #  evaluate max power, NO of changes of unabili to charge
        parcial_results_cumMW.append(checker_list_enought_power.count(0))
        parcial_results_cumMWh.append(checker_list_enought_capacity.count(0))
        parcial_results_cumcyklov.append(baterka1.number_of_charging_cycles())

        PRIEBEH_NOVY = pd.DataFrame(regulated_FVE_operations)
        PRIEBEH_NOVY.to_csv('priebeh_t'+str(cum_time) + '_MW' + str(baterka1._MWinstalled_power)+ '_MWh' + str(baterka1._MWhrated)+'.csv', index=False, encoding='utf-8', sep=';')



    results_cumMW.append(parcial_results_cumMW)
    results_cumMWh.append(parcial_results_cumMWh)
    results_cumMWcykly.append(parcial_results_cumcyklov)

vysledky_MW = pd.DataFrame.from_records(results_cumMW)
vysledky_MW.to_csv('res_MW.csv', index = False, encoding='utf-8',sep=';')

vysledky_MW = pd.DataFrame.from_records(results_cumMWh)
vysledky_MW.to_csv('res_MWh.csv', index = False, encoding='utf-8',sep=';')

vysledky_MW = pd.DataFrame.from_records(results_cumMWcykly)
vysledky_MW.to_csv('res_cykly.csv', index = False, encoding='utf-8',sep=';')