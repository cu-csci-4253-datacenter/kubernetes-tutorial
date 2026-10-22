IMAGE ?= rustfs-example:latest

.PHONY: build push

build:
	docker build -t $(IMAGE) .

# Example: make push IMAGE=your-dockerhub-user/rustfs-example:latest
push:
	docker push $(IMAGE)
