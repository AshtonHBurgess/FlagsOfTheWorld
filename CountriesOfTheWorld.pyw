import sys
import os
from PyQt5.QtWidgets import QApplication, QMainWindow, QMessageBox
from PyQt5.QtGui import QPixmap
import csv



#ADD IMPORT STATEMENT FOR YOUR GENERATED UI.PY FILE HERE
import Ui_project_CountriesOfTheWorld
#      ^^^^^^^^^^^ Change this!

#CHANGE THE SECOND PARAMETER (Ui_ChangeMe) TO MATCH YOUR GENERATED UI.PY FILE
class MyForm(QMainWindow, Ui_project_CountriesOfTheWorld.Ui_MainWindow):
#                         ^^^^^^^^^^^   Change this!
    country = []
    unsaved_changes = False
    
    # DO NOT MODIFY THIS CODE
    def __init__(self, parent=None):
        super(MyForm, self).__init__(parent)
        self.setupUi(self)
        self.frameRight.hide()
        


    # END DO NOT MODIFY
        # self.comboBox_KmOrMiles.addItem("Miles")
        # self.comboBox_KmOrMiles.addItem("Km")
        
        
        self.comboBox_KmOrMiles.currentIndexChanged.connect(self.Combobox_Item_Changed)


        self.actionShow_LoadCountry.triggered.connect(self.push_load_country)
        self.pushUpdatePopulation.clicked.connect(self.push_update_population)
        ##
        # slot for when an item is selected in the list
        self.listCountry.currentRowChanged.connect(self.country_selected_from_list)
        
       # Slots for menu drop down
        self.actionExit.triggered.connect(self.exit_program)
        #self.actionshow_message.triggered.connect(self.show_message_box)
        
        #Slots for hide and show
        self.radioButton_PerKM.clicked.connect(self.kmRadio_Clicked)
        self.radioButton_PerMile.clicked.connect(self.mileRadio_Clicked)


    
        self.actionSave_to_File.triggered.connect(self.save_action_clicked)

    # ADD SLOT FUNCTIONS HERE
    # These are the functions your slots will point to
    # Indent to this level (ie. inside the class, at same level as def __init__)

    def Combobox_Item_Changed(self):
        #p_selectedIndex
        #Get selected value text from a combo
        currentArea= int(float(self.labelCountryArea.text()))
        kmArea=currentArea * 2.58999
        picked = self.comboBox_KmOrMiles.currentText()
        if picked=="Km":
            newArea=kmArea
            
        elif picked=="Miles":
            milesArea=currentArea/2.58999
            newArea=milesArea
            
        newArea=("{0:.2f}".format(newArea))
        self.labelCountryArea.setText(newArea)
     #  self.labelCountryArea.setText(str(p_selectedIndex))

    def save_action_clicked(self):
        # call the save_changes_to_file helper function which does the heavy lifting
        self.save_changes_to_file()
        # popup a message to the user confirming that the changes were saved to the file
        QMessageBox.information(self, 'Saved', 'Changes were saved to the file', QMessageBox.Ok)
        # toggle the unsaved_changes variable back to False because we no longer have any unsaved changes
        self.unsaved_changes = False





    def kmRadio_Clicked(self,enabled):
        if enabled:
            text= self.labelPopDensity.text()
            newKmPopDensity=float(text)*2.58999
            formattedNewPopDensity=("{0:.2f}".format(newKmPopDensity))
            self.labelPopDensity.setText(formattedNewPopDensity)
       

    def mileRadio_Clicked(self,enabled):
        if enabled:
            text= self.labelPopDensity.text()
            newMilesPopDensity=float(text)/2.58999
            formattedNewPopDensity=("{0:.2f}".format(newMilesPopDensity))
            self.labelPopDensity.setText(formattedNewPopDensity)
   
   
    def push_update_population(self):
        selected_index = self.listCountry.currentRow()

        try:
            i = int(self.lineEditCountryPop.text())
        except OSError:
             QMessageBox.information(self,
                                'Error',
                                'Your entered population is not an integer')
        except ValueError:
             QMessageBox.information(self,
                                'Error',
                                'Your entered population is not an integer')
        except TypeError:
             QMessageBox.information(self,
                                'Error',
                                'Your entered population is not an integer')



        self.country[selected_index][1] =self.lineEditCountryPop.text() #<- .text() gets the current value from the textbox
        self.populate_list_with_country()
        # popup a message to the user to let them know that the data was updated
        QMessageBox.information(self,
                                'Updated',
                                'Data has been updated in memory, but hasn''t been updated in the file yet',
                                QMessageBox.Ok)
        # toggle the unsaved_changes variable to True so that the program
        # prompts you to save to file when shutting down.
        self.unsaved_changes = True
      
 


    def Radio_Clicked(self):
        self.labelChooseCountry.setStyleSheet("Background-color:orange")
        self.frameRight.show()


    # ADD SLOT FUNCTIONS HERE

    def push_load_country(self):
        self.load_country_from_file()
        self.populate_list_with_country()
        
    def country_selected_from_list(self, selected_index):#<- selected_index is the index of the item that was selected in the ui list
        self.display_country_data(selected_index)
        self.frameRight.show()


    def exit_program(self):
        QApplication.closeAllWindows()


    #ADD HELPER FUNCTIONS HERE

    def load_country_from_file(self):
        self.country.clear()
        with open("Files\countries.txt", "r") as myFile:
            # load data into reader object
            fileData = csv.reader(myFile)
            # loop through each line in reader...each line is a list of values
            for row in fileData:
                self.country.append(row)

    def populate_list_with_country(self):
        self.listCountry.clear()
        for country in self.country:
            self.listCountry.addItem(country[0])
    
    def display_country_data(self, selected_index): 
        country_name = self.country[selected_index][0] 
        cFlag=country_name.replace(" ","_")
        cFlag="Flags\\"+cFlag+".png"
        image = QPixmap(cFlag)
        s=0
        area=0
        sum=0
        #collects the sum of population, can also do the total mass
        for n,p,a in self.country:
            area=area + int(float(a))
            sum =sum + int(float(p))
 
        country_pop = self.country[selected_index][1]  #<- 1 is the pop (the second value in the line)
        country_area = self.country[selected_index][2]  #<- 2 is the area (the third value in the line)

        popDensity=(float(country_pop)/float(country_area))
        formattedPopDensity=("{0:.2f}".format(popDensity))
        self.labelPopDensity.setText(formattedPopDensity)
      
        self.labelCountryName.setText(country_name)
        self.lineEditCountryPop.setText(str(country_pop))
      
        self.labelFlag.setPixmap(image)
       

        totalPopPercent=(((float(country_pop)) / sum) * 100)
        formattedTotalPopPercent=("{0:.4f}%".format(totalPopPercent))
        
        self.labelCountryArea.setText(str(country_area))
        self.labelpopPercent.setText(formattedTotalPopPercent)

    def closeEvent(self, event):

        if self.unsaved_changes == True:

            msg = "Save changes to file before closing?"
            reply = QMessageBox.question(self, 'Save?',
                     msg, QMessageBox.Yes, QMessageBox.No)

            if reply == QMessageBox.Yes:
                self.save_changes_to_file()
                event.accept()


    def save_changes_to_file(self):
        with open("Files\countries.txt", "w") as myFile:
            for country in self.country:
                myFile.write(",".join(country) + "\n")
                # wites with "," and a line break



# DO NOT MODIFY THIS CODE
if __name__ == "__main__":
    app = QApplication(sys.argv)
    the_form = MyForm()
    the_form.show()
    sys.exit(app.exec_())
# END DO NOT MODIFY