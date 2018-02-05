import os


def get_dir_names(input_dir):
    output_dirs = []
    all_dirs = os.listdir(input_dir)
    fastqc_dirs = [i for i in all_dirs if all([
        i.endswith('fastqc'),
        os.path.isdir(os.path.join(input_dir, i)),
    ])]
    fqc_dirs = {'r1':[], 'r2':[], 'other':[]}
    for fqc_dir in fastqc_dirs:
    	if fqc_dir.find('_R1_') > -1:
            fqc_dirs['r1'].append(fqc_dir)
        elif fqc_dir.find('_R2_') > -1:
        	fqc_dirs['r2'].append(fqc_dir)
        else:
        	fqc_dirs['other'].append(fqc_dir)
    for r1_dir in fqc_dirs['r1']:
    	if r1_dir.replace('_R1_', '_R2_') in fqc_dirs['r2']:
    		output_dirs.append({
    			    'r1': os.path.join(
                    input_dir, r1_dir,
				    ),
				    'r2': os.path.join(
		            input_dir, r1_dir.replace('_R1_', '_R2_'),
				    ),
    			})
        else:
        	output_dirs.append({
    			    'r1': os.path.join(
                    input_dir, r1_dir,
				    ),
				    'r2': None,
    			})
    for r2_dir in fqc_dirs['r2']:
    	if not r2_dir.replace('_R2_', '_R1_') in fqc_dirs['r1']:
    		output_dirs.append({
			    'r1': os.path.join(
                input_dir, r2_dir,
			    ),
			    'r2': None,
			})
    for r1_dir in fqc_dirs['other']:
        output_dirs.append({
		    'r1': os.path.join(
            input_dir, r1_dir,
		    ),
		    'r2': None,
		})
    return output_dirs


def _parse_per_base_sequence_quality(out_temp1, output_fqc, headers):
	columns = None
	parsed = []
	for line in out_temp1['Per base sequence quality']['lines']:
        if not columns:
        	columns = line.strip('#\n').split('\t')
        else:
        	parsed.append(dict(zip(columns, line.strip().split('\t'))))
    for line in parsed:
    	key_str = 'pbsq_median_{}'.format(line['Base'])
    	output_fqc[key_str] = line['Median']
    	headers.append(key_str)
    return headers, output_fqc


def parse_fastqc_data(fastqc_data):
	output_fqc = {}
	out_temp1 = {}
	with open(fastqc_data) as input_fh:
		module_id = 'END_MODULE'
		for line in input_fh:
			if line.startswith('>>'):
				if module_id == 'END_MODULE':
                    module_id = line.strip('>\n').split('\t')
                    out_temp1[module_id[0]] = {
                       'outcome': module_id[1],
                       'lines': [],
                    }
                else:
                	module_id = line.strip('>\n')
            elif line.startswith('##'):
            	pass
            else:
            	out_temp1[module_id[0]]['lines'].append(line.strip())


if __name__ == '__main__':
	pass
