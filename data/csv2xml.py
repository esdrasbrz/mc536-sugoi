xml = '<?xml version="1.0" encoding="UTF-8"?>\n'
xml += '<diseases>\n'

with open('ncomms-disease.csv', 'r') as fin:
    diseases = fin.read().split('\n')[1:]
    
    for disease in diseases:
        if disease:
            name, occurrences = disease.split('|')

            xml += '\t<disease name="%s">\n' % name
            xml += '\t\t<occurrences>%s</occurrences>\n' % occurrences
            xml += '\t</disease>\n'

xml += '</diseases>\n'

# save xml file
with open('ncomms.xml', 'w') as fout:
    fout.write(xml)
