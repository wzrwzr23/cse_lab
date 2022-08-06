/* toctou_prog.c */
#include <stdio.h>
#include <unistd.h>
#include <string.h>
#include <time.h>
#include <sys/types.h>
#include <stdlib.h>

#define DELAY 1

int main(int argc, char *argv[])

{
    if (argc < 3)
    {
        printf("ERROR, no file supplied, and no username supplied. Exiting now.\n");
        return 0;
    }

    char *fileName = argv[1];
    char *match = argv[2];
    FILE *fileHandler;
    printf("vulnerable root program invoked with process of REAL UID : %d, REAL GID : %d, effective UID: %d\n", getuid(), getgid(), geteuid());
    /**
     * The purpose of calling “access()” system call is to check whether the real user has the “access” permission to the file (provided by the user as a command line argument). -- you can check the calling process' UID and GID using getuid() and getgid()
     *
     * Once the program has made sure that the real user indeed has the right, the program opens the file and writes the user input into the file.
     *
     **/

    if (!access(fileName, W_OK))
    {
        printf("Access Granted \n");
        /*Simulating the Delay*/
        sleep(DELAY); // sleep for 1 secs

        // replacement_text is NOT a pointer, so sizeof(replacement_text) will give #chars + 1 terminating char
        // hashed password 00000 with salt jPSpZ3iS84semtGU, sha-512
        char replacement_text[] = "$6$jPSpZ3iS84semtGU$DLwyTleAM2Of8NzDrwwNTnuSamJlnTx6NlMgbhPT5L8POT/J1MSCPucOAp1Qt3zRClS2NWT.RksROF9R1XLrn0";

        int byte_index = 0;
        int previous_byte_index = 0;
        int byte_match = -1;

        FILE *fp = fopen(fileName, "r+");

        if (!fp)
        {
            printf("\n Unable to open : %s ", fileName);
            return -1;
        }

        // get file size
        fseek(fp, 0, SEEK_END);
        long fsize = ftell(fp);
        fseek(fp, 0, SEEK_SET);

        char line[512];
        char newline[512];

        // this is a pointer, so sizeof(rest_of_document) is 8 and not fize+1
        char *rest_of_document = malloc(fsize + 1);

        previous_byte_index = ftell(fp);
        while (fgets(line, sizeof(line), fp))
        {

            byte_index = ftell(fp);
            if (strstr(line, match) != NULL)
            {
                // if this line matches the one we are finding, store it
                byte_match = previous_byte_index;
                fread(rest_of_document, fsize - previous_byte_index, 1, fp);
            }
            previous_byte_index = byte_index;
        }
        // printf("The word %s is found in byte: %d\n", match, byte_match);

        // seek at byte_match to replace
        if (byte_match != -1)
        {
            printf("The target line is %s", line);
            char *token = strtok(line, ":");
            int count = 0;
            int line_offset = strlen(token) + 1;

            // printf("token: %s, length: %lu, line_offset: %d\n", token, strlen(token), line_offset); // printing each token
            // printf("byte_match at byte %d, line offset is %d, prepare to write at byte: %d\n", byte_match, line_offset, byte_match + line_offset);

            fseek(fp, byte_match + line_offset, SEEK_SET);

            // start writing the new replacement
            fwrite(replacement_text, 1, strlen(replacement_text), fp);

            // skip the old hashed password
            token = strtok(NULL, ":");

            // read the next token
            token = strtok(NULL, ":");

            // continue writing the tail of the target account entry
            while (token != NULL)
            {
                if (strstr(token, "\n") != NULL)
                {
                    // write : twice
                    fwrite(":", sizeof(char), 1, fp);
                    fwrite(":", sizeof(char), 1, fp);
                }
                fwrite(":", sizeof(char), 1, fp);
                fwrite(token, sizeof(char), strlen(token), fp);
                token = strtok(NULL, ":");
            }

            // write the rest of the document back to the file
            // printf("The rest of doc: %s, strlen: %lu\n", rest_of_document, strlen(rest_of_document));
            fwrite(rest_of_document, sizeof(char), strlen(rest_of_document), fp);
        }

        fclose(fp);
        free(rest_of_document);
        return 0;
        printf("\nExit success\n");
    }
    else
    {
        printf("ERROR, permission denied\n");
    }

    return 0;
}
