#!/bin/bash

helpFunction()
{
   echo ""
   echo "Usage: $0 -t ./path/to/target/hashes";
   echo -e "\t-p Password list for crunch [Optional]";
   echo -e "\t-t Hash targets list file to bruteforce";
   echo -e "\t-o Output file to write the output to, default screen [Optional]";
   exit 1 # Exit script after printing help
}

while getopts "p:t:o:" opt
do
   case "$opt" in
      p ) password_list_path="$OPTARG" ;;
      t ) targets="$OPTARG" ;;
      c ) output="$OPTARG" ;;
      ? ) helpFunction ;; # Print helpFunction in case parameter is non-existent
   esac
done


if [ -z "$targets" ]
then
    helpFunction
fi 

if [ ! -e "$targets" ]
then
    echo "[-] The target file you provided doesn't exist!";
fi

# Print helpFunction in case parameters are empty
if [ -z "$password_list_path" ]
then
   echo "[+] Password dictionary is not provided!";
   echo "[+] I will generate one for you";
    if ! command -v crunch &> /dev/null
    then
        echo "[*] Crunch not installed!";
        echo "[*] Provide root password to install it";
        sudo apt-get install crunch
    fi

    echo "[+] Generating password list to bruteforce";

    echo "[*] Generating all the possible file extensions";

    # wrap it in a function
    crunch 5 5 -t .@@@@ -o temp.dic > /dev/null 2>&1
    cat temp.dic > pass.dic
    rm temp.dic

    crunch -t 4 4 .@@@ -o temp.dic > /dev/null 2>&1
    cat temp.dic >> pass.dic
    rm temp.dic

    crunch -t 3 3 .@@  -o temp.dic > /dev/null 2>&1
    cat temp.dic >> pass.dic
    rm temp.dic

    crunch -t 2 2 .@ -o temp.dic > /dev/null 2>&1
    cat temp.dic >> pass.dic
    rm temp.dic
fi

if [ -z "$output" ]
then
    echo "[+] No output file provided, output will be written to screen!";
    output="NONE";
fi

if [ -e "brute.bin" ]
then
    echo "[*] Starting bruteforce!";
    ./brute.bin "$targets" "$output"
    exit 1
fi

echo "[*] No brute.bin attempting to compile!"
if [ ! -e "brute.c" ]
then
    echo "[-] Please go to Github and get the source code!";
    exit 1
fi

if ! command -v gcc &> /dev/null
then
    echo "[*] gcc is not installed!";
    echo "[*] Provide root password to install it";
    sudo apt-get install gcc
fi

gcc brute.c -o brute.bin

echo "[+] Starting bruteforce!";
gdb ./brute.bin "$targets" "$output"


