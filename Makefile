run:
	docker run --name easytan_prod --restart=always -d -p 10001:9876 -v `pwd`/db:/db easytan
test:
	docker run -d -p 9876:9876 -v `pwd`/db:/db easytan:build
build:
	docker build -t easytan:build .
dev:
	docker run --rm --entrypoint sh -it -p 9876:9876 -v `pwd`/db:/db easytan:build
tag:
	docker tag -f easytan:build easytan
