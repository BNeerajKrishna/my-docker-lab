package main

import (
    "fmt"
    "html/template"
    "math/rand"
    "net/http"
    "os"
    "strings"
    "time"

    "github.com/gorilla/mux"
)

type QuoteData struct {
    Quote string
}

func main() {
    r := mux.NewRouter()
    r.HandleFunc("/", randomQuoteHandler)

    fmt.Println("Server is running on http://localhost:5000")
    if err := http.ListenAndServe(":5000", r); err != nil {
        fmt.Println("Error starting server:", err)
    }
}

func randomQuoteHandler(w http.ResponseWriter, r *http.Request) {
    quotes := readQuotesFromFile("quotes.txt")
    rand.Seed(time.Now().UnixNano())
    quote := quotes[rand.Intn(len(quotes))]

    t, err := template.ParseFiles("index.html")
    if err != nil {
        http.Error(w, err.Error(), http.StatusInternalServerError)
        return
    }

    data := QuoteData{Quote: quote}

    if err := t.Execute(w, data); err != nil {
        http.Error(w, err.Error(), http.StatusInternalServerError)
    }
}

func readQuotesFromFile(filename string) []string {
    file, err := os.ReadFile(filename)
    if err != nil {
        return []string{"Error reading quotes."}
    }
    // Split the content by new lines and return as a slice
    return strings.Split(string(file), "\n")
}