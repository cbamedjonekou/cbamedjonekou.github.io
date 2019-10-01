---
layout: post
title: "Blackhat Series: Creating TCP Client w/ Socket Module & Python 3"
date: 2019-09-23
tags: blackhat python3 tcp-client socket 
---

### Creating a TCP CLient using the socket module 

####  Assumptions:

* Assumed success in our connection and included no exception handling

* Assumed that the server is expecting us to send data first. This does not always happen in the order.

* Assumed that the server will always send us data back in a timely fashion. This is not always the case.


```python
import socket

# We define variables that hold the target host and port number 
# we're going to pull data from.
target_host, target_port = "wwww.google.com", 80

# Then we create our socket object
# socket.socket() is used to create the socket object
# It takes two parameters: AF_INET, and SOCK_STREAM
# The AF_INET parameter is saying we are going to use a standard IPv4 address or hostname
# AF_INET represents the parameter for the socket domain (Address Family-Internet Networking)
# SOCK_STREAM indicates that this will be a TCP client. 
# SOCK_STREAM represents the parameter for the socket type
# Link: https://github.com/python/cpython/blob/3.7/Lib/socket.py
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# After we connect the the socket to a remote address (client.connect(address)).
# For IP sockets, the address is a tuple (host, port).
address = (target_host, target_port)
client.connect(address)
```

The following can also be written as such where adding `b` to the front of the string in sentData treats it as a `bytes parameter`:

```python
sentData = b"GET / HTTP/1.1\r\nHost: google.com\r\n\r\n"
client.send(sentData)

buffersize = 4096
response = client.recv(buffersize)
```


```python
# Once we connect we send some data
# Sent Data is in the form of a unicode string
sentData = "GET / HTTP/1.1\r\nHost: google.com\r\n\r\n"
client.send(sentData.encode('utf-8'))


# Then we retrieve the response
buffersize = 4096
response = client.recv(buffersize).decode('utf-8')
```

#### Response for sending some data


```python
print(response)
```

    HTTP/1.1 200 OK
    Server: nginx
    Date: Mon, 10 Jun 2019 20:39:48 GMT
    Content-Type: text/html; charset=utf-8
    Transfer-Encoding: chunked
    Connection: close
    Expires: Mon, 10 Jun 2019 20:49:48 GMT
    Cache-Control: max-age=600
    X-Frame-Options: DENY
    
    366
    <!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd"><html><head><meta http-equiv="refresh" content="0;url=https://searchassist.verizon.com/main?ParticipantID=euekiz39ksg8nwp7iqj2fp5wzfwi5q76&FailedURI=http%3A%2F%2Fgoogle.com%2F&FailureMode=1&Implementation=&AddInType=4&Version=pywr1.0&ClientLocation=us"/><script type="text/javascript">url="https://searchassist.verizon.com/main?ParticipantID=euekiz39ksg8nwp7iqj2fp5wzfwi5q76&FailedURI=http%3A%2F%2Fgoogle.com%2F&FailureMode=1&Implementation=&AddInType=4&Version=pywr1.0&ClientLocation=us";if(top.location!=location){var w=window,d=document,e=d.documentElement,b=d.body,x=w.innerWidth||e.clientWidth||b.clientWidth,y=w.innerHeight||e.clientHeight||b.clientHeight;url+="&w="+x+"&h="+y;}window.location.replace(url);</script></head><body></body></html>
    0
    
    

