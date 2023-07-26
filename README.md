# Problem Set Generator

This is a quick prototype of a web application, built to help me review for the Chemical Engineering Board Exams. The Problem Set Generator randomly samples questions from a CSV data source and presents them in a quiz format, similar to what you would find in the "Canvas" Learning Management System. After answering the problem set, the app also provides graphs and statistics to analyze my performance.

## Demo



https://github.com/jskherman/che-pset/assets/68434444/ee11c50a-6df6-4ea4-b213-9b7c2a005514



## Installation

1. Clone this repository to your local machine.
2. Install the required dependencies by running `pip install -r requirements.txt`.
3. Set the required secrets in the `.streamlit/secrets.toml` file.
    - `QNA_CSV`: Path to the CSV file containing the question and answer data.
    - `ACCESS_KEY`: Access key for the generator.
4. Run the application using the command `streamlit run App.py`.

The format of the CSV file should be as follows:

| ID | Question                                                                                                                                             | Choices                       | Answer | Tags                    |
|----|------------------------------------------------------------------------------------------------------------------------------------------------------|-------------------------------|--------|-------------------------|
| 1  | If **aspirin** is made using the raw materials salicylic acid and acetic anhydride with a yield of 75%, how many grams of aspirin will be produced?  | 1; 30; 25; 15                 | 15     | PCP; General Chemistry  |
| 2  | How many beta particles are emitted in the decomposition of ${\ }^{238}_{92} \text{ U }$ to ${\ }^{208}_{82} \text{ Pb }$?                           | 6; 2; 8; 4                    | 8      | PCP; Energy Engineering |
| 3  | Give the mass empirical formula of the following compound if a sample contains $57.8\%\ \text{C}$, $36\%\ \text{H}$, and $38.6\%\ \text{O}$ by mass. | C12H9O6; C8H6O4; C2HO; C4H3O2 | C4H3O2 | General Chemistry; PCP  |

<details><summary>Show CSV</summary>

```csv
"ID","Question","Choices","Answer","Tags"
"1","If **aspirin** is made using the raw materials salicylic acid and acetic anhydride with a yield of 75%, how many grams of aspirin will be produced?","1; 30; 25; 15","15","PCP; General Chemistry"
"2","How many beta particles are emitted in the decomposition of ${\ }^{238}_{92} 	ext{ U }$ to ${\ }^{208}_{82} \text{ Pb }$?","6; 2; 8; 4","8","PCP; Energy Engineering"
"3","Give the mass empirical formula of the following compound if a sample contains $57.8\%\ \text{C}$, $36\%\ \text{H}$, and $38.6\%\ \text{O}$ by mass.","C12H9O6; C8H6O4; C2HO; C4H3O2","C4H3O2","General Chemistry; PCP"
```
</details>

## Usage

1. Launch the app by executing the command mentioned above.
2. The homepage will appear, providing brief instructions on using the app.
3. Click on the "Generate Problem Set" button to create a new set of random questions.
4. The app will generate a problem set containing multiple choice questions.
5. Answer each question by selecting the appropriate option.
6. After completing the problem set, click on the "Submit" button to view your performance summary.
7. The app will display graphs and statistics showing your performance, including score distribution, question difficulty analysis, and time taken for each question.

## Possible Future Extensions

This prototype can be extended in several ways to enhance its functionality:

- Integration with a larger question database to provide a wider range of topics and difficulty levels.
- Adding support for different question types (e.g., fill in the blanks, matching) to diversify problem sets.
- Allowing users to customize problem sets based on specific topics or exam categories (already implemented using "OR" tags).
- Implementing user authentication to track progress and provide personalized recommendations for improvement.
