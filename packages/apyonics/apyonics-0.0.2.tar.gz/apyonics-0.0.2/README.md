# apyonics

Client for interacting with AIONICS APIs

### usage instructions

##### import the package:

    import apyonics

##### start a client:

    client = apyonics.Client(service_url="https://your.service.url",api_key="your-api-key")

##### get feature set for a training set compound by formula: 

    feats = client.get_trainingset_features('Li2Ge7O15')

##### get conductivity of a training set compound by formula:

    feats = client.get_trainingset_conductivity('Li2Ge7O15')

##### get feature set for a candidate compound by Materials Project id:

    feats = client.get_candidate_features('mp-1153')

##### get conductivity of a candidate compound by Materials Project id:

    feats = client.get_candidate_conductivity('mp-1153')

##### get superionic likelihood for a POSCAR file:

    feats = client.predict_from_poscar('/path/to/your/POSCAR')

