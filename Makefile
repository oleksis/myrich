format-check:
	black --check .
format:
	black .
test:
	pytest --cov-report term-missing --cov=myrich tests/ -vv
.PHONY: all
all: format-check format test
