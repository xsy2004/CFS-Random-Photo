# -*- coding=utf-8
from qcloud_cos import CosConfig
from qcloud_cos import CosS3Client
from random import choice
# https://console.cloud.tencent.com/cam/capi 生成
secret_id = ''
secret_key = ''
region = ''
scheme = 'https'
bucket = ''


def render_template(html, keys={}):
    for k, v in keys.items():
        html = html.replace("${" + k + "}", v)
    return html


def main_handler(event, context):
    config = CosConfig(Region=region, SecretId=secret_id, SecretKey=secret_key, Scheme=scheme)
    client = CosS3Client(config)
    listObjects = client.list_objects(Bucket=bucket)
    fileList = []
    # 遍历所有文件名
    for fileName in listObjects['Contents']:
        fileList.append(fileName["Key"])

    # 随机选取文件名
    randomFileName = choice(fileList)

    fileUrl = client.get_presigned_url(
        Method='GET',
        Bucket=bucket,
        Key=randomFileName,
        Expired=120,
        # Params={
        #     'response-content-disposition': 'inline;'  # 参见 https://cloud.tencent.com/document/product/436/7753
        # },
    )
    f = open("./index.html")
    html = f.read()
    keys = {
        "link": fileUrl,
    }
    html = render_template(html, keys)
    print(fileUrl)
    return {
        "isBase64Encoded": False,
        "statusCode": 200,
        "headers": {'Content-Type': 'text/html'},
        "body": html
    }
