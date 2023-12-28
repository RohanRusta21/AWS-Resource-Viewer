import streamlit as st
import pandas as pd
import boto3

def display_ec2_instances(session):
    ec2_client = session.client("ec2")
    instances = ec2_client.describe_instances()["Reservations"]

    resource_details = []
    for instance in instances:
        for instance_info in instance["Instances"]:
            resource_details.append(
                f"Instance ID: {instance_info['InstanceId']}\n"
                f"Instance Type: {instance_info['InstanceType']}\n"
                f"State: {instance_info['State']['Name']}\n{'-'*12}"
            )
    return len(instances), resource_details

def display_s3_buckets(session):
    s3_client = session.client("s3")
    buckets = s3_client.list_buckets()["Buckets"]

    resource_details = []
    for bucket in buckets:
        resource_details.append(
            f"Bucket Name: {bucket['Name']}\n{'-'*12}"
        )
    return len(buckets), resource_details

def display_rds_instances(session):
    rds_client = session.client("rds")
    instances = rds_client.describe_db_instances()["DBInstances"]

    resource_details = []
    for db_instance in instances:
        resource_details.append(
            f"DB Instance ID: {db_instance['DBInstanceIdentifier']}\n"
            f"Engine: {db_instance['Engine']}\n"
            f"Status: {db_instance['DBInstanceStatus']}\n{'-'*12}"
        )
    return len(instances), resource_details

def display_dynamodb_tables(session):
    dynamodb_client = session.client("dynamodb")
    tables = dynamodb_client.list_tables()["TableNames"]
    
    resource_details = []
    for table in tables:
        resource_details.append(
            f"Table Name: {table}\n{'-'*12}"
        )
    return len(tables), resource_details

def display_lambda_functions(session):
    lambda_client = session.client("lambda")
    functions = lambda_client.list_functions()["Functions"]

    resource_details = []
    for function in functions:
        resource_details.append(
            f"Function Name: {function['FunctionName']}\n"
            f"Runtime: {function['Runtime']}\n"
            f"Last Modified: {function['LastModified']}\n{'-'*12}"
        )
    return len(functions), resource_details

def display_iam_users(session):
    iam_client = session.client("iam")
    users = iam_client.list_users()["Users"]

    resource_details = []
    for user in users:
        resource_details.append(
            f"IAM User Name: {user['UserName']}\n{'-'*12}"
        )
    return len(users), resource_details

def display_cloudformation_stacks(session):
    cloudformation_client = session.client("cloudformation")
    stacks = cloudformation_client.describe_stacks()["Stacks"]

    resource_details = []
    for stack in stacks:
        resource_details.append(
            f"Stack Name: {stack['StackName']}\n"
            f"Stack Status: {stack['StackStatus']}\n{'-'*12}"
        )
    return len(stacks), resource_details

def main():
    st.title("AWS Resource Viewer")

    # Collect user input
    access_key = st.text_input("AWS Access Key", type="password")
    secret_key = st.text_input("AWS Secret Access Key", type="password")
    region = st.selectbox("Region", list(boto3.Session().get_available_regions("ec2")))

    # Select which resources to display
    col1, col2, col3 = st.columns(3)
    show_ec2 = col1.checkbox("Show EC2 Instances", value=True)
    show_s3 = col2.checkbox("Show S3 Buckets", value=True)
    show_rds = col3.checkbox("Show RDS Instances", value=True)

    col4, col5, col6 = st.columns(3)
    show_dynamodb = col4.checkbox("Show DynamoDB Tables", value=True)
    show_lambda = col5.checkbox("Show Lambda Functions", value=True)
    show_iam = col6.checkbox("Show IAM Users", value=True)

    col7, col8, col9 = st.columns(3)
    show_cloudformation = col7.checkbox("Show CloudFormation Stacks", value=True)

    # Authenticate with AWS (only if inputs are valid)
    if access_key and secret_key:
        try:
            session = boto3.Session(
                aws_access_key_id=access_key,
                aws_secret_access_key=secret_key,
                region_name=region
            )

            # Display selected AWS resources
            resource_counts = []
            resource_labels = []
            resource_details = []

            if show_ec2:
                count, details = display_ec2_instances(session)
                resource_counts.append(count)
                resource_labels.append("EC2")
                resource_details.extend(details)

            if show_s3:
                count, details = display_s3_buckets(session)
                resource_counts.append(count)
                resource_labels.append("S3")
                resource_details.extend(details)

            if show_rds:
                count, details = display_rds_instances(session)
                resource_counts.append(count)
                resource_labels.append("RDS")
                resource_details.extend(details)

            if show_dynamodb:
                count, details = display_dynamodb_tables(session)
                resource_counts.append(count)
                resource_labels.append("DynamoDB")
                resource_details.extend(details)

            if show_lambda:
                count, details = display_lambda_functions(session)
                resource_counts.append(count)
                resource_labels.append("Lambda")
                resource_details.extend(details)

            if show_iam:
                count, details = display_iam_users(session)
                resource_counts.append(count)
                resource_labels.append("IAM Users")
                resource_details.extend(details)

            if show_cloudformation:
                count, details = display_cloudformation_stacks(session)
                resource_counts.append(count)
                resource_labels.append("CloudFormation")
                resource_details.extend(details)

            # Display total count
            total_resources = sum(resource_counts)
            st.success(f"Total Number of Resources: {total_resources}")

            # Display dynamic bar chart
            df = pd.DataFrame({"Resource": resource_labels, "Count": resource_counts})
            st.bar_chart(df.set_index("Resource"))

            # Display resource details
            st.subheader("Resource Details")
            for detail in resource_details:
                st.text(detail)

        except Exception as e:
            st.error(f"Error: {e}")

if __name__ == "__main__":
    main()
