import unittest

import numpy as np

from pymoo.algorithms.moo.rvea import APDSurvival, RVEA
from pymoo.factory import DTLZ2
from pymoo.model.population import Population
from tests import path_to_test_resources


class RVEATest(unittest.TestCase):

    def test_survival(self):
        problem = DTLZ2(n_obj=3)

        for k in range(1, 11):

            print("TEST RVEA GEN", k)

            ref_dirs = np.loadtxt(path_to_test_resources('rvea', f"ref_dirs_{k}.txt"))
            F = np.loadtxt(path_to_test_resources('rvea', f"F_{k}.txt"))
            pop = Population.new(F=F)

            algorithm = RVEA(ref_dirs)
            algorithm.setup(problem, termination=('n_gen', 500))
            algorithm.n_gen = k
            algorithm.pop = pop

            survival = APDSurvival(ref_dirs)
            survivors = survival.do(problem, algorithm.pop, len(pop), algorithm=algorithm, return_indices=True)

            apd = pop[survivors].get("apd")
            correct_apd = np.loadtxt(path_to_test_resources('rvea', f"apd_{k}.txt"))
            np.testing.assert_allclose(apd, correct_apd)


if __name__ == '__main__':
    unittest.main()