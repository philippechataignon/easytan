run:
	docker run --restart=always -d -p 10001:9876 -v `pwd`/db:/db easytan
test:
	docker run -d -p 9876:9876 -v `pwd`/db:/db easytan:build
build:
	docker build -t easytan:build .
debug:
	docker run --entrypoint sh --rm -it -p 9876:9876 -v `pwd`/db:/db easytan:build
