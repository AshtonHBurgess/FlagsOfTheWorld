import sys
import os


selectedIndexList=[1,2,3,4,5,6,7,]

country_name="Canada"

path = '\PROG 1700-703 Logic and Programming\PROG1700_SourceCode\project-countriesoftheworld-AshtonHBurgess\Flags'
pngList=[]
l_files = os.listdir(path)
for file in l_files:
    file=file.replace(".png","")
    file=file.replace("_"," ")
    if file==country_name:
        
        file=(str(file) +".png")
        file=file.replace(" ","_")
        pngList.append(file)
        print(file)
x=("\PROG 1700-703 Logic and Programming\PROG1700_SourceCode\project-countriesoftheworld-AshtonHBurgess\Flags" + str(pngList[0]))
print(x)




#print(pngList)
