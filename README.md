This tracks the steps to use dismod-mr

install conda using the conda-forge script in the folder

remove the constraints in /etc/pip/constraint.txt file if needed.

https://github.com/ihmeuw/dismod_mr

```
conda create --name=dismod_mr python=3.6 pymc==2.3.8
conda activate dismod_mr
pip install dismod_mr
```

Now let's fit the data

