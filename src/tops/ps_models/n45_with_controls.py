#N45 version made by Martin Teignes (no tuning)

def load():
    return {
        'base_mva': 1000,
        'f': 50,
        'slack_bus': '3300', #3300
        # 24 = SE_4
        # 23 = SE_3
        # 22 = SE_2
        # 21 = SE_1
        # 11 = NO_1
        # 12 = NO_2
        # 13 = NO_3
        # 14 = NO_4
        # 15 = NO_5
        # 31 = FI
        #
        'buses': [
            ['name', 'V_n', 'Area', 'V_0'],
            ['3000', 420, 23, 0.9857],
            ['3020', 420, 23, 0.9843],
            ['3100', 420, 22, 1.0044],
            ['3115', 420, 21, 1.0000],
            ['3200', 420, 23, 1.0067],
            ['3245', 420, 22, 1.0000],
            ['3249', 420, 21, 1.0000],
            ['3300', 420, 23, 1.0000],
            ['3359', 420, 23, 1.0000],
            ['3360', 135, 23, 0.9913],
            ['3701', 300, 21, 0.9971],
            ['5110', 420, 11, 1.0015],
            ['5120', 420, 11, 1.0000],
            ['5130', 300, 11, 0.9514],
            ['5210', 420, 12, 0.9961],
            ['5220', 420, 12, 0.9988],
            ['5230', 420, 12, 1.0000],
            ['5231', 300, 12, 0.9994],
            ['5240', 420, 12, 1.0000],
            ['5250', 300, 12, 1.0000],
            ['5260', 300, 12, 0.9971],
            ['5270', 300, 12, 0.9937],
            ['5280', 420, 12, 1.0006],
            ['5310', 420, 13, 1.0000],
            ['5320', 420, 13, 1.0000],
            ['5321', 420, 13, 0.9761],
            ['5330', 420, 13, 0.9990],
            ['5410', 300, 14, 0.9999],
            ['5420', 420, 14, 1.0000],
            ['5430', 420, 14, 0.9604],
            ['5431', 420, 14, 0.9365],
            # Raised Check_lineflow from 0.9365 (from PF in PSSE) to 0.95, in order to regain stability.
            ['5510', 420, 15, 1.0000],
            ['5520', 420, 15, 1.0000],
            ['5530', 420, 15, 0.9932],
            ['5540', 300, 15, 0.9939],
            ['5550', 420, 15, 0.9962],
            ['5551', 300, 15, 1.0000],
            ['5560', 300, 15, 0.9963],
            ['7000', 420, 31, 1.0000],
            ['7010', 420, 31, 0.9964],
            ['7020', 420, 31, 1.0000],
            ['7100', 420, 31, 1.0000],
            ['8500', 420, 24, 0.9987],
            ['8600', 420, 24, 0.9986],
            ['8700', 420, 24, 0.9986],
        ],


        'lines': [
            ['name', 'from_bus', 'to_bus', 'length', 'S_n', 'V_n', 'unit', 'R', 'X', 'B'],
            ['L3000-3020', '3000', '3020', 1, 0, 0, 'p.u.', 0.000000, 0.006000, 0.000000],
            ['L3000-3115', '3000', '3115', 1, 0, 0, 'p.u.', 0.045000, 0.540000, 0.500000],
            ['L3000-3245', '3000', '3245', 1, 0, 0, 'p.u.', 0.004800, 0.072000, 0.050000],
            ['L3000-3245', '3000', '3245', 1, 0, 0, 'p.u.', 0.010800, 0.120000, 0.050000],
            ['L3000-3300', '3000', '3300', 1, 0, 0, 'p.u.', 0.003600, 0.048000, 0.030000],
            ['L3000-3300', '3000', '3300', 1, 0, 0, 'p.u.', 0.005400, 0.060000, 0.025000],
            ['L3100-3115', '3100', '3115', 1, 0, 0, 'p.u.', 0.018000, 0.240000, 0.110000],
            ['L3100-3200', '3100', '3200', 1, 0, 0, 'p.u.', 0.024000, 0.144000, 0.200000],
            ['L3100-3200', '3100', '3200', 1, 0, 0, 'p.u.', 0.024000, 0.144000, 0.200000],
            ['L3100-3200', '3100', '3200', 1, 0, 0, 'p.u.', 0.024000, 0.144000, 0.200000],
            ['L3100-3249', '3100', '3249', 1, 0, 0, 'p.u.', 0.018000, 0.258000, 0.160000],
            ['L3100-3359', '3100', '3359', 1, 0, 0, 'p.u.', 0.048000, 0.300000, 0.250000],
            ['L3100-3359', '3100', '3359', 1, 0, 0, 'p.u.', 0.024000, 0.138000, 0.240000],
            ['L3115-3245', '3115', '3245', 1, 0, 0, 'p.u.', 0.027000, 0.300000, 0.140000],
            ['L3115-3249', '3115', '3249', 1, 0, 0, 'p.u.', 0.009000, 0.120000, 0.080000],
            ['L3115-5430', '3115', '5430', 1, 0, 0, 'p.u.', 0.014400, 0.210000, 0.100000],
            ['L3115-7100', '3115', '7100', 1, 0, 0, 'p.u.', 0.024000, 0.078000, 0.130000],
            ['L3200-3300', '3200', '3300', 1, 0, 0, 'p.u.', 0.012000, 0.120000, 0.060000],
            ['L3200-3359', '3200', '3359', 1, 0, 0, 'p.u.', 0.006000, 0.120000, 0.070000],
            ['L3200-8500', '3200', '8500', 1, 0, 0, 'p.u.', 0.006000, 0.102000, 0.060000],
            ['L3245-5330', '3245', '5330', 1, 0, 0, 'p.u.', 0.007200, 0.180000, 0.050000],
            ['L3249-7100', '3249', '7100', 1, 0, 0, 'p.u.', 0.012000, 0.045000, 0.078000],
            ['L3300-8500', '3300', '8500', 1, 0, 0, 'p.u.', 0.012000, 0.138000, 0.060000],
            ['L3300-8500', '3300', '8500', 1, 0, 0, 'p.u.', 0.007200, 0.162000, 0.100000],
            ['L3359-5110', '3359', '5110', 1, 0, 0, 'p.u.', 0.005760, 0.030000, 0.090000],
            ['L3359-5110', '3359', '5110', 1, 0, 0, 'p.u.', 0.007200, 0.030000, 0.060000],
            ['L3359-8500', '3359', '8500', 1, 0, 0, 'p.u.', 0.007200, 0.162000, 0.100000],
            ['L3359-8500', '3359', '8500', 1, 0, 0, 'p.u.', 0.015000, 0.192000, 0.090000],
            ['L5110-5120', '5110', '5120', 1, 0, 0, 'p.u.', 0.006000, 0.060000, 0.040000],
            ['L5110-5280', '5110', '5280', 1, 0, 0, 'p.u.', 0.004800, 0.030000, 0.080000],
            ['L5120-5240', '5120', '5240', 1, 0, 0, 'p.u.', 0.010800, 0.060000, 0.130000],
            ['L5120-5520', '5120', '5520', 1, 0, 0, 'p.u.', 0.010800, 0.165600, 0.130000],
            ['L5120-5530', '5120', '5530', 1, 0, 0, 'p.u.', 0.010800, 0.165600, 0.130000],
            ['L5210-5220', '5210', '5220', 1, 0, 0, 'p.u.', 0.002400, 0.030000, 0.050000],
            ['L5210-5240', '5210', '5240', 1, 0, 0, 'p.u.', 0.005400, 0.084000, 0.100000],
            ['L5210-5280', '5210', '5280', 1, 0, 0, 'p.u.', 0.005400, 0.060000, 0.100000],
            ['L5220-5230', '5220', '5230', 1, 0, 0, 'p.u.', 0.002400, 0.030000, 0.050000],
            ['L5230-5240', '5230', '5240', 1, 0, 0, 'p.u.', 0.005760, 0.091800, 0.090000],
            ['L5240-5280', '5240', '5280', 1, 0, 0, 'p.u.', 0.005400, 0.060000, 0.100000],
            ['L5250-5260', '5250', '5260', 1, 0, 0, 'p.u.', 0.010800, 0.122400, 0.020000],
            ['L5250-5270', '5250', '5270', 1, 0, 0, 'p.u.', 0.010800, 0.122400, 0.020000],
            ['L5260-5270', '5260', '5270', 1, 0, 0, 'p.u.', 0.010800, 0.122400, 0.020000],
            ['L5310-5320', '5310', '5320', 1, 0, 0, 'p.u.', 0.014400, 0.480000, 0.100000],
            ['L5310-5550', '5310', '5550', 1, 0, 0, 'p.u.', 0.012000, 0.480000, 0.100000],
            ['L5320-5321', '5320', '5321', 1, 0, 0, 'p.u.', 0.007200, 0.072000, 0.050000],
            ['L5320-5330', '5320', '5330', 1, 0, 0, 'p.u.', 0.007200, 0.060000, 0.050000],
            ['L5320-5420', '5320', '5420', 1, 0, 0, 'p.u.', 0.018000, 0.048000, 0.120000],
            ['L5420-5430', '5420', '5430', 1, 0, 0, 'p.u.', 0.018000, 0.180000, 0.120000],
            ['L5430-5431', '5430', '5431', 1, 0, 0, 'p.u.', 0.018000, 0.180000, 0.130000],
            ['L5510-5520', '5510', '5520', 1, 0, 0, 'p.u.', 0.002304, 0.036000, 0.028000],
            ['L5520-5530', '5520', '5530', 1, 0, 0, 'p.u.', 0.006000, 0.060000, 0.025000],
            ['L7000-7010', '7000', '7010', 1, 0, 0, 'p.u.', 0.000000, 0.006000, 0.000000],
            ['L7000-7020', '7000', '7020', 1, 0, 0, 'p.u.', 0.000000, 0.006000, 0.000000],
            ['L7000-7100', '7000', '7100', 1, 0, 0, 'p.u.', 0.024000, 0.072000, 0.130000],
            ['L7000-7100', '7000', '7100', 1, 0, 0, 'p.u.', 0.024000, 0.072000, 0.130000],
            ['L7000-7100', '7000', '7100', 1, 0, 0, 'p.u.', 0.024000, 0.084000, 0.130000],
            ['L8500-8600', '8500', '8600', 1, 0, 0, 'p.u.', 0.000000, 0.006000, 0.000000],
            ['L8500-8700', '8500', '8700', 1, 0, 0, 'p.u.', 0.000000, 0.006000, 0.000000],
        ],

        'transformers': [
            ['name', 'from_bus', 'to_bus', 'S_n', 'V_n_from', 'V_n_to', 'R', 'X', 'ratio'],
            ['T3249-3701', '3249', '3701', 1000, 0, 0, 0.020000, 1.000000, 1],
            ['T3359-3360', '3359', '3360', 1000, 0, 0, 0.005000, 0.020000, 1],
            ['T3701-5420', '3701', '5420', 1000, 0, 0, 0.020000, 2.000000, 1],
            ['T5120-5130', '5120', '5130', 1000, 0, 0, 0.024000, 1.000000, 1],
            ['T5130-5320', '5130', '5320', 1000, 0, 0, 0.024000, 1.350000, 1],
            ['T5230-5231', '5230', '5231', 1000, 0, 0, 0.000200, 0.007600, 1],
            ['T5240-5250', '5240', '5250', 1000, 0, 0, 0.000200, 0.007600, 1],
            ['T5260-5510', '5260', '5510', 1000, 0, 0, 0.000200, 0.480000, 1],
            ['T5320-5410', '5320', '5410', 1000, 0, 0, 0.020000, 0.500000, 1],
            ['T5410-5420', '5410', '5420', 1000, 0, 0, 0.020000, 0.500000, 1],
            ['T5510-5560', '5510', '5560', 1000, 0, 0, 0.000400, 0.015000, 1],
            ['T5530-5540', '5530', '5540', 1000, 0, 0, 0.001600, 0.061000, 1],
            ['T5540-5550', '5540', '5550', 1000, 0, 0, 0.001600, 0.061000, 1],
            ['T5550-5551', '5550', '5551', 1000, 0, 0, 0.001600, 0.061000, 1],
            ['T5550-5560', '5550', '5560', 1000, 0, 0, 0.000400, 0.015000, 1],
        ],

        'loads': [
            ['name', 'bus', 'P', 'Q', 'model'],
            ['L3000-1', '3000', 1059.376, 422.8077, 'Z'],
            ['L3000-2', '3000', 1059.376, 422.8077, 'Z'],
            ['L3000-3', '3000', 1059.376, 422.8077, 'Z'],
            ['L3020-1', '3020', 450, 227.3995, 'Z'],
            ['L3100-1', '3100', 1454.3, 283.7681, 'Z'],
            ['L3115-1', '3115', 272.4, 244.1441, 'Z'],
            ['L3249-1', '3249', 850.7484, 244.1441, 'Z'],
            ['L3300-1', '3300', 1295.5, 298.277, 'Z'],
            ['L3300-2', '3300', 907.7763, 298.277, 'Z'],
            ['L3359-1', '3359', 1089.33, 447.4156, 'Z'],
            ['L3359-2', '3359', 1089.33, 447.4156, 'Z'],
            ['L3359-3', '3359', 1089.33, 447.4156, 'Z'],
            ['L3359-4', '3359', 1089.33, 447.4156, 'Z'],
            ['L3360-1', '3360', 714, 566.8727, 'Z'],
            ['L5120-1', '5120', 1045.9, 25, 'Z'],
            ['L5120-2', '5120', 1095, 25, 'Z'],
            ['L5120-3', '5120', 1095, 25, 'Z'],
            ['L5210-1', '5210', 990, 50, 'Z'],
            ['L5210-2', '5210', 1099, 50, 'Z'],
            ['L5220-1', '5220', 0, 0, 'Z'],
            #['L5230-1', '5230', 1436, 50, 'Z'], #VSC
            ['L5231-1', '5231', 1099, 50, 'Z'],
            #['L5240-1', '5240', 1099, 50, 'Z'], #VSC
            ['L5240-2', '5240', 637, 50, 'Z'],
            ['L5270-1', '5270', 461.2, 50, 'Z'],
            ['L5310-1', '5310', 773, 250, 'Z'],
            ['L5320-1', '5320', 778.6, 250, 'Z'],
            ['L5320-2', '5320', 773, 250, 'Z'],
            ['L5321-1', '5321', 773, 250, 'Z'],
            ['L5420-1', '5420', 749, 50, 'Z'],
            ['L5430-1', '5430', 627, 50, 'Z'],
            ['L5431-1', '5431', 749, 50, 'Z'],
            ['L5530-1', '5530', 500, 100, 'Z'],
            ['L5560-1', '5560', 614.5, 400, 'Z'],
            ['L5560-2', '5560', 629, 400, 'Z'],
            ['L7000-1', '7000', 1138.1, 51.0442, 'Z'],
            ['L7000-2', '7000', 1162.006, 51.0442, 'Z'],
            ['L7000-3', '7000', 1162.006, 51.0442, 'Z'],
            ['L7000-4', '7000', 1162.006, 51.0442, 'Z'],
            ['L7000-5', '7000', 1162.006, 51.0442, 'Z'],
            ['L7010-1', '7010', -450, 600, 'Z'],
            #['L7020-1', '7020', 514, -5, 'Z'], #VSC
            ['L7020-2', '7020', 0, 0, 'Z'],
            ['L7100-1', '7100', 1043.985, 145.8405, 'Z'],
            ['L7100-2', '7100', 1043.985, 145.8405, 'Z'],
            ['L8500-1', '8500', 788.5, 295.5341, 'Z'],
            ['L8500-2', '8500', 846.3333, 295.5341, 'Z'],
            ['L8500-3', '8500', 846.3333, 295.5341, 'Z'],
            ['L8600-1', '8600', 449, 10, 'Z'],  # 624
            ['L8600-2', '8600', 175, 4, 'Z'],
            ['L8700-1', '8700', 344, 0, 'Z'],
            #['L8700-2', '8700', 413, 0, 'Z'], #VSC
        ],

        'generators': {
            'GEN': [
                ['name',     'bus',  'S_n',   'V_n', 'P',       'V',   'H', 'D', 'X_d',  'X_q',   'X_d_t', 'X_q_t', 'X_d_st', 'X_q_st', 'T_d0_t', 'T_q0_t', 'T_d0_st', 'T_q0_st'],
                ['G3000-1',  '3000', 1100.00,  0,     709.5763,  1,     6,   0,   2.22,   2.13,    0.36,    0.468,   0.225,    0.225,    5,        1,        0.05,      0.05],
                ['G3000-2',  '3000', 1100.00,  0,     709.5763,  1,     6,   0,   2.22,   2.13,    0.36,    0.468,   0.225,    0.225,    5,        1,        0.05,      0.05],
                ['G3115-1',  '3115', 1400.00,  0,     834.5784,  1,     3,   0,   0.946,  0.565,   0.29,    0.565,   0.23,     0.23,     7.57,     1,        0.045,     0.1],
                ['G3115-2',  '3115', 1400.00,  0,     834.5784,  1,     3,   0,   0.946,  0.565,   0.29,    0.565,   0.23,     0.23,     7.57,     1,        0.045,     0.1],
                ['G3245-1',  '3245', 7000.00,  0,     5840,      1,     3,   0,   0.75,   0.5,     0.25,    0.5,     0.15385,  0.15385,  5,        1,        0.06,      0.1],
                ['G3249-1',  '3249', 1600.00,  0,     1005.422,  1,     3,   0,   1.036,  0.63,    0.28,    0.63,    0.21,     0.21,     10.13,    1,        0.06,      0.1],
                ['G3249-2',  '3249', 1600.00,  0,     1005.422,  1,     3,   0,   1.036,  0.63,    0.28,    0.63,    0.21,     0.21,     10.13,    1,        0.06,      0.1],
                ['G3300-1',  '3300', 1700.00,  0,     787.5246,  1,     6,   0,   2.42,   2,       0.23,    0.4108,  0.16,     0.16,     10.8,     1,        0.05,      0.05],
                ['G3300-2',  '3300', 1700.00,  0,     787.5246,  1,     6,   0,   2.42,   2,       0.23,    0.4108,  0.16,     0.16,     10.8,     1,        0.05,      0.05],
                ['G3300-3',  '3300', 1700.00,  0,     787.5246,  1,     6,   0,   2.42,   2,       0.23,    0.4108,  0.16,     0.16,     10.8,     1,        0.05,      0.05],
                ['G3359-1',  '3359', 1200.00,  0,     766.3424,  1,     3,   0,   2.13,   2.03,    0.31,    0.403,   0.1937,   0.1937,   4.75,     1,        0.05,      0.05],
                ['G3359-2',  '3359', 1200.00,  0,     766.3424,  1,     3,   0,   2.13,   2.03,    0.31,    0.403,   0.1937,   0.1937,   4.75,     1,        0.05,      0.05],
                ['G3359-3',  '3359', 1200.00,  0,     766.3424,  1,     3,   0,   2.13,   2.03,    0.31,    0.403,   0.1937,   0.1937,   4.75,     1,        0.05,      0.05], 
                ['G3359-4',  '3359', 1200.00,  0,     766.3424,  1,     3,   0,   2.13,   2.03,    0.31,    0.403,   0.1937,   0.1937,   4.75,     1,        0.05,      0.05],
                ['G3359-5',  '3359', 1200.00,  0,     766.3424,  1,     3,   0,   2.13,   2.03,    0.31,    0.403,   0.1937,   0.1937,   4.75,     1,        0.05,      0.05],
                ['G5120-1',  '5120', 1500.00,  0,     964.5,     1,     3,   0,   1.1332, 0.68315, 0.24302, 0.68315, 0.15135,  0.15135,  4.9629,   1,        0.05,      0.15],
                ['G5120-2',  '5120', 1500.00,  0,     964.5,     1,     3,   0,   1.14,   0.84,    0.34,    0.84,    0.26,     0.26,     6.4,      1,        0.05,      0.15],
                ['G5230-1',  '5230', 1300.00,  0,     870,       1,     3,   0,   1.14,   0.84,    0.34,    0.84,    0.26,     0.26,     6.4,      1,        0.05,      0.15],
                ['G5230-2',  '5230', 1300.00,  0,     870,       1,     3,   0,   1.02,   0.63,    0.25,    0.63,    0.16,     0.16,     6.5,      1,        0.05,      0.15],
                ['G5240-1',  '5240', 1300.00,  0,     870,       1,     3,   0,   1.02,   0.63,    0.25,    0.63,    0.16,     0.16,     6.5,      1,        0.05,      0.15],
                ['G5240-2',  '5240', 1300.00,  0,     870,       1,     3,   0,   1.2364, 0.65567, 0.37415, 0.65567, 0.22825,  0.22825,  7.198,    1,        0.05,      0.15],
                ['G5240-3',  '5240', 1300.00,  0,     870,       1,     3,   0,   1,      0.51325, 0.38,    0.51325, 0.28,     0.28,     7.85,     1,        0.05,      0.15],
                ['G5250-1',  '5250', 1300.00,  0,     870,       1,     3,   0,   1,      0.51325, 0.38,    0.51325, 0.28,     0.28,     7.85,     1,        0.05,      0.15],
                ['G5310-1',  '5310', 1400.00,  0,     952.75,    1,     3,   0,   1.28,   0.94,    0.37,    0.94,    0.28,     0.28,     9.7,      1,        0.05,      0.15],
                ['G5320-1',  '5320', 1400.00,  0,     925.75,    1,     3,   0,   1.2,    0.73,    0.37,    0.73,    0.18,     0.18,     9.9,      1,        0.05,      0.15],
                ['G5320-2',  '5320', 1400.00,  0,     925.75,    1,     3,   0,   1.2,    0.73,    0.37,    0.73,    0.18,     0.18,     9.9,      1,        0.05,      0.15],
                ['G5320-3',  '5320', 1400.00,  0,     925.75,    1,     3,   0,   1.2,    0.73,    0.37,    0.73,    0.18,     0.18,     9.9,      1,        0.05,      0.15],
                ['G5420-1',  '5420', 1600.00,  0,     1050.67,   1,     3,   0,   1.2,    0.73,    0.37,    0.73,    0.18,     0.18,     9.9,      1,        0.05,      0.15],
                ['G5420-2',  '5420', 1600.00,  0,     1050.67,   1,     3,   0,   1.2,    0.73,    0.37,    0.73,    0.18,     0.18,     9.9,      1,        0.05,      0.15],
                ['G5420-3',  '5420', 1600.00,  0,     1050.67,   1,     3,   0,   1.0679, 0.642,   0.23865, 0.642,   0.15802,  0.15802,  5.4855,   1,        0.05,      0.15],
                ['G5510-1',  '5510', 1000.00,  0,     652.33,    1,     3,   0,   1.0679, 0.642,   0.23865, 0.642,   0.15802,  0.15802,  5.4855,   1,        0.05,      0.15],
                ['G5510-2',  '5510', 1000.00,  0,     652.33,    1,     3,   0,   1.0679, 0.642,   0.23865, 0.642,   0.15802,  0.15802,  5.4855,   1,        0.05,      0.15],
                ['G5520-1',  '5520', 1000.00,  0,     652.33,    1,     3,   0,   1.0679, 0.642,   0.23865, 0.642,   0.15802,  0.15802,  5.4855,   1,        0.05,      0.15],
                ['G5520-2',  '5520', 1000.00,  0,     652.33,    1,     3,   0,   1.1044, 0.66186, 0.25484, 0.66186, 0.17062,  0.17062,  5.24,     1,        0.05,      0.15],
                ['G5551-1',  '5551', 1000.00,  0,     652.33,    1,     3,   0,   1.1044, 0.66186, 0.25484, 0.66186, 0.17062,  0.17062,  5.24,     1,        0.05,      0.15],
                ['G5560-1',  '5560', 1000.00,  0,     652.33,    1,     3,   0,   1.1044, 0.66186, 0.25484, 0.66186, 0.17062,  0.17062,  5.24,     1,        0.05,      0.15],
                ['G7000-1',  '7000', 1200.00,  0,     788.1652,  1,     6,   0,   2.22,   2.13,    0.36,    0.468,   0.225,    0.225,    10,       1,        0.05,      0.05],
                ['G7000-2',  '7000', 1200.00,  0,     788.1652,  1,     6,   0,   2.22,   2.13,    0.36,    0.468,   0.225,    0.225,    10,       1,        0.05,      0.05],
                ['G7000-3',  '7000', 1200.00,  0,     788.1652,  1,     6,   0,   2.22,   2.13,    0.36,    0.468,   0.225,    0.225,    10,       1,        0.05,      0.05],
                ['G7000-4',  '7000', 1200.00,  0,     788.1652,  1,     6,   0,   2.22,   2.13,    0.36,    0.468,   0.225,    0.225,    10,       1,        0.05,      0.05],
                ['G7000-5',  '7000', 1200.00,  0,     788.1652,  1,     6,   0,   2.22,   2.13,    0.36,    0.468,   0.225,    0.225,    10,       1,        0.05,      0.05],
                ['G7000-6',  '7000', 1200.00,  0,     788.1652,  1,     6,   0,   2.22,   2.13,    0.36,    0.468,   0.225,    0.225,    10,       1,        0.05,      0.05],
                ['G7000-7',  '7000', 1200.00,  0,     788.1652,  1,     6,   0,   2.22,   2.13,    0.36,    0.468,   0.225,    0.225,    10,       1,        0.05,      0.05],
                ['G7100-1',  '7100', 900.00,   0,     634.9218,  1,     3,   0,   0.75,   0.5,     0.25,    0.5,     0.15385,  0.15385,  5,        1,        0.06,      0.1],
                ['G7100-2',  '7100', 900.00,   0,     634.9218,  1,     3,   0,   0.75,   0.5,     0.25,    0.5,     0.15385,  0.15385,  5,        1,        0.06,      0.1],
                ['G8500-1',  '8500', 1800.00,  0,     859,       1.02,  6,   0,   2.42,   2,       0.23,    0.4108,  0.17062,  0.17062,  10,       1,        0.06,      0.1],
            ]
        },

        'gov': {
            'HYGOV': [
                ['name',    'gen',     'R',   'r',  'T_f', 'T_r', 'T_g', 'A_t', 'T_w', 'q_nl', 'D_turb', 'G_min', 'V_elm', 'G_max', 'P_N'],
                ['HYGOV2',  'G3115-1', 0.06,  1.5,  0.05,  3.3,   0.2,   1,     1,     0.01,   0.01,    0,      100,    2,      0],
                ['HYGOV3',  'G3115-2', 0.06,  1.5,  0.05,  3.3,   0.2,   1,     1,     0.01,   0.01,    0,      100,    2,      0],
                ['HYGOV4',  'G3245-1', 0.06,  1.5,  0.05,  3.3,   0.2,   1,     1,     0.01,   0.01,    0,      100,    2,      0],
                ['HYGOV5',  'G3249-1', 0.06,  1.5,  0.05,  3.3,   0.2,   1,     1,     0.01,   0.01,    0,      100,    2,      0],
                ['HYGOV6',  'G3249-2', 0.06,  1.5,  0.05,  3.3,   0.2,   1,     1,     0.01,   0.01,    0,      100,    2,      0],
                ['HYGOV7',  'G5120-1', 0.06,  1.5,  0.05,  3.3,   0.2,   1,     1,     0.01,   0.01,    0,      100,    2,      0],
                ['HYGOV8',  'G5120-2', 0.06,  1.5,  0.05,  3.3,   0.2,   1,     1,     0.01,   0.01,    0,      100,    2,      0],
                ['HYGOV9',  'G5230-1', 0.06,  1.5,  0.05,  3.3,   0.2,   1,     1,     0.01,   0.01,    0,      100,    2,      0],
                ['HYGOV10', 'G5230-2', 0.06,  1.5,  0.05,  3.3,   0.2,   1,     1,     0.01,   0.01,    0,      100,    2,      0],
                ['HYGOV11', 'G5240-1', 0.06,  1.5,  0.05,  3.3,   0.2,   1,     1,     0.01,   0.01,    0,      100,    2,      0],
                ['HYGOV12', 'G5240-2', 0.06,  1.5,  0.05,  3.3,   0.2,   1,     1,     0.01,   0.01,    0,      100,    2,      0],
                ['HYGOV13', 'G5240-3', 0.06,  1.5,  0.05,  3.3,   0.2,   1,     1,     0.01,   0.01,    0,      100,    2,      0],
                ['HYGOV14', 'G5250-1', 0.06,  1.5,  0.05,  3.3,   0.2,   1,     1,     0.01,   0.01,    0,      100,    2,      0],
                ['HYGOV15', 'G5310-1', 0.06,  1.5,  0.05,  3.3,   0.2,   1,     1,     0.01,   0.01,    0,      100,    2,      0],
                ['HYGOV16', 'G5320-1', 0.06,  1.5,  0.05,  3.3,   0.2,   1,     1,     0.01,   0.01,    0,      100,    2,      0],
                ['HYGOV17', 'G5410-1', 0.06,  1.5,  0.05,  3.3,   0.2,   1,     1,     0.01,   0.01,    0,      100,    2,      0],
                ['HYGOV18', 'G5420-1', 0.06,  1.5,  0.05,  3.3,   0.2,   1,     1,     0.01,   0.01,    0,      100,    2,      0],
                ['HYGOV19', 'G5420-2', 0.06,  1.5,  0.05,  3.3,   0.2,   1,     1,     0.01,   0.01,    0,      100,    2,      0],
                ['HYGOV20', 'G5420-3', 0.06,  1.5,  0.05,  3.3,   0.2,   1,     1,     0.01,   0.01,    0,      100,    2,      0],
                ['HYGOV21', 'G5435-1', 0.06,  1.5,  0.05,  3.3,   0.2,   1,     1,     0.01,   0.01,    0,      100,    2,      0],
                ['HYGOV22', 'G5510-1', 0.06,  1.5,  0.05,  3.3,   0.2,   1,     1,     0.01,   0.01,    0,      100,    2,      0],
                ['HYGOV23', 'G5510-2', 0.06,  1.5,  0.05,  3.3,   0.2,   1,     1,     0.01,   0.01,    0,      100,    2,      0],
                ['HYGOV24', 'G5510-3', 0.06,  1.5,  0.05,  3.3,   0.2,   1,     1,     0.01,   0.01,    0,      100,    2,      0],
                ['HYGOV25', 'G5610-1', 0.06,  1.5,  0.05,  3.3,   0.2,   1,     1,     0.01,   0.01,    0,      100,    2,      0],
                ['HYGOV26', 'G5610-2', 0.06,  1.5,  0.05,  3.3,   0.2,   1,     1,     0.01,   0.01,    0,      100,    2,      0],
                ['HYGOV27', 'G5620-1', 0.06,  1.5,  0.05,  3.3,   0.2,   1,     1,     0.01,   0.01,    0,      100,    2,      0],
                ['HYGOV28', 'G7100-1', 0.06,  1.5,  0.05,  3.3,   0.2,   1,     1,     0.01,   0.01,    0,      100,    2,      0],
                ['HYGOV29', 'G7100-2', 0.06,  1.5,  0.05,  3.3,   0.2,   1,     1,     0.01,   0.01,    0,      100,    2,      0],
                ['HYGOV30', 'G3359-1', 0.06,  1.5,  0.05,  3.3,   0.2,   1,     1,     0.01,   0.01,    0,      100,    2,      0],
                ['HYGOV31', 'G3359-2', 0.06,  1.5,  0.05,  3.3,   0.2,   1,     1,     0.01,   0.01,    0,      100,    2,      0],
                ['HYGOV32', 'G3359-3', 0.06,  1.5,  0.05,  3.3,   0.2,   1,     1,     0.01,   0.01,    0,      100,    2,      0],
                ['HYGOV33', 'G3359-4', 0.06,  1.5,  0.05,  3.3,   0.2,   1,     1,     0.01,   0.01,    0,      100,    2,      0],
                ['HYGOV34', 'G3359-5', 0.06,  1.5,  0.05,  3.3,   0.2,   1,     1,     0.01,   0.01,    0,      100,    2,      0],
            ],

            'TGOV1': [
                ['name', 'gen', 'R', 'D_t', 'V_min', 'V_max', 'T_1', 'T_2', 'T_3'],
                ['GOV2', 'G3300-1', 0.35, 0.02, 0, 2, 0.1, 0.1, 0.3],
                ['GOV3', 'G3300-2', 0.35, 0.02, 0, 2, 0.1, 0.1, 0.3],
                ['GOV4', 'G3300-3', 0.35, 0.02, 0, 2, 0.1, 0.1, 0.3],
                ['GOV5', 'G7000-1', 0.35, 0.02, 0, 2, 0.1, 0.1, 0.3],
                ['GOV6', 'G7000-2', 0.35, 0.02, 0, 2, 0.1, 0.1, 0.3],
                ['GOV7', 'G7000-3', 0.35, 0.02, 0, 2, 0.1, 0.1, 0.3],
                ['GOV8', 'G7000-4', 0.35, 0.02, 0, 2, 0.1, 0.1, 0.3],
                ['GOV9', 'G7000-5', 0.35, 0.02, 0, 2, 0.1, 0.1, 0.3],
                ['GOV10', 'G7000-6', 0.35, 0.02, 0, 2, 0.1, 0.1, 0.3],
                ['GOV11', 'G7000-7', 0.35, 0.02, 0, 2, 0.1, 0.1, 0.3],
                ['GOV12', 'G8500-1', 0.35, 0.02, 0, 2, 0.1, 0.1, 0.3],
                ['GOV13', 'G3000-1', 0.35, 0.02, 0, 2, 0.1, 0.1, 0.3],
                ['GOV14', 'G3000-2', 0.35, 0.02, 0, 2, 0.1, 0.1, 0.3],
            ]
        },

        'avr': {
            'SEXS': [
                ['name', 'gen', 'K', 'T_a', 'T_b', 'T_e', 'E_min', 'E_max'],
                ['AVR2', 'G3115-1', 100, 0.5, 3.0, 0.1, -3, 6],
                ['AVR3', 'G3115-2', 100, 0.5, 3.0, 0.1, -3, 6],
                ['AVR4', 'G3245-1', 100, 0.5, 3.0, 0.1, -3, 6],
                ['AVR5', 'G3249-1', 100, 0.5, 3.0, 0.1, -3, 6],
                ['AVR6', 'G3249-2', 100, 0.5, 3.0, 0.1, -3, 6],
                ['AVR7', 'G5120-1', 100, 0.5, 3.0, 0.1, -3, 6],
                ['AVR8', 'G5120-2', 100, 0.5, 3.0, 0.1, -3, 6],
                ['AVR9', 'G5230-1', 100, 0.5, 3.0, 0.1, -3, 6],
                ['AVR10', 'G5230-2', 100, 0.5, 3.0, 0.1, -3, 6],
                ['AVR11', 'G5240-1', 100, 0.5, 3.0, 0.1, -3, 6],
                ['AVR12', 'G5240-2', 100, 0.5, 3.0, 0.1, -3, 6],
                ['AVR13', 'G5240-3', 100, 0.5, 3.0, 0.1, -3, 6],
                ['AVR14', 'G5250-1', 100, 0.5, 3.0, 0.1, -3, 6],
                ['AVR15', 'G5310-1', 100, 0.5, 3.0, 0.1, -3, 6],
                ['AVR16', 'G5320-1', 100, 0.5, 3.0, 0.1, -3, 6],
                ['AVR17', 'G5410-1', 100, 0.5, 3.0, 0.1, -3, 6],
                ['AVR18', 'G5420-1', 100, 0.5, 3.0, 0.1, -3, 6],
                ['AVR19', 'G5420-2', 100, 0.5, 3.0, 0.1, -3, 6],
                ['AVR20', 'G5420-3', 100, 0.5, 3.0, 0.1, -3, 6],
                ['AVR21', 'G5435-1', 100, 0.5, 3.0, 0.1, -3, 6],
                ['AVR22', 'G5510-1', 100, 0.5, 3.0, 0.1, -3, 6],
                ['AVR23', 'G5510-2', 100, 0.5, 3.0, 0.1, -3, 6],
                ['AVR24', 'G5510-3', 100, 0.5, 3.0, 0.1, -3, 6],
                ['AVR25', 'G5610-1', 100, 0.5, 3.0, 0.1, -3, 6],
                ['AVR26', 'G5610-2', 100, 0.5, 3.0, 0.1, -3, 6],
                ['AVR27', 'G5620-1', 100, 0.5, 3.0, 0.1, -3, 6],
                ['AVR28', 'G7100-1', 100, 0.5, 3.0, 0.1, -3, 6],
                ['AVR29', 'G7100-2', 100, 0.5, 3.0, 0.1, -3, 6],
                ['AVR30', 'G3300-1', 100, 0.5, 3.0, 0.1, -3, 6],
                ['AVR31', 'G3300-2', 100, 0.5, 3.0, 0.1, -3, 6],
                ['AVR32', 'G3300-3', 100, 0.5, 3.0, 0.1, -3, 6],
                ['AVR33', 'G3359-1', 100, 0.5, 3.0, 0.1, -3, 6],
                ['AVR34', 'G3359-2', 100, 0.5, 3.0, 0.1, -3, 6],
                ['AVR35', 'G3359-3', 100, 0.5, 3.0, 0.1, -3, 6],
                ['AVR36', 'G3359-4', 100, 0.5, 3.0, 0.1, -3, 6],
                ['AVR37', 'G3359-5', 100, 0.5, 3.0, 0.1, -3, 6],
                ['AVR38', 'G7000-1', 100, 0.5, 3.0, 0.1, -3, 6],
                ['AVR39', 'G7000-2', 100, 0.5, 3.0, 0.1, -3, 6],
                ['AVR40', 'G7000-3', 100, 0.5, 3.0, 0.1, -3, 6],
                ['AVR41', 'G7000-4', 100, 0.5, 3.0, 0.1, -3, 6],
                ['AVR42', 'G7000-5', 100, 0.5, 3.0, 0.1, -3, 6],
                ['AVR43', 'G7000-6', 100, 0.5, 3.0, 0.1, -3, 6],
                ['AVR44', 'G7000-7', 100, 0.5, 3.0, 0.1, -3, 6],
                ['AVR45', 'G8500-1', 100, 0.5, 3.0, 0.1, -3, 6],
            ]
        },
        'pss': {
            'STAB1': [
                ['name',    'gen',      'K',  'T',    'T_1',  'T_2',  'T_3',  'T_4',  'H_lim'],
        #         ['PSS2',    'G3115-1',   50,     10.0,   0.5,    0.5,    0.05,   0.05,   0.03],
        #         ['PSS3',    'G3115-2',   50,     10.0,   0.5,    0.5,    0.05,   0.05,   0.03],
        #         ['PSS4',    'G3245-1',   50,     10.0,   0.5,    0.5,    0.05,   0.05,   0.03],
        #         ['PSS5',    'G3249-1',   50,     10.0,   0.5,    0.5,    0.05,   0.05,   0.03],
        #         ['PSS6',    'G3249-2',   50,     10.0,   0.5,    0.5,    0.05,   0.05,   0.03],
        #         ['PSS7',    'G5120-1',   50,     10.0,   0.5,    0.5,    0.05,   0.05,   0.03],
        #         ['PSS8',    'G5120-2',   50,     10.0,   0.5,    0.5,    0.05,   0.05,   0.03],
        #         ['PSS9',    'G5230-1',   50,     10.0,   0.5,    0.5,    0.05,   0.05,   0.03],
        #         ['PSS10',   'G5230-2',   50,     10.0,   0.5,    0.5,    0.05,   0.05,   0.03],
        #         ['PSS11',   'G5240-1',   50,     10.0,   0.5,    0.5,    0.05,   0.05,   0.03],
        #         ['PSS12',   'G5240-2',   50,     10.0,   0.5,    0.5,    0.05,   0.05,   0.03],
        #         ['PSS13',   'G5240-3',   50,     10.0,   0.5,    0.5,    0.05,   0.05,   0.03],
        #         ['PSS14',   'G5250-1',   50,     10.0,   0.5,    0.5,    0.05,   0.05,   0.03],
        #         ['PSS15',   'G5310-1',   50,     10.0,   0.5,    0.5,    0.05,   0.05,   0.03],
        #         ['PSS16',   'G5320-1',   50,     10.0,   0.5,    0.5,    0.05,   0.05,   0.03],
        #         ['PSS17',   'G5410-1',   50,     10.0,   0.5,    0.5,    0.05,   0.05,   0.03],
        #         ['PSS18',   'G5420-1',   50,     10.0,   0.5,    0.5,    0.05,   0.05,   0.03],

                ['PSS19',   'G5420-2',   9.5,     1.4,   0.154,    0.033,    0.05,   0.05,   0.03],
                #['PSS19',   'G5420-2',   50,     10.0,   0.5,    0.5,    0.05,   0.05,   0.03],

        #         ['PSS20',   'G5420-3',   50,     10.0,   0.5,    0.5,    0.05,   0.05,   0.03],
        #         ['PSS21',   'G5435-1',   50,     10.0,   0.5,    0.5,    0.05,   0.05,   0.03],

                ['PSS22',   'G5510-1',   9.5,     1.4,   0.154,    0.033,    0.05,   0.05,   0.03],
                #['PSS22',   'G5510-1',   50,     10.0,   0.5,    0.5,    0.05,   0.05,   0.03],

        #         ['PSS23',   'G5510-2',   50,     10.0,   0.5,    0.5,    0.05,   0.05,   0.03],
        #         ['PSS24',   'G5510-3',   50,     10.0,   0.5,    0.5,    0.05,   0.05,   0.03],
        #         ['PSS25',   'G5610-1',   50,     10.0,   0.5,    0.5,    0.05,   0.05,   0.03],
        #         ['PSS26',   'G5610-2',   50,     10.0,   0.5,    0.5,    0.05,   0.05,   0.03],
        #         ['PSS27',   'G5620-1',   50,     10.0,   0.5,    0.5,    0.05,   0.05,   0.03],
        #         ['PSS28',   'G7100-1',   50,     10.0,   0.5,    0.5,    0.05,   0.05,   0.03],
        #         ['PSS29',   'G7100-2',   50,     10.0,   0.5,    0.5,    0.05,   0.05,   0.03],
        #         ['PSS30',   'G3300-1',   50,     10.0,   0.5,    0.5,    0.05,   0.05,   0.03],
        #         ['PSS31',   'G3300-2',   50,     10.0,   0.5,    0.5,    0.05,   0.05,   0.03],
        #         ['PSS32',   'G3300-3',   50,     10.0,   0.5,    0.5,    0.05,   0.05,   0.03],
        #         ['PSS33',   'G3359-1',   50,     10.0,   0.5,    0.5,    0.05,   0.05,   0.03],
        #         ['PSS34',   'G3359-2',   50,     10.0,   0.5,    0.5,    0.05,   0.05,   0.03],
        #         ['PSS35',   'G3359-3',   50,     10.0,   0.5,    0.5,    0.05,   0.05,   0.03],
        #         ['PSS36',   'G3359-4',   50,     10.0,   0.5,    0.5,    0.05,   0.05,   0.03],
        #         ['PSS37',   'G3359-5',   50,     10.0,   0.5,    0.5,    0.05,   0.05,   0.03],
        #         ['PSS38',   'G7000-1',   50,     10.0,   0.5,    0.5,    0.05,   0.05,   0.03],
        #         ['PSS39',   'G7000-2',   50,     10.0,   0.5,    0.5,    0.05,   0.05,   0.03],
        #         ['PSS40',   'G7000-3',   50,     10.0,   0.5,    0.5,    0.05,   0.05,   0.03],

                ['PSS41',   'G7000-4',   9.5,     1.4,   0.154,    0.033,    0.05,   0.05,   0.03],
                #['PSS41',   'G7000-4',   50,     10.0,   0.5,    0.5,    0.05,   0.05,   0.03],

        #         ['PSS42',   'G7000-5',   50,     10.0,   0.5,    0.5,    0.05,   0.05,   0.03],
        #         ['PSS43',   'G7000-6',   50,     10.0,   0.5,    0.5,    0.05,   0.05,   0.03],
        #         ['PSS44',   'G7000-7',   50,     10.0,   0.5,    0.5,    0.05,   0.05,   0.03],
        #         ['PSS45',   'G8500-1',   50,     10.0,   0.5,    0.5,    0.05,   0.05,   0.03],
            ]
        },
        'vsc': {
            'VSC_SI': [
                ['name',    'bus',    'S_n',   'p_ref',     'q_ref',    'k_p',   'k_q',   'T_p',   'T_q',     'k_pll',    'T_pll',     'T_i',    'i_max',   'K_SI',             'T_rocof', 'P_SI_max'],
                ['NO_2-GB', '5240',    1400,     1,        0.036,       1,      1,        0.05,     0.05,         5,          0.1,         0.01,      1.2,        0,        0.1,       1.2],
                ['NO_2-DE', '5230',    1400,     0.5,         0,           1,      1,        0.05,     0.05,         5,          0.1,         0.01,      1.2,        0,        0.1,       1.2],
                ['SE_4-LT', '8700',    700,      0.2,         0,           1,      1,        0.05,     0.05,         5,          0.1,         0.01,      1.2,        0,        0.1,       1.2],
                ['FI-EE',   '7020',    650,      0.79,        0,           1,      1,        0.05,     0.05,         5,          0.1,         0.01,      1.2,        0,        0.1,       1.2],
            ]   
        },
    }
