import os
from datetime import datetime, date
import argparse
import asyncio
from tabulate import tabulate
from dotenv import load_dotenv
from azure.identity import DefaultAzureCredential
from azure.mgmt.resource.resources.v2022_09_01 import ResourceManagementClient
from azure.core.exceptions import ResourceNotFoundError
from resource_graph_query import run_azure_rg_query

async def list_resource_groups_with_temporary_tag(subscription_id: str):
	"""
	List the resource groups in authenticated subscriptions with Temporary tag value as TRUE
	:return:
	"""
	# load_dotenv()
	credential = DefaultAzureCredential()
	resource_management_client = ResourceManagementClient(subscription_id=subscription_id, credential=credential)
	tag_filter= f"tagName eq 'Temporary' and tagValue eq 'TRUE'"
	all_rgs_filtered = resource_management_client.resource_groups.list(filter=tag_filter)
	rgs_to_deleted = []
	for rg in all_rgs_filtered:
		rg_dict = {
			'name': rg.name,
			'location': rg.location
		}
		rgs_to_deleted.append(rg_dict) # final dictionary of rgs to be deleted with Temporary tag value as TRUE

	# print(rgs_to_deleted)
	return rgs_to_deleted


async def delete_resource_groups(subscription_id: str, rgs_to_be_deleted: list[dict]):
	"""
	Delete the resource groups with Temporary tag value as TRUE
	:return:
	"""
	credential = DefaultAzureCredential()
	resource_management_client = ResourceManagementClient(subscription_id=subscription_id, credential=credential)

	for rg in rgs_to_be_deleted:
		try:
			print(f"Deleting {rg['name']} from {subscription_id} subscription")
			resource_management_client.resource_groups.begin_delete(resource_group_name=rg['name']).result()
			print(f"Successfully deleted {rg['name']}")

		except ResourceNotFoundError:

			print(f"Resource group '{rg['name']}' not found.")

		except Exception as e:

			print(f"Failed to delete resource group '{rg['name']}': {e}")
		# Optional: Add a short delay between deletions to prevent overwhelming the service
		await asyncio.sleep(1)


def list_resources_in_rg(subscription_id:str, rgs_to_be_deleted: list[dict]):
	"""
	get the list of resources inside an RG
	:param rgs_to_be_deleted:
	:return:
	"""
	credential = DefaultAzureCredential()
	resource_management_client = ResourceManagementClient(subscription_id=subscription_id, credential=credential)

	details_to_display = []
	for rg in rgs_to_be_deleted:
		try:
			resource_list = resource_management_client.resources.list_by_resource_group(resource_group_name=rg['name'])
			for resources in resource_list:
				resource = {
					'name' : resources.name,
					'resource_id' : resources.id,
					'resource_type' : resources.type,
					'resource_group' : rg['name']
				}
				details_to_display.append(resource)

		except Exception as e:

			print(f"Failed to reteive resources from resource group '{rg['name']}': {e}")

	return details_to_display


async def main():
	"""To test the code"""
	start_time = datetime.utcnow()  # Get start time in UTC
	print(f"Process started at (UTC): {start_time}")
	load_dotenv()
	parser = argparse.ArgumentParser("Decommission nolonger used resource groups in Azure.")
	parser.add_argument("--subscription_name", type=str, required=True,help="Azure subscription name")

	args = parser.parse_args()

	subscription_name = args.subscription_name
	subscription_id = run_azure_rg_query(subscription_name=subscription_name)
	rgs_to_deleted = await list_resource_groups_with_temporary_tag(subscription_id=subscription_id)
	details_to_dispaly = list_resources_in_rg(subscription_id=subscription_id, rgs_to_be_deleted=rgs_to_deleted)
	await delete_resource_groups(subscription_id=subscription_id, rgs_to_be_deleted=rgs_to_deleted)
	print(f"The below resources are decommisioned on {date.today()}")
	# Extracting headers and rows
	headers = ["Name", "Type", "ID", "Resource Group Name"]
	rows = [[item["name"], item["resource_type"], item["resource_id"], item["resource_group"]] for item in details_to_dispaly]
	# Printing in tabular format
	print(tabulate(rows, headers=headers, tablefmt="grid"))
	end_time = datetime.utcnow()  # Get end time in UTC
	print(f"Process completed at (UTC): {end_time}")
	# Calculate and print elapsed time
	elapsed_time = end_time - start_time
	print(f"Total elapsed time: {elapsed_time} (hh:mm:ss)")

if __name__ == "__main__":
	asyncio.run(main())
