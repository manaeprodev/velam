# velam

Test de l'API : 
Création du compte JCDecaux
Création de l'API key
Test sur postman :
https://api.jcdecaux.com/vls/v1/stations?contract=amiens&apiKey=c92532304cc789279b443569fbb33317df04807f
L'API fonctionne bien.

GCP :
gcloud storage buckets create gs://ma_data_velam_bucket --default-storage-class=STANDARD --location=EUROPE-WEST1
activer cloud shell

gcloud functions deploy velam-api --runtime php82 --trigger-http
activer les API Cloud Functions, Cloud Build, Artifact Registry, Cloud Run, Logging, Pub/Sub, Eventarc

Créer un sujet : gcloud pubsub topics create sujet_velam
