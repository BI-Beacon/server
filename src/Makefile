GO_BUILD := GOOS=linux go build
GO_DIST_BUILD := CGO_ENABLED=0 $(GO_BUILD) -a -installsuffix cgo -ldflags="-s -w"

all:
	$(GO_BUILD) -o main . 

dist:
	$(GO_DIST_BUILD) -o main . 
	upx --brute main
	docker build -t test .

clean:
	rm -rf *~ main main.[0-9]* main.upx main.exe golint-report.out

run:
	docker run -it --rm test

tests:
	go get github.com/golang/lint/golint
	cd .. && golint src > golint-report.out
