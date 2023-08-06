DATA_INFO = dict(
	CamVid=dict(dir='CamVid',
				n_classes=13),
	leaf=dict(dir='leaf-classification',
				n_classes=99),
	DUT=dict(dir='DUT-OMRON'),
	MSRA_B=dict(dir='MSRA_B')
)


DATA_ROOT = dict(
	root_dir='/run/media/hanshan/data2/Data',
	dataset_dir='DataSets',
	csv_dir='CSVs',
	data_name='CamVid',
	data_info=DATA_INFO['CamVid'],
	normalize=dict(
		mean=[0.485, 0.456, 0.406],
		std=[0.229, 0.224, 0.225]
	),
	resize=(224, 224),

	train=dict(
		batch_size=16,
		num_workers=8
	),
	valid=dict(
		batch_size=16,
		num_workers=8,
	)
)


class DataConfiger(object):
	@classmethod
	def set_data_root_dir(cls, data_root_dir):
		DATA_ROOT['root_dir'] = data_root_dir
	@classmethod
	def get_all_data_name(cls):
		return DATA_INFO.keys()

	@classmethod
	def get_data_config(cls, data_name):
		new_config = DATA_ROOT
		new_config['data_info'] = DATA_INFO[data_name]
		new_config['data_name'] = DATA_INFO[data_name]['dir']
		return new_config
