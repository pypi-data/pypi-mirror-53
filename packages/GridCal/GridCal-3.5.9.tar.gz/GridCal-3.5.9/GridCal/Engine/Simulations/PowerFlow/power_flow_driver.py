# This file is part of GridCal.
#
# GridCal is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# GridCal is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with GridCal.  If not, see <http://www.gnu.org/licenses/>.

from enum import Enum
import numpy as np
from PySide2.QtCore import QRunnable


from GridCal.Engine.basic_structures import BusMode, BranchImpedanceMode
from GridCal.Engine.Simulations.PowerFlow.linearized_power_flow import dcpf, lacpf
from GridCal.Engine.Simulations.PowerFlow.helm_power_flow import helm
from GridCal.Engine.Simulations.PowerFlow.jacobian_based_power_flow import IwamotoNR
from GridCal.Engine.Simulations.PowerFlow.jacobian_based_power_flow import LevenbergMarquardtPF
from GridCal.Engine.Simulations.PowerFlow.jacobian_based_power_flow import NR_LS2, NR_I_LS
from GridCal.Engine.Simulations.PowerFlow.fast_decoupled_power_flow import FDPF
from GridCal.Engine.Simulations.PowerFlow.power_flow_results import PowerFlowResults
from GridCal.Engine.Core.calculation_inputs import CalculationInputs
from GridCal.Engine.Core.multi_circuit import MultiCircuit


class SolverType(Enum):
    """
    Refer to the :ref:`Power Flow section<power_flow>` for details about the different
    algorithms supported by **GridCal**.
    """

    NR = 'Newton Raphson'
    NRFD_XB = 'Fast decoupled XB'
    NRFD_BX = 'Fast decoupled BX'
    GAUSS = 'Gauss-Seidel'
    DC = 'Linear DC'
    HELM = 'Holomorphic Embedding'
    ZBUS = 'Z-Gauss-Seidel'
    IWAMOTO = 'Iwamoto-Newton-Raphson'
    CONTINUATION_NR = 'Continuation-Newton-Raphson'
    HELMZ = 'HELM-Z'
    LM = 'Levenberg-Marquardt'
    FASTDECOUPLED = 'Fast decoupled'
    LACPF = 'Linear AC'
    DC_OPF = 'Linear DC OPF'
    AC_OPF = 'Linear AC OPF'
    NRI = 'Newton-Raphson in current'
    DYCORS_OPF = 'DYCORS OPF'
    GA_OPF = 'Genetic Algorithm OPF'
    NELDER_MEAD_OPF = 'Nelder Mead OPF'


class ReactivePowerControlMode(Enum):
    """
    The :ref:`ReactivePowerControlMode<q_control>` offers 3 modes to control how
    :ref:`Generator<generator>` objects supply reactive power:

    **NoControl**: In this mode, the :ref:`generators<generator>` don't try to regulate
    the voltage at their :ref:`bus<bus>`.

    **Direct**: In this mode, the :ref:`generators<generator>` try to regulate the
    voltage at their :ref:`bus<bus>`. **GridCal** does so by applying the following
    algorithm in an outer control loop. For grids with numerous
    :ref:`generators<generator>` tied to the same system, for example wind farms, this
    control method sometimes fails with some :ref:`generators<generator>` not trying
    hard enough*. In this case, the simulation converges but the voltage controlled
    :ref:`buses<bus>` do not reach their target voltage, while their
    :ref:`generator(s)<generator>` haven't reached their reactive power limit. In this
    case, the slower **Iterative** control mode may be used (see below).

        ON PV-PQ BUS TYPE SWITCHING LOGIC IN POWER FLOW COMPUTATION
        Jinquan Zhao

        1) Bus i is a PQ bus in the previous iteration and its
           reactive power was fixed at its lower limit:

            If its voltage magnitude Vi >= Viset, then

                it is still a PQ bus at current iteration and set Qi = Qimin .

                If Vi < Viset , then

                    compare Qi with the upper and lower limits.

                    If Qi >= Qimax , then
                        it is still a PQ bus but set Qi = Qimax .
                    If Qi <= Qimin , then
                        it is still a PQ bus and set Qi = Qimin .
                    If Qimin < Qi < Qi max , then
                        it is switched to PV bus, set Vinew = Viset.

        2) Bus i is a PQ bus in the previous iteration and
           its reactive power was fixed at its upper limit:

            If its voltage magnitude Vi <= Viset , then:
                bus i still a PQ bus and set Q i = Q i max.

                If Vi > Viset , then

                    Compare between Qi and its upper/lower limits

                    If Qi >= Qimax , then
                        it is still a PQ bus and set Q i = Qimax .
                    If Qi <= Qimin , then
                        it is still a PQ bus but let Qi = Qimin in current iteration.
                    If Qimin < Qi < Qimax , then
                        it is switched to PV bus and set Vinew = Viset

        3) Bus i is a PV bus in the previous iteration.

            Compare Q i with its upper and lower limits.

            If Qi >= Qimax , then
                it is switched to PQ and set Qi = Qimax .
            If Qi <= Qimin , then
                it is switched to PQ and set Qi = Qimin .
            If Qi min < Qi < Qimax , then
                it is still a PV bus.

    **Iterative**: As mentioned above, the **Direct** control mode may not yield
    satisfying results in some isolated cases. The **Direct** control mode tries to
    jump to the final solution in a single or few iterations, but in grids where a
    significant change in reactive power at one :ref:`generator<generator>` has a
    significant impact on other :ref:`generators<generator>`, additional iterations may
    be required to reach a satisfying solution.

    Instead of trying to jump to the final solution, the **Iterative** mode raises or
    lowers each :ref:`generator's<generator>` reactive power incrementally. The
    increment is determined using a logistic function based on the difference between
    the current :ref:`bus<bus>` voltage its target voltage. The steepness factor
    :code:`k` of the logistic function was determined through trial and error, with the
    intent of reducing the number of iterations while avoiding instability. Other
    values may be specified in :ref:`PowerFlowOptions<pf_options>`.

    The :math:`Q_{Increment}` in per unit is determined by:

    .. math::

        Q_{Increment} = 2 * \\left[\\frac{1}{1 + e^{-k|V_2 - V_1|}}-0.5\\right]

    Where:

        k = 30 (by default)

    """
    NoControl = "NoControl"
    Direct = "Direct"
    Iterative = "Iterative"


class TapsControlMode(Enum):
    """
    The :ref:`TapsControlMode<taps_control>` offers 3 modes to control how
    :ref:`transformers<transformer>`' :ref:`tap changer<tap_changer>` regulate
    voltage on their regulated :ref:`bus<bus>`:

    **NoControl**: In this mode, the :ref:`transformers<transformer>` don't try to
    regulate the voltage at their :ref:`bus<bus>`.

    **Direct**: In this mode, the :ref:`transformers<transformer>` try to regulate
    the voltage at their bus. **GridCal** does so by jumping straight to the tap that
    corresponds to the desired transformation ratio, or the highest or lowest tap if
    the desired ratio is outside of the tap range.

    This behavior may fail in certain cases, especially if both the
    :ref:`TapControlMode<taps_control>` and :ref:`ReactivePowerControlMode<q_control>`
    are set to **Direct**. In this case, the simulation converges but the voltage
    controlled :ref:`buses<bus>` do not reach their target voltage, while their
    :ref:`generator(s)<generator>` haven't reached their reactive power limit. When
    this happens, the slower **Iterative** control mode may be used (see below).

    **Iterative**: As mentioned above, the **Direct** control mode may not yield
    satisfying results in some isolated cases. The **Direct** control mode tries to
    jump to the final solution in a single or few iterations, but in grids where a
    significant change of tap at one :ref:`transformer<transformer>` has a
    significant impact on other :ref:`transformers<transformer>`, additional
    iterations may be required to reach a satisfying solution.

    Instead of trying to jump to the final solution, the **Iterative** mode raises or
    lowers each :ref:`transformer's<transformer>` tap incrementally.
    """

    NoControl = "NoControl"
    Direct = "Direct"
    Iterative = "Iterative"


#######################################################################################
# Power flow classes
#######################################################################################


class PowerFlowOptions:
    """
    Power flow options class; its object is used as an argument for the
    :ref:`PowerFlowMP<pf_mp>` constructor.

    Arguments:

        **solver_type** (:ref:`SolverType<solver_type>`, SolverType.NR): Solver type

        **retry_with_other_methods** (bool, True): Use a battery of methods to tackle
        the problem if the main solver fails

        **verbose** (bool, False): Print additional details in the logger

        **initialize_with_existing_solution** (bool, True): *To be detailed*

        **tolerance** (float, 1e-6): Solution tolerance for the power flow numerical methods

        **max_iter** (int, 25): Maximum number of iterations for the power flow
        numerical method

        **max_outer_loop_iter** (int, 100): Maximum number of iterations for the
        controls outer loop

        **control_q** (:ref:`ReactivePowerControlMode<q_control>`,
        ReactivePowerControlMode.NoControl): Control mode for the PV nodes reactive
        power limits

        **control_taps** (:ref:`TapsControlMode<taps_control>`,
        TapsControlMode.NoControl): Control mode for the transformer taps equipped with
        a voltage regulator (as part of the outer loop)

        **multi_core** (bool, False): Use multi-core processing? applicable for time series

        **dispatch_storage** (bool, False): Dispatch storage?

        **control_p** (bool, False): Control active power (optimization dispatch)

        **apply_temperature_correction** (bool, False): Apply the temperature
        correction to the resistance of the branches?

        **branch_impedance_tolerance_mode** (BranchImpedanceMode,
        BranchImpedanceMode.Specified): Type of modification of the branches impedance

        **q_steepness_factor** (float, 30): Steepness factor :math:`k` for the
        :ref:`ReactivePowerControlMode<q_control>` iterative control

        **distributed_slack** (bool, False): Applies the redistribution of the slack power proportionally
                                             among the controlled generators

        **ignore_single_node_islands** (bool, False): If True the islands of 1 node are ignored

        **correction_parameter** (float, 1e-4): parameter used to correct the "bad" iterations,
                                                should be be between 1e-4 ~ 0.5
    """

    def __init__(self,
                 solver_type: SolverType = SolverType.NR,
                 retry_with_other_methods=True,
                 verbose=False,
                 initialize_with_existing_solution=True,
                 tolerance=1e-6,
                 max_iter=25,
                 max_outer_loop_iter=100,
                 control_q=ReactivePowerControlMode.NoControl,
                 control_taps=TapsControlMode.NoControl,
                 multi_core=False,
                 dispatch_storage=False,
                 control_p=False,
                 apply_temperature_correction=False,
                 branch_impedance_tolerance_mode=BranchImpedanceMode.Specified,
                 q_steepness_factor=30,
                 distributed_slack=False,
                 ignore_single_node_islands=False,
                 correction_parameter=1e-4):

        self.solver_type = solver_type

        self.retry_with_other_methods = retry_with_other_methods

        self.tolerance = tolerance

        self.max_iter = max_iter

        self.max_outer_loop_iter = max_outer_loop_iter

        self.control_Q = control_q

        self.control_P = control_p

        self.verbose = verbose

        self.initialize_with_existing_solution = initialize_with_existing_solution

        self.multi_thread = multi_core

        self.dispatch_storage = dispatch_storage

        self.control_taps = control_taps

        self.apply_temperature_correction = apply_temperature_correction

        self.branch_impedance_tolerance_mode = branch_impedance_tolerance_mode

        self.q_steepness_factor = q_steepness_factor

        self.distributed_slack = distributed_slack

        self.ignore_single_node_islands = ignore_single_node_islands

        self.acceleration_parameter = correction_parameter


class PowerFlowMP:
    """
    Power flow without QT to use with multi processing.

    Arguments:

        **grid** (:ref:`MultiCircuit<multicircuit>`): Electrical grid to run the power
        flow in

        **options** (:ref:`PowerFlowOptions<pf_options>`): Power flow options to use
    """

    def __init__(self, grid: MultiCircuit, options: PowerFlowOptions, t=None):

        # Grid to run a power flow in
        self.grid = grid

        # Options to use
        self.options = options

        self.results = None

        self.last_V = None

        self.t = t

        self.logger = list()

        self.convergence_reports = list()

        self.__cancel__ = False

    @staticmethod
    def compile_types(Sbus, types=None, logger=list()):
        """
        Compile the types.
        """

        pq = np.where(types == BusMode.PQ.value[0])[0]
        pv = np.where(types == BusMode.PV.value[0])[0]
        ref = np.where(types == BusMode.REF.value[0])[0]
        sto = np.where(types == BusMode.STO_DISPATCH.value)[0]

        if len(ref) == 0:  # there is no slack!

            if len(pv) == 0:  # there are no pv neither -> blackout grid

                logger.append('There are no slack nodes selected')

            else:  # select the first PV generator as the slack

                mx = max(Sbus[pv])
                if mx > 0:
                    # find the generator that is injecting the most
                    i = np.where(Sbus == mx)[0][0]

                else:
                    # all the generators are injecting zero, pick the first pv
                    i = pv[0]

                # delete the selected pv bus from the pv list and put it in the slack list
                pv = np.delete(pv, np.where(pv == i)[0])
                ref = [i]
                # print('Setting bus', i, 'as slack')

            ref = np.ndarray.flatten(np.array(ref))
            types[ref] = BusMode.REF.value[0]
        else:
            pass  # no problem :)

        pqpv = np.r_[pq, pv]
        pqpv.sort()

        return ref, pq, pv, pqpv

    @staticmethod
    def solve(solver_type, V0, Sbus, Ibus, Ybus, Yseries, B1, B2, Bpqpv, Bref, pq, pv, ref, pqpv, tolerance, max_iter,
              acceleration_parameter=1e-5):
        """
        Run a power flow simulation using the selected method (no outer loop controls).

            **solver_type**:

            **V0**: Voltage solution vector

            **Sbus**: Power injections vector

            **Ibus**: Current injections vector

            **Ybus**: Admittance matrix

            **Yseries**: Series elements' Admittance matrix

            **B1**: B' for the fast decoupled method

            **B2**: B'' for the fast decoupled method

            **Bpqpv**: PQ-PV, PQ-PV submatrix of the susceptance matrix (used in the DC power flow)

            **Bref**: PQ-PV, Ref submatrix of the susceptance matrix (used in the DC power flow)

            **pq**: list of pq nodes

            **pv**: list of pv nodes

            **ref**: list of slack nodes

            **pqpv**: list of pq and pv nodes

            **tolerance**: power error tolerance

            **max_iter**: maximum iterations

        Returns:

            V0 (Voltage solution), converged (converged?), normF (error in power),
            Scalc (Computed bus power), iterations, elapsed
        """
        # type HELM
        if solver_type == SolverType.HELM:
            V0, converged, normF, Scalc, it, el = helm(Vbus=V0,
                                                       Sbus=Sbus,
                                                       Ybus=Ybus,
                                                       pq=pq,
                                                       pv=pv,
                                                       ref=ref,
                                                       pqpv=pqpv,
                                                       tol=tolerance,
                                                       max_coefficient_count=max_iter)

        # type DC
        elif solver_type == SolverType.DC:
            V0, converged, normF, Scalc, it, el = dcpf(Ybus=Ybus,
                                                       Bpqpv=Bpqpv,
                                                       Bref=Bref,
                                                       Sbus=Sbus,
                                                       Ibus=Ibus,
                                                       V0=V0,
                                                       ref=ref,
                                                       pvpq=pqpv,
                                                       pq=pq,
                                                       pv=pv)

        # LAC PF
        elif solver_type == SolverType.LACPF:

            V0, converged, normF, Scalc, it, el = lacpf(Y=Ybus,
                                                        Ys=Yseries,
                                                        S=Sbus,
                                                        I=Ibus,
                                                        Vset=V0,
                                                        pq=pq,
                                                        pv=pv)

        # Levenberg-Marquardt
        elif solver_type == SolverType.LM:
            V0, converged, normF, Scalc, it, el = LevenbergMarquardtPF(Ybus=Ybus,
                                                                       Sbus=Sbus,
                                                                       V0=V0,
                                                                       Ibus=Ibus,
                                                                       pv=pv,
                                                                       pq=pq,
                                                                       tol=tolerance,
                                                                       max_it=max_iter)

        # Fast decoupled
        elif solver_type == SolverType.FASTDECOUPLED:
            V0, converged, normF, Scalc, it, el = FDPF(Vbus=V0,
                                                       Sbus=Sbus,
                                                       Ibus=Ibus,
                                                       Ybus=Ybus,
                                                       B1=B1,
                                                       B2=B2,
                                                       pq=pq,
                                                       pv=pv,
                                                       pqpv=pqpv,
                                                       tol=tolerance,
                                                       max_it=max_iter)

        # Newton-Raphson
        elif solver_type == SolverType.NR:
            # Solve NR with the linear AC solution
            V0, converged, normF, Scalc, it, el = NR_LS2(Ybus=Ybus,
                                                         Sbus=Sbus,
                                                         V0=V0,
                                                         Ibus=Ibus,
                                                         pv=pv,
                                                         pq=pq,
                                                         tol=tolerance,
                                                         max_it=max_iter,
                                                         acceleration_parameter=acceleration_parameter)

        # Newton-Raphson-Iwamoto
        elif solver_type == SolverType.IWAMOTO:
            V0, converged, normF, Scalc, it, el = IwamotoNR(Ybus=Ybus,
                                                            Sbus=Sbus,
                                                            V0=V0,
                                                            Ibus=Ibus,
                                                            pv=pv,
                                                            pq=pq,
                                                            tol=tolerance,
                                                            max_it=max_iter,
                                                            robust=True)

        # Newton-Raphson in current equations
        elif solver_type == SolverType.NRI:
            # NR_I_LS(Ybus, Sbus_sp, V0, Ibus_sp, pv, pq, tol, max_it
            V0, converged, normF, Scalc, it, el = NR_I_LS(Ybus=Ybus,
                                                          Sbus_sp=Sbus,
                                                          V0=V0,
                                                          Ibus_sp=Ibus,
                                                          pv=pv,
                                                          pq=pq,
                                                          tol=tolerance,
                                                          max_it=max_iter)

        # for any other method, for now, do a LM
        else:
            V0, converged, \
            normF, Scalc, it, el = LevenbergMarquardtPF(Ybus=Ybus,
                                                        Sbus=Sbus,
                                                        V0=V0,
                                                        Ibus=Ibus,
                                                        pv=pv,
                                                        pq=pq,
                                                        tol=tolerance,
                                                        max_it=max_iter)

        return V0, converged, normF, Scalc, it, el

    def single_power_flow(self, circuit: CalculationInputs, solver_type: SolverType, voltage_solution, Sbus, Ibus,
                          t=None):
        """
        Run a power flow simulation for a single circuit using the selected outer loop
        controls. This method shouldn't be called directly.

        Arguments:

            **circuit**: CalculationInputs instance

            **solver_type**: type of power flow to use first

            **voltage_solution**: vector of initial voltages

            **Sbus**: vector of power injections

            **Ibus**: vector of current injections

            **Sinstalled**: vector of installed power per bus in MVA

            **t**: (optional) time step

        Return:

            PowerFlowResults instance
        """

        # get the original types and compile this class' own lists of node types for thread independence
        original_types = circuit.types.copy()
        ref, pq, pv, pqpv = self.compile_types(Sbus, original_types)

        # copy the tap positions
        tap_positions = circuit.tap_position.copy()

        tap_module = circuit.tap_mod.copy()

        # control flags
        any_q_control_issue = True
        any_tap_control_issue = True

        # outer loop max iterations
        control_max_iter = self.options.max_outer_loop_iter

        # The control iterations are either the number of tap_regulated transformers or 10, the larger of the two
        # if self.options.control_Q == ReactivePowerControlMode.Iterative:
        #     control_max_iter = 999  # TODO: Discuss what to do with these options
        # else:
        #     control_max_iter = 10
        #
        # # Alter the outer loop max iterations if the transformer tap control is active
        # for k in circuit.bus_to_regulated_idx:   # indices of the branches that are regulated at the bus "to"
        #     control_max_iter = max(control_max_iter, circuit.max_tap[k] + circuit.min_tap[k])

        inner_it = list()
        outer_it = 0
        elapsed = list()
        methods = list()
        converged_lst = list()
        errors = list()
        it = list()  # iterations
        el = list()  # elapsed

        # For the iterate_pv_control logic:
        Vset = voltage_solution.copy()  # Origin voltage set-points

        # this the "outer-loop"
        while (any_q_control_issue or any_tap_control_issue) and outer_it < control_max_iter:

            if len(circuit.ref) == 0:
                voltage_solution = np.zeros(len(Sbus), dtype=complex)
                normF = 0
                Scalc = Sbus.copy()
                any_q_control_issue = False
                converged = True
                self.logger.append('Not solving power flow because there is no slack bus')
            else:

                # run the power flow method that shall be run
                voltage_solution, converged, normF, Scalc, it, el = self.solve(solver_type=solver_type,
                                                                               V0=voltage_solution,
                                                                               Sbus=Sbus,
                                                                               Ibus=Ibus,
                                                                               Ybus=circuit.Ybus,
                                                                               Yseries=circuit.Yseries,
                                                                               B1=circuit.B1,
                                                                               B2=circuit.B2,
                                                                               Bpqpv=circuit.Bpqpv,
                                                                               Bref=circuit.Bref,
                                                                               pq=pq,
                                                                               pv=pv,
                                                                               ref=ref,
                                                                               pqpv=pqpv,
                                                                               tolerance=self.options.tolerance,
                                                                               max_iter=self.options.max_iter,
                                                                               acceleration_parameter=self.options.acceleration_parameter)
                if self.options.distributed_slack:
                    # Distribute the slack power
                    slack_power = Scalc[ref].real.sum()
                    installed_power = circuit.Sinstalled.sum()

                    if installed_power > 0.0:
                        delta = slack_power * circuit.Sinstalled / installed_power

                        # repeat power flow with the redistributed power
                        voltage_solution, converged, normF, Scalc, it2, el2 = self.solve(solver_type=solver_type,
                                                                                         V0=voltage_solution,
                                                                                         Sbus=Sbus + delta,
                                                                                         Ibus=Ibus,
                                                                                         Ybus=circuit.Ybus,
                                                                                         Yseries=circuit.Yseries,
                                                                                         B1=circuit.B1,
                                                                                         B2=circuit.B2,
                                                                                         Bpqpv=circuit.Bpqpv,
                                                                                         Bref=circuit.Bref,
                                                                                         pq=pq,
                                                                                         pv=pv,
                                                                                         ref=ref,
                                                                                         pqpv=pqpv,
                                                                                         tolerance=self.options.tolerance,
                                                                                         max_iter=self.options.max_iter,
                                                                                         acceleration_parameter=self.options.acceleration_parameter)
                        # increase the metrics with the second run numbers
                        it += it2
                        el += el2

                # record the method used
                methods.append(solver_type)

                if converged:

                    # Check controls
                    if self.options.control_Q == ReactivePowerControlMode.Direct:

                        voltage_solution, \
                        Qnew, \
                        types_new, \
                        any_q_control_issue = self.control_q_direct(V=voltage_solution,
                                                                    Vset=np.abs(voltage_solution),
                                                                    Q=Scalc.imag,
                                                                    Qmax=circuit.Qmax,
                                                                    Qmin=circuit.Qmin,
                                                                    types=circuit.types,
                                                                    original_types=original_types,
                                                                    verbose=self.options.verbose,
                                                                    )

                    elif self.options.control_Q == ReactivePowerControlMode.Iterative:

                        Qnew, \
                        types_new, \
                        any_q_control_issue = self.control_q_iterative(V=voltage_solution,
                                                                       Vset=Vset,
                                                                       Q=Scalc.imag,
                                                                       Qmax=circuit.Qmax,
                                                                       Qmin=circuit.Qmin,
                                                                       types=circuit.types,
                                                                       original_types=original_types,
                                                                       verbose=self.options.verbose,
                                                                       k=self.options.q_steepness_factor)

                    else:
                        # did not check Q limits
                        any_q_control_issue = False
                        types_new = circuit.types
                        Qnew = Scalc.imag

                    # Check the actions of the Q-control
                    if any_q_control_issue:
                        circuit.types = types_new
                        Sbus = Sbus.real + 1j * Qnew
                        ref, pq, pv, pqpv = self.compile_types(Sbus, types_new)
                    else:
                        if self.options.verbose:
                            print('Q controls Ok')

                    # control the transformer taps
                    stable = True
                    if self.options.control_taps == TapsControlMode.Direct:

                        stable, tap_module, \
                        tap_positions = self.control_taps_direct(voltage=voltage_solution,
                                                                 T=circuit.T,
                                                                 bus_to_regulated_idx=circuit.bus_to_regulated_idx,
                                                                 tap_position=tap_positions,
                                                                 tap_module=tap_module,
                                                                 min_tap=circuit.min_tap,
                                                                 max_tap=circuit.max_tap,
                                                                 tap_inc_reg_up=circuit.tap_inc_reg_up,
                                                                 tap_inc_reg_down=circuit.tap_inc_reg_down,
                                                                 vset=circuit.vset,
                                                                 verbose=self.options.verbose)

                    elif self.options.control_taps == TapsControlMode.Iterative:

                        stable, tap_module, \
                        tap_positions = self.control_taps_iterative(voltage=voltage_solution,
                                                                    T=circuit.T,
                                                                    bus_to_regulated_idx=circuit.bus_to_regulated_idx,
                                                                    tap_position=tap_positions,
                                                                    tap_module=tap_module,
                                                                    min_tap=circuit.min_tap,
                                                                    max_tap=circuit.max_tap,
                                                                    tap_inc_reg_up=circuit.tap_inc_reg_up,
                                                                    tap_inc_reg_down=circuit.tap_inc_reg_down,
                                                                    vset=circuit.vset,
                                                                    verbose=self.options.verbose)

                    if not stable:
                        # recompute the admittance matrices based on the tap changes
                        circuit.re_calc_admittance_matrices(tap_module)
                    any_tap_control_issue = not stable

                else:
                    any_q_control_issue = False
                    any_tap_control_issue = False

            # increment the inner iterations counter
            inner_it.append(it)

            # increment the outer control iterations counter
            outer_it += 1

            # add the time taken by the solver in this iteration
            elapsed.append(el)

            # append loop error
            errors.append(normF)

            # append converged
            converged_lst.append(bool(converged))

        if self.options.verbose:
            print("Stabilized in {} iteration(s) (outer control loop)".format(outer_it))

        # Compute the branches power and the slack buses power
        Sbranch, Ibranch, Vbranch, loading, losses, \
            flow_direction, Sbus = self.power_flow_post_process(calculation_inputs=circuit, V=voltage_solution, t=t)

        # voltage, Sbranch, loading, losses, error, converged, Qpv
        results = PowerFlowResults(Sbus=Sbus,
                                   voltage=voltage_solution,
                                   Sbranch=Sbranch,
                                   Ibranch=Ibranch,
                                   Vbranch=Vbranch,
                                   loading=loading,
                                   losses=losses,
                                   flow_direction=flow_direction,
                                   tap_module=tap_module,
                                   error=errors,
                                   converged=converged_lst,
                                   Qpv=Sbus.imag[pv],
                                   inner_it=inner_it,
                                   outer_it=outer_it,
                                   elapsed=elapsed,
                                   methods=methods)

        return results

    @staticmethod
    def get_q_increment(V1, V2, k):
        """
        Logistic function to get the Q increment gain using the difference
        between the current voltage (V1) and the target voltage (V2).

        The gain varies between 0 (at V1 = V2) and inf (at V2 - V1 = inf).

        The default steepness factor k was set through trial an error. Other values may
        be specified as a :ref:`PowerFlowOptions<pf_options>`.

        Arguments:

            **V1** (float): Current voltage

            **V2** (float): Target voltage

            **k** (float, 30): Steepness factor

        Returns:

            Q increment gain
        """

        return 2 * (1 / (1 + np.exp(-k * abs(V2 - V1))) - 0.5)

    def control_q_iterative(
        self,
        V,
        Vset,
        Q,
        Qmax,
        Qmin,
        types,
        original_types,
        verbose,
        k,
    ):

        """
        Change the buses type in order to control the generators reactive power using
        iterative changes in Q to reach Vset.

        Arguments:

            **V** (list): array of voltages (all buses)

            **Vset** (list): Array of set points (all buses)

            **Q** (list): Array of reactive power (all buses)

            **Qmin** (list): Array of minimal reactive power (all buses)

            **Qmax** (list): Array of maximal reactive power (all buses)

            **types** (list): Array of types (all buses)

            **original_types** (list): Types as originally intended (all buses)

            **verbose** (list): output messages via the console

            **k** (float, 30): Steepness factor

        Return:

            **Qnew** (list): New reactive power values

            **types_new** (list): Modified types array

            **any_control_issue** (bool): Was there any control issue?
        """

        if verbose:
            print('Q control logic (iterative)')

        n = len(V)
        Vm = abs(V)
        Qnew = Q.copy()
        types_new = types.copy()
        any_control_issue = False
        precision = 4
        inc_prec = int(1.5 * precision)
        #inc_prec = precision

        for i in range(n):

            if types[i] == BusMode.REF.value[0]:
                pass

            elif types[i] == BusMode.PQ.value[0] and original_types[i] == BusMode.PV.value[0]:

                gain = self.get_q_increment(Vm[i], abs(Vset[i]), k)

                if round(Vm[i], precision) < round(abs(Vset[i]), precision):
                    increment = round(abs(Qmax[i] - Q[i])*gain, inc_prec)

                    if increment > 0 and Q[i] + increment < Qmax[i]:
                        # I can push more VAr, so let's do so
                        Qnew[i] = Q[i] + increment
                        if verbose:
                            print("Bus {} gain = {} (V = {}, Vset = {})".format(i,
                                                                                round(gain, precision),
                                                                                round(Vm[i], precision),
                                                                                abs(Vset[i])))
                            print("Bus {} increment = {} (Q = {}, Qmax = {})".format(i,
                                                                                     round(increment, inc_prec),
                                                                                     round(Q[i], precision),
                                                                                     round(abs(Qmax[i]), precision),
                                                                                     )
                            )
                            print("Bus {} raising its Q from {} to {} (V = {}, Vset = {})".format(i,
                                                                                                  round(Q[i], precision),
                                                                                                  round(Qnew[i], precision),
                                                                                                  round(Vm[i], precision),
                                                                                                  abs(Vset[i]),
                                                                                                  )
                            )
                        any_control_issue = True

                    else:
                        if verbose:
                            print("Bus {} stable enough (inc = {}, Q = {}, Qmax = {}, V = {}, Vset = {})".format(i,
                                                                                                                 round(increment, inc_prec),
                                                                                                                 round(Q[i], precision),
                                                                                                                 round(abs(Qmax[i]), precision),
                                                                                                                 round(Vm[i], precision),
                                                                                                                 abs(Vset[i]),
                                                                                                                 )
                            )

                elif round(Vm[i], precision) > round(abs(Vset[i]), precision):
                    increment = round(abs(Qmin[i] - Q[i])*gain, inc_prec)

                    if increment > 0 and Q[i] - increment > Qmin[i]:
                        # I can pull more VAr, so let's do so
                        Qnew[i] = Q[i] - increment
                        if verbose:
                            print("Bus {} increment = {} (Q = {}, Qmin = {})".format(i,
                                                                                     round(increment, inc_prec),
                                                                                     round(Q[i], precision),
                                                                                     round(abs(Qmin[i]), precision),
                                                                                     )
                            )
                            print("Bus {} gain = {} (V = {}, Vset = {})".format(i,
                                                                                round(gain, precision),
                                                                                round(Vm[i], precision),
                                                                                abs(Vset[i]),
                                                                                )
                            )
                            print("Bus {} lowering its Q from {} to {} (V = {}, Vset = {})".format(i,
                                                                                                   round(Q[i], precision),
                                                                                                   round(Qnew[i], precision),
                                                                                                   round(Vm[i], precision),
                                                                                                   abs(Vset[i]),
                                                                                                   )
                            )
                        any_control_issue = True

                    else:
                        if verbose:
                            print("Bus {} stable enough (inc = {}, Q = {}, Qmin = {}, V = {}, Vset = {})".format(i,
                                                                                                                 round(increment, inc_prec),
                                                                                                                 round(Q[i], precision),
                                                                                                                 round(abs(Qmin[i]), precision),
                                                                                                                 round(Vm[i], precision),
                                                                                                                 abs(Vset[i]),
                                                                                                                 )
                            )

                else:
                    if verbose:
                        print("Bus {} stable (V = {}, Vset = {})".format(i,
                                                                         round(Vm[i], precision),
                                                                         abs(Vset[i]),
                                                                         )
                        )

            elif types[i] == BusMode.PV.value[0]:
                # If it's still in PV mode (first run), change it to PQ mode
                types_new[i] = BusMode.PQ.value[0]
                Qnew[i] = 0
                if verbose:
                    print("Bus {} switching to PQ control, with a Q of 0".format(i))
                any_control_issue = True

        return Qnew, types_new, any_control_issue

    @staticmethod
    def power_flow_post_process(calculation_inputs: CalculationInputs, V, only_power=False, t=None):
        """
        Compute the power flows trough the branches.

        Arguments:

            **calculation_inputs**: instance of Circuit

            **V**: Voltage solution array for the circuit buses

            **only_power**: compute only the power injection

        Returns:

            Sbranch (MVA), Ibranch (p.u.), loading (p.u.), losses (MVA), Sbus(MVA)
        """
        # Compute the slack and pv buses power
        Sbus = calculation_inputs.Sbus

        vd = calculation_inputs.ref
        pv = calculation_inputs.pv

        # power at the slack nodes
        Sbus[vd] = V[vd] * np.conj(calculation_inputs.Ybus[vd, :].dot(V))

        # Reactive power at the pv nodes
        P = Sbus[pv].real
        Q = (V[pv] * np.conj(calculation_inputs.Ybus[pv, :].dot(V))).imag
        Sbus[pv] = P + 1j * Q  # keep the original P injection and set the calculated reactive power

        if not only_power:
            # Branches current, loading, etc
            Vf = calculation_inputs.C_branch_bus_f * V
            Vt = calculation_inputs.C_branch_bus_t * V
            If = calculation_inputs.Yf * V
            It = calculation_inputs.Yt * V
            Sf = Vf * np.conj(If)
            St = Vt * np.conj(It)

            # Branch losses in MVA
            losses = (Sf + St) * calculation_inputs.Sbase

            flow_direction = Sf.real / np.abs(Sf + 1e-20)

            # branch voltage increment
            Vbranch = Vf - Vt

            # Branch current in p.u.
            Ibranch = np.maximum(If, It)

            # Branch power in MVA
            Sbranch = np.maximum(Sf, St) * calculation_inputs.Sbase

            # Branch loading in p.u.
            if t is None:
                loading = Sbranch / (calculation_inputs.branch_rates + 1e-9)
            else:
                loading = Sbranch / (calculation_inputs.branch_rates_prof[t, :] + 1e-9)

            return Sbranch, Ibranch, Vbranch, loading, losses, flow_direction, Sbus

        else:
            no_val = np.zeros(calculation_inputs.nbr, dtype=complex)
            flow_direction = np.ones(calculation_inputs.nbr, dtype=complex)
            return no_val, no_val, no_val, no_val, no_val, flow_direction, Sbus

    @staticmethod
    def control_q_direct(V, Vset, Q, Qmax, Qmin, types, original_types, verbose):
        """
        Change the buses type in order to control the generators reactive power.

        Arguments:

            **pq** (list): array of pq indices

            **pv** (list): array of pq indices

            **ref** (list): array of pq indices

            **V** (list): array of voltages (all buses)

            **Vset** (list): Array of set points (all buses)

            **Q** (list): Array of reactive power (all buses)

            **types** (list): Array of types (all buses)

            **original_types** (list): Types as originally intended (all buses)

            **verbose** (bool): output messages via the console

        Returns:

            **Vnew** (list): New voltage values

            **Qnew** (list): New reactive power values

            **types_new** (list): Modified types array

            **any_control_issue** (bool): Was there any control issue?

        ON PV-PQ BUS TYPE SWITCHING LOGIC IN POWER FLOW COMPUTATION
        Jinquan Zhao

        1) Bus i is a PQ bus in the previous iteration and its
           reactive power was fixed at its lower limit:

            If its voltage magnitude Vi ≥ Viset, then

                it is still a PQ bus at current iteration and set Qi = Qimin .

                If Vi < Viset , then

                    compare Qi with the upper and lower limits.

                    If Qi ≥ Qimax , then
                        it is still a PQ bus but set Qi = Qimax .
                    If Qi ≤ Qimin , then
                        it is still a PQ bus and set Qi = Qimin .
                    If Qimin < Qi < Qi max , then
                        it is switched to PV bus, set Vinew = Viset.

        2) Bus i is a PQ bus in the previous iteration and
           its reactive power was fixed at its upper limit:

            If its voltage magnitude Vi ≤ Viset , then:
                bus i still a PQ bus and set Q i = Q i max.

                If Vi > Viset , then

                    Compare between Qi and its upper/lower limits

                    If Qi ≥ Qimax , then
                        it is still a PQ bus and set Q i = Qimax .
                    If Qi ≤ Qimin , then
                        it is still a PQ bus but let Qi = Qimin in current iteration.
                    If Qimin < Qi < Qimax , then
                        it is switched to PV bus and set Vinew = Viset

        3) Bus i is a PV bus in the previous iteration.

            Compare Q i with its upper and lower limits.

            If Qi ≥ Qimax , then
                it is switched to PQ and set Qi = Qimax .
            If Qi ≤ Qimin , then
                it is switched to PQ and set Qi = Qimin .
            If Qi min < Qi < Qimax , then
                it is still a PV bus.
        """

        if verbose:
            print('Q control logic (fast)')

        n = len(V)
        Vm = abs(V)
        Qnew = Q.copy()
        Vnew = V.copy()
        types_new = types.copy()
        any_control_issue = False
        for i in range(n):

            if types[i] == BusMode.REF.value[0]:
                pass

            elif types[i] == BusMode.PQ.value[0] and original_types[i] == BusMode.PV.value[0]:

                if Vm[i] != Vset[i]:

                    if Q[i] >= Qmax[i]:  # it is still a PQ bus but set Qi = Qimax .
                        Qnew[i] = Qmax[i]

                    elif Q[i] <= Qmin[i]:  # it is still a PQ bus and set Qi = Qimin .
                        Qnew[i] = Qmin[i]

                    else:  # switch back to PV, set Vinew = Viset.
                        if verbose:
                            print('Bus', i, 'switched back to PV')
                        types_new[i] = BusMode.PV.value[0]
                        Vnew[i] = complex(Vset[i], 0)

                    any_control_issue = True

                else:
                    pass  # The voltages are equal

            elif types[i] == BusMode.PV.value[0]:

                if Q[i] >= Qmax[i]:  # it is switched to PQ and set Qi = Qimax .
                    if verbose:
                        print('Bus', i, 'switched to PQ: Q', Q[i], ' Qmax:', Qmax[i])
                    types_new[i] = BusMode.PQ.value[0]
                    Qnew[i] = Qmax[i]
                    any_control_issue = True

                elif Q[i] <= Qmin[i]:  # it is switched to PQ and set Qi = Qimin .
                    if verbose:
                        print('Bus', i, 'switched to PQ: Q', Q[i], ' Qmin:', Qmin[i])
                    types_new[i] = BusMode.PQ.value[0]
                    Qnew[i] = Qmin[i]
                    any_control_issue = True

                else:  # it is still a PV bus.
                    pass

            else:
                pass

        return Vnew, Qnew, types_new, any_control_issue

    @staticmethod
    def tap_up(tap, max_tap):
        """
        Go to the next upper tap position
        """
        if tap + 1 <= max_tap:
            return tap + 1
        else:
            return tap

    @staticmethod
    def tap_down(tap, min_tap):
        """
        Go to the next upper tap position
        """
        if tap - 1 >= min_tap:
            return tap - 1
        else:
            return tap

    def control_taps_iterative(self, voltage, T, bus_to_regulated_idx, tap_position, tap_module, min_tap, max_tap,
                              tap_inc_reg_up, tap_inc_reg_down, vset, verbose=False):
        """
        Change the taps and compute the continuous tap magnitude.

        Arguments:

            **voltage** (list): array of bus voltages solution

            **T** (list): array of indices of the "to" buses of each branch

            **bus_to_regulated_idx** (list): array with the indices of the branches that regulate the bus "to"

            **tap_position** (list): array of branch tap positions

            **tap_module** (list): array of branch tap modules

            **min_tap** (list): array of minimum tap positions

            **max_tap** (list): array of maximum tap positions

            **tap_inc_reg_up** (list): array of tap increment when regulating up

            **tap_inc_reg_down** (list): array of tap increment when regulating down

            **vset** (list): array of set voltages to control

        Returns:

            **stable** (bool): Is the system stable (i.e.: are controllers stable)?

            **tap_magnitude** (list): Tap module at each bus in per unit

            **tap_position** (list): Tap position at each bus
        """

        stable = True
        for i in bus_to_regulated_idx:  # traverse the indices of the branches that are regulated at the "to" bus

            j = T[i]  # get the index of the "to" bus of the branch "i"
            v = abs(voltage[j])
            if verbose:
                print("Bus", j, "regulated by branch", i, ": U =", round(v, 4), "pu, U_set =", vset[i])

            if tap_position[i] > 0:

                if vset[i] > v + tap_inc_reg_up[i] / 2:
                    if tap_position[i] == min_tap[i]:
                        if verbose:
                            print("Branch", i, ": Already at lowest tap (", tap_position[i], "), skipping")
                    else:
                        tap_position[i] = self.tap_down(tap_position[i], min_tap[i])
                        tap_module[i] = 1.0 + tap_position[i]*tap_inc_reg_up[i]
                        if verbose:
                            print("Branch", i, ": Lowering from tap ", tap_position[i])
                        stable = False

                elif vset[i] < v - tap_inc_reg_up[i] / 2:
                    if tap_position[i] == max_tap[i]:
                        if verbose:
                            print("Branch", i, ": Already at highest tap (", tap_position[i], "), skipping")
                    else:
                        tap_position[i] = self.tap_up(tap_position[i], max_tap[i])
                        tap_module[i] = 1.0 + tap_position[i]*tap_inc_reg_up[i]
                        if verbose:
                            print("Branch", i, ": Raising from tap ", tap_position[i])
                        stable = False

            elif tap_position[i] < 0:
                if vset[i] > v + tap_inc_reg_down[i]/2:
                    if tap_position[i] == min_tap[i]:
                        if verbose:
                            print("Branch", i, ": Already at lowest tap (", tap_position[i], "), skipping")
                    else:
                        tap_position[i] = self.tap_down(tap_position[i], min_tap[i])
                        tap_module[i] = 1.0 + tap_position[i]*tap_inc_reg_down[i]
                        if verbose:
                            print("Branch", i, ": Lowering from tap", tap_position[i])
                        stable = False

                elif vset[i] < v - tap_inc_reg_down[i]/2:
                    if tap_position[i] == max_tap[i]:
                        print("Branch", i, ": Already at highest tap (", tap_position[i], "), skipping")
                    else:
                        tap_position[i] = self.tap_up(tap_position[i], max_tap[i])
                        tap_module[i] = 1.0 + tap_position[i]*tap_inc_reg_down[i]
                        if verbose:
                            print("Branch", i, ": Raising from tap", tap_position[i])
                        stable = False

            else:
                if vset[i] > v + tap_inc_reg_up[i]/2:
                    if tap_position[i] == min_tap[i]:
                        if verbose:
                            print("Branch", i, ": Already at lowest tap (", tap_position[i], "), skipping")
                    else:
                        tap_position[i] = self.tap_down(tap_position[i], min_tap[i])
                        tap_module[i] = 1.0 + tap_position[i]*tap_inc_reg_down[i]
                        if verbose:
                            print("Branch", i, ": Lowering from tap ", tap_position[i])
                        stable = False

                elif vset[i] < v - tap_inc_reg_down[i] / 2:
                    if tap_position[i] == max_tap[i]:
                        if verbose:
                            print("Branch", i, ": Already at highest tap (", tap_position[i], "), skipping")
                    else:
                        tap_position[i] = self.tap_up(tap_position[i], max_tap[i])
                        tap_module[i] = 1.0 + tap_position[i]*tap_inc_reg_up[i]
                        if verbose:
                            print("Branch", i, ": Raising from tap ", tap_position[i])
                        stable = False

        return stable, tap_module, tap_position

    @staticmethod
    def control_taps_direct(voltage, T, bus_to_regulated_idx, tap_position, tap_module, min_tap, max_tap,
                           tap_inc_reg_up, tap_inc_reg_down, vset, verbose=False):
        """
        Change the taps and compute the continuous tap magnitude.

        Arguments:

            **voltage** (list): array of bus voltages solution

            **T** (list): array of indices of the "to" buses of each branch

            **bus_to_regulated_idx** (list): array with the indices of the branches
            that regulate the bus "to"

            **tap_position** (list): array of branch tap positions

            **tap_module** (list): array of branch tap modules

            **min_tap** (list): array of minimum tap positions

            **max_tap** (list): array of maximum tap positions

            **tap_inc_reg_up** (list): array of tap increment when regulating up

            **tap_inc_reg_down** (list): array of tap increment when regulating down

            **vset** (list): array of set voltages to control

        Returns:

            **stable** (bool): Is the system stable (i.e.: are controllers stable)?

            **tap_magnitude** (list): Tap module at each bus in per unit

            **tap_position** (list): Tap position at each bus
        """
        stable = True
        for i in bus_to_regulated_idx:  # traverse the indices of the branches that are regulated at the "to" bus

            j = T[i]  # get the index of the "to" bus of the branch "i"
            v = abs(voltage[j])
            if verbose:
                print("Bus", j, "regulated by branch", i, ": U=", round(v, 4), "pu, U_set=", vset[i])

            tap_inc = tap_inc_reg_up
            if tap_inc_reg_up.all() != tap_inc_reg_down.all():
                print("Error: tap_inc_reg_up and down are not equal for branch {}".format(i))

            desired_module = v / vset[i] * tap_module[i]
            desired_pos = round((desired_module - 1) / tap_inc[i])

            if desired_pos == tap_position[i]:
                continue

            elif desired_pos > 0 and desired_pos > max_tap[i]:
                if verbose:
                    print("Branch {}: Changing from tap {} to {} (module {} to {})".format(i,
                                                                                           tap_position[i],
                                                                                           max_tap[i],
                                                                                           tap_module[i],
                                                                                           1 + max_tap[i] * tap_inc[i]))
                tap_position[i] = max_tap[i]

            elif desired_pos < 0 and desired_pos < min_tap[i]:
                if verbose:
                    print("Branch {}: Changing from tap {} to {} (module {} to {})".format(i,
                                                                                           tap_position[i],
                                                                                           min_tap[i],
                                                                                           tap_module[i],
                                                                                           1 + min_tap[i] * tap_inc[i]))
                tap_position[i] = min_tap[i]

            else:
                if verbose:
                    print("Branch {}: Changing from tap {} to {} (module {} to {})".format(i,
                                                                                           tap_position[i],
                                                                                           desired_pos,
                                                                                           tap_module[i],
                                                                                           1 + desired_pos * tap_inc[i]))
                tap_position[i] = desired_pos

            tap_module[i] = 1 + tap_position[i] * tap_inc[i]
            stable = False

        return stable, tap_module, tap_position

    def run_pf(self, circuit: CalculationInputs, Vbus, Sbus, Ibus, t=None):
        """
        Run a power flow for a circuit. In most cases, the **run** method should be
        used instead.

        Arguments:

            **circuit** (:ref:`CalculationInputs<calculation_inputs>`): CalculationInputs instance

            **Vbus** (array): Initial voltage at each bus in complex per unit

            **Sbus** (array): Power injection at each bus in complex MVA

            **Ibus** (array): Current injection at each bus in complex MVA

            **t** (optional) time step index

        Returns:

            :ref:`PowerFlowResults<power_flow_results>` instance
        """

        # Retry with another solver

        if self.options.retry_with_other_methods:
            solvers = [self.options.solver_type,
                       SolverType.IWAMOTO,
                       # SolverType.FASTDECOUPLED,
                       SolverType.LM,
                       SolverType.LACPF]
        else:
            # No retry selected
            solvers = [self.options.solver_type]

        # set worked to false to enter in the loop
        worked = False
        solver_idx = 0
        methods = list()
        inner_it = list()
        elapsed = list()
        errors = list()
        converged_lst = list()
        outer_it = 0
        results = PowerFlowResults()

        while solver_idx < len(solvers) and not worked:

            # get the solver
            solver = solvers[solver_idx]

            # set the initial voltage
            V0 = Vbus.copy()

            # solve the power flow
            results = self.single_power_flow(circuit=circuit,
                                             solver_type=solver,
                                             voltage_solution=V0,
                                             Sbus=Sbus,
                                             Ibus=Ibus,
                                             t=t)

            # did it worked?
            worked = np.all(results.converged)

            # record the solver steps
            methods += results.methods
            inner_it += results.inner_iterations
            outer_it += results.outer_iterations
            elapsed += results.elapsed
            errors += results.error
            converged_lst += results.converged

            solver_idx += 1

        if not worked:
            self.logger.append('Did not converge, even after retry!, Error:' + str(results.error))
            return results

        else:
            # set the total process variables:
            results.methods = methods
            results.inner_iterations = inner_it
            results.outer_iterations = outer_it
            results.elapsed = elapsed
            results.error = errors
            results.converged = converged_lst

            # check the power flow limits
            results.check_limits(F=circuit.F, T=circuit.T,
                                 Vmax=circuit.Vmax, Vmin=circuit.Vmin,
                                 wo=1, wv1=1, wv2=1)

            return results

    def run_multi_island(self, calculation_inputs, Vbus, Sbus, Ibus):
        """
        Power flow execution for optimization purposes.

        Arguments:

            **calculation_inputs**:

            **Vbus**:

            **Sbus**:

            **Ibus**:

        Returns:

            PowerFlowResults instance

        """
        n = len(self.grid.buses)
        m = len(self.grid.branches)
        results = PowerFlowResults()
        results.initialize(n, m)

        if len(calculation_inputs) > 1:

            # simulate each island and merge the results
            for i, calculation_input in enumerate(calculation_inputs):

                if len(calculation_input.ref) > 0:

                    bus_original_idx = calculation_input.original_bus_idx
                    branch_original_idx = calculation_input.original_branch_idx

                    # run circuit power flow
                    res = self.run_pf(calculation_input,
                                      Vbus[bus_original_idx],
                                      Sbus[bus_original_idx],
                                      Ibus[bus_original_idx])

                    # merge the results from this island
                    results.apply_from_island(res, bus_original_idx, branch_original_idx)

                else:
                    self.logger.append('There are no slack nodes in the island ' + str(i))
        else:

            # run circuit power flow
            results = self.run_pf(calculation_inputs[0], Vbus, Sbus, Ibus)

        return results

    def run(self):
        """
        Run a power flow for a circuit (wrapper for run_pf).

        Returns:

            :ref:`PowerFlowResults<pf_results>` instance (self.results)
        """

        # print('PowerFlow at ', self.grid.name)
        n = len(self.grid.buses)
        m = len(self.grid.branches)
        results = PowerFlowResults()
        results.initialize(n, m)
        # self.progress_signal.emit(0.0)

        # columns of the report
        self.convergence_reports.clear()

        # print('Compiling...', end='')
        numerical_circuit = self.grid.compile()
        calculation_inputs = numerical_circuit.compute(apply_temperature=self.options.apply_temperature_correction,
                                                       branch_tolerance_mode=self.options.branch_impedance_tolerance_mode,
                                                       ignore_single_node_islands=self.options.ignore_single_node_islands)

        results.bus_types = numerical_circuit.bus_types

        if len(calculation_inputs) > 1:

            # simulate each island and merge the results
            for i, calculation_input in enumerate(calculation_inputs):

                if len(calculation_input.ref) > 0:
                    Vbus = calculation_input.Vbus
                    Sbus = calculation_input.Sbus
                    Ibus = calculation_input.Ibus

                    # run circuit power flow
                    res = self.run_pf(calculation_input, Vbus, Sbus, Ibus, t=self.t)

                    bus_original_idx = calculation_input.original_bus_idx
                    branch_original_idx = calculation_input.original_branch_idx

                    # merge the results from this island
                    results.apply_from_island(res, bus_original_idx, branch_original_idx)

                    # # build the report
                    self.convergence_reports.append(res.get_report_dataframe())
                else:
                    self.logger.append('There are no slack nodes in the island ' + str(i))
        else:

            if len(calculation_inputs[0].ref) > 0:
                # only one island
                Vbus = calculation_inputs[0].Vbus
                Sbus = calculation_inputs[0].Sbus
                Ibus = calculation_inputs[0].Ibus

                # run circuit power flow
                results = self.run_pf(calculation_inputs[0], Vbus, Sbus, Ibus, t=self.t)

                # build the report
                self.convergence_reports.append(results.get_report_dataframe())
            else:
                self.logger.append('There are no slack nodes')

        # check the limits
        results.check_limits(F=numerical_circuit.F, T=numerical_circuit.T,
                             Vmax=numerical_circuit.Vmax, Vmin=numerical_circuit.Vmin,
                             wo=1, wv1=1, wv2=1)

        self.results = results

        return self.results

    def cancel(self):
        self.__cancel__ = True


def power_flow_worker(t, options: PowerFlowOptions, circuit: CalculationInputs, Vbus, Sbus, Ibus, return_dict):
    """
    Power flow worker to schedule parallel power flows
        **t: execution index
        **options: power flow options
        **circuit: circuit
        **Vbus: Voltages to initialize
        **Sbus: Power injections
        **Ibus: Current injections
        **return_dict: parallel module dictionary in wich to return the values
    :return:
    """

    instance = PowerFlowMP(None, options, t=t)
    return_dict[t] = instance.run_pf(circuit, Vbus, Sbus, Ibus)


def power_flow_worker_args(args):
    """
    Power flow worker to schedule parallel power flows

    args -> t, options: PowerFlowOptions, circuit: Circuit, Vbus, Sbus, Ibus, return_dict


        **t: execution index
        **options: power flow options
        **circuit: circuit
        **Vbus: Voltages to initialize
        **Sbus: Power injections
        **Ibus: Current injections
        **return_dict: parallel module dictionary in wich to return the values
    :return:
    """
    t, options, circuit, Vbus, Sbus, Ibus, return_dict = args
    instance = PowerFlowMP(None, options)
    return_dict[t] = instance.run_pf(circuit, Vbus, Sbus, Ibus)


class PowerFlow(QRunnable):
    """
    Power flow wrapper to use with Qt
    """

    def __init__(self, grid: MultiCircuit, options: PowerFlowOptions):
        """
        PowerFlow class constructor
        **grid: MultiCircuit Object
        """
        QRunnable.__init__(self)

        # Grid to run a power flow in
        self.grid = grid

        # Options to use
        self.options = options

        self.results = PowerFlowResults()

        self.pf = PowerFlowMP(grid, options)

        self.__cancel__ = False

    @staticmethod
    def get_steps():
        return list()

    def run(self):
        """
        Pack run_pf for the QThread
        """

        results = self.pf.run()
        self.results = results

    def run_pf(self, circuit: CalculationInputs, Vbus, Sbus, Ibus):
        """
        Run a power flow for every circuit
        @return:
        """

        return self.pf.run_pf(circuit, Vbus, Sbus, Ibus)

    def cancel(self):
        self.__cancel__ = True

