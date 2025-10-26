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
            return results[0]["Effect"]
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
            return results[0]["Steps"]
        return []
    
    def _python_list_to_prolog(self, py_list):
        """Convert Python list to Prolog list format"""
        return "[" + ",".join(py_list) + "]"


class PizzaGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("🍕 Pizza Maker Expert System")
        self.root.geometry("600x700")
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
        
        # Start with base ingredients screen
        self.show_base_ingredients()
    
    def clear_window(self):
        """Clear all widgets from window"""
        for widget in self.root.winfo_children():
            widget.destroy()
    
    def show_base_ingredients(self):
        """Screen 1: Select base ingredients"""
        self.clear_window()
        
        # Title
        title = tk.Label(self.root, text="🍕 Pizza Maker Expert System", 
                        font=("Arial", 20, "bold"), bg="#f0f0f0", fg="#333")
        title.pack(pady=20)
        
        subtitle = tk.Label(self.root, text="STEP 1: Select Base Ingredients", 
                           font=("Arial", 14), bg="#f0f0f0", fg="#666")
        subtitle.pack(pady=10)
        
        # Frame for checkboxes
        frame = tk.Frame(self.root, bg="white", relief=tk.RIDGE, bd=2)
        frame.pack(pady=20, padx=40, fill=tk.BOTH, expand=True)
        
        # Get ingredients
        essential = self.expert.get_essential_base_ingredients()
        extra = self.expert.get_extra_base_ingredients()
        
        # Essential section
        essential_label = tk.Label(frame, text="Essential Ingredients:", 
                                   font=("Arial", 12, "bold"), bg="white")
        essential_label.pack(anchor="w", padx=20, pady=(20, 5))
        
        self.base_vars = {}
        for ing in essential:
            var = tk.BooleanVar()
            cb = tk.Checkbutton(frame, text=ing.replace("_", " ").title(), 
                               variable=var, font=("Arial", 11), bg="white")
            cb.pack(anchor="w", padx=40, pady=2)
            self.base_vars[ing] = var
        
        # Extra section
        extra_label = tk.Label(frame, text="\nExtra Ingredients:", 
                              font=("Arial", 12, "bold"), bg="white")
        extra_label.pack(anchor="w", padx=20, pady=(10, 5))
        
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
        
        # Title
        title = tk.Label(self.root, text="❌ Missing Essential Ingredients", 
                        font=("Arial", 18, "bold"), bg="#f0f0f0", fg="#d32f2f")
        title.pack(pady=30)
        
        # Main message
        message = tk.Label(self.root, text="You miss basic ingredients", 
                          font=("Arial", 16, "bold"), bg="#f0f0f0", fg="#333")
        message.pack(pady=20)
        
        # Frame for missing ingredients
        frame = tk.Frame(self.root, bg="white", relief=tk.RIDGE, bd=2)
        frame.pack(pady=20, padx=40, fill=tk.BOTH, expand=True)
        
        # Get essential ingredients
        essential = self.expert.get_essential_base_ingredients()
        
        info_label = tk.Label(frame, text="To make a pizza base, you need ALL of these essential ingredients:", 
                             font=("Arial", 12), bg="white", fg="#666")
        info_label.pack(pady=(20, 10))
        
        # List essential ingredients
        for ing in essential:
            ingredient_label = tk.Label(frame, text=f"• {ing.replace('_', ' ').title()}", 
                                       font=("Arial", 14, "bold"), bg="white", fg="#d32f2f")
            ingredient_label.pack(anchor="w", padx=40, pady=5)
        
        # Help message
        help_msg = tk.Label(frame, text="\nWhat would you like to do?", 
                           font=("Arial", 12, "bold"), bg="white", fg="#333")
        help_msg.pack(pady=20)
        
        # Buttons frame
        buttons_frame = tk.Frame(self.root, bg="#f0f0f0")
        buttons_frame.pack(pady=20)
        
        # List missing ingredients button
        list_btn = tk.Button(buttons_frame, text="📋 List Missing Ingredients", 
                            command=self.show_missing_ingredients_list,
                            font=("Arial", 12, "bold"), bg="#FF9800", fg="white",
                            padx=20, pady=10, cursor="hand2")
        list_btn.pack(side=tk.LEFT, padx=10)
        
        # Quit button
        quit_btn = tk.Button(buttons_frame, text="❌ Quit", 
                            command=self.quit_application,
                            font=("Arial", 12, "bold"), bg="#f44336", fg="white",
                            padx=30, pady=10, cursor="hand2")
        quit_btn.pack(side=tk.LEFT, padx=10)
    
    def show_missing_ingredients_list(self):
        """Show detailed list of missing ingredients (placeholder view)"""
        self.clear_window()
        
        # Title
        title = tk.Label(self.root, text="📋 Missing Ingredients List", 
                        font=("Arial", 18, "bold"), bg="#f0f0f0", fg="#333")
        title.pack(pady=30)
        
        # Main content frame
        frame = tk.Frame(self.root, bg="white", relief=tk.RIDGE, bd=2)
        frame.pack(pady=20, padx=40, fill=tk.BOTH, expand=True)
        
        # Placeholder message
        message = tk.Label(frame, text="This is a placeholder view for the missing ingredients list.", 
                          font=("Arial", 14), bg="white", fg="#666")
        message.pack(pady=50)
        
        sub_message = tk.Label(frame, text="Logic will be added later.", 
                              font=("Arial", 12, "italic"), bg="white", fg="#999")
        sub_message.pack(pady=10)
        
        # Back button
        back_btn = tk.Button(self.root, text="← Back", 
                            command=self.show_missing_ingredients_view,
                            font=("Arial", 12, "bold"), bg="#607D8B", fg="white",
                            padx=30, pady=10, cursor="hand2")
        back_btn.pack(pady=20)
    
    def quit_application(self):
        """Quit the application"""
        self.root.quit()
        self.root.destroy()
    
    def show_base_results(self):
        """Show base analysis results"""
        self.clear_window()
        
        # Title
        title = tk.Label(self.root, text="Base Analysis Results", 
                        font=("Arial", 18, "bold"), bg="#f0f0f0", fg="#333")
        title.pack(pady=20)
        
        # Results frame
        frame = tk.Frame(self.root, bg="white", relief=tk.RIDGE, bd=2)
        frame.pack(pady=20, padx=40, fill=tk.BOTH, expand=True)
        
        # Success message
        success = tk.Label(frame, text="✅ A basic pizza base is fine", 
                          font=("Arial", 14, "bold"), bg="white", fg="green")
        success.pack(pady=20)
        
        # Check for missing extras
        missing_extra = self.expert.find_missing_extra(self.user_base)
        
        if missing_extra:
            warning = tk.Label(frame, text="⚠️  Missing Extra Ingredients:", 
                             font=("Arial", 12, "bold"), bg="white", fg="orange")
            warning.pack(pady=(20, 10))
            
            for ing in missing_extra:
                effect = self.expert.get_missing_extra_effect(ing)
                text = f"• {ing.replace('_', ' ').title()}: {effect}"
                label = tk.Label(frame, text=text, font=("Arial", 10), 
                               bg="white", fg="#666", wraplength=500, justify="left")
                label.pack(anchor="w", padx=40, pady=2)
        
        # Continue button
        continue_btn = tk.Button(self.root, text="Continue to Toppings →", 
                                command=self.show_topping_ingredients,
                                font=("Arial", 12, "bold"), bg="#4CAF50", fg="white",
                                padx=30, pady=10, cursor="hand2")
        continue_btn.pack(pady=20)
    
    def show_topping_ingredients(self):
        """Screen 2: Select topping ingredients"""
        self.clear_window()
        
        # Title
        title = tk.Label(self.root, text="STEP 2: Select Topping Ingredients", 
                        font=("Arial", 16, "bold"), bg="#f0f0f0", fg="#333")
        title.pack(pady=20)
        
        # Frame for checkboxes
        frame = tk.Frame(self.root, bg="white", relief=tk.RIDGE, bd=2)
        frame.pack(pady=20, padx=40, fill=tk.BOTH, expand=True)
        
        # Get topping ingredients
        toppings = self.expert.get_topping_ingredients()
        
        label = tk.Label(frame, text="Available Toppings:", 
                        font=("Arial", 12, "bold"), bg="white")
        label.pack(anchor="w", padx=20, pady=(20, 10))
        
        self.topping_vars = {}
        for ing in toppings:
            var = tk.BooleanVar()
            cb = tk.Checkbutton(frame, text=ing.replace("_", " ").title(), 
                               variable=var, font=("Arial", 11), bg="white")
            cb.pack(anchor="w", padx=40, pady=2)
            self.topping_vars[ing] = var
        
        # Analyze button
        analyze_btn = tk.Button(self.root, text="Analyze Toppings →", 
                               command=self.analyze_toppings,
                               font=("Arial", 12, "bold"), bg="#2196F3", fg="white",
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
            messagebox.showerror("No Pizzas Available", 
                               "Cannot make any pizza with these toppings!")
            return
        
        self.show_pizza_selection(makeable_pizzas)
    
    def show_pizza_selection(self, makeable_pizzas):
        """Screen 3: Choose pizza type"""
        self.clear_window()
        
        # Title
        title = tk.Label(self.root, text="STEP 3: Choose Your Pizza", 
                        font=("Arial", 16, "bold"), bg="#f0f0f0", fg="#333")
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
                           font=("Arial", 14, "bold"), bg="#FF9800", fg="white",
                           padx=20, pady=15, cursor="hand2", relief=tk.RAISED, bd=3)
            btn.pack(pady=10, padx=20, fill=tk.X)
    
    def select_pizza(self, pizza_type):
        """Select pizza and show steps"""
        self.chosen_pizza = pizza_type
        self.show_steps()
    
    def show_steps(self):
        """Screen 4: Show preparation steps"""
        self.clear_window()
        
        # Title
        title = tk.Label(self.root, 
                        text=f"📝 Steps to Make {self.chosen_pizza.replace('_', ' ').title()}", 
                        font=("Arial", 16, "bold"), bg="#f0f0f0", fg="#333")
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
        
        # Success message
        success = tk.Label(self.root, text="🎉 Enjoy your homemade pizza!", 
                          font=("Arial", 14, "bold"), bg="#f0f0f0", fg="green")
        success.pack(pady=20)
        
        # Restart button
        restart_btn = tk.Button(self.root, text="🔄 Start Over", 
                               command=self.show_base_ingredients,
                               font=("Arial", 12, "bold"), bg="#9C27B0", fg="white",
                               padx=30, pady=10, cursor="hand2")
        restart_btn.pack(pady=10)


def main():
    root = tk.Tk()
    app = PizzaGUI(root)
    root.mainloop()


if __name__ == "__main__":
    main()