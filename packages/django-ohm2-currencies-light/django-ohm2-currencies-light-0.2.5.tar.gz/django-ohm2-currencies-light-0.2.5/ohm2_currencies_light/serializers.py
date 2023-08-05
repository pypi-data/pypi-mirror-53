from rest_framework import serializers
from . import models as ohm2_currencies_light_models
from . import settings



class Currency(serializers.ModelSerializer):
	class Meta:
		model = ohm2_currencies_light_models.Currency
		fields = (
			'identity',
			'created',
			'last_update',
			'alpha_3',
			'name',
			'symbol',
			'decimals',
			'available',
		)


class ConvertionRate(serializers.ModelSerializer):
	input = Currency()
	output = Currency()

	class Meta:
		model = ohm2_currencies_light_models.ConvertionRate
		fields = (
			'identity',
			'created',
			'last_update',
			'input',
			'output',
			'source',
			'rate',
		)


class LastConvertionRate(serializers.ModelSerializer):
	input = Currency()
	output = Currency()
	convertion_rate = ConvertionRate()
	
	class Meta:
		model = ohm2_currencies_light_models.LastConvertionRate
		fields = (
			'identity',
			'created',
			'last_update',
			'input',
			'output',
			'convertion_rate',
		)
