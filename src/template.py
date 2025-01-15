
template0 = """
    PatientData:
        sources:
            - patientWeightSource
        s: protrait:PatientID/$(hn_bl_id)
        po:
            - [a,ncit:C16960]
            {% for prod in prods %}
            - p: "protrait:has"
              o: protrait:PatientID/$(hn_bl_id)/{{prod }}
            {% endfor %}

    """

template = """
    {{ name_var}}:
        sources:
            - patientWeightSource
        s: protrait:PatientID/$(hn_bl_id)/{{ p1 }}{{ '/' + p2 if p2 else '' }}{{ '/' + p3 if p3 else '' }}{{ '/' + p4 if p4 else '' }}{{ '/' + p5 if p5 else '' }}{{ '/' + p6 if p6 else '' }}/{{name_var}}

        po:
            - {{ po_value }}
            - p: protrait:has
              o:
                value: "$({{ name_var}})"

"""

template2 = """
    {{name}}:
        sources:
            - patientWeightSource
        s: protrait:PatientID/$(hn_bl_id){{ '/' + p1 if p1 else '' }}{{ '/' + p2 if p2 else '' }}{{ '/' + p3 if p3 else '' }}{{ '/' + p4 if p4 else '' }}{{ '/' + p5 if p5 else '' }}{{ '/' + p6 if p6 else '' }}/{{name}}
        {% if parents %}
        po:

            {% for parent in parents %}
            - p: "protrait:has"
              o: protrait:PatientID/$(hn_bl_id){{ '/' + p1 if p1 else '' }}{{ '/' + p2 if p2 else '' }}{{ '/' + p3 if p3 else '' }}{{ '/' + p4 if p4 else '' }}{{ '/' + p5 if p5 else '' }}{{ '/' + p6 if p6 else '' }}/{{name}}/{{parent}}
            {% endfor %}
        {% endif %}

    """