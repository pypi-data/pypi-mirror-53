# MD Generator (mdgenerator)

mdgenerator is a package to generate different kinds of markdown texts

Following details the functionality provided by the package:

- Generate File Structure Trees in Markdown
- Generate Tables in Markdown from pandas dataframe or python arrays

## Installation

There are two ways to install mdgenerator:

- Install mdgenerator from PyPI (recommended):

```
pip install mdgenerator
```

- Install mdgenerator from the Github source:

```
git clone https://github.com/nilansaha/mdgenerator.git
cd mdgenerator
pip install .
```

## Usage

- Generate File Tree Structure in Markdown
	
	- Using Python


	```
	from mdgenerator import generate_file_structure
	
	generate_file_structure(target_dir='/path/to/directory', output_dir='/output/directory')
	```
	
	- Using the terminal


	```
	mdgenerator --target_dir "/path/to/directory" --output_dir "/output/directory"
	```
	
	**Output** is stored in `file_structure.md` in the specified `output_dir`
	
	Sample Output - 

	```
	├── .DS_Store
	├── mdgenerator.py
	├── __init__.py
	├── test.py
	├── cli.py
	├── file-structure.md
	├── ABC
	|   ├── a.txt
	|   ├── BCD
	|   |   ├── b.txt
	├── __pycache__
	|   ├── mdgenerator.cpython-37.pyc
	```

- Generate Markdown Table using Python
	
	- Using Python lists

	```
	from mdgenerator import generate_table

	data = [['Word_1','Word_2'],['Happy','Sad'],['Nice','Bad']]
	table = generate_table(data)
	print(table)
	```
	**Output**

	|Word_1|Word_2|
	|---|---|
	|Happy|Sad|
	|Nice|Bad|

	
	- Using Pandas DataFrame

	```
	import pandas as pd
	from mdgenerator import generate_table

	df = pd.DataFrame([['Happy','Sad'], ['Nice','Bad']], columns = ['Word_1','Word_2'])
	table = generate_table(df)
	print(table)
	```
	**Output**

	|Word_1|Word_2|
	|---|---|
	|Happy|Sad|
	|Nice|Bad|
	


