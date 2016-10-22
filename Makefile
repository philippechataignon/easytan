build:
	python setup.py sdist
	docker build -t easytan:build .
run:
	docker run --name easytan_prod --restart=always -d -p 10001:9876 -v `pwd`/db:/db easytan
test:
	docker run -d -p 9877:9876 -v `pwd`/db:/db easytan:build
dev:
	docker run --rm --entrypoint sh -it -p 9876:9876 -v `pwd`/db:/db  easytan:build
tag:
	docker tag -f easytan:build easytan
