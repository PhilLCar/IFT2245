#!/usr/bin/python3
# -*- coding: utf-8 -*-

## ch.py --- Un shell pour les hélvètes.

import os
import sys

#-------------------------------------------------------------------------------| MAX-COL

def main():
    index = 0
    history = []
    start_path = os.getcwd()
    out = sys.stdout
    
    while True:
        try:
            sys.stdout.write(os.getcwd() + " % ")
            
            sys.stdout.flush()
            
            # Récupère les arguments et la commande
            user_input = sys.stdin.readline()
            if user_input == "": break
            else: user_input = user_input[:-1].split(' ')
        
            command = user_input[0]
            p_args = user_input[1:]

            # Gestion de l'historique de commande
            history += command

            ### GESTION DE LA REDIRECTION (3) ### !!! Pour l'instant juste 1 redirection possible
            redir_in = []
            redir_out = []
            args = []
            
            for arg in p_args:
                if arg[0] == '<':
                    redir_in += [arg[1:]]
                elif arg[0] == '>':
                    redir_out += [arg[1:]]
                else:
                    args += [arg]

            if len(redir_out):
                out = os.fdopen(os.open(redir_out[0],
                    os.O_CREAT |
                    os.O_WRONLY |
                    os.O_TRUNC), 'w+')

            ### INTERPRÉTATION DES COMMANDES (1) ###
            if command == "cd":
                if len(args) == 0:
                    os.chdir(start_path)
                else:
                    try:
                        os.chdir(args[0])
                    except:
                        sys.stdout.write("No such file or directory: " + args[0] + "\n")

            # http://stackoverflow.com/questions/25113767/infinite-while-not-working-with-os-execvp
            if command in ["cat", "bc", "ls"]: #Ajouter toutes commandes de base
                pid = os.fork()
                if pid:
                    os.waitpid(pid, 0)
                else:
                    sys.stdout = out # ne fonctionne pas
                    os.execv('/usr/bin/' + command, [command] + args)
                
            if command == "exit":
                break
        
            sys.stdout.flush()
        
        except KeyboardInterrupt:
            sys.stdout.write("\n")
    
    sys.stdout.write("Bye!\n")
    sys.exit(0)

main ()
