import requests
import urllib.request
from requests.exceptions import HTTPError
import click

class github_api:
    def get_list_of_gitignore_files(self):
        response = requests.get("https://api.github.com/repos/github/gitignore/contents").json()
        list_of_gitignore_files = [obj for obj in response 
            if obj["type"] == "file" and ".gitignore" in obj["name"]]
        return list_of_gitignore_files

    def download_gitignore_file(self, language):
        click.echo("Trying to download .gitignore file...\n")

        try:
            list_of_gitignore_files = self.get_list_of_gitignore_files()

            # get a list with all (the only) files that are named <language>.gitignore in the repo
            language_gitignore_object = [obj for obj in list_of_gitignore_files 
                if obj["name"].lower() == language.lower() + ".gitignore"]
            # if this list is not empty, download the file
            if len(language_gitignore_object) != 0:
                language_gitignore_object = language_gitignore_object[0]
                url = language_gitignore_object["download_url"]
                click.echo("Downloading " + language_gitignore_object["name"] + " from " + url)
                urllib.request.urlretrieve(url, ".gitignore") # download file
                click.echo("Download successful")
            # else, the user typed the language wrong
            else:
                click.echo(".gitignore not found for " + language + ". Use download-gitignore list to list all the available files.")
                    
        except HTTPError as http_err:
            click.echo("HTTP error occurred: " + http_err)
        except Exception as err:
            click.echo("Other error occurred: " + err) 
            click.echo("\nYou may want to check your internet connection.")