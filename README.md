# ProTrait Template Generator

This project provides a Python script to generate YAML templates for ProTrait ontology mapping using hierarchical relationships and parent-predicate mappings derived from a CSV file. The script processes the input data and produces structured YAML output, leveraging Jinja2 templates.

---

## Features

- **Concept Extraction**: Automatically extract unique concepts from dataset columns.
- **Hierarchical Parent Mapping**: Build relationships between concepts and their parent entries.
- **Template Rendering**: Use Jinja2 templates to dynamically generate YAML mappings.
- **CSV Parsing**: Easily process datasets with hierarchical data.
- **Customizable Templates**: Pre-defined templates allow flexibility for different output requirements.

---

## Prerequisites

Ensure the following dependencies are installed before running the script:

- Python 3.7 or higher
- Required Python libraries:
  - `pandas`
  - `jinja2`

Install dependencies with the following command:

```bash
pip install pandas jinja2
```

---

## Usage

1. **Clone the Repository**:
   ```bash
   git clone https://github.com/yourusername/protrait-template-generator.git
   cd protrait-template-generator
   ```

2. **Prepare Input Data**:
   - Place the input CSV file (e.g., `onto.csv`) in the working directory.
   - Ensure the CSV contains the following columns:
     - `ProTrait Name`
     - `Namespace prefix`
     - `Class (R2RML)` or `Class suggested`
     - `Parent #1` to `Parent #6` (representing the hierarchy).

3. **Customize Templates**:
   - Modify `template0`, `template2`, or `template` in `template.py` as needed.

4. **Run the Script**:
   Execute the script with the following command:
   ```bash
   python main.py
   ```
   The generated YAML file will be saved to:
   ```
   ../output_example/output_template_test.yaml
   ```

---

## Input Data Example

### CSV Format (`onto.csv`)

| ProTrait Name | Namespace prefix | Class (R2RML) | Parent #1 | Parent #2 | Parent #3 | Parent #4 | Parent #5 | Parent #6 |
|---------------|------------------|---------------|-----------|-----------|-----------|-----------|-----------|-----------|
| Trait1        | ex               | Class1        | Parent1   | Parent2   |           |           |           |           |
| Trait2        | schema           | Class2        | Parent3   |           |           |           |           |           |

---

## Output Example

The script generates a structured YAML file. Example:

```yaml
prefixes:
  ex: "http://www.example.com/"
  schema: "http://schema.org/"
  rdf: "http://www.w3.org/1999/02/22-rdf-syntax-ns#"
  ncit: "http://ncicb.nci.nih.gov/xml/owl/EVS/Thesaurus.owl#"
  protrait: "https://protrait.com/"
  grel: http://users.ugent.be/~bjdmeest/function/grel.ttl#
  roo: "http://www.cancerdata.org/roo/"
  purl: "http://purl.bioontology.org/ontology/SNMI/"

sources:
  patientWeightSource:
    #query: SELECT * FROM public.hn_bl;
    access: "/app/data/dataexport.csv"
    referenceFormulation: ql:CSV

mappings:
  - name: Trait1
    parents:
      - Parent1
      - Parent2
  - name: Trait2
    parents:
      - Parent3
```

---

## Functions Overview

### `iterate_over_concept(data_f, concept)`
Extracts unique concepts from the specified columns.

### `create_parent1(data_f, list_c)`
Builds hierarchical parent-predicate mappings for each concept.

### `generate_template_concept(templ, list_p_p, list_col_p)`
Generates YAML mappings for each concept based on their parents and predicates.

### `column_process(dt)`
Processes columns to associate them with their respective parents.

### `generate_template_column(dt)`
Generates individual column templates using Jinja2.

---

## Customization

- Modify `template0`, `template2`, or `template` in `template.py` to change the generated output structure.
- Update the `content` block in the script for additional prefixes or source configurations.

---

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

---


