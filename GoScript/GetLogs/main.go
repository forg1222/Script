package main

import (
	"bufio"
	"fmt"
	"io/ioutil"
	"net/http"
	"os"
	"strconv"
)

func readLogs(year string, month string, day string) string {
	client := &http.Client{
		Transport: &http.Transport{
			//Proxy: http.ProxyURL(proxyUrl),
		},
	}
	url := "http://www.webhack123.com/App/Runtime/Logs/" + year + "_" + month + "_" + day + ".log"
	req, err := http.NewRequest("GET", url, nil)
	resp, err := client.Do(req)
	if err == nil && resp.StatusCode == 200 {
		body, _ := ioutil.ReadAll(resp.Body)
		//fmt.Println(string(body))
		fmt.Println(url)
		return string(body)

	}
	//defer resp.Body.Close()
	return ""
}

func wrtLogs(res string) {
	filePath := "logs.txt"
	file, err := os.OpenFile(filePath, os.O_WRONLY|os.O_CREATE|os.O_APPEND, 0666)
	if err != nil {
		fmt.Println("文件打开失败", err)
	}
	//及时关闭file句柄
	defer file.Close()
	//写入文件时，使用带缓存的 *Writer
	write := bufio.NewWriter(file)
	write.WriteString(res)

	//Flush将缓存的文件真正写入到文件中
	write.Flush()
}

func main() {
	strJ := ""
	strZ := ""
	for i := 18; i < 22; i++ {
		for j := 1; j < 13; j++ {
			if j < 10 {
				strJ = "0" + strconv.Itoa(j)
			} else {
				strJ = strconv.Itoa(j)
			}
			for z := 1; z < 32; z++ {
				if z < 10 {
					strZ = "0" + strconv.Itoa(z)
				} else {
					strZ = strconv.Itoa(z)
				}
				res := readLogs(strconv.Itoa(i), strJ, strZ)
				wrtLogs(res)
			}

		}
	}

}
