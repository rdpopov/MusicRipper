init:
	pip install -r requirements.txt || pip3 install -r requirements.txt
test:
	python -m unittest || python3 -m unittest
# add server
# add normal operation

.PHONY: init test
