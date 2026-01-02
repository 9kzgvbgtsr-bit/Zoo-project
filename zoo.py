from abc import ABC, abstractmethod
import random

class Animal(ABC):
    def __init__(self, name, age, energy_level):
        self.name = name
        self.age = age
        self.energy_level = energy_level

    sleep_position = "comfortably"
    sleep_time = "night"
    allowed_foods: frozenset = frozenset()
    
    def choose_food(self):
        if not self.allowed_foods:
            raise NotImplementedError("allowed_foods not defined")
        return random.choice(tuple(self.allowed_foods))
    
    @abstractmethod
    def eat(self, food):
        pass

    @abstractmethod
    def interact(self, visitor):
        # How this animal responds when a visitor tries to interact.
        pass

    @abstractmethod
    def interact_with(self, other):
        # How this animal interacts with other animals.
        pass

    def change_energy(self, level):
        self.energy_level = max(0, self.energy_level + level)

    def sleep(self, position, sleep_time):
        self.change_energy(10)
        return f"{self.name} sleeps {position} during the {sleep_time}"
    
    def _spend_energy(self, cost: int, too_tired_msg: str):
        # Common rule: if not enough energy, do nothing; otherwise spend energy.
        if self.energy_level <= 0:
            return False, too_tired_msg
        self.change_energy(-cost)
        return True, None
    
    def __str__(self):
        return f"{self.__class__.__name__} {self.name}"

class Herbivore(Animal):

    allowed_foods = frozenset({"grass", "leaves"})
    eat_style = "chews the {food} slowly."
    interact_cost = 1
    predator_cost = 2

    def interact_with(self, other):
        if isinstance(other, Carnivore):
            ok, msg = self._spend_energy(
                self.predator_cost,
                f"{self.name} is too tired to react to {other.name}."
            )
            return msg or f"{self.name} keeps a wary eye on {other.name}."
        ok, msg = self._spend_energy(
            self.interact_cost,
            f"{self.name} is too tired to react to {other.name}."
        )
        return msg or f"{self.name} calmly watches {other.name}."
    
    def eat(self, food):
        if food not in self.allowed_foods:
            return f"{self.name} refuses to eat the {food}."
        self.change_energy(10)
        return f"{self.name} " + self.eat_style.format(food=food)

class Carnivore(Animal):
    
    allowed_foods = frozenset({"deer", "rabbit", "chicken", "ghazal", "buffalo", "antelope"})
    eat_style = "takes big bites of the {food}."
    hunt_cost = 2
    hunt_action = "stalks"
    neutral_action = "ignores"
    interact_cost = 1

    def interact_with(self, other):
        if isinstance(other, Herbivore):
            ok, msg = self._spend_energy(
                self.hunt_cost,
                f"{self.name} is too tired to bother chasing {other.name}."
            )
            return msg or f"{self.name} {self.hunt_action} {other.name} (under supervision)."
        ok, msg = self._spend_energy(
            self.interact_cost,
            f"{self.name} is too tired to react to {other.name}."
        )
        return msg or f"{self.name} {self.neutral_action} {other.name}."
    
    def eat(self, food):
        if food not in self.allowed_foods:
            return f"{self.name} refuses to eat the {food}."
        self.change_energy(10)
        return f"{self.name} " + self.eat_style.format(food=food)

class Omnivore(Animal):

    allowed_foods = frozenset({"banana", "nuts"})
    eat_style = "eats the {food}."
    interact_cost = 1

    def interact_with(self, other):
        ok, msg = self._spend_energy(
            self.interact_cost,
            f"{self.name} is too tired to react to {other.name}."
        )
        return msg or f"{self.name} looks curiously at {other.name}."

    def eat(self, food):
        if food not in self.allowed_foods:
            return f"{self.name} refuses to eat the {food}."
        self.change_energy(10)
        return f"{self.name} " + self.eat_style.format(food=food)

class Giraffe(Herbivore):

    sleep_position = "standing"

    def interact(self, visitor):
       ok, msg = self._spend_energy(1, f"{self.name} is too tired to interact.")
       return msg or f"{self.name} gently leans down while {visitor.name} waves hello."

class Lion(Carnivore):

    eat_style = "devours the {food} like a king."
    hunt_action = "stalks"
    neutral_action = "ignores"
    sleep_position = "lying down"
    sleep_time = "day"

    def interact(self, visitor):
       ok, msg = self._spend_energy(1, f"{self.name} is resting and ignores everyone.")
       return msg or f"{self.name} lets out a loud roar and {visitor.name} is a little bit scared."

# New animal species added
class Tiger(Carnivore):
    
    eat_style = "tears into the {food}."
    hunt_action = "creeps after"
    neutral_action = "watches"

    def interact(self, visitor):
        ok, msg = self._spend_energy(1, f"{self.name} is hiding.")
        return msg or f"{self.name} is running fast and {visitor.name} is a little bit scared."

class Monkey(Omnivore):

    eat_style = "peels the {food} before eating."
    sleep_position = "on a tree"

    def interact_with(self, other):
        if isinstance(other, Monkey):
            ok, msg = self._spend_energy(1, f"{self.name} is too tired to play with {other.name}.")
            return msg or f"{self.name} plays with {other.name}."
        ok, msg = self._spend_energy(1, f"{self.name} is too tired to react to {other.name}.")
        return msg or f"{self.name} chatters at {other.name}."

    def interact(self, visitor):
       ok, msg = self._spend_energy(2, f"{self.name} does not want to play.")
       return msg or f"{self.name} chatters and mimics {visitor.name}'s gestures."

class Visitor:

    def __init__(self, name):
        self.name = name

    def feed(self, animal: Animal, food):
        eating = animal.eat(food)
        return f"{self.name} feeds {animal} with {food} under supervision. {eating}"
    
    def interact(self, animal: Animal):
        return animal.interact(self)
    
class Zoo:

    def __init__(self, name, animals, visitors):
        self.name = name
        self.animals = animals
        self.visitors = visitors
        self.day = 0
        self.today_food = {}
        self.food_supply = {
        "deer": 5, "rabbit": 10, "chicken": 12, "ghazal": 4, "buffalo": 2, "antelope": 5,
        "grass": 999, "leaves": 999, "banana": 40, "nuts": 40}

    def restock_daily(self):
        # Add food each day
        restock = {
            "grass": 50,
            "leaves": 30,
            "banana": 10,
            "nuts": 10,
            "rabbit": 3,
            "chicken": 3,
            "deer": 1,
            "antelope": 1,
            "ghazal": 1,
            "buffalo": 0,
        }
        for food, amount in restock.items():
            self.food_supply[food] = self.food_supply.get(food, 0) + amount

    def choose_available_food(self, animal):
        # Pick a food the animal can eat that is still in stock.
        choices = [f for f in animal.allowed_foods if self.food_supply.get(f, 0) > 0]
        if not choices:
            return None
        return random.choice(choices)
    
    def prompt_user(self):
        print("\nWhat would you like to do?")
        print("1) Run one day")
        print("2) Run multiple days")
        print("3) Exit")

        return input("Enter choice (1-3): ").strip()
    

    # Add a simple text-based interface for user interaction.
    def interactive_run(self):
        while True:
            choice = self.prompt_user()

            if choice == "1":
                for line in self.run(1):
                    print(line)

            elif choice == "2":
                days = input("How many days? ").strip()
                if days.isdigit():
                    for line in self.run(int(days)):
                        print(line)
                else:
                    print("Invalid number.")

            elif choice == "3":
                print("Goodbye!")
                break

            else:
                print("Invalid choice.")


    def morning(self, visitors):
        messages = []
        messages.append("\n---Morning---")
        if not visitors:
            messages.append("No visitors today.")
            return messages
        # Choose one visitor for today
        greeter = random.choice(visitors)
        for a in self.animals:
            messages.append(greeter.interact(a))
        return messages
    
    def midday(self, visitors):
        messages = []
        self.today_food = {}
        if not visitors:
            messages.append("No visitors available to feed animals today.")
            return messages
        # Choose one visitor for today
        feeder = random.choice(visitors)
        messages.append("\n---Midday (Feeding)---")
        for a in self.animals:
            food = self.choose_available_food(a)
            if food is None:
                self.today_food[a] = "Nothing"
                messages.append(f"{feeder.name} could not find suitable food for {a}.")
                continue
            # Consume stock
            self.food_supply[food] -= 1
            self.today_food[a] = food
            # Feed once per animal
            messages.append(feeder.feed(a, food))
        return messages

    def animal_interactions(self):
        messages = []
        if len(self.animals) < 2:
            return messages
        for i in range(len(self.animals) - 1):
            a1 = self.animals[i]
            a2 = self.animals[i + 1]

            messages.append(a1.interact_with(a2))
            messages.append(a2.interact_with(a1))
        return messages

    def evening(self):
        messages = []

        messages.append("\n---Evening---")
        for a in self.animals:
            messages.append(a.sleep(a.sleep_position, a.sleep_time))
        return messages
    
    def roll_daily_events(self):
        #Decide random events for the day.
        rainy = random.random() < 0.5
        if rainy:
            visitors_present = random.random() < 0.3 
        else:
            visitors_present = random.random() < 0.8 
        return {
            "rainy": rainy,
            "visitors_present": visitors_present
        }

    def report(self):
        messages = []
        messages.append("\nEnergy levels:")
        for a in self.animals:
            messages.append(f"{a}: {a.energy_level}")
    
        messages.append("\nTodays food:")
        for a in self.animals:
            messages.append(f"{a}: {self.today_food.get(a, 'Not fed today')}")

        messages.append("\nFood supply:")
        for food, count in sorted(self.food_supply.items()):
            messages.append(f"{food}: {count}")
        return messages
        
    def run(self, days = 10):
        output = []
        if days <= 0:
            return []
        for i in range(1, days + 1):
            self.day = i
            events = self.roll_daily_events()
            active_visitors = self.visitors if events["visitors_present"] else []
            if events["rainy"]:
                output.append("It is raining today.")
            else:
                output.append("The weather is clear today.")
            self.restock_daily()
            output.append(f"\n================ Day {i} ================\n")
            output.append("It is raining today." if events["rainy"] else "The weather is clear today.")
            output.extend(self.morning(active_visitors))
            output.extend(self.midday(active_visitors))
            output.extend(self.animal_interactions())
            output.extend(self.evening())
            output.extend(self.report())
        return output

g = Giraffe(name="Lulu", age=4, energy_level=5)
l = Lion(name="King", age=10, energy_level= 15)
m = Monkey(name="Marcel", age=1, energy_level= 30)
m2 = Monkey(name="Coco", age=5, energy_level= 30)
t = Tiger(name="Shadow", age=6, energy_level= 20)
animals = [g, l, m, m2, t]
visitors = [Visitor("Alice"), Visitor("Bob")]
zoo = Zoo("Stockholm Zoo", animals, visitors)
zoo.interactive_run()
