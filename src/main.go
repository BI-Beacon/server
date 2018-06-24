package main

import (
	"fmt"
	"log"
	"io"
	"hash/fnv"
	"regexp"
	"io/ioutil"
	"errors"
	"net/http"
	"path/filepath"
	"os"
)

var stateRootPath = "./state"

// path := filepath.Join(someRootPath, someSubPath)

var validPath = regexp.MustCompile("^/v1/([a-zA-Z0-9]+)$")

func FNV32a(text string) uint32 {
    algorithm := fnv.New32a()
    algorithm.Write([]byte(text))
    return algorithm.Sum32()
}

func getStateCacheFilename(beaconId string ) string {
	return fmt.Sprintf( "%s/%03X/%s", stateRootPath, FNV32a(beaconId)&0x3FF, beaconId )
}

func saveState(beaconId string, color string ) error {
	var filename = getStateCacheFilename(beaconId)
	os.MkdirAll( filepath.Dir( filename ), os.ModePerm )
	return ioutil.WriteFile( filename, []byte(color), 0600)
}

func loadState(beaconId string) (string, error) {
	body, err := ioutil.ReadFile(getStateCacheFilename(beaconId))
	if err != nil {
		return "", err
	}
	return string(body), nil
}

func HandleSetState(w http.ResponseWriter, r *http.Request) {
	beaconId, err := getBeaconId(w, r)
	if err != nil {
		return
	}
	log.Println( r )
	err = saveState(beaconId,"red")
	if err != nil {
		http.Error(w, "Internal server error", 500)
		return
	}
	fmt.Fprintf( w, "{ message: '%s updated' }", beaconId );
	io.WriteString(w, "\n\nget state\n")
}

func HandleGetState(w http.ResponseWriter, r *http.Request) {
	beaconId, err := getBeaconId(w, r)
   if err != nil {
      return
   }
	r.ParseForm()
	log.Println(r.PostForm)
	body, err := loadState(beaconId)
	if ( err != nil ) {
		http.NotFound(w, r)
	}
	io.WriteString(w, body)
}

func HandleApiRequest(w http.ResponseWriter, r *http.Request) {
	if ( r.Method == "GET" ) {
		HandleGetState(w, r)
		return
	}
	if ( r.Method == "POST" ) {
		HandleSetState(w, r)
		return
	}
	http.Error(w, "unknown request method", http.StatusMethodNotAllowed)
}

func main() {
	http.HandleFunc("/v1/", HandleApiRequest)
	log.Fatal(http.ListenAndServe(":8080", nil))
}

func getBeaconId(w http.ResponseWriter, r *http.Request) (string, error) {
	m := validPath.FindStringSubmatch(r.URL.Path)
	if m == nil {
		http.NotFound(w, r)
		return "", errors.New("Invalid State Title")
	}
	return m[1], nil
}
