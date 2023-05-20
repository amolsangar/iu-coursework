#include <stdio.h>
#include <string.h>

void send_http(char* host, char* msg, char* resp, size_t len);

/*
  Implement a program that takes a host, verb, and path and
  prints the contents of the response from the request
  represented by that request.
 */
int main(int argc, char* argv[]) {
  if (argc != 4) {
    printf("Invalid arguments - %s <host> <GET|POST> <path>\n", argv[0]);
    return -1;
  }
  
  char* host = argv[1];
  char* verb = argv[2];
  char* path = argv[3];

  if(strcmp(verb,"GET") != 0 && strcmp(verb,"POST") != 0) {
    return 0;
  }
  
  char response[4096];
  char arg2[100];
  sprintf(arg2, "%s %s HTTP/1.1\r\nHost: %s\r\n\r\n", verb, path, host);
  send_http(host, arg2, response, 4096);
  printf("%s\n", response);

  return 0;
}
