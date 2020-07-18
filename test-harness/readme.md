###Install instructions

If the bundled maven is not working, write in 
_Settings => Build, Execution and Deployment => Build Tools => Maven => Maven Home Directory_
the output of command _which maven_, as explained in
https://stackoverflow.com/questions/44796833/command-line-mvn-compile-but-not-intellij

Python environment for Python Jupyter notebook _scripts/experiments_processing.ipynb_:

conda create -n java_experiments python=3.7.7 jupyter=1.0.0 pandas=0.24.2 numpy=1.16.4 matplotlib=3.1.3