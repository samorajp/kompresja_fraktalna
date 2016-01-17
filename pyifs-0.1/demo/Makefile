# Makefile for IFS examples.

IFS = $(wildcard *.ifs)
PNG = $(subst .ifs,.png,${IFS})

all: $(PNG)

%.png: %.ifs
	./ifs2png $< $@

clean:; rm -f *.png
