import math
import numpy as np

def saldo(FVE_production,battery):

    saldo = FVE_production + battery

    return saldo

def analyze_FVE(list_of_values,average_past=0,vahovanie=False):

    time= list(range(0,len(list_of_values)))

    if vahovanie==True and len(time)>0:
        dlzka=len(list_of_values)
        vahy=[(x+1)/(dlzka/1.88) for x in time]


    if len(list_of_values) != 0:

        if vahovanie==True:
            x1w1 = [x * y for x, y in zip(list_of_values, vahy)]
            average = calc_average(x1w1)
        else:
            average = calc_average(list_of_values)
    else:
        average =0

   # if average_past - average >3:
   #     average=average * average/average_past


    B0, B1 = estimate_coef(time,list_of_values)

    return average,B0,B1

def cumval(value,list_of_values, cumulation_no=10):
    '''
    uklada hodnoty do list ak je dostatočny počet vypluje release = true ak nie vypluje FAlse
    :param value:
    :param list_of_values:
    :param cumulation_no:
    :return: list hodnoty
    '''
    dlzka= len(list_of_values)
    release=False
    if dlzka<= cumulation_no:

        list_of_values.append(value)

        if dlzka  == cumulation_no:
            release = True
    else:
        if dlzka -1 == cumulation_no:
            list_of_values.clear()

        list_of_values.append(value)
        release=False

    return list_of_values,release



def BMS_class_A_smooth_core(FVE,expectations,baterry,deadband=0):

    percentage_stored=baterry.get_percented_stored()

    saldo = expectations - FVE
    status="iddle"

    proposed_value = 0
    release_enery = 0
    if saldo >= 0+deadband:
        status = "discharge"
        proposed_value=saldo
        # regulacia na dolny  limit
        # if baterry_spetna_vazba ==True:
        #
        #     if percentage_stored <0.20:
        #         proposed_value=proposed_value*0.8
        #
        #     if percentage_stored <0.14:
        #         proposed_value=proposed_value*0.5
        #
        #     if percentage_stored <0.11:
        #         proposed_value=proposed_value*0.2
        #
        #     if percentage_stored <0.10:
        #         proposed_value=proposed_value*0
        #
        #     if percentage_stored > 0.80:
        #         proposed_value = proposed_value * 1.2
        #
        #     if percentage_stored > 0.86:
        #         proposed_value = proposed_value * 1.5
        #
        #     if percentage_stored > 0.88:
        #         proposed_value = proposed_value * 1.8

        release_enery=baterry.discharge(abs(proposed_value))


    if saldo <=0-deadband:
        status="charge"
        proposed_value=saldo
        # regulacia na horny limit
        # if baterry_spetna_vazba == True:
        #     if percentage_stored >0.80:
        #         proposed_value=proposed_value*0.8
        #
        #     if percentage_stored >0.86:
        #         proposed_value=proposed_value*0.5
        #
        #     if percentage_stored >0.88:
        #         proposed_value=proposed_value*0.2
        #
        #     if percentage_stored >0.9:
        #         proposed_value=proposed_value*0.0
        #
        #     if percentage_stored <0.20:
        #         proposed_value=proposed_value*1.2
        #
        #     if percentage_stored <0.14:
        #         proposed_value=proposed_value*1.5
        #
        #     if percentage_stored <0.11:
        #         proposed_value=proposed_value*1.8


        release_enery=baterry.charge(abs(proposed_value))


    if saldo < 0+deadband and saldo > 0-deadband:
        status="iddle"
        baterry.iddle()

    regulated_FVE = FVE + release_enery

    return status,proposed_value,release_enery,regulated_FVE


def estimate_coef(x_list, y_list):
    # number of observations/points
    x = np.array(x_list)
    y = np.array(y_list)

    n = np.size(x)

    # mean of x and y vector
    m_x = np.mean(x)
    m_y = np.mean(y)

    # calculating cross-deviation and deviation about x
    SS_xy = np.sum(y * x) - n * m_y * m_x
    SS_xx = np.sum(x * x) - n * m_x * m_x

    # calculating regression coefficients
    b_1 = SS_xy / SS_xx
    b_0 = m_y - b_1 * m_x

    return (b_0, b_1)


def list_substraction(list1,list2):
    # Subtract two lists with numpy
    array1 = np.array(list1)
    array2 = np.array(list2)
    subtracted_array = np.subtract(array1, array2)
    subtracted = list(subtracted_array)

    return subtracted

def calc_average(list):
    result = sum(list) / len(list)
    return result

def calc_weght_average(list):
    average=calc_average(list)

    citatel=0
    menovatel=0
    result=0
    if average != 0 :
        for element in list:

            weight=(element/average) *(element/average)
            citatel=citatel+ weight*element
            menovatel=menovatel + weight



        result= citatel/menovatel

    return result

def calc_time_of_day(minute):

    daytime = minute%1441

    return daytime