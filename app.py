import streamlit as st
import boto3

def display_ec2_instances(session):
    ec2_client = session.client("ec2")
    instances = ec2_client.describe_instances()["Reservations"]

    st.subheader("EC2 Instances")
    instance_count = 0
    for instance in instances:
        for instance_info in instance["Instances"]:
            instance_count += 1
            st.write(f"{instance_count}. Instance ID: {instance_info['InstanceId']}")
            st.write(f"   Instance Type: {instance_info['InstanceType']}")
            st.write(f"   State: {instance_info['State']['Name']}")
            st.write("------------")
    return instance_count

def display_s3_buckets(session):
    s3_client = session.client("s3")
    buckets = s3_client.list_buckets()["Buckets"]

    st.subheader("S3 Buckets")
    bucket_count = 0
    for bucket in buckets:
        bucket_count += 1
        st.write(f"{bucket_count}. Bucket Name: {bucket['Name']}")
        st.write("------------")
    return bucket_count

def display_rds_instances(session):
    rds_client = session.client("rds")
    instances = rds_client.describe_db_instances()["DBInstances"]

    st.subheader("RDS Instances")
    rds_count = 0
    for db_instance in instances:
        rds_count += 1
        st.write(f"{rds_count}. DB Instance ID: {db_instance['DBInstanceIdentifier']}")
        st.write(f"   Engine: {db_instance['Engine']}")
        st.write(f"   Status: {db_instance['DBInstanceStatus']}")
        st.write("------------")
    return rds_count

def display_dynamodb_tables(session):
    dynamodb_client = session.client("dynamodb")
    tables = dynamodb_client.list_tables()["TableNames"]

    st.subheader("DynamoDB Tables")
    dynamodb_count = 0
    for table in tables:
        dynamodb_count += 1
        st.write(f"{dynamodb_count}. Table Name: {table}")
        st.write("------------")
    return dynamodb_count

def display_lambda_functions(session):
    lambda_client = session.client("lambda")
    functions = lambda_client.list_functions()["Functions"]

    st.subheader("Lambda Functions")
    lambda_count = 0
    for function in functions:
        lambda_count += 1
        st.write(f"{lambda_count}. Function Name: {function['FunctionName']}")
        st.write(f"   Runtime: {function['Runtime']}")
        st.write(f"   Last Modified: {function['LastModified']}")
        st.write("------------")
    return lambda_count

def display_cloudformation_stacks(session):
    cloudformation_client = session.client("cloudformation")
    stacks = cloudformation_client.describe_stacks()["Stacks"]

    st.subheader("CloudFormation Stacks")
    stack_count = 0
    for stack in stacks:
        stack_count += 1
        st.write(f"{stack_count}. Stack Name: {stack['StackName']}")
        st.write(f"   Stack Status: {stack['StackStatus']}")
        st.write("------------")
    return stack_count

# Add similar display and count logic for other resources

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
    show_cloudformation = col6.checkbox("Show CloudFormation Stacks", value=True)

    # Authenticate with AWS (only if inputs are valid)
    if access_key and secret_key:
        try:
            session = boto3.Session(
                aws_access_key_id=access_key,
                aws_secret_access_key=secret_key,
                region_name=region
            )

            # Display selected AWS resources
            resource_count = 0
            if show_ec2:
                resource_count += display_ec2_instances(session)
            if show_s3:
                resource_count += display_s3_buckets(session)
            if show_rds:
                resource_count += display_rds_instances(session)
            if show_dynamodb:
                resource_count += display_dynamodb_tables(session)
            if show_lambda:
                resource_count += display_lambda_functions(session)
            if show_cloudformation:
                resource_count += display_cloudformation_stacks(session)

            # Display total count
            st.success(f"Total Number of Resources: {resource_count}")

        except Exception as e:
            st.error(f"Error: {e}")

if __name__ == "__main__":
    main()
