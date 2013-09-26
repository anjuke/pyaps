.PHONY: test

test:
	cd tests/unit && python -munittest all
