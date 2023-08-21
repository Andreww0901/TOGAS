# TOGAS

---

#### T-Count Optimising Genetic Algorithm for State-Preparation

- Random state preperation using genetic algorithms
- Optimised for T-Count (Can be more generally applied to different types of quantum computer instead of just IBM Quantum systems)

**Execute from GUI.py**

Note: 

 - If simulating using noise, you will need an IBM Quantum account. 

 - In ```MainGUI.py``` uncomment: ```IBMProvider.save_account(token="MY_API_TOKEN", overwrite=True)``` (*Line 13*) and replace ```MY_API_TOKEN``` with the token in your IBM Quantum account. 

 - You will only need to do this for one execution - from then on, that line can be removed/commented out again.

 - Noise simulation is very slow and utilises the current noise model from the 7 Qubit IBM Lagos Quantum computer. If using more than 7 Qubits, the program will crash.

 - For more detail on adding your IBMQ Token, see the quick start guide from Qiskit: https://qiskit.org/ecosystem/ibm-provider/tutorials/Migration_Guide_from_qiskit-ibmq-provider.html