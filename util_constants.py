<<<<<<< HEAD
def getDivisions(batch_name,noOfDivisions):
    divisions=["A","B","C","D","E","F"]
    for i in range(noOfDivisions):
        pass
=======
def getDivisions(noOfDivisions):
    divisions=["A","B","C","D","E","F"]
    possible_div=[]
    for i in range(noOfDivisions):
        possible_div.append(divisions[i])
    return possible_div

def getPracticalBatches(noOfPracBatches):
    batches=[]
    for i in range(noOfPracBatches):
        batches.append("B"+str(i+1))
    possible_batches=[]
    for i in range(noOfPracBatches):
        possible_batches.append(batches[i])
    return possible_batches

>>>>>>> otherUpdates-local
