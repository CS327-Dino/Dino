check: 
	python -m unittest test.$(FILE)

checkall:
	python -m unittest discover -s test