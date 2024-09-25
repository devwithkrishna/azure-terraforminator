# azure-terraforminator
 A pipeline to delete unused resources in azure based on a specific tag

[![azure-decommision-unsed-resource-groups-with-temporary-tag-as-true](https://github.com/devwithkrishna/azure-terraforminator/actions/workflows/azure-terraforminator.yaml/badge.svg)](https://github.com/devwithkrishna/azure-terraforminator/actions/workflows/azure-terraforminator.yaml)

# What this does

* Reducing cloud costs and decommissioning unused resources are essential practices for efficient cloud management. 

#### Cost Savings
* Pay-as-you-go model: Cloud services charge based on resource usage, so any unused or idle resources still incur costs. Decommissioning these saves money that can be allocated elsewhere.
* Hidden costs: Over-provisioned or forgotten services like unused VMs, storage, or databases can rack up unexpected costs over time.
#### Resource Optimization
* Avoid over-provisioning: Scaling down unused or underutilized resources ensures you're only paying for what you need, preventing waste.
* Better performance: By right-sizing resources, you allocate appropriate computing power to services, improving overall performance.
#### Improved Security
* Minimize attack surface: Decommissioning unused resources reduces potential vulnerabilities that could be exploited by attackers.
* Avoid data leakage: Retiring unnecessary storage or services prevents accidental exposure of sensitive data.
#### Operational Efficiency
* Simplified management: Fewer resources mean less administrative overhead in terms of monitoring, patching, and maintenance.
* Compliance and governance: Removing outdated or unnecessary assets helps maintain compliance with regulatory standards, as only necessary resources are active


### This is defined in a way that it decommisions a resource group based on a specific tag in azure. When the autmation finds `Temporary` tag wth Value as `TRUE` it decommisions.


#### For the automation to work we needd a service principal which has access to the subscription level atleast with contributor permission as deletion of resources are involved.

#### Configure the below environment variables as GitHub secrets

```markdown
AZURE_CLIENT_ID = "value"
AZURE_CLIENT_SECRET = "value"
AZURE_TENANT_ID = "value"
```

* The code is using python with poetry as package management tool

* This job is set to run as a cron every day and as a manual trigger as well if necessary

```markdown

This is a sample of output showing what are the resources deleted

The below resources are decommisioned on <Date : yyyy-mm-dd>
+------------------------+-----------------------------------+----------------------------------------------------------------------------------------------------------------------------------------------------+-----------------------+
| Name                   | Type                              | ID                                                                                                                                                 | Resource Group Name   |
+========================+===================================+====================================================================================================================================================+=======================+
| Name of resource   | Type | Resource Id   | Rg name          |
+------------------------+-----------------------------------+----------------------------------------------------------------------------------------------------------------------------------------------------+-----------------------+
| mystorageaccountswswwe | Microsoft.Storage/storageAccounts | /subscriptions/es271149ae-05d3-4dcsssf-b946-d71f3f39/resourceGroups/ARCHITECTS-3/providers/Microsoft.Storage/storageAccounts/mystorageaccountswswwe | ARCHITECTS-3          |
+------------------------+-----------------------------------+----------------------------------------------------------------------------------------------------------------------------------------------------+-----------------------+

```