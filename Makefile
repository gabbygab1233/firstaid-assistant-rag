# .PHONY: install
# install:
# 	pip install -r requirements.txt

.PHONY: pre-commit
pre-commit:
	- pre-commit run --all-files

.PHONY: clean
clean:
	@echo "Cleaning cache and build files"
	find . -name '*.pyc' -delete
# 	Remove Python cache directories and files
	find . -name '__pycache__' -delete
# 	Remove pytest cache files
	rm -rf .pytest_cache
# 	Remove mypy cache files
	rm -rf .mypy_cache*

	rm -rf .chainlit

default: pre-commit, clean
