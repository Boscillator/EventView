from tkinter import *
from tkinter.ttk import *
import matplotlib.pyplot as plt

class ParticalTree(object):
    """description of class"""

    def __init__(self,root,df,momentumScale = 1):
        """
        Creates a ParticalTree object
        Args:
            root (Tk): the root object to append to.
            eventReader (Dataframe): A dataframe for the event file.
        """
        self.tree = Treeview(root)
        self.df = df
        self.ms = momentumScale

        fieldnames = list(self.df.columns.values)
        self.tree['columns'] = fieldnames

        self.tree.column('#0',width=100)
        #Configure every column
        for field in fieldnames:
            self.tree.column(field,width=80)
            self.tree.heading(field, text=field)

        for i,row in self.df.iterrows():
            values = [row[field] for field in fieldnames]
            #if not (tree.exists(row['mother1'])):
            if not self.tree.exists(row['mother1']):
                parent = ''
            else:
                parent = row['mother1']
            self.tree.insert(
                iid = row["id"],  #give this the id of the partical id
                index = 'end',  #append it to the end of the list,
                parent=parent, #make it root TODO: do correct mothering
                text='', #no heading text
                values=values #user the data to populate the tree
                )

        self.tree.bind('<<TreeviewSelect>>',self.handelSelect)
        self.tree.pack()

    def getChildren(self,id):
        """
        Gets a list of all the children, and their children and so on of a row in the tree.
        Args:
            id (float): The id of the partical you want to get.
        Returns:
            (float[]): The list of ids of the children.
        """
        children = list(self.tree.get_children(id))
        grandChildren = []
        for child in children:
            grandChildren.extend(self.getChildren(child))

        children.extend(grandChildren)  #Merge the two lists
        return children

    def getSelection(self):
        """
        Returns the id of the selected rows, their children, thier grandchildren etc.
        Retruns:
            (float[]): List of the selected ids
        """
        rawSelection = self.tree.selection()
        selection = []
        for row in rawSelection:
            selection.extend(self.getChildren(row))
        selection.extend(rawSelection)
        return selection

    def handelSelect(self,event):
        plt.clf()
        selection = self.getSelection()
        self.plotSelection(selection)

    def plotSelection(self,selection):
        for particalId in selection:
            print('.',end="",flush=True)
            particals = self.df[self.df["id"] == float(particalId)]
            for i,partical in particals.iterrows():
                x = [partical['xProd'], (partical['xProd'] + partical['px']) * self.ms]
                y = [partical['yProd'], (partical['yProd'] + partical['py']) * self.ms]
                plt.plot(x,y)
        plt.show()
        print("")