# Readme
 
 - program simuluje spravanie BESS
 - hlavny subor je main.py
 
 ## data
 import dat z csv defaul je tam FVE_2021_1MIN_FULL_NO_DIFF.csv . tento subor na tri hlavne stlpce kde je vroba z FVE pre slovensko a po distribučkach
 - je možne  zvolit si den
 - alebo počitat celi rok
 
 ## nastavenia
 
 - TRIEDA 
   - A  - vyhladzovanie priebehu
   - B  - kombinacia peakshave a day shift podla parametrov baterie a požiadaviek regulacie
   
  - static_window - ak TRUE staticke okno ak false dynamicke okno
  - average_method - ak True priemeruje ak FAlse počita slope a snaži sa aproximovat ( slope nefunguje spravne experimentalna verzia )

 - cum_time - cumulativny čas na vypočet priemeru pre smoothing
 - baterry_limit_nabijania - limitacia baterie vzhladom na jej aktualnu kapacitu aby nebolo presiahnute 90 % alebo menej ako 10% kapacity podrobne nastavenia su vo funkcii BMS_class_A_smooth_core 
 - deadband necitlivost baterie
 
 - slope_for_classB MW/min zmena ktorou može sa vybijat bateria len pre B
 - regulate_at_MW_max_ratio  - percentualna hodnota <0-1> v max vykonu dna na ktoru  sa drži vykon B
  
  ## funkcionalita
  
  je potrebe sa hrať s marametrami  vystupom su grafy a  čiselne zavilosti. ešte sa dopracuje vystup regulovaneho vykonu, ktory potom je možne porovnat s neregulovaniu hodnotou
  .program obsahuje objekt baterku a BMS je implementovane cez main v pojeni s funkciou  "BMS_class_A_smooth_core" ktora je pre obe triedy
  ### trieda A
   
  ako vystupy na porovnanie su k dispozicii počty minut kedy nevedel zregulovat vykonovo a počty minut kedy už nebola kapacita v baterke