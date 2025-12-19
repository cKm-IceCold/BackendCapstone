def create_property(user, validated_data):
    validated_data["registered_by"] = user
    return Property.objects.create(**validated_data)


def update_property(property_obj, validated_data):
    for field, value in validated_data.items():
        setattr(property_obj, field, value)
    property_obj.save()
    return property_obj
