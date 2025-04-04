import argparse
import pandas as pd

def add_args(parser: argparse.ArgumentParser):
    parser.add_argument('--bucket', type=str, default='',
        help='gcs bucket name')
    parser.add_argument('--prefix', type=str, default='',
        help='gcs bucket prefix')

def get_metadata(bucket, prefix, **kwargs):
    from google.cloud.storage import Client
    import pytz
    from datetime import datetime

    gcs = Client.from_service_account_json('service_account.json')
    model_blobs = gcs.list_blobs(bucket, prefix=prefix, match_glob='**.usdz')
    cutoff_date = datetime(2024, 9, 1)
    tz_ny= pytz.timezone('America/New_York')
    date_tmz = tz_ny.localize(cutoff_date)
    
    blobs = []
    for page in model_blobs.pages:
        for blob in page:
            if blob.time_created >= date_tmz:
                blobs.append(blob)

    blobs.sort(key=lambda blob: blob.time_created, reverse=True)
     
    metadata = {'sha256': [], 'file_identifier': [], 'aesthetic_score': [], 'captions': [], 'rendered': [], 'voxelized': [], 'num_voxels': [], 'cond_rendered': []}
    blob
    for blob in blobs:
        metadata['sha256'].append(blob.md5_hash)
        metadata['file_identifier'].append(blob.name)
        metadata['aesthetic_score'].append(7.0)
        metadata['captions'].append('["A photorealistic human body"]')
        metadata['rendered'].append(False)
        metadata['voxelized'].append(False)
        metadata['num_voxels'].append(0)
        metadata['cond_rendered'].append(False)        
    return pd.DataFrame(metadata, columns=['sha256', 'file_identifier', 'aesthetic_score', 'captions', 'rendered', 'voxelized', 'num_voxels', 'cond_rendered'])

def download(metadata, output_dir, bucket, **kwargs):
    from google.cloud.storage import Client, transfer_manager
    import os

    raw_dir = os.path.join(output_dir, 'raw')
    os.makedirs(raw_dir, exist_ok=True)

    gcs = Client.from_service_account_json('service_account.json')
    
    bucket = gcs.bucket(bucket)
    
    blob_names = metadata['file_identifier'].tolist()
    
    results = transfer_manager.download_many_to_path(
        bucket, blob_names, destination_directory=raw_dir, max_workers=8, skip_if_exists=True
    )

    downloaded = {}

    metadata = metadata.set_index("file_identifier")
    for name, result in zip(blob_names, results):
        if isinstance(result, Exception):
            print("Failed to download {} due to exception: {}".format(name, result))
        else:
            sha256 = metadata.loc[name, "sha256"]
            downloaded[sha256] = os.path.join('raw', name)

    return pd.DataFrame(downloaded.items(), columns=['sha256', 'local_path'])


def foreach_instance(metadata, output_dir, func, max_workers=None, desc='Processing objects') -> pd.DataFrame:
    import os
    from concurrent.futures import ThreadPoolExecutor
    from tqdm import tqdm
    
    # load metadata
    metadata = metadata.to_dict('records')

    # processing objects
    records = []
    max_workers = max_workers or os.cpu_count()
    try:
        with ThreadPoolExecutor(max_workers=max_workers) as executor, \
            tqdm(total=len(metadata), desc=desc) as pbar:
            def worker(metadatum):
                try:
                    local_path = metadatum['file_identifier']
                    sha256 = metadatum['sha256']
                    file = os.path.join(output_dir, 'raw', local_path)
                    record = func(file, sha256)
                    if record is not None:
                        records.append(record)
                    pbar.update()
                except Exception as e:
                    print(f"Error processing object {sha256}: {e}")
                    pbar.update()
            
            executor.map(worker, metadata)
            executor.shutdown(wait=True)
    except:
        print("Error happened during processing.")
        
    return pd.DataFrame.from_records(records)
