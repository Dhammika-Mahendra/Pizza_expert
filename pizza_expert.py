from pyswip import Prolog
import tkinter as tk
from tkinter import ttk, messagebox

class PizzaExpertSystem:
    def __init__(self, kb_file="pizza_expert.pl"):
        """Initialize the Prolog engine and load knowledge base"""
        self.prolog = Prolog()
        self.prolog.consult(kb_file)
    
    def get_essential_base_ingredients(self):
        """Get list of essential base ingredients"""
        ingredients = []
        for result in self.prolog.query("essential_base(X)"):
            ingredients.append(result["X"])
        return ingredients
    
    def get_extra_base_ingredients(self):
        """Get list of extra base ingredients"""
        ingredients = []
        for result in self.prolog.query("extra_base(X)"):
            ingredients.append(result["X"])
        return ingredients
    
    def get_topping_ingredients(self):
        """Get list of all topping ingredients"""
        ingredients = []
        for result in self.prolog.query("topping_ingredient(X)"):
            ingredients.append(result["X"])
        return ingredients
    
    def check_essential_base(self, user_base):
        """Check if user has all essential base ingredients"""
        prolog_list = self._python_list_to_prolog(user_base)
        query = f"has_essential_base({prolog_list})"
        result = list(self.prolog.query(query))
        return len(result) > 0
    
    def find_missing_extra(self, user_base):
        """Find missing extra base ingredients"""
        prolog_list = self._python_list_to_prolog(user_base)
        query = f"find_missing_extra({prolog_list}, Missing)"
        results = list(self.prolog.query(query))
        if results:
            return results[0]["Missing"]
        return []
    
    def get_missing_extra_effect(self, ingredient):
        """Get effect message for missing extra ingredient"""
        query = f"missing_extra_effect({ingredient}, Effect)"
        results = list(self.prolog.query(query))
        if results:
            effect = results[0]["Effect"]
            # Handle bytes object returned by PySwip
            if isinstance(effect, bytes):
                effect = effect.decode('utf-8')
            return effect
        return None
    
    def find_makeable_pizzas(self, user_toppings):
        """Find all pizzas that can be made with given toppings"""
        prolog_list = self._python_list_to_prolog(user_toppings)
        query = f"find_makeable_pizzas({prolog_list}, Pizzas)"
        results = list(self.prolog.query(query))
        if results:
            return results[0]["Pizzas"]
        return []
    
    def get_user_extras(self, user_base):
        """Get which extra ingredients user has"""
        prolog_list = self._python_list_to_prolog(user_base)
        query = f"get_user_extras({prolog_list}, Extras)"
        results = list(self.prolog.query(query))
        if results:
            return results[0]["Extras"]
        return []
    
    def generate_steps(self, pizza_type, user_extras):
        """Generate complete step list for chosen pizza"""
        extras_list = self._python_list_to_prolog(user_extras)
        query = f"generate_steps({pizza_type}, {extras_list}, Steps)"
        results = list(self.prolog.query(query))
        if results:
            steps = results[0]["Steps"]
            # Handle bytes objects in step list
            decoded_steps = []
            for step in steps:
                if isinstance(step, bytes):
                    decoded_steps.append(step.decode('utf-8'))
                else:
                    decoded_steps.append(step)
            return decoded_steps
        return []
    
    def get_pizza_types(self):
        """Get list of available pizza types"""
        query = "get_pizza_types(PizzaTypes)"
        results = list(self.prolog.query(query))
        if results:
            return results[0]["PizzaTypes"]
        return []
    
    def get_pizza_ingredients(self, pizza_type):
        """Get all ingredients needed for a specific pizza type"""
        query = f"get_pizza_ingredients({pizza_type}, AllIngredients)"
        results = list(self.prolog.query(query))
        if results:
            return results[0]["AllIngredients"]
        return []
    
    def _python_list_to_prolog(self, py_list):
        """Convert Python list to Prolog list format"""
        return "[" + ",".join(py_list) + "]"


class PizzaGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("🍕 Pizza Maker Expert System")
        self.root.geometry("600x600")
        self.root.configure(bg="#f0f0f0")
        
        # Initialize expert system
        try:
            self.expert = PizzaExpertSystem("pizza_expert.pl")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to load knowledge base:\n{e}")
            root.destroy()
            return
        
        self.user_base = []
        self.user_toppings = []
        self.chosen_pizza = None
        
        # Start with welcome screen
        self.show_welcome_screen()
    
    def clear_window(self):
        """Clear all widgets from window"""
        for widget in self.root.winfo_children():
            widget.destroy()
    
    ##################################################################################
    #        welcome screen
    ##################################################################################

    def show_welcome_screen(self):
        """Welcome screen with two main choices"""
        self.clear_window()
        
        # Title
        title = tk.Label(self.root, text="🍕 Pizza Maker Expert System", 
                        font=("Arial", 24, "bold"), bg="#f0f0f0", fg="#333")
        title.pack(pady=50)
        
        
        # Main choices frame
        choices_frame = tk.Frame(self.root, bg="#f0f0f0")
        choices_frame.pack(pady=10)
        
        # Option A: I already have ingredients
        have_btn = tk.Button(choices_frame, 
                            text="start making pizza", 
                            command=self.show_base_ingredients,
                            font=("Arial", 14, "bold"), bg="#4CAF50", fg="white",
                            padx=40, pady=30, cursor="hand2", relief=tk.RAISED, bd=3,
                            wraplength=300, justify="center")
        have_btn.pack(pady=20)
        
        # Option B: Show me ingredients
        show_btn = tk.Button(choices_frame, 
                            text="show Me Ingredients", 
                            command=self.show_ingredients_info,
                            font=("Arial", 14, "bold"), bg="#2196F3", fg="white",
                            padx=40, pady=30, cursor="hand2", relief=tk.RAISED, bd=3,
                            wraplength=300, justify="center")
        show_btn.pack(pady=20)


    ##################################################################################
    #         Pizza type selection for ingredients information
    ##################################################################################
    
    def show_ingredients_info(self):
        """Show pizza type selection for ingredients information"""
        self.clear_window()
        
        # Title
        title = tk.Label(self.root, text="Pizza Ingredients Information", 
                        font=("Arial", 12, "bold"), bg="#f0f0f0", fg="#666")
        title.pack(pady=30)
        
        # Instruction
        instruction = tk.Label(self.root, text="Select a pizza type :", 
                              font=("Arial", 12), bg="#f0f0f0", fg="#666")
        instruction.pack(pady=20)
        
        # Main content frame
        frame = tk.Frame(self.root, bg="white", relief=tk.RIDGE, bd=2)
        frame.pack(pady=20, padx=40, fill=tk.BOTH, expand=True)
        
        # Get available pizza types
        pizza_types = self.expert.get_pizza_types()
        
        # Create buttons for each pizza type
        for pizza_type in pizza_types:
            btn = tk.Button(frame, 
                           text=f"{pizza_type.replace('_', ' ').title()} Pizza", 
                           command=lambda p=pizza_type: self.show_pizza_ingredients(p),
                           font=("Arial", 12, "bold"), bg="green", fg="white",
                           padx=30, pady=15, cursor="hand2", relief=tk.RAISED, bd=2)
            btn.pack(pady=15, padx=20, fill=tk.X)
        
        # Navigation buttons
        buttons_frame = tk.Frame(self.root, bg="#f0f0f0")
        buttons_frame.pack(pady=20)
        
        # Back to welcome button
        back_btn = tk.Button(buttons_frame, text="← Back", 
                            command=self.show_welcome_screen,
                            font=("Arial", 12, "bold"), bg="#4CAF50", fg="white",
                            padx=20, pady=10, cursor="hand2")
        back_btn.pack(side=tk.LEFT, padx=10)
    
    ##################################################################################
    #        Show Ingredients Info
    ##################################################################################
    
    def show_pizza_ingredients(self, pizza_type):
        """Show all ingredients needed for selected pizza type"""
        self.clear_window()
        
        # Title
        title = tk.Label(self.root, 
                        text=f"Ingredients for {pizza_type.replace('_', ' ').title()} Pizza", 
                        font=("Arial", 12, "bold"), bg="#f0f0f0", fg="#333")
        title.pack(pady=20)
        
        # Main content frame (matching other views structure)
        frame = tk.Frame(self.root, bg="white", relief=tk.RIDGE, bd=2)
        frame.pack(pady=20, padx=40, fill=tk.BOTH, expand=True)
        
        # Get all ingredients for this pizza type
        all_ingredients = self.expert.get_pizza_ingredients(pizza_type)
        essential = self.expert.get_essential_base_ingredients()
        extra = self.expert.get_extra_base_ingredients()
        
        # Essential Base Ingredients Section
        essential_title = tk.Label(frame, text="Essentials:", 
                                  font=("Arial", 12,"bold"), bg="white", fg="#666")
        essential_title.pack(anchor="w", padx=20, pady=(20, 10))
        
        for ing in essential:
            ingredient_label = tk.Label(frame, text=f"◦ {ing.replace('_', ' ').title()}", 
                                       font=("Arial", 12), bg="white", fg="#666")
            ingredient_label.pack(anchor="w", padx=40, pady=2)
        
        # Extra Base Ingredients Section
        extra_title = tk.Label(frame, text="\nExtra:", 
                              font=("Arial", 12, "bold"), bg="white", fg="#666")
        extra_title.pack(anchor="w", padx=20, pady=(20, 10))
        
        for ing in extra:
            ingredient_label = tk.Label(frame, text=f"◦ {ing.replace('_', ' ').title()}", 
                                       font=("Arial", 12), bg="white", fg="#666")
            ingredient_label.pack(anchor="w", padx=40, pady=2)
        
        # Required Toppings Section
        pizza_toppings = [ing for ing in all_ingredients if ing not in essential and ing not in extra]
        
        if pizza_toppings:
            toppings_title = tk.Label(frame, text=f"\nToppings for {pizza_type.replace('_', ' ').title()}:", 
                                     font=("Arial", 12, "bold"), bg="white", fg="#666")
            toppings_title.pack(anchor="w", padx=20, pady=(20, 10))
            
            for ing in pizza_toppings:
                ingredient_label = tk.Label(frame, text=f"◦ {ing.replace('_', ' ').title()}", 
                                           font=("Arial", 12), bg="white", fg="#666")
                ingredient_label.pack(anchor="w", padx=40, pady=2)
        
        # Navigation buttons
        buttons_frame = tk.Frame(self.root, bg="#f0f0f0")
        buttons_frame.pack(pady=20)
        
        # Back button
        back_btn = tk.Button(buttons_frame, text="← Back", 
                            command=self.show_ingredients_info,
                            font=("Arial", 12, "bold"), bg="#4CAF50", fg="white",
                            padx=20, pady=10, cursor="hand2")
        back_btn.pack(side=tk.LEFT, padx=10)
    
    ##################################################################################
    #        Show Base Ingredients
    ##################################################################################
    
    def show_base_ingredients(self):
        """Screen 1: Select base ingredients"""
        self.clear_window()
        
        subtitle = tk.Label(self.root, text="STEP 1: Select Base Ingredients", 
                           font=("Arial", 12, "bold"), bg="#f0f0f0", fg="#666")
        subtitle.pack(pady=10)
        
        # Frame for checkboxes
        frame = tk.Frame(self.root, bg="white", relief=tk.RIDGE, bd=2)
        frame.pack(pady=20, padx=40, fill=tk.BOTH, expand=True)
        
        # Get ingredients
        essential = self.expert.get_essential_base_ingredients()
        extra = self.expert.get_extra_base_ingredients()
        
        # Essential section        
        self.base_vars = {}
        for ing in essential:
            var = tk.BooleanVar()
            cb = tk.Checkbutton(frame, text=ing.replace("_", " ").title(), 
                               variable=var, font=("Arial", 11), bg="white")
            cb.pack(anchor="w", padx=40, pady=2)
            self.base_vars[ing] = var
        
        # Extra section  
        for ing in extra:
            var = tk.BooleanVar()
            cb = tk.Checkbutton(frame, text=ing.replace("_", " ").title(), 
                               variable=var, font=("Arial", 11), bg="white")
            cb.pack(anchor="w", padx=40, pady=2)
            self.base_vars[ing] = var
        
        # Next button
        next_btn = tk.Button(self.root, text="Next →", command=self.analyze_base,
                            font=("Arial", 12, "bold"), bg="#4CAF50", fg="white",
                            padx=30, pady=10, cursor="hand2")
        next_btn.pack(pady=20)
    
    def analyze_base(self):
        """Analyze base ingredients and show results"""
        # Get selected ingredients
        self.user_base = [ing for ing, var in self.base_vars.items() if var.get()]
        
        if not self.user_base:
            messagebox.showwarning("No Selection", "Please select at least one ingredient!")
            return
        
        # Check essentials
        has_essential = self.expert.check_essential_base(self.user_base)
        
        if not has_essential:
            # Show missing ingredients view instead of popup
            self.show_missing_ingredients_view()
            return
        
        # Show results
        self.show_base_results()
    
    def show_missing_ingredients_view(self):
        """Show view when user is missing essential base ingredients"""
        self.clear_window()
        
        # Frame for missing ingredients
        frame = tk.Frame(self.root, bg="white", relief=tk.RIDGE, bd=2)
        frame.pack(pady=20, padx=40, fill=tk.BOTH, expand=True)

        # missing message
        miss = tk.Label(frame, text="❌ Missing Essential Ingredients", 
                          font=("Arial", 12, "bold"), bg="white", fg="red")
        miss.pack(pady=20)
        
        # Get essential ingredients
        essential = self.expert.get_essential_base_ingredients()
        
        info_label = tk.Label(frame, text="To make a pizza base, you need ALL of these essential ingredients:", 
                             font=("Arial", 12), bg="white", fg="#666")
        info_label.pack(pady=(20, 10))
        
        # List essential ingredients
        for ing in essential:
            ingredient_label = tk.Label(frame, text=f"• {ing.replace('_', ' ').title()}", 
                                       font=("Arial", 12), bg="white", fg="#666")
            ingredient_label.pack(anchor="w", padx=40, pady=5)
        
        # Buttons frame
        buttons_frame = tk.Frame(self.root, bg="#f0f0f0")
        buttons_frame.pack(pady=20)
        
        # See ingredients button
        see_ingredients_btn = tk.Button(buttons_frame, text="📋 See Ingredients", 
                                       command=self.show_ingredients_info,
                                       font=("Arial", 12, "bold"), bg="#2196F3", fg="white",
                                       padx=20, pady=10, cursor="hand2")
        see_ingredients_btn.pack(side=tk.LEFT, padx=10)
        
        # Quit button
        quit_btn = tk.Button(buttons_frame, text="❌ Quit", 
                            command=self.quit_application,
                            font=("Arial", 12, "bold"), bg="#f44336", fg="white",
                            padx=30, pady=10, cursor="hand2")
        quit_btn.pack(side=tk.LEFT, padx=10)

    def quit_application(self):
        """Quit the application"""
        self.root.quit()
        self.root.destroy()
    
    def show_base_results(self):
        """Show base analysis results"""
        self.clear_window()
        
        # Results frame
        frame = tk.Frame(self.root, bg="white", relief=tk.RIDGE, bd=2)
        frame.pack(pady=20, padx=40, fill=tk.BOTH, expand=True)
        
        # Success message
        success = tk.Label(frame, text="✅ A basic pizza base is fine", 
                          font=("Arial", 12, "bold"), bg="white", fg="green")
        success.pack(pady=20)
        
        # Check for missing extras
        missing_extra = self.expert.find_missing_extra(self.user_base)
        
        if missing_extra:
            warning = tk.Label(frame, text="⚠️ Missing Extra Ingredients:", 
                             font=("Arial", 12, "bold"), bg="white", fg="orange")
            warning.pack(anchor="w", padx=20, pady=(20, 10))
            
            for ing in missing_extra:
                effect = self.expert.get_missing_extra_effect(ing)
                text = f"• {ing.replace('_', ' ').title()}: {effect}"
                label = tk.Label(frame, text=text, font=("Arial", 10), 
                               bg="white", fg="#666", wraplength=500, justify="left")
                label.pack(anchor="w", padx=40, pady=2)
        
        # Buttons frame
        buttons_frame = tk.Frame(self.root, bg="#f0f0f0")
        buttons_frame.pack(pady=20)
        
        # Back button
        back_btn = tk.Button(buttons_frame, text="← Back", 
                            command=self.show_base_ingredients,
                            font=("Arial", 12, "bold"), bg="#666", fg="white",
                            padx=30, pady=10, cursor="hand2")
        back_btn.pack(side=tk.LEFT, padx=10)

        # Continue button
        continue_btn = tk.Button(buttons_frame, text="Next →", 
                                command=self.show_topping_ingredients,
                                font=("Arial", 12, "bold"), bg="#4CAF50", fg="white",
                                padx=30, pady=10, cursor="hand2")
        continue_btn.pack(side=tk.LEFT, padx=10)

    
    def show_topping_ingredients(self):
        """Screen 2: Select topping ingredients"""
        self.clear_window()
        
        # Title
        title = tk.Label(self.root, text="STEP 2: Select Topping Ingredients", 
                        font=("Arial", 12, "bold"), bg="#f0f0f0", fg="#333")
        title.pack(pady=20)
        
        # Frame for checkboxes
        frame = tk.Frame(self.root, bg="white", relief=tk.RIDGE, bd=2)
        frame.pack(pady=20, padx=40, fill=tk.BOTH, expand=True)
        
        # Get topping ingredients
        toppings = self.expert.get_topping_ingredients()
        
        
        self.topping_vars = {}
        for ing in toppings:
            var = tk.BooleanVar()
            cb = tk.Checkbutton(frame, text=ing.replace("_", " ").title(), 
                               variable=var, font=("Arial", 11), bg="white")
            cb.pack(anchor="w", padx=40, pady=2)
            self.topping_vars[ing] = var
        
        # Analyze button
        analyze_btn = tk.Button(self.root, text="Next →", 
                               command=self.analyze_toppings,
                               font=("Arial", 12, "bold"), bg="#4CAF50", fg="white",
                               padx=30, pady=10, cursor="hand2")
        analyze_btn.pack(pady=20)
    
    def analyze_toppings(self):
        """Analyze toppings and show makeable pizzas"""
        # Get selected toppings
        self.user_toppings = [ing for ing, var in self.topping_vars.items() if var.get()]
        
        if not self.user_toppings:
            messagebox.showwarning("No Selection", "Please select at least one topping!")
            return
        
        # Find makeable pizzas
        makeable_pizzas = self.expert.find_makeable_pizzas(self.user_toppings)
        
        if not makeable_pizzas:
            # Navigate to missing toppings view instead of popup
            self.show_missing_toppings_view()
            return
        
        self.show_pizza_selection(makeable_pizzas)
    
    def show_missing_toppings_view(self):
        """Show view when user is missing required toppings"""
        self.clear_window()
        
        # Frame for information
        frame = tk.Frame(self.root, bg="white", relief=tk.RIDGE, bd=2)
        frame.pack(pady=20, padx=40, fill=tk.BOTH, expand=True)
        
                # Success message
        miss = tk.Label(frame, text="❌ Missing Required Toppings", 
                          font=("Arial", 12, "bold"), bg="white", fg="red")
        miss.pack(pady=20)

        # Information message
        info_label = tk.Label(frame, text="Cannot make any pizza with the toppings you have selected.", 
                             font=("Arial", 12), bg="white", fg="#666")
        info_label.pack(pady=(20, 10))
        
        # Show selected toppings
        if self.user_toppings:
            selected_label = tk.Label(frame, text="Your selected toppings:", 
                                     font=("Arial", 12, "bold"), bg="white", fg="#333")
            selected_label.pack(pady=(20, 10))
            
            for topping in self.user_toppings:
                topping_label = tk.Label(frame, text=f"• {topping.replace('_', ' ').title()}", 
                                        font=("Arial", 11), bg="white", fg="#666")
                topping_label.pack(anchor="w", padx=40, pady=2)
        
        # Buttons frame
        buttons_frame = tk.Frame(self.root, bg="#f0f0f0")
        buttons_frame.pack(pady=20)
        
        # See ingredients button
        see_ingredients_btn = tk.Button(buttons_frame, text="📋 See Ingredients", 
                                       command=self.show_ingredients_info,
                                       font=("Arial", 12, "bold"), bg="#2196F3", fg="white",
                                       padx=20, pady=10, cursor="hand2")
        see_ingredients_btn.pack(side=tk.LEFT, padx=10)
        
        # Quit button
        quit_btn = tk.Button(buttons_frame, text="❌ Quit", 
                            command=self.quit_application,
                            font=("Arial", 12, "bold"), bg="#f44336", fg="white",
                            padx=30, pady=10, cursor="hand2")
        quit_btn.pack(side=tk.LEFT, padx=10)
    
    def show_pizza_selection(self, makeable_pizzas):
        """Screen 3: Choose pizza type"""
        self.clear_window()
        
        # Title
        title = tk.Label(self.root, text="STEP 3: Select Pizza Type", 
                        font=("Arial", 12, "bold"), bg="#f0f0f0", fg="#666")
        title.pack(pady=20)
        
        subtitle = tk.Label(self.root, 
                           text=f"✅ You can make {len(makeable_pizzas)} pizza type(s):", 
                           font=("Arial", 12), bg="#f0f0f0", fg="green")
        subtitle.pack(pady=10)
        
        # Frame for pizza buttons
        frame = tk.Frame(self.root, bg="white", relief=tk.RIDGE, bd=2)
        frame.pack(pady=20, padx=40, fill=tk.BOTH, expand=True)
        
        # Create button for each pizza
        for pizza in makeable_pizzas:
            btn = tk.Button(frame, text=pizza.replace("_", " ").title() + " Pizza", 
                           command=lambda p=pizza: self.select_pizza(p),
                           font=("Arial", 12, "bold"), bg="green", fg="white",
                           padx=20, pady=15, cursor="hand2", relief=tk.RAISED, bd=3)
            btn.pack(pady=10, padx=30, fill=tk.X)
        
        # Navigation buttons
        buttons_frame = tk.Frame(self.root, bg="#f0f0f0")
        buttons_frame.pack(pady=20)
        
        # Back button
        back_btn = tk.Button(buttons_frame, text="← Back", 
                            command=self.show_topping_ingredients,
                            font=("Arial", 12, "bold"), bg="#666", fg="white",
                            padx=30, pady=10, cursor="hand2")
        back_btn.pack(side=tk.LEFT, padx=10)
    
    def select_pizza(self, pizza_type):
        """Select pizza and show steps"""
        self.chosen_pizza = pizza_type
        self.show_steps()
    
    def show_steps(self):
        """Screen 4: Show preparation steps"""
        self.clear_window()
        
        # Title
        title = tk.Label(self.root, 
                        text=f"Steps to Make {self.chosen_pizza.replace('_', ' ').title()} pizza", 
                        font=("Arial", 12, "bold"), bg="#f0f0f0", fg="#666")
        title.pack(pady=20)
        
        # Frame for steps
        frame = tk.Frame(self.root, bg="white", relief=tk.RIDGE, bd=2)
        frame.pack(pady=20, padx=40, fill=tk.BOTH, expand=True)
        
        # Get steps from Prolog
        user_extras = self.expert.get_user_extras(self.user_base)
        steps = self.expert.generate_steps(self.chosen_pizza, user_extras)
        
        # Display each step
        for i, step in enumerate(steps, 1):
            step_label = tk.Label(frame, text=f"{i}. {step}", 
                                 font=("Arial", 11), bg="white", fg="#333",
                                 wraplength=500, justify="left")
            step_label.pack(anchor="w", padx=20, pady=8)
        
        # Navigation buttons
        buttons_frame = tk.Frame(self.root, bg="#f0f0f0")
        buttons_frame.pack(pady=20)
        
        # Back button
        back_btn = tk.Button(buttons_frame, text="← Back", 
                            command=lambda: self.show_pizza_selection(self.expert.find_makeable_pizzas(self.user_toppings)),
                            font=("Arial", 12, "bold"), bg="#666", fg="white",
                            padx=30, pady=10, cursor="hand2")
        back_btn.pack(side=tk.LEFT, padx=10)
        
        # Restart button
        restart_btn = tk.Button(buttons_frame, text="🔄 Start Over", 
                               command=self.show_base_ingredients,
                               font=("Arial", 12, "bold"), bg="#f44336", fg="white",
                               padx=30, pady=10, cursor="hand2")
        restart_btn.pack(side=tk.LEFT, padx=10)


def main():
    root = tk.Tk()
    app = PizzaGUI(root)
    root.mainloop()


if __name__ == "__main__":
    main()