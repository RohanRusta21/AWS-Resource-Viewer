import streamlit as st
import boto3
from datetime import datetime, timedelta
from botocore.exceptions import ClientError

def get_cost_explorer_data(aws_access_key_id, aws_secret_access_key, aws_region, start_date, end_date):
    try:
        # Set up Boto3 Cost Explorer client with provided credentials and region
        ce_client = boto3.client('ce',
                                aws_access_key_id=aws_access_key_id,
                                aws_secret_access_key=aws_secret_access_key,
                                region_name=aws_region)

        # Define other parameters for the Cost Explorer query
        granularity = 'DAILY'
        metrics = ['BlendedCost']

        # Specify dimensions to group by (e.g., service, instanceType)
        dimensions = [{'Type': 'DIMENSION', 'Key': 'SERVICE'}, {'Type': 'DIMENSION', 'Key': 'INSTANCE_TYPE'}]

        # Execute the Cost Explorer query
        response = ce_client.get_cost_and_usage(
            TimePeriod={'Start': start_date, 'End': end_date},
            Granularity=granularity,
            Metrics=metrics,
            GroupBy=dimensions
        )

        return response

    except ClientError as e:
        # Handle the specific exception
        error_message = str(e.response['Error']['Message'])
        st.error(f"An error occurred: {error_message}")
        return None

# Streamlit app
st.title("AWS Cost Explorer App")

# Input fields for AWS credentials, region, and date
aws_access_key_id = st.text_input("Enter your AWS Access Key ID:", type="password")
aws_secret_access_key = st.text_input("Enter your AWS Secret Access Key:", type="password")
aws_region = st.selectbox("Region", list(boto3.Session().get_available_regions("ec2")))
selected_date = st.date_input("Select a date", value=(datetime.now() - timedelta(days=1)))

# Button to get cost explorer data
if st.button("Get Cost Explorer Data"):
    if aws_access_key_id and aws_secret_access_key and aws_region:
        # Convert selected date to start and end dates for the query
        start_date = selected_date.strftime('%Y-%m-%d')
        end_date = (selected_date + timedelta(days=1)).strftime('%Y-%m-%d')

        # Call the function and display the results
        result = get_cost_explorer_data(aws_access_key_id, aws_secret_access_key, aws_region, start_date, end_date)

        # Extract and display relevant cost information
        if result is not None and 'ResultsByTime' in result:
            for result_by_time in result['ResultsByTime']:
                st.write(f"Start Time: {result_by_time['TimePeriod']['Start']}")
                st.write(f"End Time: {result_by_time['TimePeriod']['End']}")
                
                # Check if 'Groups' key is present in the response
                if 'Groups' in result_by_time:
                    # Display costs for each dimension
                    total_cost = 0
                    for group in result_by_time['Groups']:
                        # Check if 'Keys' and 'Metrics' keys are present in the group
                        if 'Keys' in group and 'Metrics' in group:
                            cost_amount = round(float(group['Metrics']['BlendedCost']['Amount']), 2)
                            total_cost += cost_amount
                            st.write(f"{group['Keys'][0]}: {cost_amount:.2f} {group['Metrics']['BlendedCost']['Unit']}")
                    
                    # Display total cost for the day
                    st.success(f"**Total Cost for the Day:** {total_cost:.2f} USD")
                else:
                    st.warning("No cost data available for the selected region and time period.")
                
                st.write("\n")
    else:
        st.warning("Please provide AWS credentials and region.")
