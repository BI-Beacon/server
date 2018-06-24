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

// FNV32a returns the hash of 'text' string, according to 32-bit FNV-1a.
func FNV32a(text string) uint32 {
    algorithm := fnv.New32a()
    algorithm.Write([]byte(text))
    return algorithm.Sum32()
}

func getStateCacheFilename(beaconID string ) string {
	return fmt.Sprintf( "%s/%03X/%s", stateRootPath, FNV32a(beaconID)&0x3FF, beaconID )
}

func saveState(beaconID string, color string ) error {
	var filename = getStateCacheFilename(beaconID)
	os.MkdirAll( filepath.Dir( filename ), os.ModePerm )
	return ioutil.WriteFile( filename, []byte(color), 0600)
}

func loadState(beaconID string) (string, error) {
	body, err := ioutil.ReadFile(getStateCacheFilename(beaconID))
	if err != nil {
		return "", err
	}
	return string(body), nil
}

// HandleSetState handles HTTP requests for setting beacon state
func HandleSetState(w http.ResponseWriter, r *http.Request) {
	beaconID, err := getBeaconID(w, r)
	if err != nil {
		return
	}
	log.Println( r )
	err = saveState(beaconID,"red")
	if err != nil {
		http.Error(w, "Internal server error", 500)
		return
	}
	fmt.Fprintf( w, "{ message: '%s updated' }", beaconID );
	io.WriteString(w, "\n\nget state\n")
}

// HandleGetState handles HTTP requests for getting beacon state
func HandleGetState(w http.ResponseWriter, r *http.Request) {
	beaconID, err := getBeaconID(w, r)
   if err != nil {
      return
   }
	r.ParseForm()
	log.Println(r.PostForm)
	body, err := loadState(beaconID)
	if ( err != nil ) {
		http.NotFound(w, r)
	}
	io.WriteString(w, body)
}

// HandleAPIRequest is the main function for handling API requests (both get and set)
func HandleAPIRequest(w http.ResponseWriter, r *http.Request) {
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
	http.HandleFunc("/v1/", HandleAPIRequest)
	log.Fatal(http.ListenAndServe(":8080", nil))
}

func getBeaconID(w http.ResponseWriter, r *http.Request) (string, error) {
	m := validPath.FindStringSubmatch(r.URL.Path)
	if m == nil {
		http.NotFound(w, r)
		return "", errors.New("Invalid State Title")
	}
	return m[1], nil
}
