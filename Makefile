init:
	pip install -r requirements.txt || pip3 install -r requirements.txt
sync:
	./src/ytdlp_sync_library.sh && ./metadator.py

.PHONY: init test
