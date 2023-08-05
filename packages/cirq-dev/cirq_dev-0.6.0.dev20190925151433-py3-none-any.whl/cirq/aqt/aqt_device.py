"""Current device parameters for the AQT/UIBK ion trap device

The device is based on a linear calcium ion string with
arbitrary connectivity. For more information see:

https://quantumoptics.at/en/publications/journal-articles.html

https://iopscience.iop.org/article/10.1088/1367-2630/15/12/123012/meta

The native gate set consists of the local gates: X,Y, and XX entangling gates

"""
import json
from typing import Union, Tuple, List, Sequence, cast
import numpy as np
from cirq import ops, devices, study
from cirq import Circuit, LineQubit, IonDevice, Duration
from cirq import DensityMatrixSimulator

gate_dict = {'X': ops.X, 'Y': ops.Y, 'MS': ops.XX}


def get_op_string(op_obj: ops.Operation):
    """Find the string representation for a given gate
    Params:
        op_obj: Gate object, out of: XXPowGate, XPowGate, YPowGate"""
    if isinstance(op_obj, ops.XXPowGate) or ops.op_gate_of_type(
            op_obj, ops.XXPowGate):
        op_str = 'MS'
    elif isinstance(op_obj, ops.XPowGate) or ops.op_gate_of_type(
            op_obj, ops.XPowGate):
        op_str = 'X'
    elif isinstance(op_obj, ops.YPowGate) or ops.op_gate_of_type(
            op_obj, ops.YPowGate):
        op_str = 'Y'
    elif isinstance(op_obj, ops.MeasurementGate) or ops.op_gate_of_type(
            op_obj, ops.MeasurementGate):
        op_str = 'Meas'
    else:
        raise ValueError('Got unknown gate:', op_obj)
    return op_str


class AQTNoiseModel(devices.NoiseModel):
    """A noise model for the AQT ion trap """

    def __init__(self):
        self.noise_op_dict = get_default_noise_dict()

    def noisy_moment(self, moment: ops.Moment,
                     system_qubits: Sequence[ops.Qid]):
        noise_list = []
        for op in moment.operations:
            op_str = get_op_string(op)
            try:
                noise_op = self.noise_op_dict[op_str]
            except KeyError:
                break
            for qubit in op.qubits:
                noise_list.append(noise_op.on(qubit))
            noise_list += self.get_crosstalk_operation(op, system_qubits)
        return list(moment) + noise_list

    def get_crosstalk_operation(self, operation: ops.Operation,
                                system_qubits: Sequence[ops.Qid]):
        """
        Returns operation on
        Args:
            operation: Ideal operation
            system_qubits: Tuple of line qubits
        """
        cast(Tuple[LineQubit], system_qubits)
        num_qubits = len(system_qubits)
        xtlk_arr = np.zeros(num_qubits)
        for qubit in operation.qubits:
            idx = system_qubits.index(qubit)
            neighbors = [idx - 1, idx + 1]
            for neigh_idx in neighbors:
                if neigh_idx >= 0 and neigh_idx < num_qubits:
                    xtlk_arr[neigh_idx] = self.noise_op_dict['crosstalk']
        xtlk_op_list = []
        op_str = get_op_string(operation)
        if len(operation.qubits) == 1:
            for idx in xtlk_arr.nonzero()[0]:
                exponent = operation.gate.exponent  #type:ignore
                exponent = exponent * xtlk_arr[idx]
                xtlk_op = gate_dict[op_str].on(system_qubits[idx])**exponent
                xtlk_op_list.append(xtlk_op)
        #TODO: Add xtalk for 2 qubit operations
        return xtlk_op_list


class AQTSimulator:
    """A simulator for the AQT device."""

    def __init__(self,
                 num_qubits: int,
                 circuit: Circuit = Circuit(),
                 simulate_ideal: bool = False,
                 noise_dict: Union[dict, None] = None):
        """Initializes the AQT simulator
        Args:
            num_qubits: Number of qubits
            circuit: Optional, circuit to be simulated.
            Last moment needs to be a measurement over all qubits with key 'm'
            simulate_ideal: If True, an ideal circuit will be simulated
        """
        self.circuit = circuit
        self.num_qubits = num_qubits
        self.qubit_list = LineQubit.range(num_qubits)
        if noise_dict is None:
            noise_dict = get_default_noise_dict()
        self.noise_dict = noise_dict
        self.simulate_ideal = simulate_ideal

    def generate_circuit_from_list(self, json_string: str):
        """Generates a list of cirq operations from a json string
        Args:
            json_string: json that specifies the sequence
        """
        self.circuit = Circuit()
        # TODO add ion device here, is this still required?
        json_obj = json.loads(json_string)
        for gate_list in json_obj:
            gate = gate_list[0]
            angle = gate_list[1]
            qubits = [self.qubit_list[i] for i in gate_list[2]]
            self.circuit.append(gate_dict[gate].on(*qubits)**angle)
        # TODO: Better solution for measurement at the end
        self.circuit.append(
            ops.measure(*[qubit for qubit in self.qubit_list], key='m'))

    def simulate_samples(self, repetitions: int) -> study.TrialResult:
        """Samples the circuit
        Args:
            repetitions: Number of times the circuit is simulated
        Returns:
            TrialResult from Cirq.Simulator
        """
        if self.simulate_ideal:
            noise_model = devices.NO_NOISE
        else:
            noise_model = AQTNoiseModel()
        if self.circuit == Circuit():
            raise RuntimeError('simulate ideal called without a valid circuit')
        sim = DensityMatrixSimulator(noise=noise_model)
        result = sim.run(self.circuit, repetitions=repetitions)
        return result


def get_aqt_device(num_qubits: int) -> Tuple[IonDevice, List[LineQubit]]:
    """Returns an AQT ion device
    Args:
        num_qubits: number of qubits
    Returns:
         IonDevice, qubit_list
    """
    qubit_list = LineQubit.range(num_qubits)
    us = 1000 * Duration(nanos=1)
    ion_device = IonDevice(measurement_duration=100 * us,
                           twoq_gates_duration=200 * us,
                           oneq_gates_duration=10 * us,
                           qubits=qubit_list)
    return ion_device, qubit_list


def get_default_noise_dict():
    """Returns the current noise parameters"""
    default_noise_dict = {
        'X': ops.depolarize(1e-3),
        'Y': ops.depolarize(1e-3),
        'MS': ops.depolarize(1e-2),
        'crosstalk': 0.03
    }
    return default_noise_dict
