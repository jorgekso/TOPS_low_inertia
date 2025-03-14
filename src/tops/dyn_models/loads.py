import numpy as np
from tops.dyn_models.utils import DAEModel
from tops.dyn_models.blocks import TimeConstant


class Load(DAEModel):
    def __init__(self, data, sys_par, **kwargs):
        super().__init__(data, sys_par, **kwargs)
        self.data = data
        self.par = data
        self.n_units = len(data)

        self.bus_idx = np.array(np.zeros(self.n_units), dtype=[(key, int) for key in self.bus_ref_spec().keys()])
        self.bus_idx_red = np.array(np.zeros(self.n_units), dtype=[(key, int) for key in self.bus_ref_spec().keys()])
        self.sys_par = sys_par  # {'s_n': 0, 'f_n': 50, 'bus_v_n': None}

    def bus_ref_spec(self):
        return {'terminal': self.par['bus']}

    def reduced_system(self):
        return self.par['bus']

    def load_flow_pq(self):
        return self.bus_idx['terminal'], self.par['P'], self.par['Q']

    def init_from_load_flow(self, x_0, v_0, S):
        self.v_0 = v_0[self.bus_idx['terminal']]
        s_load = (self.par['P'] + 1j * self.par['Q']) / self.sys_par['s_n']
        z_load = np.conj(abs(self.v_0) ** 2 / s_load)
        self.y_load = 1/z_load

        V_n = self.sys_par['bus_v_n'][self.bus_idx['terminal']]
        self.I_n = self.sys_par['s_n']/(np.sqrt(3)*V_n)

    def dyn_const_adm(self):
        return self.y_load, (self.bus_idx_red['terminal'],)*2

    def i(self, x, v):
        return v[self.bus_idx_red['terminal']]*self.y_load
    
    def I(self, x, v):
        return self.i(x, v)*self.I_n
    
    def s(self, x, v):
        return v[self.bus_idx_red['terminal']]*np.conj(self.i(x, v))

    def p(self, x, v):
        # p.u. system base
        return self.s(x, v).real

    def q(self, x, v):
        # p.u. system base
        return self.s(x, v).imag
    
    def P(self, x, v):
        # MW
        return self.s(x, v).real*self.sys_par['s_n']

    def Q(self, x, v):
        # MVA
        return self.s(x, v).imag*self.sys_par['s_n']
    
    def activate_FFR(self, P_FFR):
        # MW
        self.par['P'] -= P_FFR 
        return (f'FFR activated at {self.par["bus"]} with power injected = {P_FFR} MW')
    


class DynamicLoad(DAEModel):
    def __init__(self, data, sys_par, **kwargs):
        super().__init__(data, sys_par, **kwargs)
        self.data = data
        self.par = data
        self.n_units = len(data)

        self.bus_idx = np.array(np.zeros(self.n_units), dtype=[(key, int) for key in self.bus_ref_spec().keys()])
        self.bus_idx_red = np.array(np.zeros(self.n_units), dtype=[(key, int) for key in self.bus_ref_spec().keys()])
        self.sys_par = sys_par  # {'s_n': 0, 'f_n': 50, 'bus_v_n': None}

    def input_list(self):
        return ['g_setp', 'b_setp']
    
    def bus_ref_spec(self):
        return {'terminal': self.par['bus']}

    def reduced_system(self):
        return self.par['bus']

    def load_flow_pq(self):
        return self.bus_idx['terminal'], self.par['P'], self.par['Q']

    def init_from_load_flow(self, x_0, v_0, S):
        self.v_0 = v_0[self.bus_idx['terminal']]
        s_load = (self.par['P'] + 1j * self.par['Q']) / self.sys_par['s_n']
        z_load = np.conj(abs(self.v_0) ** 2 / s_load)
        y_load = 1/z_load
        self._input_values['g_setp'] = y_load.real
        self._input_values['b_setp'] = y_load.imag

        V_n = self.sys_par['bus_v_n'][self.bus_idx['terminal']]
        self.I_n = self.sys_par['s_n']/(np.sqrt(3)*V_n)

    def g_load(self, x, v):
        return self.g_setp(x, v)

    def b_load(self, x, v):
        return self.b_setp(x, v)

    def y_load(self, x, v):
        return self.g_load(x, v) + 1j*self.b_load(x, v)

    def dyn_var_adm(self, x, v):
        return self.y_load(x, v), (self.bus_idx_red['terminal'],)*2

    def i(self, x, v):
        return v[self.bus_idx_red['terminal']]*self.y_load(x, v)
    
    def I(self, x, v):
        return self.i(x, v)*self.I_n
    
    def s(self, x, v):
        return v[self.bus_idx_red['terminal']]*np.conj(self.i(x, v))

    def p(self, x, v):
        # p.u. system base
        return self.s(x, v).real

    def q(self, x, v):
        # p.u. system base
        return self.s(x, v).imag
    
    def P(self, x, v):
        # MW
        return self.s(x, v).real*self.sys_par['s_n']

    def Q(self, x, v):
        # MVA
        return self.s(x, v).imag*self.sys_par['s_n']


class DynamicLoadFiltered(DynamicLoad):
    """Dynamic load where the input is filtered using a low pass filter. 
    
    The load is an admittance which is determined by the output of two low pass filters,
    one for G (conductance) and one for B (susceptance).
    """

    def add_blocks(self):
        p = self.par
        self.lpf_g = TimeConstant(T=p['T_g'])
        self.lpf_g.input = lambda x, v: self.g_setp(x, v)

        self.lpf_b = TimeConstant(T=p['T_b'])
        self.lpf_b.input = lambda x, v: self.b_setp(x, v)

    def g_load(self, x, v):
        return self.lpf_g.output(x, v)

    def b_load(self, x, v):
        return self.lpf_b.output(x, v)

    def init_from_load_flow(self, x_0, v_0, S):
        self.v_0 = v_0[self.bus_idx['terminal']]
        s_load = (self.par['P'] + 1j * self.par['Q']) / self.sys_par['s_n']
        z_load = np.conj(abs(self.v_0) ** 2 / s_load)
        y_load = 1/z_load
        self._input_values['g_setp'] = y_load.real
        self._input_values['b_setp'] = y_load.imag

        self.lpf_g.initialize(x_0, v_0, y_load.real)
        self.lpf_b.initialize(x_0, v_0, y_load.imag)

        V_n = self.sys_par['bus_v_n'][self.bus_idx['terminal']]
        self.I_n = self.sys_par['s_n']/(np.sqrt(3)*V_n)