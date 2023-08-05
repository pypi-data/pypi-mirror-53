from dq import _queue, TIME_FORMAT

import boto3
from boto3.dynamodb.conditions import Key
from datetime import datetime
from time import sleep


class DynamoDB(_queue):
    def __init__(self, name):
        super().__init__(name)
        self.client = boto3.client('dynamodb')
        self.table = boto3.resource('dynamodb').Table(self.name)
        try:
            desc = self.table.load()
            if desc['TableDescription']['TableStatus'] != 'ACTIVE':
                raise Exception('Table %s not ready' % self.name)
        except Exception as e:
            if 'ResourceNotFoundException' in str(e):
                self.create_table(name)

    def __exit__(self, exc_type, exc_val, exc_tb):
        with self.table.batch_writer() as writer:
            for txn in self.get_log():
                action, qitem = txn
                if action == self.CREATE:
                    writer.put_item(Item=qitem)
                elif action == self.DELETE:
                    del (qitem['val'])
                    self.table.delete_item(Key=qitem)

    def __call__(self, qid=None, start_time=None, end_time=None, limit=0):
        start_time = datetime(1, 1, 1) if start_time is None else start_time
        end_time = datetime.utcnow() if end_time is None else end_time
        kwargs = {
            'Select': 'ALL_ATTRIBUTES',
            'KeyConditionExpression': Key('ts').between(start_time.strftime(TIME_FORMAT),
                                                        end_time.strftime(TIME_FORMAT)),
            'ConsistentRead': True,
            'ScanIndexForward': False
        }
        if qid is not None:
            kwargs['KeyConditionExpression'] &= Key('qid').eq(qid)
        if limit > 0:
            kwargs['Limit'] = int(limit)
        response = self.table.query(**kwargs)
        with self.mutex:
            self.queue.extend(response['Items'])
        lek = response['LastEvaluatedKey'] if 'LastEvaluatedKey' in response else None
        while lek is not None:
            kwargs['ExclusiveStartKey'] = lek
            response = self.table.query(**kwargs)
            with self.mutex:
                self.queue.extend(response['Items'])
            lek = response['LastEvaluatedKey'] if 'LastEvaluatedKey' in response else None

    def create_table(self, name):
        self.client.create_table(TableName=name, AttributeDefinitions=[
            {'AttributeName': 'qid', 'AttributeType': 'S'},
            {'AttributeName': 'ts', 'AttributeType': 'S'}
        ], KeySchema=[
            {'AttributeName': 'qid', 'KeyType': 'HASH'},
            {'AttributeName': 'ts', 'KeyType': 'RANGE'}
        ], ProvisionedThroughput={
            'ReadCapacityUnits': 1,
            'WriteCapacityUnits': 1
        })
        while True:
            sleep(0.2)
            resp = self.client.describe_table(TableName=name)
            if resp['Table']['TableStatus'] == 'ACTIVE':
                break
