import qiskit
import numpy as np
from qiskit.providers.aer import QasmSimulator
from qiskit import QuantumCircuit, transpile
from qiskit.visualization import plot_histogram
from qiskit.tools.monitor import job_monitor
from azure.quantum.qiskit import AzureQuantumProvider

listaTeste = ["Hadamard", "PauliZ", "RX"]


def initialize(level):
    provider = AzureQuantumProvider(
    resource_id="/subscriptions/b1d7f7f8-743f-458e-b3a0-3e09734d716d/resourceGroups/aq-hackathons/providers/Microsoft.Quantum/Workspaces/aq-hackathon-01",
    location="East US"
    )
    #print([backend.name() for backend in provider.backends()])
    simulator = provider.get_backend("ionq.simulator")
    scoreCircuit = QuantumCircuit(level+2, level+2)
    playerCircuit = QuantumCircuit(1,1)

    quantumGateDict= {"Hadamard": playerCircuit.h , "PauliX": playerCircuit.x,
                "PauliY": playerCircuit.y, "PauliZ": playerCircuit.z,}

    quantumRotDict= {"RX": playerCircuit.rx, "RY":playerCircuit.ry, "RZ":playerCircuit.rz}

    return scoreCircuit, playerCircuit, quantumGateDict, quantumRotDict, simulator

def execute_measurement(qGates, simulator, playerCircuit, quantumRotDict, quantumGateDict, measurement):
    playerCircuit.reset(0)
    for gate in qGates:
        if gate in quantumGateDict:
            quantumGateDict[gate](0)
        if gate in quantumRotDict:
            quantumRotDict[gate](np.pi/2, 0)
    if measurement == "Z":
        playerCircuit.measure(0, 0)
    elif measurement == "Y":
        playerCircuit.h(0)
        playerCircuit.sdg(0)
        playerCircuit.h(0)
        playerCircuit.measure(0,0)
    else:
        playerCircuit.h(0)
        playerCircuit.h(0)
        playerCircuit.measure(0, 0)

    # compiled_circuit = transpile(playerCircuit, simulator)
    # job = simulator.run(compiled_circuit, shots = 100)
    # result = job.result()
    # counts = result.get_counts(playerCircuit)
    counts = {"0": 1, "1":2}
    if counts["0"] >= counts["1"]:
        return 0
    else:
        return 1

def Score_circuit(level, qGates, scoreCircuit):
    count = 0
    for gate in qGates:
        if gate == "CNOT":
            scoreCircuit.cnot(count, count +1)
            count = count +1
        else:
            scoreCircuit.h(count)
    if count+1 == level:
        return 1, scoreCircuit.draw(output = 'mpl')
    else:
        return 0, scoreCircuit.draw(output = 'mpl')                         

#scoreCircuit, playerCircuit, quantumGateDict, quantumRotDict, simulator = initialize()

#execute_measurement(listaTeste)
#playerCircuit.draw(output = 'mpl')
