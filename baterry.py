class baterry:
    '''
    Simple reprezentation of baterry
    '''
    def __init__(self,Name,
                 MWhrated=None,
                 MWinstalled_power=None,
                 MWhstored=None,
                 status=None,
                 upper_alert=None,
                 lower_alert=None,
                 operation_timestep=60):

        self._name=Name
        self._MWhrated=MWhrated
        self._MWinstalled_power=MWinstalled_power
        self._MWhstored = MWhrated/2
        self._percentage_stored = self._MWhstored / self._MWhrated
        self._status=status
        self._upper_alert=upper_alert
        self._lower_alert=lower_alert
        self._operation_timestep = operation_timestep
        self._enougth_power =1
        self._enougth_capacity=1
        # todo max min percento z inštalovane vykonu kde ma pracovat



    def baterry_work(self,status,value):

        if status == "charge":

            self.charge(self, value)

        elif status == "discharge":

            self.discharge(self,value)





    def charge(self,MWh_requsted):

        #Kontrola na max inšt vykon baterie
        if self._MWinstalled_power > MWh_requsted:
            MWh= MWh_requsted
            self._enougth_power=1
        else:
            MWh = self._MWinstalled_power
            self._enougth_power = 0


        # Nie je energy ktoru sa snazim vložit do bess ataka že prekračuje max kapacitu ?
        if  self._MWhrated < self._MWhstored + MWh/self._operation_timestep:
            energy = (self._MWhrated - self._MWhstored )*self._operation_timestep *-1
            self._MWhstored = self._MWhrated
            self._enougth_capacity = 0
        else:
            self._MWhstored =self._MWhstored + MWh / self._operation_timestep
            energy = MWh*-1
            self._enougth_capacity=1

        #urči percentualny zostatok kapacity
        self._percentage_stored = self._MWhstored / self._MWhrated

        return energy


    def discharge(self,MWh_requsted):

        #Kontrola na max inšt vykon baterie
        if self._MWinstalled_power > MWh_requsted:
            MWh= MWh_requsted
            self._enougth_power = 1
        else:
            MWh = self._MWinstalled_power
            self._enougth_power = 0

        # je energia v BESS dostatočna aby som ju dodal ?
        if  self._MWhstored >  MWh/self._operation_timestep:
            energy = MWh
            self._MWhstored = self._MWhstored - MWh/self._operation_timestep
            self._enougth_capacity = 1
        else:

            energy = self._MWhstored*self._operation_timestep
            self._MWhstored =0
            self._enougth_capacity = 0

        #urči percentualny zostatok kapacity
        self._percentage_stored = self._MWhstored / self._MWhrated

        return energy


    def get_percented_stored(self):
        return self._percentage_stored

    def get_enougth_power(self):
        return self._enougth_power

    def get_enougth_capacity(self):
        return self._enougth_capacity




