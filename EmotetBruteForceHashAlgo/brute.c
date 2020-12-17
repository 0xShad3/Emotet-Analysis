#include <stdlib.h>
#include <stdio.h>
#include <string.h>

int hash(char *word);
int main(int argc, char **argv)
{

	int hashtest;
	int i = 0;
	int cnt;
	int targets_length;
	int MAX_LINE_LENGTH = 5;
	char line[MAX_LINE_LENGTH];
	char **_targets;
	int *targets;
	char *pend;
	char row[32];

	if (argc < 2)
	{
		printf("[*] An error occured!\n");
		printf("[-] Not enough arguments provided!\n");
		exit(EXIT_FAILURE);
	}

	FILE *targets_file = fopen(argv[1], "r");
	if (targets_file == NULL)
	{
		printf("[-] There was an error with the hashes file.\n");
		return EXIT_FAILURE;
	}
	// assume 100 targets
	_targets = (char **)calloc(100, sizeof(char *));
	while (fgets(row, sizeof(row), targets_file) != NULL)
	{
		_targets[i] = (char *)calloc(strlen(row), sizeof(char));
		strcpy(_targets[i], row);
		i++;
		if (i >= 100)
			break;
	}

	if (fclose(targets_file))
	{
		printf("[-] There was an error while trying to close the hashes file.\n");
		return EXIT_FAILURE;
	}
	targets_length = i;
	targets = (int *)calloc(targets_length, sizeof(int));
	for (i = 0; i < targets_length; i++)
	{
		targets[i] = strtol(_targets[i], &pend, 16);
	}
	/* Get each line until there are none left */
	if (!strcmp(argv[2], "NONE"))
	{
		cnt = 0;
		FILE *wl_file = fopen("pass.dic", "r");
		while (fgets(line, MAX_LINE_LENGTH, wl_file))
		{
			/* Print each line */
			line[strlen(line) - 1] != '\n';
			hashtest = hash(line);
			for (i = 0; i < targets_length; i++)
			{
				if (targets[i] == hashtest)
				{
					fprintf(stdout, "%x:%s\n", targets[i], line);
					cnt++;
				}
			}

			if (cnt == targets_length)
				break;

			if (cnt > targets_length)
				printf("[-] An error occured while bruteforcing, Collision???\n");
		}
		if (fclose(wl_file))
		{
			printf("[-] There was an error while trying to close the dictionary file.\n");
			return EXIT_FAILURE;
		}
	}
	else
	{
		cnt = 0;
		FILE *wl_file = fopen("pass.dic", "r");
		FILE *fp = fopen(argv[2], "r+");
		if (fp == NULL)
		{
			printf("[-] There was an error while trying to close the output file.\n");
			return EXIT_FAILURE;
		}
		while (fgets(line, MAX_LINE_LENGTH, wl_file))
		{
			/* Print each line */
			line[strlen(line) - 1] != '\n';
			hashtest = hash(line);
			for (i = 0; i < targets_length; i++)
			{
				if (targets[i] == hashtest)
				{
					fprintf(fp, "%x:%s\n", targets[i], line);
					cnt++;
				}
			}

			if (cnt == targets_length)
				break;

			if (cnt > targets_length)
				printf("[-] An error occured while bruteforcing, Collision???\n");
		}
		if (fclose(wl_file))
		{
			printf("[-] There was an error while trying to close the dictionary file.\n");
			return EXIT_FAILURE;
		}
	}

	return 0;
}

int hash(char *word)
{
	char *v1;
	int v2;
	int i;
	v1 = word;
	for (i = 0; *v1; i = (i << 16) + (i << 6) + v2 - i)
	{
		v2 = *v1;
		if (v2 >= 0x41 && v2 <= 0x5a)
		{
			v2 += 32;
		}
		++v1;
	}
	return i;
}