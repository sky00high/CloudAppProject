import boto3
import json
client = boto3.client('lambda')


def lambda_handler(event, context):
    print event
    if(event['relationship'] == 'follow'):
        if(event['operation'] == 'create'):
            createFollowRelationship(event['own_email'],event['target_email'])
    

def createFollowRelationship(ownUUID, targetUUID):
    checkExistOrCreateCustomerInGraph(ownUUID)
    checkExistOrCreateCustomerInGraph(targetUUID);

    addRelationship("follow", ownUUID, targetUUID)


def checkExistOrCreateCustomerInGraph(UUID):
    payload = {
            "operation" : "get",
            "type" : "node",
            "label" : "customer",
            "UUID" : UUID,
            }
    
    response = invokeNeo4jLambda(payload)
    incomingPayload = getPayload(response)

    if(incomingPayload['status'] == 'fail'):
        createCustomer(UUID)

def getPayload(response):
    return json.loads(response['Payload'].read())


def invokeNeo4jLambda(payload):
    response = client.invoke(
        FunctionName =  'Neo4jAPI',
        Payload = json.dumps(payload)
    )

    return response


def createCustomer(UUID):
    try:
        payload = {
                "operation" : "create",
                "type" : "node",
                "label" : "customer",
                "href" : UUID + "lalala",
                "UUID" : UUID
        }

        response = invokeNeo4jLambda(payload)
        incomingPayload = getPayload(response)
        if(incomingPayload['status'] != 'success'):
            raise Exception("500 creating customer failed")
    except:
        raise Exception("500 creating customer failed")


def addRelationship(relationshipType, ownUUID, targetUUID):
    payload = { "operation" : "create",
            "type" : "relationship",
            "relationship_type" : relationshipType,
            "start_UUID" : ownUUID,
            "end_UUID" : targetUUID
    }

    response = invokeNeo4jLambda(payload)


