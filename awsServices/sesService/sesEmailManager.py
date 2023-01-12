import boto3
import logging
import os
from app.settings import *
from botocore.exceptions import ClientError
# from ses.client.exceptions import TemplateDoesNotExist


LOG_FORMAT = ('%(levelname) -10s %(asctime)s %(name) -30s %(funcName) '
              '-35s %(lineno) -5d: %(message)s')
logger = logging.getLogger(__name__)

logging.basicConfig(level=logging.INFO, format=LOG_FORMAT)


credentials = {
    "ENDPOINT_URL": os.environ.get("ENDPOINT_URL", ""),
    "AWS_ACCESS_KEY_ID": os.environ.get("AWS_ACCESS_KEY_ID", ""),
    "AWS_DEFAULT_REGION": os.environ.get("AWS_DEFAULT_REGION", ""),
    "AWS_SECRET_ACCESS_KEY": os.environ.get("AWS_SECRET_ACCESS_KEY", ""),
    "SMPT_USER": os.environ.get("SMTP_USER", "")
}


class SesEmailManager():

    def __init__(self):
        self.client = boto3.client('ses', endpoint_url=credentials.get("ENDPOINT_URL"), region_name=credentials.get("AWS_DEFAULT_REGION"))


    @staticmethod
    def create_template(client, template_name, subject_part, text_part):
        try:
            response = client.create_template(
            Template = {
                'TemplateName' : template_name,
                'SubjectPart'  : subject_part,
                'TextPart'     : text_part
            }
            )
        except ClientError as e:
            logging.error(e)
            return False
        return response

    def get_template(self, template_name):
        try:
            response = self.client.get_template(TemplateName = template_name)
        except self.client.exceptions.TemplateDoesNotExistException:
            response = self.create_template(self.client, template_name='ses_template', subject_part='Innotter', text_part='New post')
        return response


    @staticmethod
    def verify_email(client):
        email = client.verify_email_identity(
            EmailAddress=credentials.get("SMPT_USER"),
            )
        return email


    def send_mail(self, email_list):
        try:
            SesEmailManager.verify_email(self.client)
            response = self.client.send_templated_email(
                Source=credentials.get("SMPT_USER"),
                Destination={
                    'ToAddresses': email_list,
                },
                Template='ses_template',
                TemplateData='{ \"REPLACEMENT_TAG_NAME\":\"REPLACEMENT_VALUE\" }'
            )
        except ClientError:
            logger.exception(
                "Couldn't send email")
            raise
        return response
    