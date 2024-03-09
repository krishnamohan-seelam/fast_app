### How to build in dev mode
#### Create pyproject.toml and requirements.txt and run the below command
> pip install --editable ".[dev]"   
#### Perform Static Code Analysis and Security Scanning
> python -m black fast_app --check  
> python -m isort fast_app --check
> python -m flake8 fast_app

#### Reformat files
> python -m  black fast_app/  

#### Import fixes
> python -m isort fast_app/
