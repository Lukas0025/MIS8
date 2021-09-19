install:
	pip install intelhex
	cp mis8_asm.py /usr/bin/mis8_asm
	chmod +x /usr/bin/mis8_asm

uninstall:
	rm -f /usr/bin/mis8_asm

test:
	python mis8_asm.py -i tests/test.asm -o tests/testout_new.txt -f txtbin
	diff tests/testout.txt tests/testout_new.txt
	rm -f tests/testout_new.txt