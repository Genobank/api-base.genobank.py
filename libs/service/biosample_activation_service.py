from libs.dao import biosample_activation_dao
from libs.exceptions import DomainInjectionError


class biosample_activation_service:
    def __init__(
        self,
        _biosample_activation,
    ):
        if not isinstance(
            _biosample_activation, biosample_activation_dao.biosample_activation_dao
        ):
            raise DomainInjectionError.DomainInjectionError(
                "biosample_activation_service", "biosample_activation"
            )
        self.biosample_activation = _biosample_activation

    def fetch(self, _filters={}, _projection={}):
        biosample_activations = self.biosample_activation.fetch(_filters, _projection)
        if not biosample_activations:
            raise ValueError("400 Biosample Activation Not Found")
        else:
            return self.biosample_activation.cur_list_to_scheme(biosample_activations)

    def fetch_v2(self, _filters={}, _projection={}):
        biosample_activations = self.biosample_activation.fetch(_filters, _projection)
        if not biosample_activations:
            return None
        return self.biosample_activation.cur_list_to_scheme(biosample_activations)

    def fetch_one(self, _filters={}, _projection={}):
        biosample_activations = self.biosample_activation.fetch(_filters, _projection)
        if not biosample_activations:
            return None
        result = self.biosample_activation.cur_list_to_scheme(biosample_activations)
        return result["data"][0]

    def create(self, data):
        inserted = self.biosample_activation.create_in_db(data)
        return inserted

    def find_all(self):
        biosample_list = self.biosample_activation.find_all()
        if not biosample_list:
            return []
        else:
            return self.biosample_activation.cur_list_to_scheme(biosample_list)

    def find_all_filtered_by(self, filter):
        biosample_list = self.biosample_activation.find_all_filtered(filter)
        print("\n\n\n biosample_liste_filtered: ", biosample_list)
        if not biosample_list:
            raise ValueError("400 Biosample Activation Not Found")
        else:
            return self.biosample_activation.cur_list_to_scheme(biosample_list)["data"]

    def find_by_serial(self, serial):
        biosample = self.biosample_activation.find_by_serial(serial)
        if not biosample:
            return []
        else:
            return biosample

    def update(self, _filter, new_data):
        return self.biosample_activation.update(_filter, new_data)