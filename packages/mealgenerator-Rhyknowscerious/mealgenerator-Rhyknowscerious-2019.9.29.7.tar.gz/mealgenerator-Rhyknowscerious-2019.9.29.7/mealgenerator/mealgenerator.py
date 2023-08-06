'''mealgenerator.py
More on this later...
'''

# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.
#
# Copyright 2019 Ryan James Decker

# IMPORTS/DEPENDENCIES
import Tkinter as tk, tkMessageBox, random, pickle, os #, ttk
from pprint import pprint, pformat
#from PIL import ImageTk, Image


# EXCEPTIONS
class RootWindowError(Exception):
    '''RootWindowError happens when you try to launch multiple applications 
    at the same time.'''
    
    def __init__(self, message):
        '''This is an error that inherits from the builtin Exception class'''
        
        super(RootWindowError, self).__init__(message)


# STATIC CLASSES
class DataModel:
    '''This is he "M" in MVC. Anything relating to the state and/or structure 
    of data goes here. Manipulating application data and the UI are handled by 
    the Controller and the View, respectively.'''
    
    meal = {
        'drink': 'None',
        'main_ingredient': 'None', 
        'main_spice': 'None',
        'side_ingredient': 'None',
        'side_spice': 'None'
    }

    ingredients = {
        'drinks': [_ingredient.lower() for _ingredient in [
            'Apple Juice',
            'Beer', 
            'Braturst', 
            'Cider', 
            'Coffee', 
            'Kombucha', 
            'Milk', 
            'Mimosa',
            'Orange Juice', 
            'Soda', 
            'Sparkling Water', 
            'Tea',
            #'Water', 
            'Wine'
        ]], 
        'main_ingredients': [_ingredient.lower() for _ingredient in [
            'Chicken', 
            'Duck', 
            'Eggplant',
            'Goat',
            'Ham',
            'Hamburger',
            'Kielbasa', 
            'Salmon',
            #'Steak',
            'Turkey', 
            'Venison'
        ]],
        'side_ingredients': [_ingredient.lower() for _ingredient in [
            'Asparagus', 
            'Beans', 
            'Brussels Sprouts',
            'Lentils', 
            'Red Potato', 
            'Lettuce', 
            'Pasta', 
            'Rice',
            'Samosas', 
            'Shrimp', 
            'Stuffed Mushrooms', 
            'Sweet Potato'
        ]],
        'spices': [_ingredient.lower() for _ingredient in [
            'Basil', 
            'Berbere', 
            'Cardamom', 
            'Cayenne', 
            'Celery Salt',  
            'Cumin', 
            'Cinnamon', 
            'Fenugreek',
            'Garam Masala', 
            'Garlic',
            'Ginger',
            'Jerk', 
            'Oregano', 
            'Lemongrass', 
            'Lemon Pepper', 
            'Paprika', 
            'Pepercorn',
            'Turmeric'
        ]]
    }

class View:
    '''This is the "V" in MVC. The static View class can create a 
    "Tkinter.Tk()" instance. If you try to launch the app twice, you'll get 
    an error because there should only be 1 instance of Tkinter.Tk() and one 
    corresponding mainloop to that instance. There is no instance constructor 
    because this is a static class.'''
    
    rootWindow = None
    
    rootWindowCount = 0
    
    editWindow = None

    childWindows = []

    @classmethod
    def initMainMenu(View, title='Meal Generator',geometry=None):
        '''This is a class method which loads tk and tcl and loads the
        root window as a Tkinter.Toplevel instance. If you run this method \
        twice, you'll get an error.'''
 
        print 'Initializing application {}...'.format(View)

        # Start the application only if it's not already running
        if View.rootWindowCount < 1 :

            # Live log output
            print('Configuring root window...')

            # Instantiate root window
            View.rootWindow = tk.Tk()

            # Live log outuput
            print(
                'Creating root window: {}...'.format(View.rootWindow)
            )

            # Live log output
            print(
                'Applying title: "{}"'.format(title)
            )

            # Apply title
            View.rootWindow.title(title)
            
            # Live log output
            print(
                'Applying window geometry: "{}"'.format(geometry)
            )

            # Apply geometry
            View.rootWindow.geometry(geometry)

            # Create main window frame
            print(
                'Creating main window frame...'
            )

            
            # Init the frame
            View.mainFrame = tk.Frame(
                View.rootWindow, 
                padx=20, 
                pady=20
                #bg='yellow',
                #image = background_image
            )
            # Pack the frame
            View.mainFrame.pack(
                fill=tk.BOTH,
                expand=True
            )
            
            # Configure grid for children

            # Set Grid row 1 to dynamically match child aspect ratio with 
            # window
            View.mainFrame.rowconfigure(
                0, weight=1
            )
            # Set Grid column 1 to do the same
            View.mainFrame.columnconfigure(
                0, weight=1
            )
            # Set Grid column 2 to do the same
            View.mainFrame.columnconfigure(
                1, weight=1
            )

            # Live log output
            print 'Main frame created: {}'.format(
                View.mainFrame
            )
            print('Applying hard-coded interface widgets.')

            # Start user definded hard-coded widgets...
            '''
            design root window here
            | | | | | | | | | | | | -------------------------------
            V V V V V V V V V V V V
            '''
            
            # Container
            # Left Frame --------
            View.leftFrame = tk.Frame(
                View.mainFrame, 
                #image=background_image,
                #bg='black'
            )
            View.leftFrame.grid(
                column=0, row=0,
                sticky = tk.N + tk.S + tk.E + tk.W
            )

            # Button in Left Frame
            View.btnGenerate = tk.Button(
                View.leftFrame,
                width=10,
                text='Generate',
                command=Controller.btnGenerateHandler
            )
            View.btnGenerate.pack(
                expand=1,
            )
            
            # Button in Left Frame
            View.btnEdit = tk.Button(
                View.leftFrame,
                width=10,
                text='Edit',
                command=Controller.btnEditHandler
            )
            View.btnEdit.pack(
                expand=1,
            )
            
            # Container
            # Right Frame ----------
            View.rightFrame = tk.Frame(
                View.mainFrame,
                #bg='gray'
            )
            View.rightFrame.grid(
                column = 1, row = 0,
                sticky = tk.N + tk.S + tk.E + tk.W
            )
            
            # Text in Right Frame
            View.lblDrink = tk.Label(
                View.rightFrame,
                width=15, # Because of stretching this doesn't need to apply to the other labels below
                text=DataModel.meal['drink'],
                anchor=tk.CENTER,
                #bg='blue',
                #fg='white'
            )
            View.lblDrink.pack(
                fill=tk.X,
                expand=1,
                padx=20
            )
            
            # Text in Right Frame
            View.lblMainSpice = tk.Label(
                View.rightFrame,
                text=DataModel.meal['main_spice'],
                anchor=tk.CENTER,
                #bg='yellow'
            )
            View.lblMainSpice.pack(
                fill=tk.X,
                expand=1,
                padx=20
            )

            # Text in Right Frame
            View.lblMainIngredient = tk.Label(
                View.rightFrame,
                text=DataModel.meal['main_ingredient'],
                anchor=tk.CENTER,
                #bg='red'
            )
            View.lblMainIngredient.pack(
                fill=tk.X,
                expand=1,
                padx=20
            )

            # Text in Right Frame
            View.lblSidespice = tk.Label(
                View.rightFrame,
                text=DataModel.meal['side_spice'],
                anchor=tk.CENTER,
                #bg='cyan'
            )
            View.lblSidespice.pack(
                fill=tk.X,
                expand=1,
                padx=20
            )

            # Text in Right Frame
            View.lblSideIngredient = tk.Label(
                View.rightFrame,
                text=DataModel.meal['side_ingredient'],
                anchor=tk.CENTER,
                #bg='green'
            )
            View.lblSideIngredient.pack(
                fill=tk.X,
                expand=1,
                padx=20
            )

            '''
            ^ ^ ^ ^ ^ ^ ^ ^ ^ ^ ^ ^
            | | | | | | | | | | | |
            design root window here
            '''

            # Start the Tk().mainloop
            print(
                'Launching application {}. Running...'.format(View)
            )
            
            # Todo: Either this shouldn't be here or all window 
            # initializations need to be handled by the Controller
            Controller.mergeIngredients()
            
            View.rootWindow.mainloop()

            print('View terminated.')
                        
            View.rootWindowCount += 1

        # If there's already a root window, raise an error
        else:

            raise RootWindowError('Only one root window allowed.')
        
    # Makes a new window
    @classmethod
    def newWindow(View, *args, **kwargs):
        '''Create child window from root window.'''
        
        print('Generating child window from root window...')

        childWindow = ChildWindow(
            master=View.rootWindow,
            *args,
            **kwargs
        )
                
        child_window_index = len(View.childWindows)
        
        print 'Appending child window to root window at index {}...'.format(
            child_window_index
        )
        
        View.childWindows.append(childWindow)
        
        return View.childWindows[child_window_index]        

    @classmethod
    def initEditWindow(View):
        '''Control what happens when you click the btnEdit button'''
                
        # Memory leak here. invoke the garbage collector to keep track of 
        # child windows
        '''
        View.newWindow() creates a new Toplevel and appends it to 
        View.childWindows. When you close this window, the childWindows array 
        does not remove this element. I think the solutoin is to use the 
        open() builtin function. The ChildWindow class needs to add the 
        special methods to enable open() functionality with this ChildWindow 
        instance.
        '''
        
        View.editWindow = View.newWindow()
        
        View.editWindow.geometry(None)
        
        View.editWindow.title('Edit Ingredients')

        # Init the frame
        View.editWindow.mainFrame = tk.Frame(
            View.editWindow, 
            padx=20, 
            pady=20
            #bg='yellow'
        )
        # Pack the frame
        View.editWindow.mainFrame.pack(
            fill=tk.BOTH,
            expand=True
        )
            
        # Configure grid for children

        # Set Grid rows to dynamically match child aspect ratio with window
        View.editWindow.mainFrame.rowconfigure(
            0, weight=1
        )
        View.editWindow.mainFrame.rowconfigure(
            1, weight=1
        )
        # Set Grid column 1 to do the same
        View.editWindow.mainFrame.columnconfigure(
            0, weight=1
        )
        # Set Grid column 2 to do the same
        View.editWindow.mainFrame.columnconfigure(
            1, weight=1
        )
        
        # Container
        # Left Frame --------
        View.editWindow.leftFrame = tk.Frame(
            View.editWindow.mainFrame,
            #bg='black'
        )
        View.editWindow.leftFrame.grid(
            column=0, row=0,
            sticky = tk.N + tk.S + tk.E + tk.W
        )
        
        # Label - Update Drink
        View.editWindow.lblUpdateDrink = tk.Label(
            View.editWindow.leftFrame,
            text='Update drink:',
            anchor=tk.CENTER,
            width=20,
            #bg='cyan'
        )
        View.editWindow.lblUpdateDrink.pack(
            fill=tk.X,
            expand=1,
            padx=20
        )
        
        # Label - Update Main Ingredient
        View.editWindow.lblUpdateMainIngredient = tk.Label(
            View.editWindow.leftFrame,
            text='Update main ingredient:',
            anchor=tk.CENTER,
            width=20,
            #bg='yellow'
        )
        View.editWindow.lblUpdateMainIngredient.pack(
            fill=tk.X,
            expand=1,
            padx=20
        )
        
        # Label - Update Side
        View.editWindow.lblUpdateSideIngredient = tk.Label(
            View.editWindow.leftFrame,
            text='Update side ingredient:',
            anchor=tk.CENTER,
            width=20, 
            #bg='blue',
            #fg='white'
        )
        View.editWindow.lblUpdateSideIngredient.pack(
            fill=tk.X,
            expand=1,
            padx=20
        )
        
        # Label - Update Spice
        View.editWindow.lblUpdateSpice = tk.Label(
            View.editWindow.leftFrame,
            text='Update spice:',
            anchor=tk.CENTER,
            width=20,
            #bg='red'
        )
        View.editWindow.lblUpdateSpice.pack(
            fill=tk.X,
            expand=1,
            padx=20
        )
        
        # Container
        # Right Frame --------
        View.editWindow.rightFrame = tk.Frame(
            View.editWindow.mainFrame,
            #bg='red'
        )
        View.editWindow.rightFrame.grid(
            column=1, row=0,
            sticky = tk.N + tk.S + tk.E + tk.W
        )
        
        # Entry - Add Drink
        View.editWindow.entryUpdateDrink = tk.Entry(
            View.editWindow.rightFrame
        )
        View.editWindow.entryUpdateDrink.pack(
            fill=tk.X,
            expand=1,
            padx=20
        )

        # Entry - Add Main Ingredient
        View.editWindow.entryUpdateMainIngredient = tk.Entry(
            View.editWindow.rightFrame
        )
        View.editWindow.entryUpdateMainIngredient.pack(
            fill=tk.X,
            expand=1,
            padx=20
        )
        
        # Entry - Add Side Ingredient
        View.editWindow.entryUpdateSideIngredient = tk.Entry(
            View.editWindow.rightFrame
        )
        View.editWindow.entryUpdateSideIngredient.pack(
            fill=tk.X,
            expand=1,
            padx=20
        )
        
        # Entry - Add Spice
        View.editWindow.entryUpdateSpice = tk.Entry(
            View.editWindow.rightFrame
        )
        View.editWindow.entryUpdateSpice.pack(
            fill=tk.X,
            expand=1,
            padx=20
        )
        
        # Container
        # Bottom Frame --------
        View.editWindow.bottomFrame = tk.Frame(
            View.editWindow.mainFrame,
            #bg='green'
        )
        View.editWindow.bottomFrame.grid(
            columnspan=2,
            column=0, row=1,
            sticky = tk.N + tk.S + tk.E + tk.W
        ) 
        
        # Button - Add ingredients
        View.editWindow.btnAddIngredients = tk.Button(
            View.editWindow.bottomFrame, 
            text='Add Ingredients',
            command=Controller.btnAddIngredientsHandler,
            width=15
        )
        View.editWindow.btnAddIngredients.pack(
            expand=1,
            padx=(0,10), 
            pady=(20,0), 
            side=tk.LEFT
        )
        
        # Button - Remove ingredients
        View.editWindow.btnRemoveIngredients = tk.Button(
            View.editWindow.bottomFrame, 
            text='Remove Ingredients',
            command=Controller.btnRemoveIngredientsHandler,
            width=15
        )
        View.editWindow.btnRemoveIngredients.pack(
            expand=1,
            padx=(10,0),
            pady=(20,0),
            side=tk.LEFT
        )

class Controller:

    # Event handler for btn_generate
    @classmethod
    def btnGenerateHandler(Controller):

        # Live log output
        print('Generating meal...')

        # Generate the meal
        DataModel.meal = Controller.generateMeal(
            DataModel.ingredients
        )

        # Live log output
        pprint(DataModel.meal)
        
        View.lblDrink.config(
            text=DataModel.meal['drink']
        )
        
        View.lblMainSpice.config(
            text=DataModel.meal['main_spice']
        )
        
        View.lblMainIngredient.config(
            text=DataModel.meal['main_ingredient']
        )
        
        View.lblSidespice.config(
            text=DataModel.meal['side_spice']
        )
        
        View.lblSideIngredient.config(
            text=DataModel.meal['side_ingredient']
        )

    @classmethod
    def generateMeal(Controller, ingredients):
    
        random_meal = {
            'main_ingredient': random.choice(
                DataModel.ingredients['main_ingredients']
            ),
            'main_spice': random.choice(
                DataModel.ingredients['spices']
            ),
            'side_ingredient': random.choice(
                DataModel.ingredients['side_ingredients']
            ),
            'side_spice': random.choice(
                DataModel.ingredients['spices']
            ),
            'drink': random.choice(
                DataModel.ingredients['drinks']
            )
        }
        
        return random_meal

    @classmethod
    def btnEditHandler(Controller):
        
        Controller.showEditWindow()
        
    @classmethod
    def showEditWindow(Controller):
        
        View.initEditWindow()
        
    @classmethod
    def btnAddIngredientsHandler(Controller):
        
        Controller.addIngredients()
    
    @classmethod
    def addIngredients(Controller):
        
        new_drink = View.editWindow.entryUpdateDrink.get()
        new_main_ingredient = View.editWindow.entryUpdateMainIngredient.get()
        new_side_ingredient = View.editWindow.entryUpdateSideIngredient.get()
        new_spice = View.editWindow.entryUpdateSpice.get()
        
        if (
            new_drink not in DataModel.ingredients['drinks'] and 
            new_drink
        ):
            
            print(
                'Adding new drink "{}" to "drinks" category...'.format(
                    new_drink
                )
            )
            
            DataModel.ingredients['drinks'].append(new_drink)
        
        if (
            new_main_ingredient not in DataModel.ingredients['main_ingredients'] and 
            new_main_ingredient
        ):
            
            print(
                'Adding new main ingredient "{}" to "main_ingredients" category...'.format(
                    new_main_ingredient
                )
            )
            
            DataModel.ingredients['main_ingredients'].append(new_main_ingredient)
        
        if (
            new_side_ingredient not in DataModel.ingredients['side_ingredients'] and 
            new_side_ingredient
        ):
            
            print(
                'Adding new side ingredient "{}" to "side_ingredients" category...'.format(
                    new_side_ingredient
                )
            )
            
            DataModel.ingredients['side_ingredients'].append(new_side_ingredient)
        
        if (
            new_spice not in DataModel.ingredients['spices'] and 
            new_spice
        ):
            
            print(
                'Adding new spice "{}" to "spices" category...'.format(
                    new_spice
                )
            )
            
            DataModel.ingredients['spices'].append(new_spice)
            
        print('Finished adding ingredients.')

        if (
            new_drink or 
            new_main_ingredient or 
            new_side_ingredient or 
            new_spice
        ):
        
            save_ingredients = tkMessageBox.askyesno(
                'Meal Generator: Ingredient Update Status',
                'Finished adding ingredients. Would you like to save your '
                'ingredients to a file?',
                master=View.editWindow
            )
            
            if save_ingredients:
                
                Controller.saveIngredients(
                    DataModel.ingredients,
                    'ingredients.file'
                )
            
            View.editWindow.entryUpdateDrink.delete(0,tk.END)
            View.editWindow.entryUpdateMainIngredient.delete(0,tk.END)
            View.editWindow.entryUpdateSideIngredient.delete(0,tk.END)
            View.editWindow.entryUpdateSpice.delete(0,tk.END)
    
    @classmethod
    def btnRemoveIngredientsHandler(Controller):
        
        Controller.removeIngredients()
    
    @classmethod
    def removeIngredients(Controller):
        
        new_drink = View.editWindow.entryUpdateDrink.get().lower()
        new_main_ingredient = View.editWindow.entryUpdateMainIngredient.get().lower()
        new_side_ingredient = View.editWindow.entryUpdateSideIngredient.get().lower()
        new_spice = View.editWindow.entryUpdateSpice.get().lower()
        
        if (
            new_drink in DataModel.ingredients['drinks'] and 
            new_drink
        ):
            
            print(
                'Removing drink "{}" to "drinks" category...'.format(
                    new_drink
                )
            )
            
            DataModel.ingredients['drinks'].remove(new_drink)
        
        if (
            new_main_ingredient in DataModel.ingredients['main_ingredients'] and 
            new_main_ingredient
        ):
            
            print(
                'Removing main ingredient "{}" to "main_ingredients" category...'.format(
                    new_main_ingredient
                )
            )
            
            DataModel.ingredients['main_ingredients'].remove(new_main_ingredient)
        
        if (
            new_side_ingredient in DataModel.ingredients['side_ingredients'] and 
            new_side_ingredient
        ):
            
            print(
                'Removing side ingredient "{}" to "side_ingredients" category...'.format(
                    new_side_ingredient
                )
            )
            
            DataModel.ingredients['side_ingredients'].remove(new_side_ingredient)
        
        if (
            new_spice in DataModel.ingredients['spices'] and 
            new_spice
        ):
            
            print(
                'Removing spice "{}" to "spices" category...'.format(
                    new_spice
                )
            )
            
            DataModel.ingredients['spices'].remove(new_spice)
            
        print('Finished removing ingredients.')

        if (
            new_drink or 
            new_main_ingredient or 
            new_side_ingredient or 
            new_spice
        ):
        
            save_ingredients = tkMessageBox.askyesno(
                'Meal Generator: Ingredient Update Status',
                'Finished removing ingredients. Would you like to save your '
                'ingredients to a file?',
                master=View.editWindow
            )
            
            if save_ingredients:
                
                Controller.saveIngredients(
                    DataModel.ingredients,
                    'ingredients.file'
                )
            
            View.editWindow.entryUpdateDrink.delete(0,tk.END)
            View.editWindow.entryUpdateMainIngredient.delete(0,tk.END)
            View.editWindow.entryUpdateSideIngredient.delete(0,tk.END)
            View.editWindow.entryUpdateSpice.delete(0,tk.END)
    
    @classmethod
    def loadIngredients(Controller, path):

        print(
            'Opening file "{}" for reading...'.format(
                path
            )
        )

        try:
        
            with open(path, "rb") as file:

                print(
                    'Loading ingredients from file "{}"'.format(
                        path
                    )
                )
            
                return pickle.load(file)
        
        except IOError, Argument:
            
            print(
                'Title: "IOError" Message: "{}"'.format(Argument)
            )
            
            tkMessageBox.showwarning(
                'Meal Generator: Warning, IOError',
                Argument,
                master=View.rootWindow
            )
    
    @classmethod
    def mergeIngredients(Controller):
        
        print('Merging built-in ingredients with ingredients from file...')
        
        ingredientSets = []
        ingredientSets.append(Controller.loadIngredients('ingredients.file'))
        ingredientSets.append(DataModel.ingredients)
        
        ingredientCategories = DataModel.ingredients.keys()
        
        if ingredientSets[0] == None:
                
            try:
                
                # Todo: Make this more symantic
                raise TypeError
            
            except TypeError:
                
                title = "Meal Generator: Warning"
                
                message = 'Could not load user-added ingredients. Showing '
                'built-in ingredients only:'
                
                print(
                    'Title: "{}"'
                    'Message: "{}"'.format(
                        title, 
                        message
                    )                
                )
                
                tkMessageBox.showwarning(
                    title,
                    message,
                    parent=View.rootWindow
                )
                        
        else:
        
            for category in ingredientCategories:
                
                print(
                    'Checking category "{}"...'.format(category)
                )
                
                for ingredient in ingredientSets[0][category]:
                
                    if ingredient not in ingredientSets[1][category]:
                        
                        print(
                            'Adding new ingredient "{}" to category "{}"...'.format(
                                ingredient, category
                            )
                        )
                        
                        ingredientSets[1][category].append(ingredient.lower())
        
        print('Ingredient merge finished.')
            
    @classmethod
    def saveIngredients(Controller, ingredients, path):

        print(
            'Opening file "{}" for writing...'.format(
                path
            )
        )
        
        with open(path, "wb") as file:
        
            print(
                'Saving ingredients to file "{}"'.format(
                    path
                )
            )
            
            pickle.dump(
                ingredients, 
                file, 
                pickle.HIGHEST_PROTOCOL
            )
            
            print(
                'Done.'
            )


# INSTANCE CLASSES

# Todo make a class for each UI window: Root-window, Edit-Window...
class ChildWindow(tk.Toplevel):

    def __init__(self, title='Child of Root Window', *args, **kwargs):

        print('Creating child window...')
        
        tk.Toplevel.__init__(self, *args, **kwargs)

        print('Applying child window title...')
        
        self.title(title)
        
        self.childWindows = []

    def newWindow(self, title='Child of Child Window', *args, **kwargs):
        
        print('Generating child window from child window...')
        
        child_window = ChildWindow(self)
        
        child_window.geometry('100x100')

        print('Adding child window to child window...')
        
        child_window_index = len(self.childWindows)
        
        self.childWindows.append(child_window)
        
        return self.childWindows[child_window_index]


# MODULE METHODS
def launch():
    
    View.initMainMenu()

# SCRIPT MODULE ROUTINE
if __name__ == '__main__':
    
    launch()

