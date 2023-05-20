// Reference - https://man7.org/linux/man-pages/man3/getaddrinfo.3.html
// Reference - https://linuxhint.com/c-init-ntop-function/

#include <stdio.h>
#include <stdlib.h>
#include <netinet/in.h>
#include <sys/socket.h>
#include <sys/types.h>
#include <netdb.h>
#include <unistd.h>
#include <string.h>
#include <arpa/inet.h>

/*
  Use the `getaddrinfo` and `inet_ntop` functions to convert a string host and
  integer port into a string dotted ip address and port.
 */
int main(int argc, char* argv[]) {
  if (argc != 3) {
    printf("Invalid arguments - %s <host> <port>", argv[0]);
    return -1;
  }
  char* host = argv[1];
  long port = atoi(argv[2]);
  
  int s;
  char prt[12];
  sprintf(prt,"%ld", port);

  struct addrinfo hints;
  struct addrinfo *result, *rp;

  memset(&hints, 0, sizeof(hints));
  hints.ai_family = PF_UNSPEC;    /* Allow IPv4 or IPv6 */
  hints.ai_socktype = SOCK_STREAM;
  hints.ai_flags = AI_PASSIVE;
  hints.ai_protocol = IPPROTO_TCP;

  /* getaddrinfo() returns a list of address structures. */
  s = getaddrinfo(host, prt, &hints, &result);

  if (s != 0) {
      fprintf(stderr, "getaddrinfo: %s\n", gai_strerror(s));
      exit(EXIT_FAILURE);
  }

  for (rp = result; rp != NULL; rp = rp->ai_next) {    
    void* raw_addr;
    if (rp->ai_family == AF_INET) { // Address is IPv4
      struct sockaddr_in* tmp = (struct sockaddr_in*)rp->ai_addr; // Cast addr into AF_INET container
      raw_addr = &(tmp->sin_addr); // Extract the address from the container
      char buf[INET_ADDRSTRLEN];
      if(inet_ntop(AF_INET, raw_addr, buf, sizeof(buf)) != NULL) {
        printf("IPv4 %s\n", buf);
      }
    }
    else { // Address is IPv6
      struct sockaddr_in6* tmp = (struct sockaddr_in6*)rp->ai_addr; // Cast addr into AF_INET6 container
      raw_addr = &(tmp->sin6_addr); // Extract the address from the container
      char buf6[INET6_ADDRSTRLEN];
      if(inet_ntop(AF_INET6, raw_addr, buf6, sizeof(buf6)) != NULL) {
        printf("IPv6 %s\n", buf6);
      } 
    }
  }

  return 0;
}