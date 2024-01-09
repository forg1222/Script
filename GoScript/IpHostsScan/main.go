package main

import (
	"bufio"
	"fmt"
	"github.com/antchfx/htmlquery"
	"log"
	"net/http"
	"os"
	"strconv"
)

func Scan(subdomain string) (string, string) {
	client := &http.Client{
		Transport: &http.Transport{
			//Proxy: http.ProxyURL(proxyUrl),
		},
	}
	url := "http://192.168.0.203"
	req, err := http.NewRequest("GET", url, nil)
	if err != nil {
		fmt.Println(err)
	}
	req.Host = subdomain + ".webhack123.com"
	resp, err := client.Do(req)
	//if err == nil && resp.StatusCode == 200 {
	//body, _ := ioutil.ReadAll(resp.Body)
	doc, err := htmlquery.Parse(resp.Body)
	defer resp.Body.Close()
	//fmt.Println(string(body))
	if err != nil {
		log.Fatal(err)
	}

	title := htmlquery.InnerText(htmlquery.FindOne(doc, `/html/head/title/text()`))

	//fmt.Println(title)

	return strconv.Itoa(resp.StatusCode), title

	//}

	//return strconv.Itoa(resp.StatusCode), resp.Header
}

func wrtSubdomain(dic string) {
	file, err := os.Open(dic)
	if err != nil {
		log.Fatal(err)
	}
	// remember to close the file at the end of the program
	defer file.Close()
	scanner := bufio.NewScanner(file)

	for scanner.Scan() {
		// do something with a line
		//fmt.Printf("line: %s\n", scanner.Text())
		stausCode, title := Scan(scanner.Text())
		if stausCode == "200" {
			fmt.Printf("subDomain:%s\tStatus:%s\tTitle:%s\n", scanner.Text(), stausCode, title)
		}

	}

	if err := scanner.Err(); err != nil {
		log.Fatal(err)
	}
}

func main() {
	//stausCode, title := Scan("ww2")
	//fmt.Println("Status:"+stausCode, " Title:"+title)
	wrtSubdomain("./dicc.txt")
}
