import os

insts = [x.split('.')[0] for x in os.listdir('DATA') if x.endswith('.tsp')]

opt = {
    'Atlanta': 2003763,
    'Berlin': 7542,
    'Boston': 893536,
    'Champaign': 52643,
    'Cincinnati': 277952,
    'Denver': 100431,
    'NYC': 1555060,
    'Philadelphia': 1395981,
    'Roanoke': 655454,
    'SanFrancisco': 810196,
    'Toronto': 1176151,
    'UKansasState': 62962,
    'UMissouri': 132709
}
rep = 10
cutoff = '300'
for inst in insts:
    for alg in ('LS1', 'LS2', 'Approx'):
        total = 0
        time = 0
        for seed in range(rep):
            with open('output-2/{}_{}_{}_{}.sol'.format(inst, alg, cutoff, str(seed))) as f:
                total += int(f.readline().strip())
            with open('output-2/{}_{}_{}_{}.trace'.format(inst, alg, cutoff, str(seed))) as f:
                for line in f:
                    pass
                last_line = line
            time += float(last_line.split(',')[0])
        err = ((total / rep) - opt[inst]) / opt[inst]
        print(inst + ',' + alg + ',' + str('{:.2f}'.format(time / rep)) + ',' + str(total / rep) + ',' +
              str('{:.2f}'.format(err)))

    # sol = 0
    # time = 0
    # with open('output/{}_{}_{}.trace'.format(inst, 'BnB', '600')) as f:
    #     for line in f:
    #         pass
    #     last_line = line
    #     time = float(last_line.split(',')[0])
    # with open('output/{}_{}_{}.sol'.format(inst, 'BnB', '600')) as f:
    #     sol = int(f.readline().strip())
    #     print('BnB | ' + 'sol: ' + str(sol) + ' | time: ' +
    #           str('{:.2f}'.format(time)) + 's')
