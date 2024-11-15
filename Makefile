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

.PHONY: clean.doc
clean.doc:
	@$(RM) -rf docs/_build

.PHONY: doc
doc: clean.doc install.doc
	sphinx-build -b html docs docs/_build

.PHONY: install.doc
install.doc: check.lock
	@$(POETRY) install --only docs

