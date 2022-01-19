import strawberry

import movierental.api.definitions.film as film
from movierental.database.models import City as CityModel
from movierental.database.models import Addres as AddressModel
from movierental.database.models import Country as CountryModel


@strawberry.type(description="A country and it's properties")
class Country:
    country_id: int = strawberry.field(description="Id of the country")
    country_name: str = strawberry.field(description="Name of the country")

    @classmethod
    def from_instance(cls, instance):
        return cls(country_id=instance.country_id, country_name=instance.country)


@strawberry.type(description="A city and it's properties")
class City:
    city_id: int = strawberry.field(description="Id of the city")
    city_name: str = strawberry.field(description="Name of the city")

    instance: strawberry.Private[CityModel]

    @strawberry.field
    def country(self) -> Country:
        return Country.from_instance(self.instance.country)

    @classmethod
    def from_instance(cls, instance):
        return cls(instance=instance, city_id=instance.city_id, city_name=instance.city)


@strawberry.type(description="Address and it's properties")
class Address:
    address_id: int = strawberry.field(description="Id of the address")
    address: str = strawberry.field(description="First address field")
    address2: str = strawberry.field(description="Second address field")
    district: str = strawberry.field(description="District of address")
    postal_code: str = strawberry.field(description="Postal code of address")
    phone: str = strawberry.field(
        description="Phone number associated with the address"
    )

    instance: strawberry.Private[AddressModel]

    @strawberry.field
    def city(self) -> City:
        return City.from_instance(self.instance.city)

    @classmethod
    def from_instance(cls, instance):
        return cls(
            instance=instance,
            address_id=instance.address_id,
            address=instance.address,
            address2=instance.address2,
            district=instance.district,
            postal_code=instance.postal_code,
            phone=instance.phone,
        )
