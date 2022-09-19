init:
	pip install -r requirements.txt
test:
	python -m unittest
# add server
# add normal operation

.PHONY: init test
