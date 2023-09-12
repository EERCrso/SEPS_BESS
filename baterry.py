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
                 operation_timestep=60,
                 charge_losses=1, # ak 60 pracujeme v minutach  aj 4 tak v 15 minutach ak 1 v hodinach
                 discharge_losses=1,
                 idling_losses=1.25e-3,
                 limit_capacity=True):

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
        self._operation_limited_due_capacity_limit=False
        self._charge_losses=charge_losses
        self._discharge_losses=discharge_losses
        self._idling_losses=idling_losses
        self._limit_capacity=limit_capacity
        self._sum_of_charging_energy=0
        self._sum_of_discharging_energy=0
        # todo max min percento z inštalovane vykonu kde ma pracovat



    def baterry_work(self,status,value):

        if status == "charge":

            self.charge(self, value)

        elif status == "discharge":

            self.discharge(self,value)


    def charge(self,MWh_requsted):

        # regulacia na horny limit
        if self._limit_capacity == True:
            if self._percentage_stored > 0.80:
                MWh_requsted = MWh_requsted * 0.8
                self._operation_limited_due_capacity_limit = True
            else:
                self._operation_limited_due_capacity_limit = False

            if self._percentage_stored > 0.86:
                MWh_requsted = MWh_requsted * 0.5
                self._operation_limited_due_capacity_limit = True
            else:
                self._operation_limited_due_capacity_limit = False

            if self._percentage_stored > 0.88:
                MWh_requsted = MWh_requsted * 0.2
                self._operation_limited_due_capacity_limit = True
            else:
                self._operation_limited_due_capacity_limit = False

            if self._percentage_stored > 0.9:
                MWh_requsted = MWh_requsted * 0.0
                self._operation_limited_due_capacity_limit = True
            else:
                self._operation_limited_due_capacity_limit = False

            if self._percentage_stored < 0.20:
                MWh_requsted = MWh_requsted * 1.2
                self._operation_limited_due_capacity_limit = True
            else:
                self._operation_limited_due_capacity_limit = False

            if self._percentage_stored < 0.14:
                MWh_requsted = MWh_requsted * 1.5
                self._operation_limited_due_capacity_limit = True
            else:
                self._operation_limited_due_capacity_limit = False

            if self._percentage_stored < 0.11:
                MWh_requsted = MWh_requsted * 1.8
                self._operation_limited_due_capacity_limit = True
            else:
                self._operation_limited_due_capacity_limit = False


        looses = MWh_requsted * self._charge_losses/100
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
            self._MWhstored = self._MWhrated - looses/self._operation_timestep
            self._enougth_capacity = 0

        else:
            self._MWhstored =self._MWhstored + MWh / self._operation_timestep - looses/self._operation_timestep
            energy = MWh*-1

            if self._operation_limited_due_capacity_limit == True:
                self._enougth_capacity = 0
            else:
                self._enougth_capacity = 1

        #urči percentualny zostatok kapacity
        self._percentage_stored = self._MWhstored / self._MWhrated

        self._sum_of_charging_energy = self._sum_of_charging_energy + (energy/self._operation_timestep)*-1


        return energy


    def discharge(self,MWh_requsted):

        # regulacia na dolny  limit
        if self._limit_capacity == True:

            if self._percentage_stored < 0.20:
                MWh_requsted = MWh_requsted * 0.8
                self._operation_limited_due_capacity_limit=True
            else:
                self._operation_limited_due_capacity_limit = False

            if self._percentage_stored < 0.14:
                MWh_requsted = MWh_requsted * 0.5
                self._operation_limited_due_capacity_limit = True
            else:
                self._operation_limited_due_capacity_limit = False


            if self._percentage_stored < 0.11:
                MWh_requsted = MWh_requsted * 0.2
                self._operation_limited_due_capacity_limit = True
            else:
                self._operation_limited_due_capacity_limit = False

            if self._percentage_stored < 0.10:
                MWh_requsted = MWh_requsted * 0
                self._operation_limited_due_capacity_limit = True
            else:
                self._operation_limited_due_capacity_limit = False

            if self._percentage_stored > 0.80:
                MWh_requsted = MWh_requsted * 1.2
                self._operation_limited_due_capacity_limit = True
            else:
                self._operation_limited_due_capacity_limit = False

            if self._percentage_stored > 0.86:
                MWh_requsted = MWh_requsted * 1.5
                self._operation_limited_due_capacity_limit = True
            else:
                self._operation_limited_due_capacity_limit = False

            if self._percentage_stored > 0.88:
                MWh_requsted = MWh_requsted * 1.8
                self._operation_limited_due_capacity_limit = True
            else:
                self._operation_limited_due_capacity_limit = False


        looses=MWh_requsted*self._discharge_losses/100
        MWh_requsted=MWh_requsted

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
            self._MWhstored = self._MWhstored - (MWh+looses)/self._operation_timestep

            if self._operation_limited_due_capacity_limit == True:
                self._enougth_capacity = 0
            else:
                self._enougth_capacity = 1
        else:

            energy = self._MWhstored*self._operation_timestep - looses/self._operation_timestep
            self._MWhstored =0
            self._enougth_capacity = 0

        #urči percentualny zostatok kapacity
        self._percentage_stored = self._MWhstored / self._MWhrated

        self._sum_of_discharging_energy = self._sum_of_discharging_energy+energy/self._operation_timestep

        return energy


    def get_percented_stored(self):
        return self._percentage_stored

    def get_enougth_power(self):
        return self._enougth_power

    def get_enougth_capacity(self):
        return self._enougth_capacity

    def iddle(self):
        self._MWhstored = self._MWhstored - ((self._MWhstored*self._idling_losses)/100) / self._operation_timestep

        if self._MWhstored <= 0:
            self._MWhstored = 0

        self._percentage_stored = self._MWhstored / self._MWhrated

    def number_of_charging_cycles(self):
        no= self._sum_of_charging_energy/self._MWhrated
        return no

    def number_of_discharging_cycles(self):
        no= self._sum_of_discharging_energy/self._MWhrated
        return no




