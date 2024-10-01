#!/bin/bash

# Names of containers to be processed
containers=(
    "namenode"
    "datanode"
    "resourcemanager"
    "nodemanager"
    "historyserver"
)

# Function to process each container
update_and_install() {
    container_name=$1
    echo "Processing container: $container_name"

    # Copy sources.list to container
    /Applications/Docker.app/Contents/Resources/bin/docker cp sources.list $container_name:/etc/apt/sources.list

    # Update and install Python
    /Applications/Docker.app/Contents/Resources/bin/docker exec -it $container_name bash -c "apt update || :"
    /Applications/Docker.app/Contents/Resources/bin/docker exec -it $container_name bash -c "apt install python3 python3-pip -y"

}

# Iterate over containers and apply updates
for container in "${containers[@]}"; do
    update_and_install $container
done

echo "All containers processed."