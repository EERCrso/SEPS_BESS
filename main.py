from matplotlib import pyplot as plt
import pandas as pd
import baterry
import functions

#inicializacia data
df=pd.read_csv("FVE_2021_1MIN_FULL_NO_DIFF.csv",sep=";")
data=df["SR"].tolist() # oprions SR  SSD  ZSD  VSD

den_od=139
den_do=164
FVE_production=data[den_od*1441:den_do*1441] # vybrane interevali dni
#FVE_production=data[:] #ROK


baterka1= baterry.baterry(Name="TEST",
                          MWhrated=600,
                          MWinstalled_power=70,
                          status=None,)

#settings
trieda="B"
static_window=False # static or floating window
average_method=True


cum_time=15
baterry_limit_nabijania=True
deadband=1

slope_for_classB=1
regulate_at_MW_max_ratio = 0.8
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
                                                                    deadband=deadband,
                                                                    baterry_spetna_vazba=baterry_limit_nabijania)

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
                                                                        deadband=deadband,
                                                                        baterry_spetna_vazba=baterry_limit_nabijania)


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
axs[0].legend(['FVE_production','FVE_regulated','BESS_operation (+discharge | -charge )'])
axs[0].set_xlabel("čas t [min]")

axs[1].plot(baterry_percentage_capacity,lw=1)
axs[1].set_ylim(0, 100)
axs[1].set_title('% kapacita baterie')
axs[1].set_ylabel("aktualna kapacita [%]")
axs[1].set_xlabel("čas t [min]")
axs[1].axhline(y = 10, color = 'r', linestyle = 'dashed')
axs[1].axhline(y = 90, color = 'r', linestyle = 'dashed')
plt.show()

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

# todo count fails
#  evaluate max power, NO of changes of unabili to charge