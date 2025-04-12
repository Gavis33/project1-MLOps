from dataclasses import dataclass # dataclass is used to create a class with predefined attributes and methods 

@dataclass
class DataIngestionArtifact:
    trained_file_path: str
    test_file_path: str

