import requests
import pandas as pd
import os


def login(username, password):
    headers = {
        'Content-Type': 'application/json',
    }

    data = '{"username":"' + username + '","password":"' + password + '"}'

    token = requests.post('https://dcc.icgc.org/api/v1/auth/login', headers=headers, data=data).json()['token']

    return token


def download_file_by_primary_site(filetype, primary_site, keep_file=False):
    filename = str(filetype) + "_" + primary_site + ".tsv.gz"
    params = (
        ('filters', '{"donor":{"primarySite":{"is":["' + primary_site + '"]}}}'),
        ('info', '[{"key":"' + filetype + '","value":"TSV"}]'),
    )
    download_id = requests.get('https://dcc.icgc.org/api/v1/download/submit', params=params).json()["downloadId"]
    response = requests.get('https://dcc.icgc.org/api/v1/download/' + download_id)
    open(filename, 'wb').write(response.content)
    df = pd.read_csv(filename, sep="\t", compression="gzip", low_memory=False)
    if not keep_file:
        os.remove(filename)

    return df


def download_data_release(params, cookies, filename, keep_file):
    response = requests.get('https://dcc.icgc.org/api/v1/download', params=params, cookies=cookies)
    open(filename, 'wb').write(response.content)
    df = pd.read_csv(filename, sep="\t", compression="gzip", low_memory=False)
    if not keep_file:
        os.remove(filename)
    return df


def download_file_by_project(token, release, project_code, filetype, status="controlled", keep_file=False):
    filename = filetype + "_" + str(release) + "_" + project_code + "_" + status + ".tsv.gz"

    cookies = {
        'dcc_portal_token': str(token),
    }

    params = (
        ('fn', '/release_' + str(release) +
         '/Projects/' + str(project_code) +
         '/' + filetype + '.' + status + '.' +
         str(project_code) + '.tsv.gz'),
    )

    try:
        df = download_data_release(params, cookies, filename, keep_file)
    except:
        try:
            params = (
                ('fn', '/release_' + str(release) +
                 '/Projects/' + str(project_code) +
                 '/' + filetype + '.' + "open" + '.' +
                 str(project_code) + '.tsv.gz'),
            )
            df = download_data_release(params, cookies, filename, keep_file)
        except:
            params = (
                ('fn', '/release_' + str(release) +
                 '/Projects/' + str(project_code) +
                 '/' + filetype + '.' +
                 str(project_code) + '.tsv.gz'),
            )
            df = download_data_release(params, cookies, filename, keep_file)

    return df


def download_donor_summary(token, filetype, release, keep_file=False):
    filename = filetype + ".all_projects.tsv.gz"

    cookies = {
        'dcc_portal_token': str(token),
    }

    params = (
        ('fn', '/release_' + str(release) +
         '/Summary/' + filename),
    )

    return download_data_release(params, cookies, filename, keep_file)
