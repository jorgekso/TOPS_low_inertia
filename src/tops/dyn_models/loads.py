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
    
    def v0(self,idx):
        return self.v_0[idx]


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


class DynamicLoad2(DAEModel):
    '''
    Dynamic load model with estimation for local frequency 
    Created as a part of the master thesis of N.Lillelien and J.Sørhaug

    Instantiate:
    'loads': {
            'DynamicLoad2': [
                ['name',    'bus',   'P',    'Q',   'model', 'K_est', 'T_est'],
                ['L3000-1', '3000',  1059,   422,   'Z',       1,       0.1],    ]
            ],
        }
    '''
    def __init__(self, data, sys_par, **kwargs):
        super().__init__(data, sys_par, **kwargs)
        self.data = data
        self.par = data
        self.n_units = len(data)

        self.bus_idx = np.array(np.zeros(self.n_units), dtype=[(key, int) for key in self.bus_ref_spec().keys()])
        self.bus_idx_red = np.array(np.zeros(self.n_units), dtype=[(key, int) for key in self.bus_ref_spec().keys()])
        self.sys_par = sys_par  # {'s_n': 0, 'f_n': 50, 'bus_v_n': None}

    def input_list(self):
        return ['g_setp', 'b_setp','t_ffr_start','t_ffr_end','P_ffr']
    
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
        self._input_values['t_ffr_start'] = 0
        self._input_values['t_ffr_end'] = 0
        self._input_values['P_ffr'] = 0

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
    
    def v_t(self, x, v):
        # p.u.
        return v[self.bus_idx_red['terminal']]
    
    def v_q(self, x, v):
        # p.u.
        return (self.v_t(x,v)*np.exp(-1j*self.local_view(x)['angle'])).imag
    
    def state_list(self):
        return ['x_est', 'angle']
    
    def state_derivatives(self, dx, x, v):
        
        dX = self.local_view(dx)
        X = self.local_view(x)
        par = self.par

        dX['x_est'][:] = par['K_est']/par['T_est']*(self.v_q(x,v))
        dX['angle'][:] = X['x_est'] + par['K_est']*self.v_q(x,v)
        return  
    
    def freq_est(self, x, v):
        X = self.local_view(x)
        freq = X['x_est']/(2*np.pi)
        return 50 + freq
    def rocof_est(self, x, v):
        par = self.par
        # rocof = dX['x_est']
        rocof = par['K_est']/par['T_est']*(self.v_q(x,v))
        return rocof/(2*np.pi)

    def FFR(self, x, v,t,index):
        inputs = self._input_values
        par = self.par
        if inputs['t_ffr_start'][index] <= t <= inputs['t_ffr_end'][index] and t > 0:
            P = (par['P'][index]-inputs['P_ffr'][index])/self.sys_par['s_n']
            Q = par['Q'][index]/self.sys_par['s_n']
            z = np.conj(abs(self.v_0[index])**2/(P+1j*Q))
            y = 1/z
            g = y.real
            b = y.imag
            self._input_values['g_setp'][index] = g
            self._input_values['b_setp'][index] = b
        else:
            P = par['P'][index]/self.sys_par['s_n']
            Q = par['Q'][index]/self.sys_par['s_n']
            z = np.conj(abs(self.v_0[index])**2/(P+1j*Q))
            y = 1/z
            g = y.real
            b = y.imag
            self._input_values['g_setp'][index] = g
            self._input_values['b_setp'][index] = b
        