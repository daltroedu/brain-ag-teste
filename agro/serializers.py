from django.db import IntegrityError
from rest_framework import serializers

from .business.validators import validate_total_area
from .constants import STATE_CHOICES
from .models import Crop, CropType, Farm, Farmer
from .utils import validate_cpf_cnpj


class FarmerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Farmer
        fields = ["id", "cpf_cnpj", "name"]
        read_only_fields = ("id",)

    def validate_cpf_cnpj(self, value):
        if not validate_cpf_cnpj(value):
            raise serializers.ValidationError("Enter a valid CPF or CNPJ.")
        cpf_cnpj_only_numbers = "".join(filter(str.isdigit, value))
        return cpf_cnpj_only_numbers


class FarmSerializer(serializers.ModelSerializer):
    farmer = FarmerSerializer(read_only=True)
    farmer_id = serializers.PrimaryKeyRelatedField(
        queryset=Farmer.objects.all(), write_only=True, source="farmer"
    )

    class Meta:
        model = Farm
        fields = [
            "id",
            "farmer",
            "farmer_id",
            "name",
            "city",
            "state",
            "total_area_hectares",
            "arable_area_hectares",
            "vegetation_area_hectares",
        ]
        read_only_fields = ("id",)

    def validate_state(self, value):
        if value not in dict(STATE_CHOICES).keys():
            raise serializers.ValidationError(
                "Invalid value for the state. Please set a valid state, e.g.: SP"
            )
        return value

    def validate_total_area_hectares(self, value):
        if value <= 0:
            raise serializers.ValidationError(
                "The total area cannot be negative or zero."
            )
        return value

    def validate_arable_area_hectares(self, value):
        if value < 0:
            raise serializers.ValidationError(
                "The arable area cannot be negative."
            )
        return value

    def validate_vegetation_area_hectares(self, value):
        if value < 0:
            raise serializers.ValidationError(
                "The vegetation area cannot be negative."
            )
        return value

    def validate(self, data):
        if not validate_total_area(data):
            raise serializers.ValidationError(
                "The sum of the arable area and vegetation cannot exceed the total area of the farm."
            )
        return data


class CropTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = CropType
        fields = ["id", "name"]


class CropSerializer(serializers.ModelSerializer):
    crop_type = CropTypeSerializer(read_only=True)
    crop_type_id = serializers.PrimaryKeyRelatedField(
        queryset=CropType.objects.all(), source="crop_type", write_only=True
    )
    farm = FarmSerializer(read_only=True)
    farm_id = serializers.PrimaryKeyRelatedField(
        queryset=Farm.objects.all(), write_only=True, source="farm"
    )
    integrity_error_message = (
        "A crop with this farm and type of crop already exists."
    )

    class Meta:
        model = Crop
        fields = ["id", "farm", "farm_id", "crop_type", "crop_type_id"]
        read_only_fields = ("id",)

    def create(self, validated_data):
        try:
            return super().create(validated_data)
        except IntegrityError:
            raise serializers.ValidationError(self.integrity_error_message)

    def update(self, instance, validated_data):
        try:
            return super().update(instance, validated_data)
        except IntegrityError:
            raise serializers.ValidationError(self.integrity_error_message)
