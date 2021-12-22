import boto3


def s3_connection(access_key_id, access_key_pass):
    try:
        s3 = boto3.client(
            service_name="s3",
            region_name="ap-northeast-2",  # 자신이 설정한 bucket region
            aws_access_key_id=access_key_id,
            aws_secret_access_key=access_key_pass,
        )
    except Exception as e:
        print(e)
    else:
        print("s3 bucket connected!")
        return s3
