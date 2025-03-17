# Genetic Algorithm for Date Validation

This project implements a **Genetic Algorithm (GA)** to generate and validate random dates. The algorithm evolves a population of dates through selection, crossover, and mutation, aiming to achieve a diverse set of test cases for date validation.

## 📌 Features
- Generates random dates (valid and invalid)
- Uses **fitness function** to rank dates based on correctness
- Implements **crossover** and **mutation** to create new dates
- Dynamically adjusts **mutation rate** based on diversity
- Stops when reaching **95% coverage** or max generations
- Saves final test cases in a **CSV file**

## 🛠️ Installation
1. Clone the repository:
   ```bash
   git clone https://github.com/your-username/genetic-date-validation.git
   cd genetic-date-validation
   ```
2. Ensure you have Python installed (>=3.6).
3. No additional libraries are required (uses built-in `random` and `csv`).

## 🚀 Usage
Run the script with:
```bash
python genetic_algorithm.py
```
After execution, test cases will be saved in `finalTestCases.csv`.

## 📂 File Structure
```
├── genetic_algorithm.py  # Main script
├── finalTestCases.csv    # Output test cases (generated after execution)
├── README.md             # Documentation
```

## 📊 Output Example
```
Generation 1: Population Size = 50
Generation 2: Population Size = 50
...
Genetic Algorithm terminated at generation: 23
Test cases saved successfully!
```

## 📝 Algorithm Overview
1. **Population Initialization** → Generates a mix of valid & invalid dates.
2. **Selection** → Chooses best candidates based on **fitness function**.
3. **Crossover** → Combines parents to create new dates.
4. **Mutation** → Randomly alters some dates based on diversity.
5. **Termination** → Stops when test coverage reaches **95%** or **100 generations**.

## 📜 License
This project is licensed under the **MIT License**. Feel free to modify and use it!

## 📬 Contact
For any questions or contributions, feel free to create an **Issue** or **Pull Request**!

Happy coding! 🚀
