run:
	docker run -d -p 10001:9876 -v `pwd`/db:/db easytan
build:
	docker build -t easytan .
debug:
	docker run --entrypoint sh --rm -it -p 9876:9876 -v `pwd`/db:/db easytan
