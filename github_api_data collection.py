import requests
import base64
import pandas as pd

organization = "ALPINE ELECTRONICS" #change with your org-names
token = "COMP_TOKEN"

def get_organization_repos_with_readmes(organization, token):
  """Fetches all repository data and READMEs for a given organization.

  Args:
      organization (str): The organization's name.
      token (str): The GitHub personal access token.

  Returns:
      pandas.DataFrame: A DataFrame containing all repository data and their READMEs.
  """

  headers = {"Authorization": f"Bearer {token}"}
  repo_url = f"https://api.github.com/orgs/{organization}/repos"

  # Fetch all repositories
  repo_response = requests.get(repo_url, headers=headers)
  repo_data = repo_response.json()

  # Create a list to store repository data and READMEs
  repo_data_list = []

  # Loop through repositories and make separate calls for READMEs
  for repo in repo_data:
    repo_name = repo["name"]

    # Combine basic repo data with an empty "readme" field
    repo_dict = {**repo, "readme": None}  # ** operator unpacks the dictionary

    # Fetch and decode the README content (if it exists)
    readme_url = f"https://api.github.com/repos/{organization}/{repo_name}/readme"
    try:
      readme_response = requests.get(readme_url, headers=headers)
      readme_data = readme_response.json()
      readme_content = readme_data["content"]
      decoded_content = base64.b64decode(readme_content).decode("utf-8")
      repo_dict["readme"] = decoded_content
    except requests.exceptions.RequestException as e:
      # Handle potential errors gracefully (e.g., missing README)
      print(f"Error fetching README for {repo_name}: {e}")

    repo_data_list.append(repo_dict)

  # Create a DataFrame from the list
  repo_df = pd.DataFrame(repo_data_list)

  return repo_df

repo_df = get_organization_repos_with_readmes(organization, token)

repo_df.to_csv(f'{organization}_github_data.csv')

