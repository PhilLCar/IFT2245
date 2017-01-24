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
    
    while True:
        try:
            sys.stdout.write(os.getcwd() + " % ")
            
            sys.stdout.flush()
            
            # Récupère les arguments et la commande
            user_input = sys.stdin.readline()
            if user_input[-1:] != "\n": break
            else: user_input = user_input[:-1].split(' ')
        
            command = user_input[0]
            p_args = user_input[1:]

            # Gestion de l'historique de commande
            history += command

            ### EXPENSION D'ARGUMENTS (2) ###
            e_args = []
            
            for arg in p_args:
                if '*' == arg:
                    e_args += os.listdir(os.getcwd())
                elif '*' == arg[0]:
                    if '*' == arg[-1:]:
                        for elem in os.listdir(os.getcwd()):
                            if arg[1:-1] in elem:
                                e_args += [elem]
                    else:
                        for elem in os.listdir(os.getcwd()):
                            if arg[1:] == elem[-len(arg) + 1:]:
                                e_args += [elem]
                elif '*' == arg[-1:]:
                    for elem in os.listdir(os.getcwd()):
                        if arg[:-1] == elem[:len(arg) - 1]:
                            e_args += [elem]
                else:
                    e_args += [arg]

            ### GESTION DE LA REDIRECTION (3) ###
            #!!! Pour l'instant juste 1 redirection possible
            redir_in = []
            redir_out = []
            args = []
            
            for arg in e_args:
                if arg[0] == '<':
                    redir_in += [arg[1:]]
                elif arg[0] == '>':
                    redir_out += [arg[1:]]
                else:
                    args += [arg]

            if len(redir_out):
                stdout = os.open(redir_out[0],
                                 os.O_CREAT |
                                 os.O_WRONLY |
                                 os.O_TRUNC)
            else: stdout = 1

            if len(redir_in):
                stdin = os.open(redir_in[0], os.O_RDONLY)
            else: stdin = 0

            ### PIPING (4) ###
            pid = True
            while '|' in args:
                for x in range(len(args)):
                    if args[x] == '|':
                        r, w = os.pipe()
                        pid = os.fork()
                        
                        if pid:
                            os.close(w)
                            stdin = r
                            command = args[x + 1]
                            args = args[x + 2:]
                            break               
                        else:
                            os.close(r)
                            stdout = w
                            args = args[:x]
                            break

            ### INTERPRÉTATION DES COMMANDES (1) ###
            if command == "cd":
                if len(args) == 0:
                    os.chdir(start_path)
                else:
                    try:
                        os.chdir(args[0])
                    except:
                        sys.stdout.write("ch: cd: " + args[0] +
                                         ": No such file or directory\n")
                
            elif command == "exit":
                break

            # http://stackoverflow.com/questions/25113767
            else:
                try:
                    if pid:
                        pid = os.fork()
                    if pid:
                        os.waitpid(pid, 0)
                    else:
                        os.dup2(stdout, 1) # redirige le output de stdout (1)
                        os.dup2(stdin, 0)
                        os.execvp(command, [command] + args)
                except:
                    sys.stdout.write("ch: " + command + ": command not found\n")
                    sys.exit(1)
                
            sys.stdout.flush()
        
        except KeyboardInterrupt:
            sys.stdout.write("\n")
    
    sys.stdout.write("Bye!\n")
    sys.exit(0)

main ()
