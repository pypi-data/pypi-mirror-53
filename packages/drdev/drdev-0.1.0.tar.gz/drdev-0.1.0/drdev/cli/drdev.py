import os
import sys

import click
import docker

from environs import Env

def check_dir_exists(dirname: str):
    """Verifies that directory exists, exits otherwise."""

    if not os.path.isdir(dirname):
        print(f"{dirname} is a not a directory")
        sys.exit()


@click.command()
@click.argument("src_dir", type=click.Path(exists=True))
@click.option("-r", "--repo", default="ageekinside")
@click.option("--ssh_dir")
def run_drdev(src_dir: str, repo: str, ssh_dir: str):
    """Starts a docker container with the directory mounted as workspace.

    \b
    src_dir: Directory to mount as ~/workspace in the container.
    repo: Docker repository name.
    ssh_dir: Host directory with ssh keys to add to the container.
    """

    check_dir_exists(src_dir) 
    abs_path_src = os.path.abspath(src_dir)
    
    if ssh_dir:
        check_dir_exists(ssh_dir)        
        abs_ssh_dir = os.path.abspath(ssh_dir)
    else:
        abs_ssh_dir = None

    image_name = f"{repo}/pydev"
    volume_target = f"/home/{repo}/workspace"

    client = docker.from_env()

    container_name = f"{os.path.basename(abs_path_src)}_dev"
    volume_dict = {abs_path_src: {"bind": volume_target}}

    if abs_ssh_dir:
        volume_dict[abs_ssh_dir] = {"bind": f"/home/{repo}/.ssh-localhost"}

    print(
        f"Preparing to spin up container:\n"
        f"Image: {image_name}\n"
        f"Host dir: {abs_path_src}\n"
        f"Container name: {container_name}\n"
        f"Container workspace: {volume_target}\n"
    )

    client.containers.run(
        image_name, name=container_name, volumes=volume_dict, detach=True, auto_remove=True,
    )


if __name__ == "__main__":
    run_drdev()
