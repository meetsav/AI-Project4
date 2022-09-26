import subprocess


def writeTofile(list,query,k):
   
    file=open("wumpus"+str(k+1)+".z3","a")
    file.truncate(0)
    file.write("(declare-fun Pit (Int Int) Bool)\n")
    file.write("(declare-fun Breeze (Int Int) Bool)\n")
    file.write("(declare-fun Stench (Int Int) Bool)\n")
    file.write("(declare-fun Wumpus (Int Int) Bool)\n")
    file.write("(declare-fun Glitter (Int Int) Bool)\n")
    file.write("(declare-fun Gold (Int Int) Bool)\n")
    file.write("(declare-fun NoPit (Int Int) Bool)\n")
    file.write("(declare-fun NoBreeze (Int Int) Bool)\n")
    file.write("(declare-fun NoStench (Int Int) Bool)\n")
    file.write("(declare-fun NoGlitter (Int Int) Bool)\n")
    file.write("(declare-fun NoWumpus (Int Int) Bool)\n")
    file.write("(declare-fun NoGold (Int Int) Bool)\n")
    file.write("(declare-const gridSize Int)\n")
    file.write("(assert (= gridSize %d))\n" % max)
    file.write(
        "(define-fun adjacent((i Int)(j Int)(k Int)(l Int)) Bool (or(and(= i k)(or(= j (+ l 1))(= j (- l 1))))(and(= j l)(or(= i (+ k 1))(= i(- k 1))))))\n")
    file.write("(define-fun output((i Int)(j Int)) Bool (or(<= i 0)(> i gridSize)(<= j 0)(> j gridSize)))\n")
    #this is easy to write
    # gold<=>glitter
    file.write("(assert (forall ((i Int) (j Int)) (= (Gold i j)(Glitter i j))))\n")
    # breeze<=>Not(nobreeze)
    file.write("(assert(forall ((i Int)(j Int)) (= (NoBreeze i j)(not(Breeze i j)))))\n")
    # pit=>not(nopit)
    file.write("(assert(forall ((i Int)(j Int)) (= (NoPit i j)(not(Pit i j)))))\n")
    # gold=>Not(nogold)
    file.write("(assert(forall ((i Int) (j Int)) (= (NoGold i j)(not(Gold i j)))))\n")
    # wumpus=>Not(nowumpus)
    file.write("(assert(forall ((i Int)(j Int)) (= (NoWumpus i j)(not(Wumpus i j)))))\n")
    # stench=>Not(nostench)
    file.write("(assert(forall ((i Int)(j Int)) (= (NoStench i j)(not(Stench i j)))))\n")
    # glitter=>Not(nogiller)
    file.write("(assert(forall ((i Int) (j Int)) (= (NoGlitter i j)(not(Glitter i j)))))\n")
    #complex formulas
    #pit=>breeze
    file.write("(assert (forall ((i Int) (j Int) (k Int) (l Int)) (=> (and (Pit i j)(not(output i j))(not(output k l))(adjacent i j k l)) (Breeze k l))))\n")
    # breeze=>pit
    file.write("(assert (forall ((k Int) (l Int)) (=>(and (Breeze k l)(not(output k l))) (exists((i Int) (j Int))(and (adjacent i j k l)(not(output i j)) (Pit i j))))  ))\n")
    # wumpus=>stench
    file.write("(assert (forall ((i Int) (j Int) (k Int) (l Int)) (=> (and (Wumpus i j)(not(output i j))(not(output k l))(adjacent i j k l)) (Stench k l))))\n")
    #stench=>wumpus
    file.write("(assert (forall ((k Int) (l Int)) (=>(and (Stench k l)(not(output k l))) (exists((i Int) (j Int))(and (adjacent i j k l)(not(output i j)) (Wumpus i j))))  ))\n")

    #assigning values to the list
    for i in range(len(list)):
        if list[i][2] == 'Pit':
            file.write("(assert (Pit %s %s))\n" % (list[i][0], list[i][1]))
        elif list[i][2] == 'Breeze':
            file.write("(assert (Breeze %s %s))\n" % (list[i][0], list[i][1]))
        elif list[i][2] == 'Stench':
            file.write("(assert (Stench %s %s))\n" % (list[i][0], list[i][1]))
        elif list[i][2] == 'Wumpus':
            file.write("(assert (Wumpus %s %s))\n" % (list[i][0], list[i][1]))
        elif list[i][2] == 'Gold':
            file.write("(assert (Gold %s %s))\n" % (list[i][0], list[i][1]))
        elif list[i][2] == 'Glitter':
            file.write("(assert (Glitter %s %s))\n" % (list[i][0], list[i][1]))
        elif list[i][2] == 'NoPit':
            file.write("(assert (NoPit %s %s))\n" % (list[i][0], list[i][1]))
        elif list[i][2] == 'NoBreeze':
            file.write("(assert (NoBreeze %s %s))\n" % (list[i][0], list[i][1]))
        elif list[i][2] == 'NoStench':
            file.write("(assert (NoStench %s %s))\n" % (list[i][0], list[i][1]))
        elif list[i][2] == 'NoWumpus':
            file.write("(assert (NoWumpus %s %s))\n" % (list[i][0], list[i][1]))
        elif list[i][2] == 'NoGold':
            file.write("(assert (NoGold %s %s))\n" % (list[i][0], list[i][1]))
        elif list[i][2] == 'NoGlitter':
            file.write("(assert (NoGlitter %s %s))\n" % (list[i][0], list[i][1]))
    #add the query at last and see magic
    file.write("(assert (not(%s))) \n" % query)
    file.write("(check-sat)\n")
    file.close()


def runZ3(k):
    cmd="/usr/local/z3/bin/z3"
    process = subprocess.Popen([cmd,"wumpus"+str(k+1)+".z3"],stdout=subprocess.PIPE,universal_newlines=True).communicate()[0]
    p = subprocess.Popen(["rm", "wumpus"+str(k+1)+".z3"],stdout=subprocess.PIPE)
    if process =='sat\n':
        print("does not entails")
    elif process =='unsat\n':
        print("entails")
    else:
        print("could not make inference")


if __name__ == '__main__':
	for i in range(10):
	    global inference
	    global beliefs
	    global max
	    filename = open("10_tests/tests/"+str(i+1)+"/beliefs.txt", "r")
	    #filename = open(str(i+1)+"/beliefs.txt", "r")
	    KB = [model.rstrip('\n') for model in filename]
	    max = int(KB[0])
	    beliefs = []
	    for line in KB[1:]:
	        temp = line.split("\t")
	        if (len(temp) == 3):
	            temp[0] = int(temp[0])
	            temp[1] = int(temp[1])
	            beliefs.append(temp)
	
	
	    filename1 = open("10_tests/tests/"+str(i+1)+"/query.txt", "r")
	    #filename1 = open(str(i+1)+"/query.txt", "r")
	    inference = filename1.readline().split("\t")
	    inference[0] = int(inference[0])
	    inference[1] = int(inference[1])
	    inference[2] = inference[2].replace("\n", "")
	    query='%s %s %s'%(inference[2], inference[0],inference[1])
	
	    writeTofile(beliefs,query,i)
	    runZ3(i)



