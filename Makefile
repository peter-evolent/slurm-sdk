TAG="\n\n\033[0;32m\#\#\# "
END=" \#\#\# \033[0m\n"


########################################################
.PHONY: all
all: test

.PHONY: init
init:
	@echo $(TAG)Installing dev requirements$(END)
	pip install --upgrade --quiet -r requirements-dev.txt

	@echo $(TAG)Installing SlurmSDK$(END)
	pip install --upgrade --editable .

	@echo

.PHONY: test
test:
	@echo $(TAG)Running pytest with coverage$(END)
	pytest --verbose --cov ./slurmsdk

	@echo

.PHONY: lint
lint:
	@echo $(TAG)Running flake8$(END)
	flake8

	@echo