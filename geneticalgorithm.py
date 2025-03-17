import random
import csv

# this function will generate a random date
def generateRandomDate():
    day = random.randint(1,31)
    month = random.randint(1,12)
    year = random.randint(0, 9999)

    return (day, month, year)

def isLeapYear(year):
    if (year % 400 == 0) or (year % 4 == 0 and year % 100 != 0):
        return True
    
    return False

def validateDate(date):
    day, month, year = date

    # Validate year range
    if year < 0 or year > 9999:  # Fixed: Changed from year < 1 to year < 0
        return False

    # Validate month
    if month < 1 or month > 12:
        return False

    # Validate day
    if day < 1:
        return False

    # Days per month logic
    if month in {4, 6, 9, 11}:  # Months with 30 days
        if day > 30:
            return False
    elif month == 2:  # February
        is_leap = isLeapYear(year)
        max_day = 29 if is_leap else 28
        if day > max_day:
            return False
    elif day > 31:  # Months with 31 days
        return False

    return True

def fitness(date):
    day = date[0]
    month = date[1]
    year = date[2]

    fitness = 0

    
    # Higher base score for valid dates
    if validateDate(date):
        fitness += 5
        
        # if the date is 29 feb on a leap year, add bonus points
        if isLeapYear(year) and day == 29 and month == 2:
            fitness += 5
    else:
        # For invalid dates, give a lower base score
        fitness += 2
    
    # Add points for boundary cases
    if year == 0 or year == 9999:
        fitness += 3
    
    if day == 1 or day == 31 or (day == 30 and month in {4, 6, 9, 11}):
        fitness += 2

    return fitness
    

def initialisePopulation(n): # n is the size of the population
    population = set()      # this will make sure dates don't repeat
    
    # Fixed: Add some important boundary cases first
    boundary_cases = [
        (1, 1, 0),      # Min date
        (31, 12, 9999), # Max date
        (29, 2, 2020),  # Leap year
        (29, 2, 2021),  # Invalid leap year
        (31, 4, 2023)   # Invalid 30-day month
    ]
    
    for case in boundary_cases:
        population.add(case)
    
    while(len(population) < n):
        date = generateRandomDate()
        if(len(population) < n/2):    # half of the population will be valid dates
            if(validateDate(date)):
                population.add(date)
        else:
            if(not validateDate(date)):    # the other half will be invalid dates
                population.add(date)
        
    return list(population)     # return the population as a list
    
def selectParents(population, np):      # np is the number of parents to select
    sorted_population = sorted(population, key=fitness, reverse=True)       # this will sort the population by fitness
        
    parents = sorted_population[:np]    # select the top np parents
    return parents      # return the parents


def crossover(parents, nc):     # nc is the number of children to generate
    children = []

    for x in range(len(parents)):
        for y in range(x+1, len(parents)):
            c1 = ((parents[x][0], parents[y][1], parents[y][2]))    # this will crossover the day and set it as the day of temp
            c2 = ((parents[y][0], parents[x][1], parents[y][2]))    # this will crossover the month and set it as the day of month
            c3 = ((parents[y][0], parents[y][1], parents[x][2]))    # this will crossover the year and set it as the year of temp

            # we have to check if the length is reached as every new child is added
            if(len(children) < nc):
                children.append(c1)
            if(len(children) < nc):
                children.append(c2)
            if(len(children) < nc):
                children.append(c3)

            # if the length is reaced early, the function is ended
            if len(children) >= nc:
                return children
    
    return children

def checkMRate(population):
    unique_dates = set(population)  # Get unique test cases
    unique_ratio = len(unique_dates) / len(population)  # Diversity measure

    mrate = 0.05 + (1 - unique_ratio) * 0.2  # Adjust mutation rate based on diversity
    mrate = min(max(mrate, 0.05), 0.25)  # Ensure it stays within [5%, 25%]

    return mrate, mrate < 0.15  # Return both the mutation rate and the check result


def mutation(children, mRate): # mRate is the mutation rate 
    mutatedChildren = []

    for child in children:
        if random.random() < mRate:  # mutate based on mutation rate
            mutate = random.randint(0, 2)   # this will decide which part of the date to mutate

            if(mutate == 0):
                mutatedChild = (random.randint(1,31), child[1], child[2])       # this mutates the day of the child
            elif(mutate == 1): 
                mutatedChild = (child[0], random.randint(1,12), child[2])       # this mutates the month of the child
            else:
                # Fixed: Occasionally create boundary year cases
                if random.random() < 0.1:  # 10% chance for boundary year
                    year = random.choice([0, 9999])
                else:
                    year = random.randint(0, 9999)
                mutatedChild = (child[0], child[1], year)         # this mutates the year of the child

            mutatedChildren.append(mutatedChild)
        else:
            mutatedChildren.append(child)

    return mutatedChildren


def terminate(population, generation, coverageThreshold=0.95, maxGenerations=100):      # generation is the number of the current generation
    if(generation >= maxGenerations):
        return True
    
    # Fixed: Better coverage calculation
    valid_count = sum(1 for date in population if validateDate(date))
    invalid_count = len(population) - valid_count
    
    # Count boundary cases
    boundary_count = sum(1 for date in population if 
                        (date[2] == 0 or date[2] == 9999 or 
                        (date[0] == 29 and date[1] == 2) or
                        (date[0] == 31 and date[1] in {1, 3, 5, 7, 8, 10, 12}) or
                        (date[0] == 30 and date[1] in {4, 6, 9, 11})))
    
    # Check if we have enough of each category
    has_min_valid = valid_count >= 10
    has_min_invalid = invalid_count >= 10
    has_min_boundary = boundary_count >= 5
    
    coverage = (has_min_valid + has_min_invalid + has_min_boundary) / 3
    
    print(f"Generation {generation}: Coverage = {coverage:.2f}, Valid = {valid_count}, Invalid = {invalid_count}, Boundary = {boundary_count}")
    
    if(coverage >= coverageThreshold):
        return True              
    
    return False                # this checks 95% coverage
    

def geneticAlgorithm(n=50, np=10, nc=20, maxGenerations=100, coverageThreshold=0.95):   # n is the population size
    # np is the number of parents we want
    # nc is the number of children we want
    # max generations is the max no of generations we want the algo to run for
    # coverage threshold is the minimum coverage we want to achieve

    generation = 0
    population = initialisePopulation(n)

    while not terminate(population, generation, coverageThreshold, maxGenerations):
        parents = selectParents(population, np)     # first we select the parents

        children = crossover(parents, nc)       # we use the crossover function to generte the children

        mRate, _ = checkMRate(children)
        mutatedChildren = mutation(children, mRate)     # we check the mutation rate and then mutate the children

        # Fixed: Preserve diversity by keeping some parents
        population = parents[:5] + mutatedChildren  # Keep best 5 parents (elitism)
        
        # Make sure we don't exceed the population size
        if len(population) > n:
            population = population[:n]

        generation += 1

        print(f"Generation {generation}: Population Size = {len(population)}")

    print("Genetic Algorithm terminated at generation:", generation)
    
    return population  # Return final test cases


def save_test_cases(test_cases, filename="finalTestCases.csv"): 
    with open(filename, mode='w', newline='') as file:      # opens file in write mode
        writer = csv.writer(file)       # creates an object of csv writer
        writer.writerow(["Day", "Month", "Year", "Valid/Invalid"])      # this writes the header of the file 

        for date in test_cases:
            if(validateDate(date)== True):
                validity = "Valid"
            else:
                validity = "Invalid"       # checks if the date is valid or not

            writer.writerow([date[0], date[1], date[2], validity])      # writes onto the file

# After running geneticAlgorithm():
final_test_cases = geneticAlgorithm()
save_test_cases(final_test_cases)
print("Test cases saved successfully!")