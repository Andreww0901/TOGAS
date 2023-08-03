# TOGAS

---

#### T-Count Optimised Genetic Algorithm for State-Preparation

- Random state preperation using genetic algorithms
- Optimised for T-Count

Execute from GUI.py

Note: 

 - If simulating using noise, you will need an IBM Quantum account. 

 - Take the API key from your account and add it in ```__main__.py``` towards the top using: ```IBMProvider.save_account(token=MY_API_TOKEN)``` where ```MY_API_TOKEN``` is replaced with the token in your IBM Quantum account. 

 - You will only need to do this in one execution - from then on, that line can be removed.

 - For more detail see: https://qiskit.org/ecosystem/ibm-provider/tutorials/Migration_Guide_from_qiskit-ibmq-provider.html
