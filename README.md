
# How to use this action

* AZURE_CLIENT_ID: The Client ID of the Azure Service Principal used for authentication.

* AZURE_TENANT_ID: The Tenant ID of your Azure Active Directory where the Service Principal is registered.

* AZURE_CLIENT_SECRET: The Client Secret (password) for the Service Principal.

These values are pulled securely from GitHub repository secrets using ${{ secrets.NAME }} syntax to avoid exposing sensitive credentials in plaintext. The action uses these credentials to authenticate and interact with Azure resources.


```yaml

    - name: Run Azure Terraforminator Action
      uses: devwithkrishna/azure-terraforminator@v1
      env:
        AZURE_CLIENT_ID: ${{ secrets.AZURE_CLIENT_ID }}
        AZURE_TENANT_ID: ${{ secrets.AZURE_TENANT_ID }}
        AZURE_CLIENT_SECRET: ${{ secrets.AZURE_CLIENT_SECRET }}
      with:
        subscription_name: "<Your subscription name>"
```