#include <stdio.h>
#include <string.h>

int connect_smtp(const char* host, int port);
void send_smtp(int sock, const char* msg, char* resp, size_t len);

/*
  Use the provided 'connect_smtp' and 'send_smtp' functions
  to connect to the "lunar.open.sice.indian.edu" smtp relay
  and send the commands to write emails as described in the
  assignment wiki.
 */
int main(int argc, char* argv[]) {
  if (argc != 3) {
    printf("Invalid arguments - %s <email-to> <email-filepath>", argv[0]);
    return -1;
  }

  char* rcpt = argv[1];
  char* filepath = argv[2];
  
  FILE *fp;
  char buff[4096];
  char email_body[4096] = "";

  // Read file
  fp = fopen(filepath, "r");
  while(fgets(buff, 4096, fp) != NULL) {
      strcat(email_body,buff);
   }
  fclose(fp);

  int socket = connect_smtp("lunar.open.sice.indiana.edu", 25);
  char response[4096];

  // HELO
  send_smtp(socket, "HELO iu.edu\n", response, 4096);
  printf("%s\n", response);
  
  // MAIL FROM
  char mail_from_str[100];
  sprintf(mail_from_str, "MAIL FROM:%s\n", rcpt);
  send_smtp(socket, mail_from_str, response, 4096);
  printf("%s\n", response);
  
  // RCPT TO
  char rcpt_str[100];
  sprintf(rcpt_str, "RCPT TO:%s\n", rcpt);
  send_smtp(socket, rcpt_str, response, 4096);
  printf("%s\n", response);

  // Send DATA
  send_smtp(socket, "DATA\n", response, 4096);
  printf("%s\n", response);
  char data[4096] = "";
  strcat(data,email_body);
  strcat(data,"\r\n.\r\n");

  send_smtp(socket, data, response, 4096);
  printf("%s\n", response);

  // // QUIT
  // send_smtp(socket, "QUIT\n", response, 4096);
  // printf("%s\n", response);
  
  return 0;
}