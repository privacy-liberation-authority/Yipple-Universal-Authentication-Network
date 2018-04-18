TAG=comp6443-build-3

.PHONY: all build run clean test

all: build run

build:
	docker build -t $(TAG) .

run:
	docker run --rm -p 9447:9447 $(TAG)

clean:
	docker rmi $(TAG)

test: 
	./test.py -v
