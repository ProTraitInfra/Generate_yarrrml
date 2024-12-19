import pandas as pd
import csv
from jinja2 import Template
import math
from itertools import product
from template import template0, template2, template


def iterate_over_concept(data_f: pd.DataFrame, concept: list):
    """
    Create list of all the concepts in the columns specified in the concept list
    :param data_f:
    :param concept:
    :return:
    """
    res = []
    for k in concept:
        lo = data_f[k].unique().tolist()
        res = res + lo
    res = list(set(res))
    return res


def create_parent1(data_f, list_c):
    list_concepts = []
    for name in list_c:

        list_predicate = []
        list_prev_par = []
        dict_par = {1: [], 2: [], 3: [], 4: [], 5: [], 6: []}
        dict_pre = []
        parent_select = []
        for i in range(1, 6):
            filtered: pd.DataFrame = data_f.loc[data_f[f"Parent #{i}"] == name]
            if not filtered.empty:
                for j in range(1, 6):
                    if j == i:
                        continue
                    elif j < i:
                        parent = filtered[f"Parent #{j}"].unique().tolist()

                        cleaned_pred = [x for x in parent if not (isinstance(x, float)
                                                                  and math.isnan(
                                    x)) and x != name and x not in parent_select]
                        if cleaned_pred:
                            for x in cleaned_pred:
                                parent_select.append(x)
                            dict_par[j] = dict_par[j] + cleaned_pred

                    elif j > i and j == i + 1:
                        pred = filtered[f"Parent #{j}"].unique().tolist()
                        cleaned_pred = [x for x in pred if not (isinstance(x, float) and math.isnan(x))
                                        and x not in list_predicate and x != name]
                        if cleaned_pred:
                            #    dict_pre[j] = dict_pre[j] + cleaned_pred
                            dict_pre += cleaned_pred
                    else:
                        pass

        list_prev_par.append(dict_par)
        list_predicate = dict_pre
        dict_j = {"name_c": name, "predicate": list_predicate, "parent": list_prev_par}
        list_concepts.append(dict_j)

    print()
    return list_concepts


def generate_template_concept(templ, list_p_p, list_col_p):
    """
    Generate the template for each concept defining the uri based on the parent and their predicate
    :param list_col_p: list of dictionary with the column  name and the parent pair
    :param templ:
    :param list_p_p:list of dictionary with the concept name their parent and predicate
    :return:
    """
    lisr_t = []
    for index, entry in enumerate(list_p_p):
        name = entry["name_c"]

        if pd.isna(name):
            continue
        parent = entry["parent"]
        predicate = entry["predicate"]
        for dictionary in list_col_p:
            if dictionary["par"] == name:
                predicate.append(dictionary["col"])
        else:
            pass
        dict_l = parent[0]
        prepared_dict = {key: values if values else [None] for key, values in dict_l.items()}
        keys = prepared_dict.keys()
        combinations = product(*(prepared_dict[k] for k in keys))

        for combination in combinations:
            # Map combination values to p1, p2, ..., p6
            render_data = {f"p{i + 1}": value for i, value in enumerate(combination)}
            render_data.update({
                "name": name,
                "parents": predicate
            })
            rendered_output = templ.render(**render_data)
            lisr_t.append(rendered_output)
    return lisr_t


def column_process(dt: pd.DataFrame):
    """
    For each column entity find the parent and save it into a list
    :return:
    """
    l_res = []
    for ind, r in dt.iterrows():
        col_n = r["ProTrait Name"]

        t = [{l: r[f"Parent #{l}"]} for l in range(1, 7) if not pd.isna(r[f"Parent #{l}"])]
        if not t:
            continue
        else:
            t_max = max(t, key=lambda d: list(d.keys())[0])
            d_column = {"col": str.lower(col_n), "par": next(iter(t_max.values()))}
            l_res.append(d_column)
    return l_res


def generate_template_column(dt):
    """
    Generate for each colum their respective template with predicate and appropriate uri
    :param dt: dataframe of the data
    :return:
    """
    template_l_c = []
    for i, r in dt.iterrows():

        name_var = r["ProTrait Name"]

        if not pd.isna(name_var):
            name_var = str.lower(name_var)

        namespace = r["Namespace prefix"]

        if not pd.isna(namespace):
            namespace = str.lower(namespace)

        if not pd.isna(r["Class (R2RML)"]):
            code = r["Class (R2RML)"]
        elif not pd.isna(r["Class suggested)"]):
            code = r["Class suggested)"]
        else:
            continue
        if pd.isna(r[f"Parent #1"]):
            continue
        if pd.isna(namespace):
            continue

        po_value = f"[a,{namespace}:{code}]"
        dict_li = {"p1": "", "p2": "", "p3": "", "p4": "", "p5": "", "p6": ""}
        list_lo = []
        for j in range(1, 7):
            if not pd.isna(r[f"Parent #{j}"]) and r[f"Parent #{j}"] not in list_lo:
                list_lo.append(r[f"Parent #{j}"])
                dict_li[f"p{j}"] = r[f"Parent #{j}"]

        temp = Template(template)
        # Render the template with the dynamic values
        generated_mapping = temp.render(
            name_var=name_var,
            po_value=po_value,
            p1=dict_li["p1"],
            p2=dict_li["p2"],
            p3=dict_li["p3"],
            p4=dict_li["p4"],
            p5=dict_li["p5"],
            p6=dict_li["p6"]
        )
        template_l_c.append(generated_mapping)
    return template_l_c


if __name__ == "__main__":
    l_c = ["Parent #1", "Parent #2", "Parent #3", "Parent #4", "Parent #5", "Parent #6"]

    data = pd.read_csv("/Users/alessioromita/Downloads/onto.csv", delimiter=";")

    list_col_pre = column_process(data)

    rs = iterate_over_concept(data, l_c)

    list_parent_predicate = create_parent1(data, rs)

    tmpl = Template(template2)
    list_comp = generate_template_concept(tmpl, list_parent_predicate, list_col_pre)

    template_list_column = generate_template_column(data)

    ls_col = list(set(data["Parent #1"].dropna().to_list()))

    tmpl0 = Template(template0)
    generated_mapping_sub_predicate = tmpl0.render(
        prods=ls_col)

    output_file = "../output_example/output_template2.yaml"

    with open(output_file, "w") as f:
        f.write("""prefixes:
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
    """)

        f.write(generated_mapping_sub_predicate)

        for item in list_comp:
            f.write(item)

        for item in template_list_column:
            f.write(item)

