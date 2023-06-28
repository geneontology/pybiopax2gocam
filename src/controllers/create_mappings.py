
def create_lookup_table(file_path):
    lookup_table = {}

    with open(file_path, 'r') as file:
        for line in file:
            if not line.startswith('!'):
                cols = line.strip().split('\t')
                col1 = cols[1]
                col5 = cols[5]
                lookup_table.setdefault(col1, set()).add(col5)

    return lookup_table


if __name__ == '__main__':
    sgd_tsv_file = '../resources/idmap/YeastCyc/gp_information.559292_sgd'
    lookup_table = create_lookup_table(sgd_tsv_file)

    col1_values = lookup_table.get('URS0000A0AC1F_559292')
    print(col1_values)