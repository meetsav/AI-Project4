
Project descirption: Project-4-description.pdf
Main program is :Program.py

Running Instruction:
    just replace beliefs.txt and query.txt for 10 times for 10 different files and see the magic

Logic:
    1)i am following the standard wumpus world rules
    2)program will create z3 file run time in wumpus.z3
    3)after creating program, using subprocess it will run in command line (e.g z3 wumpus.z3)
    4)for flushing pipeline, i am removing the wumpus.z3 file each time after getting output

    it contain 3 method:
        1)writeTofile()
        2)runZ3
        3)main()

note:
    if it is not gving perfact output then do check method: runZ3()
        1)inside that there is a string named:cmd
        2)check path of z3 in cmd string
        3)and run again
