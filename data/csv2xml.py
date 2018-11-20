
# cria um dicionário de sintomas
symptoms_dic = {}
with open('ncomms-symptom.csv', 'r') as fin:
    symptoms = fin.read().split('\n')[1:]

    for symptom in symptoms:
        if symptom:
            name, occurrences = symptom.split('|')
            symptoms_dic[name] = int(occurrences)

# cria um dicionário de causas
causes_dic = {}
with open('ncomms-cause.csv', 'r') as fin:
    causes = fin.read().split('\n')[1:]

    for cause in causes:
        if cause:
            symptom, disease, occurrences, score = cause.split('|')
            if disease not in causes_dic:
                causes_dic[disease] = []

            causes_dic[disease].append({
                'symptom': symptom,
                'occurrences': int(occurrences),
                'score': float(score)
            })

xml = '<?xml version="1.0" encoding="UTF-8"?>\n'
xml += '<diseases>\n'

with open('ncomms-disease.csv', 'r') as fin:
    diseases = fin.read().split('\n')[1:]
    
    for disease in diseases:
        if disease:
            name, occurrences = disease.split('|')

            xml += '\t<disease name="%s">\n' % name
            xml += '\t\t<occurrences>%s</occurrences>\n' % occurrences

            # adiciona os sintomas
            xml += '\t\t<symptoms>\n'
            if name in causes_dic:
                for symptom in causes_dic[name]:
                    xml += '\t\t\t<symptom name="%s">\n' % symptom['symptom']
                    xml += '\t\t\t\t<occurrences>%d</occurrences>\n' % symptom['occurrences']
                    xml += '\t\t\t\t<score>%f</score>\n' % symptom['score']
                    xml += '\t\t\t</symptom>\n'

            xml += '\t\t</symptoms>\n'

            xml += '\t</disease>\n'

xml += '</diseases>\n'

# save xml file
with open('ncomms.xml', 'w') as fout:
    fout.write(xml)
