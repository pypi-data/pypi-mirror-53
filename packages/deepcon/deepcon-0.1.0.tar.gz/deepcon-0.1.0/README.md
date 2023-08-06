# deepcon-package
Python package for the DEEPCON contact prediction tool at https://github.com/ba-lab/DEEPCON

#### Contact:
Email: adhikarib@umsl.edu  
Homepage: https://badriadhikari.github.io/  
Paper: https://www.biorxiv.org/content/10.1101/590455v1 

### DEEPCON using Covariance features as input

Trained and validated using the 3456 proteins in the DeepCov dataset with the covariance features (441 channels) as input.


#### Installation Instructions:

Install DEEPCON-Covariance package
	
    pip3 install deepcon


#### Intstructions for User:

Inside Python:

	>>>import deepcon
	>>>from deepcon import deepconcovariance
	

#### Predict
```bash
>>>deepconcovariance.main("input.aln","output.rr")
```

#### Evaluate
```bash
...
```
