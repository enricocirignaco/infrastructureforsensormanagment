class RDFEnumMixin:
    _rdf_base_uri = 'http://data.bfh.ch/'

    @property
    def rdf_uri(self) -> str:
        return f'{self._rdf_base_uri}{self.__class__.__name__}/{self.value}'

    @classmethod
    def from_rdf_uri(cls, rdf_uri: str):
        cleaned_uri = rdf_uri.strip('<>')
        state_name = cleaned_uri.split('/')[-1]
        try:
            return cls(state_name)
        except ValueError:
            raise ValueError(f"Invalid RDF URI: {rdf_uri} does not correspond to a valid {cls.__name__}.")
