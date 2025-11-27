from math import comb, ceil
import numpy as np
import matplotlib.pyplot as plotter; plotter.rcParams['font.family'] = 'Monospace'
import cirq, stimcirq
# from myMWPM import MWPMDecoder1D

#ENCODER PROCEDURE
def create_repetition_code_encoder(n_qubits):

    qubits = cirq.LineQubit.range(n_qubits)
    circuit = cirq.Circuit()
    
    # The first qubit holds the quantum state
    for i in range(1, n_qubits):
        circuit.append(cirq.CNOT(qubits[0], qubits[i]))

    return circuit

encoder_3 = create_repetition_code_encoder(3)
print("3-qubit repetition code encoder:")
print(encoder_3)

#SYNDROME PROCEDURE
def get_syndrome_measurement(qubits, syndrome_qubits):

    # For each pair of adjacent qubits, measure the ZiZi+1 stabilizer
    syndrome_measurement = []
        
    for i in range(len(qubits) - 1):
        # Extract the parity of qubits i and i+1 onto syndrome qubit i
        syndrome_measurement.append(cirq.CNOT(qubits[i], syndrome_qubits[i]))
        syndrome_measurement.append(cirq.CNOT(qubits[i+1], syndrome_qubits[i]))
    
    # Measure the syndrome qubits to extract the syndrome
    syndrome_measurement.append(cirq.measure(*syndrome_qubits, key='syndrome'))
    
    return syndrome_measurement

#FULL REPETIION CODE CIRCUIT
def create_full_repetition_code_circuit(n_qubits, error_probability, error_gate = cirq.X, logical_state = '0'):

    # Create qubits: data qubits for encoding, syndrome qubits for syndrome measurement
    data_qubits = cirq.LineQubit.range(n_qubits)
    syndrome_qubits = cirq.LineQubit.range(n_qubits, 2*n_qubits - 1)
    
    circuit = cirq.Circuit()

    # Step 0: Decide what quantum state we are protecting. It's either 0 or 1. Then encode it
    encoding_circuit = create_repetition_code_encoder(n_qubits)

    # logical state |0>_L = |0000...>
    # do nothing, since all data qubits start reset at |0>.
    if logical_state == '0':
        pass
        
    # logical state |1>_L = |1111...>
    # apply X gate on all data qubits since they all start reset at |0>
    if logical_state == '1':
        circuit.append(
            cirq.Moment(cirq.X(data_qubits[0]))
                       )
    
    circuit += encoding_circuit    
    
    # Step 1: Simulate noise with a Pauli error error_type occurring with probability error_probability
    circuit.append(
        cirq.Moment([
        error_gate(qubit).with_probability(error_probability) for qubit in data_qubits
                    ])
                   )
            
    # Step 2: Measure error syndrome
    circuit += get_syndrome_measurement(data_qubits, syndrome_qubits)

    # Step 3: Measure data qubits
    # we will use it to predict the initial state by correcting the final state using the syndrome data
    # When we can't predict successfully, that's a logical error
    circuit.append(cirq.measure(*data_qubits, key='data_qubits'))
    
    return circuit

# bit-flip repetition code with 3 qubits and 2% probability of error
full_circuit = create_full_repetition_code_circuit(3, 0.02)
print(full_circuit)
