import boto3
import os

def s3_connection(access_key_id, access_key_pass):
    try:
        s3 = boto3.client(
            service_name="s3",
            region_name="ap-northeast-2", # 자신이 설정한 bucket region
            aws_access_key_id = access_key_id,
            aws_secret_access_key = access_key_pass,
        )
    except Exception as e:
        print(e)
    else:
        print("s3 bucket connected!")
        return s3

def s3_put_object(s3, bucket, filepath, access_key):
    """
    s3 bucket에 지정 파일 업로드
    :param s3: 연결된 s3 객체(boto3 client)
    :param bucket: 버킷명
    :param filepath: 파일 위치
    :param access_key: 저장 파일명
    :return: 성공 시 True, 실패 시 False 반환
    """
    try:
        s3.upload_file(
            Filename=filepath,
            Bucket=bucket,
            Key=access_key,
            ExtraArgs={"ContentType": "image/png", "ACL": "public-read"},
        )
    except Exception as e:
        print(e,"error")
        return False
    
    return True

def s3_get_image_url(s3, filename):
    """
    s3 : 연결된 s3 객체(boto3 client)
    filename : s3에 저장된 파일 명
    """
    location = s3.get_bucket_location(Bucket="12war")["LocationConstraint"]
    return f"https://12war.s3.{location}.amazonaws.com/{filename}.jpg"




