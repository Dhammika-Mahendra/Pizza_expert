% Pizza Maker Expert System Knowledge Base

% Base ingredients
essential_base(flour).
essential_base(water).
essential_base(salt).

extra_base(sugar).
extra_base(semolina).

% Topping ingredients
topping_ingredient(fresh_tomato_slices).
topping_ingredient(fresh_mozzarella).
topping_ingredient(olive_oil).
topping_ingredient(tomato_sauce).
topping_ingredient(mozzarella_cheese).
topping_ingredient(pepperoni_slices).

% Pizza topping requirements
pizza_toppings(margherita, [fresh_tomato_slices,fresh_mozzarella,olive_oil]).
pizza_toppings(pepperoni, [tomato_sauce,mozzarella_cheese,pepperoni_slices]).

% Messages for missing extra ingredients
missing_extra_effect(sugar, "Slower yeast rise, less browning").
missing_extra_effect(semolina, "Crustless crisp, more doughy").

% Check if user has all essential base ingredients
has_essential_base(UserIngredients) :-
    member(flour, UserIngredients),
    member(water, UserIngredients),
    member(salt, UserIngredients).

% Find missing essential base ingredients
find_missing_essential(UserIngredients, MissingEssential) :-
    findall(Ing, (essential_base(Ing), \+ member(Ing, UserIngredients)), MissingEssential).

% Find missing extra base ingredients
find_missing_extra(UserIngredients, MissingExtra) :-
    findall(Ing, (extra_base(Ing), \+ member(Ing, UserIngredients)), MissingExtra).

% Check if user can make a specific pizza topping
can_make_topping(PizzaType, UserToppings) :-
    pizza_toppings(PizzaType, RequiredToppings),
    subset(RequiredToppings, UserToppings).

% Helper: check if all elements of list1 are in list2
subset([], _).
subset([H|T], List) :-
    member(H, List),
    subset(T, List).

% Find all makeable pizza toppings
find_makeable_pizzas(UserToppings, MakeablePizzas) :-
    findall(Pizza, can_make_topping(Pizza, UserToppings), MakeablePizzas).

% Get extra ingredients user has
get_user_extras(UserBase, UserExtras) :-
    findall(Ing, (member(Ing, UserBase), extra_base(Ing)), UserExtras).

% --- NEW: Missing toppings per pizza ---
% Compute which required toppings are missing for a given pizza
missing_toppings_for_pizza(UserToppings, PizzaType, MissingToppings) :-
    pizza_toppings(PizzaType, RequiredToppings),
    findall(Ing, (member(Ing, RequiredToppings), \+ member(Ing, UserToppings)), MissingToppings).

% Collect all pizzas that are not makeable and their missing toppings
missing_toppings_by_pizza(UserToppings, MissingByPizza) :-
    findall([Pizza, Missing],
            ( pizza_toppings(Pizza, _),
              missing_toppings_for_pizza(UserToppings, Pizza, Missing),
              Missing \= []
            ),
            MissingByPizza).

% Basic steps for pizza base
base_step(1, "Mix flour, water, and salt").
base_step(2, "Knead the dough").
base_step(3, "Flatten the dough").

% Extra ingredient steps
extra_step(sugar, "Add sugar to the mix").
extra_step(semolina, "Add semolina to the mix").

% Pizza-specific topping steps
topping_step(margherita, 1, "Add fresh tomato slices").
topping_step(margherita, 2, "Add fresh mozzarella").
topping_step(margherita, 3, "Drizzle olive oil").

topping_step(pepperoni, 1, "Spread tomato sauce").
topping_step(pepperoni, 2, "Add mozzarella cheese").
topping_step(pepperoni, 3, "Add pepperoni slices").

% Generate complete step list for a pizza
generate_steps(PizzaType, UserExtras, Steps) :-
    findall(Step, base_step(_, Step), BaseSteps),
    findall(ExtraStep, (member(Extra, UserExtras), extra_step(Extra, ExtraStep)), ExtraSteps),
    findall(ToppingStep, topping_step(PizzaType, _, ToppingStep), ToppingSteps),
    append(BaseSteps, ExtraSteps, TempSteps),
    append(TempSteps, ToppingSteps, Steps).

% Get all available pizza types
get_pizza_types(PizzaTypes) :-
    findall(Pizza, pizza_toppings(Pizza, _), PizzaTypes).

% Get all ingredients needed for a specific pizza type
get_pizza_ingredients(PizzaType, AllIngredients) :-
    % Get essential base ingredients
    findall(Ing, essential_base(Ing), EssentialBase),
    % Get extra base ingredients  
    findall(Ing, extra_base(Ing), ExtraBase),
    % Get required toppings for this pizza type
    pizza_toppings(PizzaType, RequiredToppings),
    % Combine all ingredients
    append(EssentialBase, ExtraBase, BaseIngredients),
    append(BaseIngredients, RequiredToppings, AllIngredients).