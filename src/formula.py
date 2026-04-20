import csv
import re

def load_data(input_file):
    '''
    Load the elements data from a CSV file and return a dictionary with the symbol as key
    '''
    props = {}
    with open(input_file, mode='r') as f_input:
        reader = csv.DictReader(f_input)
        for row in reader:
            props[row['simbolo']] = {
                'mass': float(row['massa']),
                'charge': int(row['carga']),
            }
    return props



def get_ions(molecule, elements):
    '''
    Return the number of cations and anions of an molecule
    '''
    mask = (
        r'(?P<element>[A-Z][a-z]*)(?P<quantity>\d*\.?\d*)'
        r'|(?P<open>\()'
        r'|(?P<close>\))(?P<close_quantity>\d*\.?\d*)'
    )

    cations, anions = {}, {}
    total_pos_charge, total_neg_charge = 0.0, 0.0
    ions = re.finditer(mask, molecule)
    stack = [{}]

    for ion in ions:
        if ion.group('element'):
            element = ion.group('element')
            quantity = float(ion.group('quantity') or 1)
            stack[-1][element] = quantity
        elif ion.group('open'):
            stack.append({})
        elif ion.group('close'):
            group = stack.pop()
            multiplier = float(ion.group('close_quantity') or 1)
            for element, quantity in group.items():
                stack[-1][element] = stack[-1].get(element, 0) + quantity * multiplier
    
    output = stack[0]

    for el, qt in output.items():
        props = elements.get(el)
        if props:
            charge = props['charge']
            if charge > 0:
                cations[el] = qt
                total_pos_charge += qt * charge
            else:
                anions[el] = qt
                total_neg_charge += qt * charge
    
    balance = total_pos_charge + total_neg_charge

    return cations, anions, balance

def mineral_formula(input_file, output_file):
    elements = load_data('./src/data/elements.csv')

    with open(input_file, mode='r', encoding='utf-8') as f_input, \
        open(output_file, mode='w', newline='', encoding='utf-8') as f_output:
        reader = csv.DictReader(f_input)

        fieldnames = ['molecula', 'analise quimica', 'massa molar', 'prop molecular', 'prop cations', 'prop anions']
        writer = csv.DictWriter(f_output, fieldnames=fieldnames, extrasaction='ignore')
        writer.writeheader()

        for row in reader:
            mol = row.get('molecula') or row.get('Molecula')
            content_value = row.get('analise quimica') or row.get('análise química')

            if not mol or not content_value:
                print(f'Warning: linha inválida ou coluna ausente: {row}')
                continue

            try:
                content = float(str(content_value).replace(',', '.'))
            except ValueError:
                print(f'Warning: valor de análise química inválido para {mol}: {content_value}. Pulando.')
                continue

            cats, anis, balance = get_ions(mol, elements)
            all_atoms = {**cats, **anis}
            mass = sum(elements[el]['mass'] * qt for el, qt in all_atoms.items() if el in elements)

            if mass == 0:
                print(f'Warning: não foi possível calcular a massa molar de {mol}. Pulando.')
                continue

            if abs(balance) > 1e-6:
                print(f'Warning: molécula {mol} apresenta balanço de carga não nulo ({balance}). Gravando saída mesmo assim.')

            prop_mol = content / mass
            prop_cat = prop_mol * sum(cats.values())
            prop_ani = prop_mol * sum(anis.values())

            writer.writerow({
                fieldnames[0]: mol,
                fieldnames[1]: round(content, 3),
                fieldnames[2]: round(mass, 3),
                fieldnames[3]: round(prop_mol, 3),
                fieldnames[4]: round(prop_cat, 3),
                fieldnames[5]: round(prop_ani, 3),
            })
