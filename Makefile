POETRY ?= poetry

.PHONY: check.lock
check.lock:
	@$(POETRY) check --lock

.PHONY: install
install: check.lock
	@$(POETRY) install

.PHONY: test
test: install
	@$(POETRY) run python -m pytest -v tests/unittests
