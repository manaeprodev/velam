import apache_beam as beam
from apache_beam.options.pipeline_options import PipelineOptions
from apache_beam.io.gcp import bigquery
import json

beam_options = PipelineOptions(
    runner="DataflowRunner",
    project='velam-402208',
    job_name="velam-bigquery",
    region="europe-west9",
)

table_spec = bigquery.TableReference(
    projectId='velam-402208',
    datasetId='velam_dataset',
    tableId='amiens')

table_schema = {
    'fields': [
        {'name': 'nom_station', 'type': 'STRING', 'mode': 'NULLABLE'},
        {'name': 'porte_velo', 'type': 'INTEGER', 'mode': 'NULLABLE'},
        {'name': 'porte_velo_dispo', 'type': 'INTEGER', 'mode': 'NULLABLE'},
        {'name': 'velo_dispo', 'type': 'INTEGER', 'mode': 'NULLABLE'},
        {'name': 'derniere_maj', 'type': 'INTEGER', 'mode': 'NULLABLE'}
    ]
}


class StationName(beam.DoFn):
    def process(self, stations):
        return [station for station in stations]


with beam.Pipeline(options=beam_options) as p:
    (p | "Read" >> beam.io.ReadFromText('gs://ma_data_velam_bucket/')
     | "Lit les données" >> beam.Map(lambda line: json.loads(line))
     | "Split les stations" >> beam.ParDo(StationName())
     | "Nom des stations" >> beam.Map(lambda station: {
                "nom_station": station.get("name", ""),
                "porte_velo": station.get("bike_stands", None),
                "porte_velo_dispo": station.get("available_bike_stands", None),
                "velo_dispo": station.get("available_bikes", None),
                "derniere_maj": station.get("last_update", "")
            })
     | "Enregistre les données" >> beam.io.WriteToBigQuery(table_spec,
                                                           schema=table_schema,
                                                           custom_gcs_temp_location='gs://velam-collection-test',
                                                           write_disposition=beam.io.BigQueryDisposition.WRITE_TRUNCATE,
                                                           create_disposition=beam.io.BigQueryDisposition.CREATE_IF_NEEDED))

    p.run()