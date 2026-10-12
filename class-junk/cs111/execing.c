#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>
#include <sys/types.h>

// THIS FORKING IS BROKEN idk


/*

DN0a18186a:cs111 magi-nerv$ gcc -o out ./execing.c 
DN0a18186a:cs111 magi-nerv$ ./out
this should be unsuccessful
echo "But this should work!. Echoing"
DN0a18186a:cs111 magi-nerv$ 
----> waiting for child (NO SLEEP IN THIS FUNCTION)

Child (addr=0x16b4d2ce8)
String: lower
(new addr=0x16b4d2ce8)

----> Parent waited for child! (addr=0x16b4d2ce8)
----> String: upper
---->(new addr=0x16b4d2ce8)
AAAAAAA

DN0a18186a:cs111 magi-nerv$ 

*/

int main() {

    execvp("BAD PATH", NULL);
    printf("this should be unsuccessful\n");

    pid_t pid = fork();

    if (pid) {
        printf("echo \"But this should work!. Echoing\"\n", NULL);
    }

    else {
        sleep(1);
        execvp("./SAMPLE", NULL);
        printf("this should not print\n");
    }



    return -1;


}
    